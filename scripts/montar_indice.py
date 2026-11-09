"""Índice de Oferta e Acesso a Equipamentos para a Infância (skill indice-oferta-cotia, Etapas 1 e 2).

Compara a oferta e o acesso a equipamentos públicos para crianças entre os 7 territórios de CRAS.
Decisão, indicadores e fontes: dados/indice/escolha-do-indice.md. O script não acessa a rede.

Entradas:
  site/data/territorios.geojson              numero, nome, pop_0_4, pop_5_9, pop_10_14, pop_total,
                                             n_saude_atencao_basica
  site/data/equipamentos.csv                 id, camada, subtipo, territorio (nome), lat, lon
  dados/educacao-inep.csv                    id, _mat_creche, _mat_pre (o território vem de equipamentos.csv)
  dados/verificacoes/setores-territorio.csv  CD_SETOR, territorio (número), V01031, V01032, V01033
  dados/brutos/setores-cotia-2022.geojson    geometria dos setores
Saídas:
  dados/indice/indice-territorios.csv        valor, posto e pontos de cada indicador; índice, posição e faixa
  dados/indice/sensibilidade.csv             posição em cada cenário e amplitude
  dados/indice/sensibilidade-valores.csv     valor do índice em cada cenário
  dados/indice/parada-1.md                   resumo para a Parada 1
  site/data/indice.json                      o que o site mostra: indicadores, índice e faixa de cada território,
                                             e o valor de Cotia inteira em cada indicador

Crianças por setor: V01031 + V01032 + V01033. Um "X" do IBGE em qualquer faixa deixa o setor inteiro
ausente, nunca zero (decisão do João em 08/11/2026). Assim a soma por setor dá 57.157 crianças, enquanto
os campos do territorios.geojson, usados em E1, E2 e S1, somam 57.452. A diferença são as 295 crianças
publicadas nos 39 setores com alguma faixa escondida.
"""
import json

import geopandas as gpd
import numpy as np
import pandas as pd

from comum import BRUTOS, DADOS, SITE_DATA, VERIFICACOES

INDICE = DADOS / "indice"
UTM = 31983  # SIRGAS 2000 / UTM 23S, o mesmo de desenhar_territorios.py
RAIO_S2_M = 1500

NOME = "Índice de Oferta e Acesso a Equipamentos para a Infância"
FRASE = ("Este índice compara a oferta e o acesso a equipamentos públicos para crianças entre os 7 territórios de "
         "Cotia. Não mede a qualidade do atendimento, a saúde das crianças nem a rede particular.")
# Formato do site: faixas, como recomendado na Parada 1 (3 territórios variam 3 ou mais posições)
FORMATO_SITE = "faixa"

INDICADORES = {
    # id: (dimensão, nome, sentido, unidade)
    "E1": ("educacao", "Matrículas em creche", "maior", "matrículas por 100 crianças de 0–4"),
    "E2": ("educacao", "Matrículas em pré-escola", "maior", "matrículas por 100 crianças de 0–4"),
    "S1": ("saude", "UBS por crianças", "maior", "UBS por 10 mil crianças de 0–14"),
    "S2": ("saude", "Crianças perto de UBS", "maior", "% das crianças a até 1,5 km de uma UBS"),
    "S3": ("saude", "Distância à urgência", "menor", "m, média ponderada por crianças"),
    "S4": ("saude", "Distância ao CAPS Infantil", "menor", "m, média ponderada por crianças"),
    "A1": ("assistencia", "Distância ao CRAS", "menor", "m, média ponderada por crianças"),
    "A2": ("assistencia", "Distância ao Conselho Tutelar", "menor", "m, média ponderada por crianças"),
}
DIMENSOES = {"educacao": ["E1", "E2"], "saude": ["S1", "S2", "S3", "S4"], "assistencia": ["A1", "A2"]}
NOMES_DIMENSOES = {"educacao": "Educação infantil", "saude": "Saúde", "assistencia": "Assistência e proteção"}
CASAS = {"E1": 1, "E2": 1, "S1": 2, "S2": 1, "S3": 0, "S4": 0, "A1": 0, "A2": 0}

