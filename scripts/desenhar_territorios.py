"""Fase 3 — os 7 territórios de CRAS reconstruídos com setores censitários do Censo 2022.

Cotia não tem limites de bairro oficiais. O PMAS 2026–2029 publica só um mapa colorido e listas de bairros.
Método:
  1. Georreferenciamento: ajusta uma transformação (escala x/y, rotação, deslocamento) que leva o contorno
     de Cotia (união dos setores do IBGE) sobre a mancha colorida do mapa do PMAS, maximizando a
     sobreposição (IoU). O contorno inteiro funciona como milhares de pontos de controle; os quatro
     extremos (N, S, L, O) são conferidos um a um no relatório.
  2. Cada setor recebe a cor que cai sob o seu ponto interno (janela de 5×5 px, voto da maioria).
     Textos e bordas brancas do mapa são ignorados.
  3. Setores do miolo verde-pálido (área de reserva, sem CRAS) e setores sem cor herdam o território
     vizinho com quem dividem a maior fronteira.
  4. População: V01006 (moradores) e V01031–V01034 (0–4, 5–9, 10–14, 15–19 anos), com "X" (sigilo do
     IBGE) tratado como ausente; o total é comparado com o oficial (SIDRA 4709).
Saídas:
  dados/territorios-base.geojson                   polígonos + população (contagens entram em montar_equipamentos.py)
  dados/verificacoes/setores-territorio.csv        território de cada setor e como foi decidido
  dados/verificacoes/territorios.md                relatório da Parada 3
  dados/verificacoes/conferir-territorios.html     mapa de conferência (setores coloridos + mapa do PMAS por cima)
"""
import base64
import json
import re
import unicodedata

import geopandas as gpd
import numpy as np
import pandas as pd
from PIL import Image, ImageDraw
from scipy import ndimage
from scipy.optimize import minimize
from shapely import affinity
from shapely.geometry import Point
from shapely.ops import polylabel, unary_union

from comum import BRUTOS, DADOS, HOJE, INSUMOS, VERIFICACOES

PNG = INSUMOS / "mapa-territorios-cras-pmas-2026.png"
LOGO = (360, 390, 620, 526)  # caixa do brasão da prefeitura no canto inferior direito, ignorada
UTM = 31983  # SIRGAS 2000 / UTM 23S

TERRITORIOS = [
    # id, nome, cor no mapa oficial, cor medida no PNG, CRAS de referência
    (1, "Jd. Japão", "roxo", (150, 42, 90), "cras-01"),
    (2, "Caucaia do Alto", "verde-claro", (174, 210, 90), "cras-02"),
    (3, "Miguel Mirizola", "amarelo/dourado", (210, 186, 42), "cras-03"),
    (4, "Central (Monte Serrat)", "azul-claro", (90, 198, 210), "cras-04"),
    (5, "KM 21 / Granja Viana", "azul-escuro", (78, 114, 126), "cras-05"),
    (6, "Jd. Arco-Íris / Jd. Sandra", "laranja", (210, 126, 42), "cras-06"),
    (7, "Caputera", "verde-limão", (210, 222, 30), "cras-07"),
]
MIOLO = 8  # verde-pálido: área sem CRAS (reserva do Morro Grande)
PALETA = np.array([t[3] for t in TERRITORIOS] + [(210, 222, 138)], dtype=float)
LIMIAR_COR = 45.0
VARS = {"V01006": "pop_total", "V01031": "pop_0_4", "V01032": "pop_5_9", "V01033": "pop_10_14", "V01034": "pop_15_19"}


# ---------- 1. georreferenciamento ----------

def mascara_do_mapa(img):
    """Pixels do município no PNG: tudo que não é fundo branco, com buracos (textos, bordas) preenchidos."""
    rgb = np.array(img)
    fundo = (rgb > 235).all(axis=2)
    x0, y0, x1, y1 = LOGO
    fundo[y0:y1, x0:x1] = True
    rotulos, _ = ndimage.label(fundo)
    externos = np.unique(np.concatenate([rotulos[0], rotulos[-1], rotulos[:, 0], rotulos[:, -1]]))
    exterior = np.isin(rotulos, externos[externos > 0])
    return ~exterior


