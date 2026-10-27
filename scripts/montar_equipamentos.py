"""Junta as camadas de equipamentos no esquema da seção 5 do plano e liga cada ponto ao seu território.

Entradas:
  dados/saude-cnes.csv, dados/educacao-inep.csv, dados/assistencia-social.csv, dados/protecao.csv
  dados/verificacoes/coordenadas-manuais.csv      coordenadas conferidas pelo João (prevalecem)
  dados/verificacoes/coordenadas-provisorias.csv  sugestões para os pendentes (listar_pendentes.py)
  dados/territorios-base.geojson                  territórios com população (desenhar_territorios.py)
Saídas:
  site/data/equipamentos.csv, site/data/equipamentos.geojson
  site/data/territorios.geojson                   territórios + contagem de equipamentos por camada
  dados/verificacoes/territorio-equipamentos.md   equipamentos cujo bairro está na lista de outro território
"""
import json
import re
import unicodedata

import geopandas as gpd
import pandas as pd
from shapely.geometry import Point, shape

from comum import CAMPOS_EQUIPAMENTO, DADOS, HOJE, INSUMOS, SITE_DATA, VERIFICACOES

MANUAIS = VERIFICACOES / "coordenadas-manuais.csv"
PROVISORIAS = VERIFICACOES / "coordenadas-provisorias.csv"
TERRITORIOS = DADOS / "territorios-base.geojson"
ENTRADAS = ["saude-cnes.csv", "educacao-inep.csv", "assistencia-social.csv", "protecao.csv"]
CAMADAS = [
    "saude_atencao_basica", "saude_urgencia", "saude_hospital", "saude_mental", "saude_especializada",
    "reabilitacao", "educacao_infantil", "assistencia_social", "protecao",
]
UTM = 31983


def carregar_componentes():
    partes = [pd.read_csv(DADOS / n, dtype=str).fillna("") for n in ENTRADAS if (DADOS / n).exists()]
    df = pd.concat(partes, ignore_index=True)[CAMPOS_EQUIPAMENTO]
    invalidas = set(df.camada) - set(CAMADAS)
    if invalidas:
        raise SystemExit(f"Camadas fora do esquema: {invalidas}")
    if df.id.duplicated().any():
        raise SystemExit(f"IDs duplicados: {df.id[df.id.duplicated()].tolist()}")
    sem_fonte = df[(df.fonte == "") | (df.fonte_url == "") | (df.data_coleta == "")]
    if not sem_fonte.empty:
        raise SystemExit(f"Equipamentos sem fonte: {sem_fonte.id.tolist()}")
    return df


def aplicar_coordenadas_manuais(df):
    """Coordenadas conferidas à mão na revisão do João."""
    if not MANUAIS.exists():
        return df
    manuais = pd.read_csv(MANUAIS, dtype=str).fillna("")
    desconhecidos = set(manuais.id) - set(df.id)
    if desconhecidos:
        raise SystemExit(f"coordenadas-manuais.csv cita ids inexistentes: {sorted(desconhecidos)}")
    for m in manuais.itertuples():
        i = df.index[df.id == m.id][0]
        df.at[i, "lat"], df.at[i, "lon"], df.at[i, "coord_origem"] = f"{float(m.lat):.6f}", f"{float(m.lon):.6f}", "manual"
    print(f"  {len(manuais)} coordenada(s) manual(is) aplicada(s)")
    return df


def aplicar_coordenadas_provisorias(df):
    """Pendentes entram no mapa no ponto sugerido, mas continuam 'pendente' e com aviso na ficha."""
    if not PROVISORIAS.exists():
        return df
    prov = pd.read_csv(PROVISORIAS, dtype=str).fillna("").set_index("id")
    n = 0
    for i, r in df[df.coord_origem == "pendente"].iterrows():
        if r.id in prov.index:
            p = prov.loc[r.id]
            df.at[i, "lat"], df.at[i, "lon"] = f"{float(p.lat):.6f}", f"{float(p.lon):.6f}"
            aviso = f"Localização aproximada ({p.base}); o ponto exato ainda não foi conferido."
            df.at[i, "observacao"] = f"{aviso} {r.observacao}".strip()
            n += 1
    print(f"  {n} pendente(s) no ponto provisório")
    return df


