"""Camada 7 — creches e pré-escolas públicas (e conveniadas) de Cotia.

Entradas:
  dados/brutos/inep-cotia-2025.csv                         recorte dos microdados (coletar_inep.py)
  dados/brutos/inep-catalogo-escolas-cotia-2026-10-19.psv  endereço, telefone e coordenadas lidos da
      ficha de cada escola no Catálogo de Escolas do INEP (painel OBIEE; leitura assistida no navegador,
      uma ficha por escola, na URL de CATALOGO abaixo). Os microdados de 2025 não trazem mais esses campos.
Saída:
  dados/educacao-inep.csv
"""
import re

import pandas as pd

from comum import BRUTOS, DADOS, capitalizar, formatar_telefone
from geocodificar import geocodificar, preciso

DATA_CATALOGO = "2026-10-19"
CATALOGO = ("https://anonymousdata.inep.gov.br/analytics/saw.dll?Dashboard&PortalPath=%2Fshared%2FCenso%20da%20Educa%C3%A7%C3%A3o"
            "%20B%C3%A1sica%2F_portal%2FCat%C3%A1logo%20de%20Escolas&Page=Detalhamento%20Escola&Action=Navigate&P0=1&P1=eq"
            "&P2=%22F%20-%20Catalogo%20Escola%22.%22C%C3%B3digo%20Entidade%22&P3=%22{codigo}%22")
FONTE = "INEP — Censo Escolar 2025 (microdados) e Catálogo de Escolas"

# O catálogo põe o tipo de logradouro depois do número: "ITU, 23 RUA. JARDIM BARRO BRANCO."
TIPOS_LOGRADOURO = {"RUA": "RUA", "AVENIDA": "AVENIDA", "ESTRADA": "ESTRADA", "ESTRADA MUNICIPAL": "ESTRADA MUNICIPAL",
                    "ESTRADA VELHA": "ESTRADA VELHA DA", "ALAMEDA": "ALAMEDA", "TRAVESSA": "TRAVESSA", "PRACA": "PRAÇA"}
# e inverte títulos: "FRANCISCO DE ASSIS SAO" = "São Francisco de Assis"
TITULOS_INVERTIDOS = {"SAO", "SANTO", "SANTA", "PADRE", "VEREADOR", "DOUTOR", "PROFESSOR", "PROFESSORA", "DONA"}
# Nos nomes de escola, o tipo também vem no fim: "AGUINALDO SOUZA ESTRELA EM" = "EM Aguinaldo Souza Estrela"
TIPOS_ESCOLA = [("CENTRO EDUC UNIFICADO", "Centro Educacional Unificado"), ("CENTRO EDUCACIONAL DO", "Centro Educacional do"),
                ("CENTRO EDUCACIONAL DA", "Centro Educacional da"), ("CENTRO EDUCACIONAL", "Centro Educacional"),
                ("ESCOLA MUNICIPAL", "Escola Municipal"), ("EM DO", "EM do"), ("EM DA", "EM da"), ("EM", "EM"), ("CE", "CE")]
TITULOS_PESSOA = ["PROF DR", "PROFESSOR", "PROFESSORA", "PROFA", "PROF", "DRA", "DR", "ENG", "PREFEITO"]


def desinverter(nome):
    partes = nome.split()
    if len(partes) >= 2 and partes[-1] in TITULOS_INVERTIDOS and len(" ".join(partes[:-1])) > 2:
        return " ".join([partes[-1]] + partes[:-1])
    return nome


def nome_escola(bruto):
    nome = re.sub(r"\s+", " ", bruto.strip().upper())
    for tipo, rotulo in TIPOS_ESCOLA:
        if nome.endswith(" " + tipo) and not nome.startswith(tipo + " "):
            resto = nome[: -len(tipo) - 1]
            titulo = next((t for t in TITULOS_PESSOA if resto.endswith(" " + t)), "")
            if titulo:
                resto = resto[: -len(titulo) - 1]
                return f"{rotulo} {capitalizar(titulo + ' ' + resto)}"
            return f"{rotulo} {capitalizar(resto)}"
    m = re.match(r"^(EM|CE)\s+(.*)$", nome)
    if m:
        return f"{m.group(1)} {capitalizar(m.group(2))}"
    return capitalizar(nome)