def rasterizar(geom, tamanho):
    w, h = tamanho
    im = Image.new("L", (w, h), 0)
    d = ImageDraw.Draw(im)
    for p in getattr(geom, "geoms", [geom]):
        d.polygon(list(p.exterior.coords), fill=1)
        for furo in p.interiors:
            d.polygon(list(furo.coords), fill=0)
    return np.array(im, dtype=bool)


def matriz(p, centro):
    sx, sy, teta, tu, tv = p
    cx, cy = centro
    a, b = sx * np.cos(teta), -sx * np.sin(teta)
    d, e = -sy * np.sin(teta), -sy * np.cos(teta)
    return [a, b, d, e, tu - a * cx - b * cy, tv - d * cx - e * cy]


def georreferenciar(contorno, mascara):
    h, w = mascara.shape
    ys, xs = np.nonzero(mascara)
    minx, miny, maxx, maxy = contorno.bounds
    centro = ((minx + maxx) / 2, (miny + maxy) / 2)
    p0 = np.array([(xs.max() - xs.min()) / (maxx - minx), (ys.max() - ys.min()) / (maxy - miny), 0.0,
                   (xs.max() + xs.min()) / 2, (ys.max() + ys.min()) / 2])
    simples = contorno.simplify(20)

    def custo(q):
        p = np.array([p0[0] * np.exp(q[0]), p0[1] * np.exp(q[1]), q[2], p0[3] + q[3], p0[4] + q[4]])
        r = rasterizar(affinity.affine_transform(simples, matriz(p, centro)), (w, h))
        return -(r & mascara).sum() / (r | mascara).sum()

    melhor = None
    for inicio in ([0, 0, 0, 0, 0], [0.03, -0.03, 0.01, 4, -4], [-0.03, 0.03, -0.01, -4, 4]):
        simplex = np.vstack([inicio, np.array(inicio) + np.diag([0.04, 0.04, 0.02, 5, 5])])
        res = minimize(custo, inicio, method="Nelder-Mead",
                       options={"initial_simplex": simplex, "xatol": 1e-4, "fatol": 1e-5, "maxiter": 1500})
        if melhor is None or res.fun < melhor.fun:
            melhor = res
    q = melhor.x
    p = np.array([p0[0] * np.exp(q[0]), p0[1] * np.exp(q[1]), q[2], p0[3] + q[3], p0[4] + q[4]])
    return matriz(p, centro), -melhor.fun, p


def residuos_extremos(contorno, mascara, mat):
    """Distância (px) entre os extremos N/S/L/O do contorno transformado e os da mancha do PNG."""
    ys, xs = np.nonzero(mascara)
    alvo = {"norte": (xs[ys.argmin()], ys.min()), "sul": (xs[ys.argmax()], ys.max()),
            "oeste": (xs.min(), ys[xs.argmin()]), "leste": (xs.max(), ys[xs.argmax()])}
    pts = np.array(affinity.affine_transform(contorno, mat).exterior.coords) if contorno.geom_type == "Polygon" else \
        np.vstack([np.array(g.exterior.coords) for g in affinity.affine_transform(contorno, mat).geoms])
    ext = {"norte": pts[pts[:, 1].argmin()], "sul": pts[pts[:, 1].argmax()],
           "oeste": pts[pts[:, 0].argmin()], "leste": pts[pts[:, 0].argmax()]}
    return {k: float(np.hypot(*(np.array(alvo[k]) - ext[k]))) for k in alvo}


# ---------- 2. classificação dos setores ----------

def classificar_pixels(rgb):
    """Classe 1..7, 8 (miolo) ou 0 (texto, borda, fundo) para cada pixel."""
    dist = np.linalg.norm(rgb[..., None, :].astype(float) - PALETA, axis=-1)
    classe = dist.argmin(axis=-1) + 1
    return np.where(dist.min(axis=-1) <= LIMIAR_COR, classe, 0)


def voto(classes):
    v = classes[classes > 0]
    if v.size == 0:
        return 0, 0.0
    valores, cont = np.unique(v, return_counts=True)
    return int(valores[cont.argmax()]), float(cont.max() / v.size)