# Conferido em 08/11/2026 em https://pmc.ncbi.nlm.nih.gov/articles/PMC8968942 (Buccini et al.):
# Tabela 1 traz 31 pesos analíticos que somam 118,35 (média 3,818); "Coverage of daycare and preschool"
# pesa 3,79 e "Coverage of primary healthcare", 3,97. O Box 1 define a cobertura como matrículas de
# creche e pré-escola somadas ÷ população com menos de 5 anos × 100.
IMAPI_CONFIRMADO = True
PESOS_IMAPI = {"E1": 3.79 / 2, "E2": 3.79 / 2, "S1": 3.97,
               "S2": 3.82, "S3": 3.82, "S4": 3.82, "A1": 3.82, "A2": 3.82}

CONFERENCIAS = {
    "setores": 754,
    "criancas_setores": 57157,
    "criancas_territorios": 57452,
    "setores_parciais": 39,
    "criancas_setores_parciais": 295,
    "setores_sem_faixa": 35,
    "moradores": 274163,
    "equipamentos": 132,
    "escolas": 82,
    "mat_creche": 5832,
    "mat_pre": 5895,
}
CONJUNTOS = {
    # nome: (filtro, quantidade esperada, rótulo no relatório)
    "UBS": (lambda e: e.camada == "saude_atencao_basica", 26, "UBS"),
    "urgência e hospital": (lambda e: e.camada.isin(["saude_urgencia", "saude_hospital"]), 5, "pontos de urgência e hospital"),
    "urgência sem hospital": (lambda e: e.camada == "saude_urgencia", 4, "pontos de urgência sem o hospital"),
    "CAPSi": (lambda e: e.subtipo == "CAPSi", 1, "CAPSi"),
    "CRAS": (lambda e: e.subtipo == "CRAS", 7, "CRAS"),
    "Conselho Tutelar": (lambda e: e.camada == "protecao", 2, "Conselhos Tutelares"),
}

CENARIOS = [
    ("base", {}),
    ("pesos_por_indicador", {"pesos": "igual"}),
    ("pesos_imapi", {"pesos": "imapi"}),
    ("norm_minmax", {"norm": "minmax"}),
    ("norm_zscore", {"norm": "zscore"}),
    ("sem_municipais", {"fora": ["S4", "A2"], "urgencia": "urgência sem hospital"}),
    *[(f"sem_{k}", {"fora": [k]}) for k in INDICADORES],
    ("s2_1km", {"raio": 1000}),
    ("s2_2km", {"raio": 2000}),
    ("s2_2sfca", {"s2": "2sfca"}),
]
DESCRICAO_CENARIOS = {
    "base": "postos, pesos iguais por dimensão",
    "pesos_por_indicador": "os 8 indicadores com o mesmo peso",
    "pesos_imapi": "E1 e E2 dividem 3,79; S1 = 3,97; os outros 5 = 3,82",
    "norm_minmax": "min-max de 0 a 100 no lugar dos postos",
    "norm_zscore": "z-score (ddof=0) no lugar dos postos",
    "sem_municipais": "S3 sem o hospital; S4 e A2 fora",
    "s2_1km": "S2 com raio de 1.000 m",
    "s2_2km": "S2 com raio de 2.000 m",
    "s2_2sfca": "S2 trocado por 2SFCA (raio de 1.500 m, capacidade 1 por UBS)",
}


def conferir(condicao, mensagem):
    if not condicao:
        raise SystemExit(f"Conferência falhou: {mensagem}")


# ---------- leitura e conferências ----------

def ler_territorios():
    t = gpd.read_file(SITE_DATA / "territorios.geojson")
    campos = ["numero", "nome", "pop_total", "pop_0_4", "pop_5_9", "pop_10_14", "n_saude_atencao_basica"]
    ausentes = [c for c in campos if c not in t.columns]
    conferir(not ausentes, f"campos ausentes em territorios.geojson: {ausentes}")
    t = pd.DataFrame(t[campos]).sort_values("numero").set_index("numero")
    conferir(list(t.index) == list(range(1, 8)), "os territórios não são numerados de 1 a 7")
    t["criancas"] = t.pop_0_4 + t.pop_5_9 + t.pop_10_14
    conferir(int(t.pop_total.sum()) == CONFERENCIAS["moradores"],
             f"moradores em territorios.geojson: {int(t.pop_total.sum())}, esperado {CONFERENCIAS['moradores']}")
    conferir(int(t.criancas.sum()) == CONFERENCIAS["criancas_territorios"],
             f"crianças de 0–14 nos territórios: {int(t.criancas.sum())}, esperado {CONFERENCIAS['criancas_territorios']}")
    return t