def aviso_fora_do_limite(df):
    cotia = shape(json.loads((SITE_DATA / "cotia.geojson").read_text(encoding="utf-8"))["features"][0]["geometry"])
    limite = gpd.GeoSeries([cotia.boundary], crs=4326).to_crs(UTM).iloc[0]
    for i, r in df.iterrows():
        if r.lat == "" or cotia.contains(Point(float(r.lon), float(r.lat))):
            continue
        d = gpd.GeoSeries([Point(float(r.lon), float(r.lat))], crs=4326).to_crs(UTM).iloc[0].distance(limite)
        nota = f"A coordenada da fonte fica {d:.0f} m além do limite municipal do IBGE."
        df.at[i, "observacao"] = f"{r.observacao} {nota}".strip()
    return df


# ---------- territórios ----------

def normalizar_bairro(t):
    t = re.sub(r"\(.*?\)", " ", t.split(",")[0])
    t = unicodedata.normalize("NFKD", t).encode("ascii", "ignore").decode().lower()
    t = re.sub(r"\bcaucaia do alto\b", " ", t)
    t = re.sub(r"\b(jd|jardim|pq|prq|parque|vl|vila|chac|chacara|chacaras|res|residencial|cond|condominio|conj|conjunto|bairro|"
               r"granja|recanto|portal|loteamento|nucleo|estancia)\b\.?", " ", t)
    return re.sub(r"[^a-z0-9]+", " ", t).strip()


def listas_de_bairros():
    texto = (INSUMOS / "territorios-cras.md").read_text(encoding="utf-8")
    mapa = {}
    for m in re.finditer(r"^## (\d)\..*?\*\*Bairros:\*\* (.*?)\.\s*$", texto, re.M | re.S):
        for b in m.group(2).split(","):
            chave = normalizar_bairro(b)
            if chave:
                mapa.setdefault(chave, set()).add(int(m.group(1)))
    return mapa


def atribuir_territorio(df, terr):
    terr_utm = terr.to_crs(UTM)
    nomes = dict(zip(terr.numero, terr.nome))
    bairros = listas_de_bairros()
    divergentes = []
    df["_territorio_num"] = 0
    for i, r in df[df.lat != ""].iterrows():
        p = gpd.GeoSeries([Point(float(r.lon), float(r.lat))], crs=4326).to_crs(UTM).iloc[0]
        dentro = terr_utm[terr_utm.contains(p)]
        if len(dentro):
            num = int(dentro.numero.iloc[0])
        else:
            dist = terr_utm.distance(p)
            num = int(terr_utm.numero[dist.idxmin()])
        df.at[i, "_territorio_num"] = num
        df.at[i, "territorio"] = nomes[num]
        nos_bairros = bairros.get(normalizar_bairro(r.bairro), set())
        if nos_bairros and num not in nos_bairros:
            outros = " ou ".join(nomes[t] for t in sorted(nos_bairros))
            nota = f"No PMAS 2026–2029, o bairro {r.bairro.split(',')[0]} está na lista do território {outros}."
            df.at[i, "observacao"] = f"{df.at[i, 'observacao']} {nota}".strip()
            divergentes.append((r.id, r.nome, r.bairro, nomes[num], outros, r.coord_origem))
    return df, divergentes


def exportar_bairros():
    """Bairros das listas do PMAS, para a busca do site (bairro -> território)."""
    texto = (INSUMOS / "territorios-cras.md").read_text(encoding="utf-8")
    por_nome = {}
    for m in re.finditer(r"^## (\d)\..*?\*\*Bairros:\*\* (.*?)\.\s*$", texto, re.M | re.S):
        for b in m.group(2).split(","):
            nome = re.sub(r"\s+", " ", b).strip()
            if nome:
                por_nome.setdefault(nome, set()).add(int(m.group(1)))
    chave = lambda n: unicodedata.normalize("NFKD", n).encode("ascii", "ignore").decode().lower()
    lista = [{"nome": n, "territorios": sorted(t)} for n, t in sorted(por_nome.items(), key=lambda x: chave(x[0]))]
    (SITE_DATA / "bairros.json").write_text(json.dumps(lista, ensure_ascii=False), encoding="utf-8")