def classificar_setores(setores_utm, mat, classes_img):
    h, w = classes_img.shape
    linhas = []
    for idx, geom in zip(setores_utm.index, setores_utm.geometry):
        ponto = affinity.affine_transform(geom.representative_point(), mat)
        x, y = int(round(ponto.x)), int(round(ponto.y))
        c_ponto, partilha_ponto = 0, 0.0
        for raio in (2, 4):
            jan = classes_img[max(0, y - raio): y + raio + 1, max(0, x - raio): x + raio + 1]
            c_ponto, partilha_ponto = voto(jan)
            if c_ponto:
                break
        gpx = affinity.affine_transform(geom, mat)
        minx, miny, maxx, maxy = gpx.bounds
        x0, y0 = max(0, int(np.floor(minx))), max(0, int(np.floor(miny)))
        x1, y1 = min(w, int(np.ceil(maxx)) + 1), min(h, int(np.ceil(maxy)) + 1)
        c_poli, partilha_poli = 0, 0.0
        if x1 > x0 and y1 > y0:
            local = affinity.translate(gpx, -x0, -y0)
            m = rasterizar(local, (x1 - x0, y1 - y0))
            if m.any():
                c_poli, partilha_poli = voto(classes_img[y0:y1, x0:x1][m])
        linhas.append({"idx": idx, "classe_ponto": c_ponto, "partilha_ponto": round(partilha_ponto, 2),
                       "classe_poligono": c_poli, "partilha_poligono": round(partilha_poli, 2), "px": x, "py": y})
    return pd.DataFrame(linhas).set_index("idx")


TERRITORIOS_DO_DISTRITO = {"Caucaia do Alto": {1, 2}, "Cotia": {3, 4, 5, 6, 7}}


def resolver_por_vizinhos(setores_utm, territorio, distrito):
    """Setores sem território herdam o vizinho com a maior fronteira comum, preferindo um território do
    mesmo distrito do IBGE (no mapa do PMAS, os territórios 1–2 ficam em Caucaia do Alto e os 3–7 em Cotia)."""
    territorio = territorio.copy()
    pendentes = set(territorio.index[territorio == 0])
    origem = {}
    while pendentes:
        avancou = False
        for i in sorted(pendentes):
            g = setores_utm.geometry[i]
            fronteira = {}
            for j in setores_utm.sindex.query(g, predicate="intersects"):
                j = setores_utm.index[j]
                if j == i or territorio[j] == 0:
                    continue
                comp = g.boundary.intersection(setores_utm.geometry[j].boundary).length
                if comp > 0:
                    fronteira[territorio[j]] = fronteira.get(territorio[j], 0) + comp
            mesmo_distrito = {t: c for t, c in fronteira.items() if t in TERRITORIOS_DO_DISTRITO.get(distrito[i], set())}
            if mesmo_distrito:
                fronteira = mesmo_distrito
            if fronteira:
                territorio[i] = max(fronteira, key=fronteira.get)
                origem[i] = fronteira
                pendentes.discard(i)
                avancou = True
        if not avancou:
            raise SystemExit(f"Setores isolados sem vizinho com território: {sorted(pendentes)}")
    return territorio, origem


# ---------- 3. população ----------

def populacao(setores):
    dem = pd.read_csv(BRUTOS / "demografia-cotia-2022.csv", dtype=str)
    df = setores[["CD_SETOR"]].merge(dem, on="CD_SETOR", how="left")
    sigilo = (df["V01006"] == "X")
    for v in VARS:
        df[v] = pd.to_numeric(df[v].replace("X", np.nan), errors="coerce")
    df["sigilo"] = sigilo
    df["sem_dado"] = df["V01006"].isna() & ~sigilo
    return df.set_index(setores.index)


# ---------- relatório e página ----------

def normalizar(t):
    t = unicodedata.normalize("NFKD", t).encode("ascii", "ignore").decode().lower()
    t = re.sub(r"\b(jd|jardim|pq|parque|vl|vila|chac|chacara|res|residencial|cond|condominio)\b\.?", " ", t)
    return re.sub(r"[^a-z0-9]+", " ", t).strip()