def ler_setores(territorios):
    s = pd.read_csv(VERIFICACOES / "setores-territorio.csv", dtype=str)
    g = gpd.read_file(BRUTOS / "setores-cotia-2022.geojson")[["CD_SETOR", "geometry"]]
    conferir(len(s) == CONFERENCIAS["setores"] and len(g) == CONFERENCIAS["setores"],
             f"setores: {len(s)} no CSV e {len(g)} no GeoJSON, esperado {CONFERENCIAS['setores']}")
    conferir(set(s.CD_SETOR) == set(g.CD_SETOR) and not s.CD_SETOR.duplicated().any(),
             "os setores do CSV e do GeoJSON não casam um a um")

    faixas = s[["V01031", "V01032", "V01033"]].apply(pd.to_numeric, errors="coerce")
    s["criancas"] = faixas.sum(axis=1, skipna=False)
    parcial = faixas.isna().any(axis=1) & faixas.notna().any(axis=1)
    sem_faixa = faixas.isna().all(axis=1)
    s["territorio"] = pd.to_numeric(s.territorio, errors="coerce")
    conferir(s.territorio.isin(territorios.index).all(), "há setor sem território de 1 a 7")

    conferir(int(parcial.sum()) == CONFERENCIAS["setores_parciais"],
             f"setores com alguma faixa escondida: {int(parcial.sum())}, esperado {CONFERENCIAS['setores_parciais']}")
    conferir(int(sem_faixa.sum()) == CONFERENCIAS["setores_sem_faixa"],
             f"setores sem nenhuma faixa: {int(sem_faixa.sum())}, esperado {CONFERENCIAS['setores_sem_faixa']}")
    publicadas_parciais = int(faixas[parcial].sum().sum())
    conferir(publicadas_parciais == CONFERENCIAS["criancas_setores_parciais"],
             f"crianças publicadas nos setores parciais: {publicadas_parciais}, "
             f"esperado {CONFERENCIAS['criancas_setores_parciais']}")
    total = int(s.criancas.sum())
    conferir(total == CONFERENCIAS["criancas_setores"],
             f"crianças de 0–14 somando setores: {total}, esperado {CONFERENCIAS['criancas_setores']}")
    conferir(total + publicadas_parciais == int(territorios.criancas.sum()),
             "setores e territórios não se reconciliam pelas crianças dos setores parciais")

    geo = g.merge(s[["CD_SETOR", "territorio", "criancas"]], on="CD_SETOR").to_crs(UTM)
    ponto = geo.geometry.representative_point()
    setores = pd.DataFrame({"CD_SETOR": geo.CD_SETOR, "territorio": geo.territorio.astype(int),
                            "criancas": geo.criancas, "x": ponto.x, "y": ponto.y})
    setores = setores.sort_values("CD_SETOR").reset_index(drop=True)
    parciais = {int(t): int(n) for t, n in s[parcial].groupby("territorio").size().items()}
    return setores, parciais


def ler_equipamentos(territorios):
    e = pd.read_csv(SITE_DATA / "equipamentos.csv", dtype=str).fillna("")
    conferir(len(e) == CONFERENCIAS["equipamentos"],
             f"equipamentos: {len(e)}, esperado {CONFERENCIAS['equipamentos']}")
    conferir(((e.territorio != "") & (e.lat != "") & (e.lon != "")).all(),
             "há equipamento sem território ou sem coordenada")
    conferir(e.territorio.isin(territorios.nome).all(), "há equipamento com território fora dos 7")
    pontos = gpd.GeoSeries(gpd.points_from_xy(e.lon.astype(float), e.lat.astype(float)), crs=4326).to_crs(UTM)
    e["x"], e["y"] = pontos.x.values, pontos.y.values
    e["numero"] = e.territorio.map(dict(zip(territorios.nome, territorios.index)))
    for nome, (filtro, esperado, _) in CONJUNTOS.items():
        n = int(filtro(e).sum())
        conferir(n == esperado, f"pontos de {nome}: {n}, esperado {esperado}")
    ubs = e[CONJUNTOS["UBS"][0](e)].groupby("numero").size().reindex(territorios.index, fill_value=0)
    conferir((ubs == territorios.n_saude_atencao_basica).all(),
             "UBS por território em equipamentos.csv diferem de n_saude_atencao_basica")
    return e