def territorios_com_contagens(df, terr):
    terr = terr.copy()
    for c in CAMADAS:
        terr[f"n_{c}"] = [int(((df._territorio_num == n) & (df.camada == c)).sum()) for n in terr.numero]
    terr["n_cras"] = [int(((df._territorio_num == n) & (df.subtipo == "CRAS")).sum()) for n in terr.numero]
    terr["n_aproximados"] = [int(((df._territorio_num == n) & (df.coord_origem == "pendente")).sum()) for n in terr.numero]
    return terr


def relatorio_divergencias(divergentes, df):
    L = [f"# Território de cada equipamento — {HOJE}", "",
         "O território vem do ponto no polígono. Abaixo estão os equipamentos cujo bairro (do endereço da fonte) "
         "aparece na lista de bairros de outro território no PMAS 2026–2029. Pode ser ponto na fronteira, "
         "bairro dividido entre territórios ou limite do território mal aproximado.", "",
         f"Equipamentos com território atribuído: {(df._territorio_num > 0).sum()} de {len(df)}.", "",
         "| id | Equipamento | Bairro (fonte) | Território pelo mapa | Lista do PMAS | Coordenada |", "|---|---|---|---|---|---|"]
    for d in divergentes:
        L.append("| " + " | ".join(str(x) for x in d) + " |")
    if not divergentes:
        L.append("| — | nenhum caso | | | | |")
    (VERIFICACOES / "territorio-equipamentos.md").write_text("\n".join(L) + "\n", encoding="utf-8")


def main():
    df = carregar_componentes()
    df = aplicar_coordenadas_manuais(df)
    df = aplicar_coordenadas_provisorias(df)
    df = aviso_fora_do_limite(df)

    divergentes = []
    if TERRITORIOS.exists():
        terr = gpd.read_file(TERRITORIOS)
        df, divergentes = atribuir_territorio(df, terr)
        relatorio_divergencias(divergentes, df)
        terr = territorios_com_contagens(df, terr)
        terr.to_file(SITE_DATA / "territorios.geojson", driver="GeoJSON", COORDINATE_PRECISION=6)
        exportar_bairros()
    else:
        df["_territorio_num"] = 0

    df["_ordem"] = df.camada.map(CAMADAS.index)
    df = df.sort_values(["_ordem", "nome"]).drop(columns=["_ordem", "_territorio_num"])
    SITE_DATA.mkdir(parents=True, exist_ok=True)
    df.to_csv(SITE_DATA / "equipamentos.csv", index=False, encoding="utf-8")

    com_coord = df[df.lat != ""]
    features = [{
        "type": "Feature",
        "geometry": {"type": "Point", "coordinates": [float(r.lon), float(r.lat)]},
        "properties": {k: r[k] for k in CAMPOS_EQUIPAMENTO if k not in ("lat", "lon")},
    } for _, r in com_coord.iterrows()]
    (SITE_DATA / "equipamentos.geojson").write_text(
        json.dumps({"type": "FeatureCollection", "features": features}, ensure_ascii=False), encoding="utf-8")

    resumo = {
        "data": HOJE, "total": int(len(df)),
        "por_camada": {c: int((df.camada == c).sum()) for c in CAMADAS},
        "por_origem": {k: int(v) for k, v in df.coord_origem.value_counts().items()},
        "por_gestao": {k: int(v) for k, v in df.gestao.value_counts().items()},
        "divergencias_bairro": len(divergentes),
        "nao_confirmados": int((df.verificacao == "nao_confirmado").sum()),
    }
    (VERIFICACOES / "equipamentos-resumo.json").write_text(json.dumps(resumo, ensure_ascii=False, indent=1), encoding="utf-8")

    print(f"{len(df)} equipamentos ({len(df) - len(com_coord)} sem coordenada; "
          f"{(df.coord_origem == 'pendente').sum()} pendentes) -> site/data/equipamentos.csv e .geojson")
    print(df.groupby("camada").size().reindex(CAMADAS).fillna(0).astype(int).to_string())
    if TERRITORIOS.exists():
        print(f"Território divergente da lista de bairros: {len(divergentes)} (dados/verificacoes/territorio-equipamentos.md)")


if __name__ == "__main__":
    main()