def main():
    setores = gpd.read_file(BRUTOS / "setores-cotia-2022.geojson")
    setores_utm = setores.to_crs(UTM)
    contorno = unary_union(setores_utm.geometry).buffer(0)
    if contorno.geom_type == "MultiPolygon":
        contorno = max(contorno.geoms, key=lambda g: g.area)

    img = Image.open(PNG).convert("RGB")
    mascara = mascara_do_mapa(img)
    mat, iou, params = georreferenciar(contorno, mascara)
    residuos = residuos_extremos(contorno, mascara, mat)
    print(f"Georreferenciamento: IoU {iou:.3f}; rotação {np.degrees(params[2]):.2f}°; "
          f"escala {1 / params[0]:.1f} m/px (x) e {1 / params[1]:.1f} m/px (y); resíduos {residuos}")

    classes_img = classificar_pixels(np.array(img))
    x0, y0, x1, y1 = LOGO
    classes_img[y0:y1, x0:x1] = 0
    cls = classificar_setores(setores_utm, mat, classes_img)

    ponto_ok = cls.classe_ponto.between(1, 7)
    poligono_ok = cls.classe_poligono.between(1, 7)
    territorio = cls.classe_ponto.where(ponto_ok, cls.classe_poligono.where(poligono_ok, 0))
    metodo = pd.Series("cor sob o ponto interno", index=cls.index)
    metodo[~ponto_ok & poligono_ok] = "cor dominante do setor"
    metodo[~ponto_ok & ~poligono_ok & ((cls.classe_ponto == MIOLO) | (cls.classe_poligono == MIOLO))] = "miolo sem CRAS → vizinho"
    metodo[(territorio == 0) & (metodo == "cor sob o ponto interno")] = "sem cor no mapa → vizinho"
    territorio, origem = resolver_por_vizinhos(setores_utm, territorio, setores.NM_DIST)

    pop = populacao(setores)
    tab = setores[["CD_SETOR", "SITUACAO", "NM_DIST", "AREA_KM2"]].copy()
    tab["territorio"] = territorio
    tab["metodo"] = metodo
    tab = tab.join(cls[["classe_ponto", "partilha_ponto", "classe_poligono", "partilha_poligono"]])
    tab = tab.join(pop[list(VARS) + ["sigilo", "sem_dado"]])
    duvida = (tab.metodo != "cor sob o ponto interno") | \
             ((tab.classe_poligono.between(1, 7)) & (tab.classe_poligono != tab.territorio)) | \
             (tab.partilha_ponto < 0.6)
    tab["fronteira_duvidosa"] = duvida
    tab.drop(columns="AREA_KM2").to_csv(VERIFICACOES / "setores-territorio.csv", index=False, encoding="utf-8")

    oficial = json.loads((BRUTOS / "populacao-oficial-cotia-2022.json").read_text(encoding="utf-8"))["populacao_2022"]
    soma = int(tab.V01006.sum())
    dif = (oficial - soma) / oficial

    nomes = {t[0]: t for t in TERRITORIOS}
    polis = []
    for tid, grupo in tab.groupby("territorio"):
        geom = unary_union(setores_utm.geometry[grupo.index]).buffer(0)
        maior = max(getattr(geom, "geoms", [geom]), key=lambda g: g.area)
        rotulo = gpd.GeoSeries([polylabel(maior, tolerance=20)], crs=UTM).to_crs(4326).iloc[0]
        t = nomes[tid]
        polis.append({
            "id": f"t{tid}", "numero": tid, "nome": t[1], "cor_oficial": t[2], "cor_png": "#%02x%02x%02x" % t[3],
            "cras_referencia": t[4], **{VARS[v]: int(grupo[v].sum()) for v in VARS},
            "setores": int(len(grupo)), "setores_com_sigilo": int(grupo.sigilo.sum()),
            "setores_miolo": int((grupo.metodo == "miolo sem CRAS → vizinho").sum()),
            "pop_miolo": int(grupo.loc[grupo.metodo == "miolo sem CRAS → vizinho", "V01006"].sum()),
            "rotulo_lat": round(rotulo.y, 6), "rotulo_lon": round(rotulo.x, 6),
            "geometry": geom,
        })
    terr = gpd.GeoDataFrame(polis, geometry="geometry", crs=UTM)
    moradores_sigilo = oficial - soma
    terr["moradores_em_sigilo_municipio"] = moradores_sigilo
    terr_out = terr.copy()
    terr_out["geometry"] = terr_out.geometry.simplify(8)
    terr_out.to_crs(4326).to_file(DADOS / "territorios-base.geojson", driver="GeoJSON", COORDINATE_PRECISION=6)

    pop_miolo = int(tab.loc[tab.metodo == "miolo sem CRAS → vizinho", "V01006"].sum())
    print(f"População: soma dos setores {soma} × oficial {oficial} (diferença {dif:.2%}); "
          f"setores em sigilo {int(tab.sigilo.sum())}; sem dado {int(tab.sem_dado.sum())}; "
          f"miolo: {int((tab.metodo == 'miolo sem CRAS → vizinho').sum())} setores, {pop_miolo} moradores ({pop_miolo / oficial:.2%})")
    print(terr[["numero", "nome", "setores", "pop_total", "pop_0_4", "pop_5_9", "pop_10_14", "pop_15_19"]].to_string(index=False))

    relatorio(tab, terr, iou, params, residuos, soma, oficial, moradores_sigilo, pop_miolo, origem, setores)
    pagina(setores, tab, mat, img)
    resumo = {
        "data": HOJE, "setores": int(len(tab)), "iou": round(float(iou), 3), "rotacao_graus": round(float(np.degrees(params[2])), 2),
        "residuos_px": {k: round(v, 1) for k, v in residuos.items()}, "m_por_px": round(float(1 / params[0]), 1),
        "soma_setores": soma, "populacao_oficial": oficial, "moradores_em_sigilo": int(moradores_sigilo),
        "setores_sigilo": int(tab.sigilo.sum()), "setores_sem_dado": int(tab.sem_dado.sum()),
        "setores_miolo": int((tab.metodo == "miolo sem CRAS → vizinho").sum()), "pop_miolo": pop_miolo,
        "setores_cor_do_setor": int((tab.metodo == "cor dominante do setor").sum()),
        "setores_duvidosos": int(tab.fronteira_duvidosa.sum()),
    }
    (VERIFICACOES / "territorios-resumo.json").write_text(json.dumps(resumo, ensure_ascii=False, indent=1), encoding="utf-8")