def separar_endereco(bruto):
    """'ITU, 23 RUA. JARDIM BARRO BRANCO. 06716-205 Cotia - SP.' -> ('Rua Itu, 23', 'Jardim Barro Branco', '06716-205')"""
    texto = bruto.strip().rstrip(".").replace("EST. MUNIC. ", "")
    cep = (re.search(r"(\d{5}-\d{3})", texto) or [""])[0]
    texto = re.sub(r"\s*\d{5}-\d{3}\s+Cotia\s*-\s*SP\s*$", "", texto).strip().rstrip(".")
    partes = [p.strip() for p in re.split(r"\.\s+", texto) if p.strip()]
    primeira, resto = partes[0], partes[1:]
    m = re.match(r"^(.*?),\s*(\S+)\s*(.*)$", primeira)
    if not m:
        return capitalizar(primeira), capitalizar(" ".join(resto)), cep
    logradouro, numero, sobra = m.group(1).strip(), m.group(2), m.group(3).strip()
    tipo = ""
    if sobra.upper() in TIPOS_LOGRADOURO:
        tipo = TIPOS_LOGRADOURO[sobra.upper()]
        bairro = " ".join(resto)
    else:
        bairro = " ".join([sobra] + resto) if sobra else " ".join(resto)
    logradouro = re.sub(r"\s+" + re.escape(numero) + r"$", "", logradouro)
    if re.match(r"^R\s", logradouro):
        logradouro = "RUA " + logradouro[2:]
    if re.match(r"^(RUA|AVENIDA|ESTRADA|ALAMEDA|TRAVESSA)\s", logradouro):
        tipo = ""
    logradouro = desinverter(logradouro)
    metade = bairro.split()
    if len(metade) % 2 == 0 and metade[: len(metade) // 2] == metade[len(metade) // 2:]:
        bairro = " ".join(metade[: len(metade) // 2])
    return f"{capitalizar((tipo + ' ' + logradouro).strip())}, {numero}", capitalizar(bairro), cep


def subtipo(r):
    if r.QT_MAT_INF_CRE > 0 and r.QT_MAT_INF_PRE > 0:
        return "Creche e pré-escola"
    return "Creche" if r.QT_MAT_INF_CRE > 0 else "Pré-escola"


def gestao(r):
    if r.conveniada == "1":
        return "conveniada"
    return {"1": "federal", "2": "estadual", "3": "municipal"}[r.TP_DEPENDENCIA]


def main():
    inep = pd.read_csv(BRUTOS / "inep-cotia-2025.csv", dtype=str).fillna("")
    for c in ("QT_MAT_INF_CRE", "QT_MAT_INF_PRE"):
        inep[c] = inep[c].astype(int)
    cat = pd.read_csv(BRUTOS / f"inep-catalogo-escolas-cotia-{DATA_CATALOGO}.psv", sep="|", dtype=str).fillna("")
    df = inep.merge(cat, left_on="CO_ENTIDADE", right_on="co_entidade", how="left", indicator=True)
    faltam = df[df._merge != "both"]
    if not faltam.empty:
        raise SystemExit(f"Escolas sem ficha do catálogo: {faltam.CO_ENTIDADE.tolist()}")

    linhas = []
    for r in df.itertuples():
        endereco, bairro, cep = separar_endereco(r.endereco_catalogo)
        obs = []
        if r.latitude and r.longitude:
            lat, lon, origem = round(float(r.latitude), 6), round(float(r.longitude), 6), "inep"
        else:
            lat = lon = ""
            origem = "pendente"
            for consulta in (f"{endereco}, {bairro}, Cotia, SP", f"{endereco}, Cotia, SP", f"{cep}, Cotia, SP"):
                g = geocodificar(consulta)
                if preciso(g):
                    lat, lon, origem = round(float(g["lat"]), 6), round(float(g["lon"]), 6), "nominatim"
                    break
            obs.append("O Catálogo de Escolas do INEP não traz coordenadas desta escola; o ponto foi localizado pelo endereço.")
        if r.conveniada == "1":
            obs.append("Escola privada sem fins lucrativos conveniada com o poder público.")
        linhas.append({
            "id": f"inep-{r.CO_ENTIDADE}",
            "nome": nome_escola(r.NO_ENTIDADE),
            "camada": "educacao_infantil",
            "subtipo": subtipo(r),
            "gestao": gestao(r),
            "endereco": endereco,
            "bairro": bairro,
            "telefone": formatar_telefone(r.telefone),
            "territorio": "",
            "lat": lat,
            "lon": lon,
            "coord_origem": origem,
            "fonte": FONTE,
            "fonte_url": CATALOGO.format(codigo=r.CO_ENTIDADE),
            "data_coleta": DATA_CATALOGO,
            "verificacao": "confirmado",
            "observacao": " ".join(obs),
            "_cep": cep,
            "_mat_creche": r.QT_MAT_INF_CRE,
            "_mat_pre": r.QT_MAT_INF_PRE,
        })
    saida = pd.DataFrame(linhas)
    saida.to_csv(DADOS / "educacao-inep.csv", index=False, encoding="utf-8")
    print(f"{len(saida)} escolas -> dados/educacao-inep.csv")
    print(saida.groupby(["gestao", "subtipo"]).size().to_string())
    print("Coordenadas:", saida.coord_origem.value_counts().to_dict())


if __name__ == "__main__":
    main()