def ler_escolas(equipamentos):
    d = pd.read_csv(DADOS / "educacao-inep.csv", dtype=str).fillna("")
    esc = d[["id", "_mat_creche", "_mat_pre"]].merge(equipamentos[["id", "numero"]], on="id", how="inner")
    conferir(len(d) == CONFERENCIAS["escolas"] and len(esc) == CONFERENCIAS["escolas"],
             f"escolas casadas por id: {len(esc)} de {len(d)}, esperado {CONFERENCIAS['escolas']}")
    esc[["_mat_creche", "_mat_pre"]] = esc[["_mat_creche", "_mat_pre"]].astype(int)
    conferir(int(esc._mat_creche.sum()) == CONFERENCIAS["mat_creche"],
             f"matrículas em creche: {int(esc._mat_creche.sum())}, esperado {CONFERENCIAS['mat_creche']}")
    conferir(int(esc._mat_pre.sum()) == CONFERENCIAS["mat_pre"],
             f"matrículas em pré-escola: {int(esc._mat_pre.sum())}, esperado {CONFERENCIAS['mat_pre']}")
    return esc


# ---------- indicadores ----------

def matriz_distancias(setores, pontos):
    dx = setores.x.to_numpy()[:, None] - pontos.x.to_numpy()[None, :]
    dy = setores.y.to_numpy()[:, None] - pontos.y.to_numpy()[None, :]
    return np.hypot(dx, dy)


def media_ponderada(setores, valores):
    peso = setores.criancas
    return (peso * valores).groupby(setores.territorio).sum() / peso.groupby(setores.territorio).sum()


def s2_raio(setores, ubs, raio):
    perto = pd.Series(np.where(matriz_distancias(setores, ubs).min(axis=1) <= raio, setores.criancas, 0.0),
                      index=setores.index)
    return perto.groupby(setores.territorio).sum() / setores.criancas.groupby(setores.territorio).sum() * 100


def demanda_2sfca(setores, ubs, raio):
    """Crianças a até `raio` de cada UBS (passo 1 do 2SFCA) e a matriz de quem está dentro do raio."""
    dentro = matriz_distancias(setores, ubs) <= raio
    return (dentro * setores.criancas.to_numpy()[:, None]).sum(axis=0), dentro


def s2_2sfca(setores, ubs, raio):
    """2SFCA (Luo e Wang, 2003): capacidade 1 por UBS; resultado em UBS por 10 mil crianças.
    UBS sem nenhuma criança no raio não entra."""
    demanda, dentro = demanda_2sfca(setores, ubs, raio)
    razao = np.divide(1.0, demanda, out=np.zeros_like(demanda, dtype=float), where=demanda > 0)
    acesso = pd.Series((dentro * razao[None, :]).sum(axis=1), index=setores.index)
    return media_ponderada(setores, acesso) * 10_000


def calcular_valores(territorios, setores, equipamentos, escolas, raio=RAIO_S2_M,
                     urgencia="urgência e hospital", s2="raio"):
    validos = setores[setores.criancas.notna()]
    pontos = {nome: equipamentos[filtro(equipamentos)] for nome, (filtro, _, _) in CONJUNTOS.items()}
    mat = escolas.groupby("numero")[["_mat_creche", "_mat_pre"]].sum().reindex(territorios.index, fill_value=0)

    v = pd.DataFrame(index=territorios.index)
    v["E1"] = mat._mat_creche / territorios.pop_0_4 * 100
    v["E2"] = mat._mat_pre / territorios.pop_0_4 * 100
    v["S1"] = territorios.n_saude_atencao_basica / territorios.criancas * 10_000
    if s2 == "2sfca":
        v["S2"] = s2_2sfca(validos, pontos["UBS"], RAIO_S2_M)
    else:
        v["S2"] = s2_raio(validos, pontos["UBS"], raio)
    for ind, conjunto in (("S3", urgencia), ("S4", "CAPSi"), ("A1", "CRAS"), ("A2", "Conselho Tutelar")):
        distancia = pd.Series(matriz_distancias(validos, pontos[conjunto]).min(axis=1), index=validos.index)
        v[ind] = media_ponderada(validos, distancia)
    conferir(not v.isna().any().any(), "há indicador sem valor")
    return v