def relatorio(tab, terr, iou, params, residuos, soma, oficial, moradores_sigilo, pop_miolo, origem, setores):
    bairros = ler_listas_bairros()
    L = [f"# Territórios de CRAS — Parada 3 ({HOJE})", "",
         "## Georreferenciamento do mapa do PMAS", "",
         f"- Ajuste do contorno de Cotia (setores do IBGE) sobre a mancha colorida do mapa: **IoU {iou:.3f}** "
         f"(1 = sobreposição perfeita).".replace("IoU 0.", "IoU 0,"),
         f"- Rotação {np.degrees(params[2]):.2f}°; escala {1 / params[0]:.1f} m/px na horizontal e {1 / params[1]:.1f} m/px na vertical.",
         "- Pontos de controle (extremos do município), distância entre o contorno ajustado e a borda do mapa: " +
         "; ".join(f"{k} {v:.1f} px (~{v / params[0]:.0f} m)" for k, v in residuos.items()) + ".", "",
         "## População por território (Censo 2022)", "",
         "| # | Território | Setores | Moradores | 0–4 | 5–9 | 10–14 | 15–19 | Crianças 0–14 | Setores em sigilo | Setores do miolo herdados |",
         "|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|"]
    for r in terr.sort_values("numero").itertuples():
        L.append(f"| {r.numero} | {r.nome} | {r.setores} | {br(r.pop_total)} | {br(r.pop_0_4)} | {br(r.pop_5_9)} | {br(r.pop_10_14)} | "
                 f"{br(r.pop_15_19)} | {br(r.pop_0_4 + r.pop_5_9 + r.pop_10_14)} | {r.setores_com_sigilo} | {r.setores_miolo} |")
    L += ["", f"- Soma dos setores: **{br(soma)}** moradores. Total oficial de Cotia (SIDRA, tabela 4709): **{br(oficial)}**. "
          f"Diferença: {br(oficial - soma)} ({pct((oficial - soma) / oficial)}), que corresponde aos {int(tab.sigilo.sum())} setores em sigilo "
          f"(menos de 5 domicílios, valores \"X\" do IBGE). Limite do plano: 1%.",
          f"- Setores sem nenhum registro na tabela de demografia (sem moradores): {int(tab.sem_dado.sum())}.",
          f"- Miolo sem CRAS (verde-pálido): {int((tab.metodo == 'miolo sem CRAS → vizinho').sum())} setores e "
          f"{br(pop_miolo)} moradores ({pct(pop_miolo / oficial)} de Cotia). " +
          ("**Acima de 2%: o plano pede decisão do João.** Por ora, cada setor foi para o vizinho com a maior fronteira comum."
           if pop_miolo / oficial > 0.02 else "Abaixo de 2%: cada setor foi para o vizinho com a maior fronteira comum."), "",
          "## Setores de fronteira duvidosos", "",
          "Critérios: setor do miolo ou sem cor no mapa (herdou o vizinho), cor sob o ponto diferente da cor dominante do polígono, "
          "ou menos de 60% de votos na janela do ponto.", "",
          "| Setor | Distrito | Território | Como | Cor sob o ponto | Cor dominante do polígono | Moradores |", "|---|---|---|---|---|---|---:|"]
    nome = {t[0]: t[1] for t in TERRITORIOS} | {MIOLO: "miolo", 0: "sem cor"}
    for r in tab[tab.fronteira_duvidosa].sort_values(["territorio", "CD_SETOR"]).itertuples():
        pop = "" if pd.isna(r.V01006) else f"{int(r.V01006)}"
        L.append(f"| {r.CD_SETOR} | {r.NM_DIST} | {nome[r.territorio]} | {r.metodo} | {nome[r.classe_ponto]} | "
                 f"{nome[r.classe_poligono]} | {pop} |")
    L += ["", "## Listas de bairros do PMAS", "",
          "O IBGE não tem bairros cadastrados para Cotia, então os setores não trazem nome de bairro para conferir "
          "contra as listas. A conferência por bairro é feita nos equipamentos (bairro do endereço × lista do território), "
          "no relatório `territorio-equipamentos.md`.", ""]
    L += [f"- {nome[t]}: {len(b)} bairros na lista" for t, b in bairros.items()]
    (VERIFICACOES / "territorios.md").write_text("\n".join(L) + "\n", encoding="utf-8")