def valores_cotia(territorios, setores, equipamentos, escolas):
    """Os 8 indicadores para Cotia inteira, com as mesmas bases do cálculo por território."""
    validos = setores[setores.criancas.notna()]
    pontos = {nome: equipamentos[filtro(equipamentos)] for nome, (filtro, _, _) in CONJUNTOS.items()}
    peso = validos.criancas.to_numpy()
    c = {"E1": escolas._mat_creche.sum() / territorios.pop_0_4.sum() * 100,
         "E2": escolas._mat_pre.sum() / territorios.pop_0_4.sum() * 100,
         "S1": territorios.n_saude_atencao_basica.sum() / territorios.criancas.sum() * 10_000}
    perto = matriz_distancias(validos, pontos["UBS"]).min(axis=1) <= RAIO_S2_M
    c["S2"] = peso[perto].sum() / peso.sum() * 100
    for ind, conjunto in (("S3", "urgência e hospital"), ("S4", "CAPSi"), ("A1", "CRAS"), ("A2", "Conselho Tutelar")):
        c[ind] = (peso * matriz_distancias(validos, pontos[conjunto]).min(axis=1)).sum() / peso.sum()
    return {i: float(v) for i, v in c.items()}


# ---------- normalização, pesos e índice ----------

def normalizar(valores, metodo):
    n = len(valores)
    postos, pontos = pd.DataFrame(index=valores.index), pd.DataFrame(index=valores.index)
    for ind in valores.columns:
        x = valores[ind].round(9)  # evita que ruído de ponto flutuante desempate valores iguais
        menor_melhor = INDICADORES[ind][2] == "menor"
        postos[ind] = x.rank(ascending=menor_melhor, method="min").astype(int)
        if metodo == "postos":
            pontos[ind] = (n - postos[ind]) / (n - 1) * 100
        elif metodo == "minmax":
            amplitude = x.max() - x.min()
            if amplitude == 0:
                pontos[ind] = 100.0
            else:
                pontos[ind] = ((x.max() - x) if menor_melhor else (x - x.min())) / amplitude * 100
        elif metodo == "zscore":
            desvio = x.std(ddof=0)
            z = (x - x.mean()) / desvio if desvio else x * 0.0
            pontos[ind] = -z if menor_melhor else z
    return postos, pontos


def pesos(presentes, tipo="dimensao"):
    if tipo == "igual":
        return {i: 1 / len(presentes) for i in presentes}
    if tipo == "imapi":
        total = sum(PESOS_IMAPI[i] for i in presentes)
        return {i: PESOS_IMAPI[i] / total for i in presentes}
    dimensoes = {d: [i for i in inds if i in presentes] for d, inds in DIMENSOES.items()}
    dimensoes = {d: inds for d, inds in dimensoes.items() if inds}
    return {i: 1 / len(dimensoes) / len(inds) for inds in dimensoes.values() for i in inds}


def posicoes(indice):
    return indice.round(9).rank(ascending=False, method="min").astype(int)


def rodar_cenario(territorios, setores, equipamentos, escolas, opcoes):
    valores = calcular_valores(territorios, setores, equipamentos, escolas,
                               raio=opcoes.get("raio", RAIO_S2_M),
                               urgencia=opcoes.get("urgencia", "urgência e hospital"),
                               s2=opcoes.get("s2", "raio"))
    presentes = [i for i in INDICADORES if i not in opcoes.get("fora", [])]
    postos, pontos = normalizar(valores[presentes], opcoes.get("norm", "postos"))
    w = pesos(presentes, opcoes.get("pesos", "dimensao"))
    indice = sum(pontos[i] * w[i] for i in presentes)
    return {"valores": valores, "postos": postos, "pontos": pontos, "pesos": w,
            "indice": indice, "posicao": posicoes(indice)}


def faixas(posicao):
    return posicao.map(lambda p: "alta" if p <= 2 else ("média" if p <= 5 else "baixa"))


# ---------- saídas ----------

def arredondar(x, casas):
    v = round(float(x), casas)
    return int(v) if casas == 0 else v