def br(n):
    return f"{int(n):,}".replace(",", ".")


def pct(x):
    return f"{x:.2%}".replace(".", ",")


def ler_listas_bairros():
    texto = (INSUMOS / "territorios-cras.md").read_text(encoding="utf-8")
    listas = {}
    for m in re.finditer(r"^## (\d)\..*?\*\*Bairros:\*\* (.*?)\.\s*$", texto, re.M | re.S):
        listas[int(m.group(1))] = [b.strip() for b in m.group(2).split(",") if b.strip()]
    return listas


def pagina(setores, tab, mat, img):
    """Mapa de conferência: setores coloridos pelo território, dúvidas em vermelho, mapa do PMAS sobreposto."""
    s = setores[["CD_SETOR", "geometry"]].copy()
    s["t"] = tab.territorio.values
    s["d"] = tab.fronteira_duvidosa.values
    s["m"] = tab.metodo.values
    s["pop"] = tab.V01006.fillna(-1).astype(int).values
    s["geometry"] = s.to_crs(UTM).geometry.simplify(4).to_crs(4326)
    gj = json.loads(s.to_json(drop_id=True))
    for f in gj["features"]:
        f["geometry"]["coordinates"] = json.loads(re.sub(r"(\d+\.\d{5})\d+", r"\1", json.dumps(f["geometry"]["coordinates"])))
    # cantos do PNG em lat/lon (transformação inversa), para sobrepor a imagem
    a, b, d, e, xoff, yoff = mat
    inv = np.linalg.inv(np.array([[a, b], [d, e]]))
    w, h = img.size
    cantos = []
    for u, v in ((0, 0), (w, h)):
        X, Y = inv @ np.array([u - xoff, v - yoff])
        p = gpd.GeoSeries([Point(X, Y)], crs=UTM).to_crs(4326).iloc[0]
        cantos.append([p.y, p.x])
    png64 = base64.b64encode(PNG.read_bytes()).decode()
    cores = {t[0]: "#%02x%02x%02x" % t[3] for t in TERRITORIOS}
    nomes = {t[0]: t[1] for t in TERRITORIOS}
    modelo = (VERIFICACOES.parent.parent / "scripts" / "modelo-territorios.html").read_text(encoding="utf-8")
    html = (modelo.replace("/*SETORES*/null", json.dumps(gj, ensure_ascii=False))
            .replace("/*CANTOS*/null", json.dumps(cantos))
            .replace("/*CORES*/null", json.dumps(cores)).replace("/*NOMES*/null", json.dumps(nomes, ensure_ascii=False))
            .replace("{{PNG}}", png64).replace("{{HOJE}}", HOJE))
    (VERIFICACOES / "conferir-territorios.html").write_text(html, encoding="utf-8")


if __name__ == "__main__":
    main()