def escrever_json(territorios, base, cotia, n_cenarios):
    faixa = faixas(base["posicao"])
    dados = {
        "nome": NOME,
        "frase": FRASE,
        "formato": FORMATO_SITE,
        "faixas": [{"id": "alta", "regra": "os 2 maiores índices"},
                   {"id": "média", "regra": "os 3 índices seguintes"},
                   {"id": "baixa", "regra": "os 2 menores índices"}],
        "cenarios_sensibilidade": n_cenarios,
        "dimensoes": [{"id": d, "nome": NOMES_DIMENSOES[d], "indicadores": inds} for d, inds in DIMENSOES.items()],
        "indicadores": [{"id": i, "dimensao": INDICADORES[i][0], "nome": INDICADORES[i][1], "sentido": INDICADORES[i][2],
                         "unidade": INDICADORES[i][3], "peso": round(base["pesos"][i], 6),
                         "cotia": arredondar(cotia[i], CASAS[i])} for i in INDICADORES],
        "territorios": [{"numero": int(t), "nome": territorios.nome[t], "faixa": faixa[t],
                         "indice": round(float(base["indice"][t]), 1),
                         "valores": {i: arredondar(base["valores"][i][t], CASAS[i]) for i in INDICADORES}}
                        for t in territorios.index],
    }
    (SITE_DATA / "indice.json").write_text(json.dumps(dados, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")


# ---------- relatório ----------

def num(x, casas=0):
    texto = f"{x:,.{casas}f}"
    return texto.replace(",", "§").replace(".", ",").replace("§", ".")


def tabela_md(cabecalho, linhas):
    saida = ["| " + " | ".join(cabecalho) + " |", "|" + "|".join("---" for _ in cabecalho) + "|"]
    saida += ["| " + " | ".join(str(c) for c in linha) + " |" for linha in linhas]
    return saida


def escrever_relatorio(territorios, setores, base, sens_pos, cenarios_rodados, parciais, ubs_sem_demanda):
    nomes = territorios.nome
    amplitude = sens_pos.max(axis=1) - sens_pos.min(axis=1)
    recomenda_faixas = bool((amplitude >= 3).any())
    mudanca = (sens_pos.sub(sens_pos["base"], axis=0)).abs().sum().drop("base").sort_values(ascending=False)
    ordem = base["posicao"].sort_values().index

    L = ["# Índice de Oferta e Acesso a Equipamentos para a Infância — Parada 1", "",
         "> Este índice compara a oferta e o acesso a equipamentos públicos para crianças entre os 7 territórios "
         "de Cotia. Não mede a qualidade do atendimento, a saúde das crianças nem a rede particular.", "",
         "Gerado por `scripts/montar_indice.py`. O valor do índice vai de 0 a 100 e é uma régua entre os 7 "
         "territórios, sem sentido absoluto.", "",
         "## Resultado do cálculo-base", ""]
    L += tabela_md(["Posição", "Território", "Índice", "Faixa (2 · 3 · 2)"],
                   [[base["posicao"][t], nomes[t], num(base["indice"][t], 1), faixas(base["posicao"])[t]] for t in ordem])
    L += ["", "## Indicadores: valor e posto (1 = melhor)", ""]
    L += tabela_md(["Indicador", "Unidade", "Melhor"] + [nomes[t] for t in territorios.index],
                   [[f"{i} {INDICADORES[i][1]}", INDICADORES[i][3], INDICADORES[i][2]]
                    + [f"{num(base['valores'][i][t], CASAS[i])} ({base['postos'][i][t]}º)" for t in territorios.index]
                    for i in INDICADORES])
    L += ["", "## Pontos por indicador e pesos", "",
          "Pontos = (7 − posto) ÷ 6 × 100. Pesos: cada dimensão vale 1/3, dividido igualmente entre seus indicadores.", ""]
    L += tabela_md(["Indicador", "Peso"] + [nomes[t] for t in territorios.index],
                   [[i, num(base["pesos"][i] * 100, 2) + "%"] + [num(base["pontos"][i][t], 1) for t in territorios.index]
                    for i in INDICADORES])

    L += ["", f"## Sensibilidade: posição em cada um dos {len(cenarios_rodados)} cenários", ""]
    L += tabela_md(["Cenário", "O que muda"] + [nomes[t] for t in territorios.index],
                   [[c, DESCRICAO_CENARIOS.get(c, "retira " + c[4:] + "; o peso passa aos outros da dimensão")]
                    + [sens_pos[c][t] for t in territorios.index] for c in cenarios_rodados])
    L += ["", "### Amplitude por território", ""]
    linhas = []
    for t in ordem:
        p = sens_pos.loc[t]
        melhor = ", ".join(c for c in cenarios_rodados if p[c] == p.min())
        pior = ", ".join(c for c in cenarios_rodados if p[c] == p.max())
        linhas.append([nomes[t], base["posicao"][t], f"{p.min()}º a {p.max()}º", amplitude[t],
                       f"{p.min()}º em: {melhor}" if p.min() != base["posicao"][t] else "—",
                       f"{p.max()}º em: {pior}" if p.max() != base["posicao"][t] else "—"])
    L += tabela_md(["Território", "Posição-base", "Faixa de posições", "Amplitude", "Melhor posição", "Pior posição"], linhas)
    L += ["", "### Cenários que mais mexem na ordem", "",
          "Soma, nos 7 territórios, da diferença de posição em relação ao cálculo-base.", ""]
    L += tabela_md(["Cenário", "Soma das mudanças"], [[c, int(v)] for c, v in mudanca.items() if v > 0][:8])

    L += ["", "## Recomendação: posições ou faixas", ""]
    if recomenda_faixas:
        variam = ", ".join(f"{nomes[t]} ({amplitude[t]})" for t in amplitude.index if amplitude[t] >= 3)
        L += [f"**Mostrar faixas, não posições.** Pela regra da skill, basta um território variar 3 ou mais "
              f"posições entre os cenários, e aqui variam: {variam}. Faixas pelo cálculo-base: alta para os 2 "
              f"maiores índices, média para os 3 seguintes e baixa para os 2 menores."]
    else:
        L += ["**As posições são estáveis o bastante.** Nenhum território varia 3 ou mais posições entre os cenários."]

    sp = setores[setores.criancas.notna()].groupby("territorio").criancas.sum()
    L += ["", "## Base de crianças", "",
          "E1, E2 e S1 usam os campos de `territorios.geojson`. S2 a A2 usam a soma por setor, em que um \"X\" do "
          "IBGE em qualquer faixa tira o setor inteiro.", ""]
    L += tabela_md(["Território", "0–14 no geojson (E1, E2, S1)", "0–14 por setor (S2 a A2)", "Setores com faixa escondida"],
                   [[nomes[t], num(territorios.criancas[t]), num(sp.get(t, 0)), parciais.get(t, 0)] for t in territorios.index]
                   + [["Cotia", num(territorios.criancas.sum()), num(sp.sum()), sum(parciais.values())]])

    L += ["", "## IMAPI", "",
          "Conferido em 08/11/2026 em https://pmc.ncbi.nlm.nih.gov/articles/PMC8968942 (Buccini et al.). "
          "Tabela 1: 31 pesos analíticos, que somam 118,35 (média 3,818). Cobertura de creche e pré-escola pesa "
          "3,79, e cobertura de atenção primária, 3,97. Box 1: a cobertura soma as matrículas de creche e de "
          "pré-escola e divide pela população com menos de 5 anos. Aqui creche e pré-escola são dois indicadores "
          "com o mesmo denominador (0–4 anos), e S1 conta UBS, enquanto o IMAPI mede a população coberta por "
          "equipes. O cenário `pesos_imapi` foi mantido."]

    L += ["", "## Pontos de atenção", ""]
    zeros = [f"{i} = 0 em {nomes[t]}" for i in INDICADORES for t in territorios.index if base["valores"][i][t] == 0]
    empates = [f"{i}: {', '.join(nomes[t] for t in grupo)}" for i in INDICADORES
               for _, grupo in base["postos"][i].groupby(base["postos"][i]) if len(grupo) > 1]
    L += [f"- Valores zero: {'; '.join(zeros) if zeros else 'nenhum'}.",
          f"- Empates de posto no cálculo-base: {'; '.join(empates) if empates else 'nenhum'}.",
          f"- No 2SFCA, {len(ubs_sem_demanda)} das 26 UBS "
          f"{'não tem' if len(ubs_sem_demanda) == 1 else 'não têm'} criança a até 1,5 km do ponto de algum setor e "
          f"{'fica' if len(ubs_sem_demanda) == 1 else 'ficam'} fora: {', '.join(ubs_sem_demanda) or 'nenhuma'}.",
          "- 7 dos 9 pontos de assistência social e 1 dos 2 Conselhos Tutelares têm coordenada aproximada, o que "
          "afeta A1 e A2. O efeito aparece nos cenários `sem_A1` e `sem_A2`.",
          "- O território Central fica perto de quase todos os equipamentos municipais; por isso existe o "
          "cenário `sem_municipais`."]

    L += ["", "## Conferências que passaram", ""]
    L += [f"- {CONFERENCIAS['setores']} setores casados entre o CSV e o GeoJSON.",
          f"- Crianças de 0–14: {num(CONFERENCIAS['criancas_setores'])} somando setores (um X tira o setor) e "
          f"{num(CONFERENCIAS['criancas_territorios'])} somando os 7 territórios. A diferença de "
          f"{CONFERENCIAS['criancas_setores_parciais']} são as crianças publicadas nos "
          f"{CONFERENCIAS['setores_parciais']} setores com faixa escondida; outros {CONFERENCIAS['setores_sem_faixa']} "
          "setores não têm nenhuma faixa publicada.",
          f"- {num(CONFERENCIAS['moradores'])} moradores em territorios.geojson.",
          f"- {CONFERENCIAS['equipamentos']} equipamentos, todos com território e coordenada; "
          f"{CONFERENCIAS['escolas']} escolas casadas por id.",
          f"- {num(CONFERENCIAS['mat_creche'])} matrículas em creche e {num(CONFERENCIAS['mat_pre'])} em pré-escola.",
          "- Pontos: " + ", ".join(f"{esperado} {rotulo}" for _, esperado, rotulo in CONJUNTOS.values()) + "."]
    (INDICE / "parada-1.md").write_text("\n".join(L) + "\n", encoding="utf-8")
    return recomenda_faixas, amplitude, mudanca


def main():
    territorios = ler_territorios()
    setores, parciais = ler_setores(territorios)
    equipamentos = ler_equipamentos(territorios)
    escolas = ler_escolas(equipamentos)

    cenarios = [(nome, opcoes) for nome, opcoes in CENARIOS if nome != "pesos_imapi" or IMAPI_CONFIRMADO]
    resultados = {nome: rodar_cenario(territorios, setores, equipamentos, escolas, opcoes) for nome, opcoes in cenarios}
    base = resultados["base"]

    INDICE.mkdir(parents=True, exist_ok=True)
    tabela = pd.DataFrame({"nome": territorios.nome})
    for i in INDICADORES:
        tabela[f"{i}_valor"] = base["valores"][i].round(4)
        tabela[f"{i}_posto"] = base["postos"][i]
        tabela[f"{i}_pontos"] = base["pontos"][i].round(4)
    tabela["indice"] = base["indice"].round(4)
    tabela["posicao"] = base["posicao"]
    tabela["faixa"] = faixas(base["posicao"])
    tabela = tabela.sort_index().reset_index()
    tabela.to_csv(INDICE / "indice-territorios.csv", index=False, encoding="utf-8")

    nomes_cenarios = [nome for nome, _ in cenarios]
    sens_pos = pd.DataFrame({nome: resultados[nome]["posicao"] for nome in nomes_cenarios})
    sens_val = pd.DataFrame({nome: resultados[nome]["indice"].round(4) for nome in nomes_cenarios})
    saida = sens_pos.copy()
    saida.insert(0, "nome", territorios.nome)
    saida["amplitude"] = sens_pos.max(axis=1) - sens_pos.min(axis=1)
    saida.rename_axis("numero").reset_index().to_csv(INDICE / "sensibilidade.csv", index=False, encoding="utf-8")
    valores = sens_val.copy()
    valores.insert(0, "nome", territorios.nome)
    valores.rename_axis("numero").reset_index().to_csv(INDICE / "sensibilidade-valores.csv", index=False, encoding="utf-8")

    validos = setores[setores.criancas.notna()]
    ubs = equipamentos[CONJUNTOS["UBS"][0](equipamentos)]
    ubs_sem_demanda = sorted(ubs.nome[demanda_2sfca(validos, ubs, RAIO_S2_M)[0] == 0])
    recomenda_faixas, amplitude, mudanca = escrever_relatorio(
        territorios, setores, base, sens_pos, nomes_cenarios, parciais, ubs_sem_demanda)
    escrever_json(territorios, base, valores_cotia(territorios, setores, equipamentos, escolas), len(nomes_cenarios))

    print(f"{len(nomes_cenarios)} cenários; conferências ok")
    print(tabela[["numero", "nome", "indice", "posicao", "faixa"]].sort_values("posicao").to_string(index=False))
    print("Amplitude:", {territorios.nome[t]: int(a) for t, a in amplitude.items()})
    print("Recomendação:", "faixas" if recomenda_faixas else "posições")
    print("-> dados/indice/indice-territorios.csv, sensibilidade.csv, sensibilidade-valores.csv, parada-1.md;"
          " site/data/indice.json")


if __name__ == "__main__":
    main()
