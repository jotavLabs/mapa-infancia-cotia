"""Recorta do Censo Escolar 2025 (INEP) as escolas de Cotia com creche ou pré-escola.

O zip dos microdados (~540 MB) fica em dados/brutos/ e fora do Git; só o recorte de Cotia é versionado.
Variáveis conferidas no dicionário de 2025 (ANEXO I):
  - Tabela de Escola: CO_MUNICIPIO, CO_ENTIDADE, NO_ENTIDADE, TP_DEPENDENCIA (1 federal, 2 estadual,
    3 municipal, 4 privada), TP_SITUACAO_FUNCIONAMENTO (1 em atividade), IN_PODER_PUBLICO_PARCERIA,
    TP_PODER_PUBLICO_PARCERIA (1 municipal, 2 estadual, 3 ambos), TP_LOCALIZACAO.
  - Tabela de Matrícula: QT_MAT_INF_CRE, QT_MAT_INF_PRE.
  - IN_INF_CRE e IN_INF_PRE não existem mais na tabela de escola de 2025: oferta de creche/pré é
    definida por matrícula maior que zero.
  - Os campos de endereço e de coordenadas foram retirados dos microdados de 2025; vêm do Catálogo
    de Escolas (coletar_catalogo_escolas.py).

Saída: dados/brutos/inep-cotia-2025.csv
"""
import sys
import zipfile

import pandas as pd
import requests

from comum import BRUTOS, USER_AGENT

ANO = 2025
URL = "https://download.inep.gov.br/dados_abertos/microdados_censo_escolar_2025_.zip"
ZIP = BRUTOS / f"microdados_censo_escolar_{ANO}.zip"
CO_MUNICIPIO = 3513009

COLS_ESCOLA = ["CO_ENTIDADE", "NO_ENTIDADE", "CO_MUNICIPIO", "TP_DEPENDENCIA", "TP_CATEGORIA_ESCOLA_PRIVADA",
               "TP_LOCALIZACAO", "TP_SITUACAO_FUNCIONAMENTO", "IN_PODER_PUBLICO_PARCERIA", "TP_PODER_PUBLICO_PARCERIA"]
COLS_MATRICULA = ["CO_ENTIDADE", "QT_MAT_INF", "QT_MAT_INF_CRE", "QT_MAT_INF_PRE"]


def baixar():
    if ZIP.exists():
        return
    print(f"Baixando {URL} ...")
    with requests.get(URL, headers={"User-Agent": USER_AGENT}, stream=True, timeout=120) as r:
        r.raise_for_status()
        with ZIP.open("wb") as f:
            for bloco in r.iter_content(1 << 20):
                f.write(bloco)


def ler_cotia(z, sufixo, colunas):
    arq = next(n for n in z.namelist() if n.endswith(sufixo))
    partes = []
    with z.open(arq) as f:
        for bloco in pd.read_csv(f, sep=";", encoding="latin-1", usecols=colunas + (["CO_MUNICIPIO"] if "CO_MUNICIPIO" not in colunas else []),
                                 dtype=str, chunksize=50_000):
            partes.append(bloco[bloco.CO_MUNICIPIO == str(CO_MUNICIPIO)])
    return pd.concat(partes)


def main():
    BRUTOS.mkdir(parents=True, exist_ok=True)
    baixar()
    z = zipfile.ZipFile(ZIP)
    escolas = ler_cotia(z, f"Tabela_Escola_{ANO}_V2.csv", COLS_ESCOLA)
    matriculas = ler_cotia(z, f"Tabela_Matricula_{ANO}_V2.csv", COLS_MATRICULA).drop(columns="CO_MUNICIPIO")
    df = escolas.merge(matriculas, on="CO_ENTIDADE", how="left")
    for c in ["QT_MAT_INF", "QT_MAT_INF_CRE", "QT_MAT_INF_PRE"]:
        df[c] = pd.to_numeric(df[c], errors="coerce").fillna(0).astype(int)
    print(f"Cotia: {len(df)} escolas no Censo {ANO}")

    oferta = (df.QT_MAT_INF_CRE > 0) | (df.QT_MAT_INF_PRE > 0)
    ativa = df.TP_SITUACAO_FUNCIONAMENTO == "1"
    publica = df.TP_DEPENDENCIA.isin(["1", "2", "3"])
    conveniada = (df.TP_DEPENDENCIA == "4") & (df.IN_PODER_PUBLICO_PARCERIA == "1") & df.TP_PODER_PUBLICO_PARCERIA.isin(["1", "2", "3"])
    recorte = df[oferta & ativa & (publica | conveniada)].copy()
    recorte["conveniada"] = conveniada[recorte.index].map({True: "1", False: "0"})
    saida = BRUTOS / f"inep-cotia-{ANO}.csv"
    recorte.sort_values(["TP_DEPENDENCIA", "NO_ENTIDADE"]).to_csv(saida, index=False, encoding="utf-8")

    print(f"  com creche ou pré, em atividade: {(oferta & ativa).sum()} (todas as redes)")
    print(f"  públicas: {(oferta & ativa & publica).sum()} | privadas conveniadas: {(oferta & ativa & conveniada).sum()}")
    print(recorte.groupby(["TP_DEPENDENCIA", "conveniada"]).agg(escolas=("CO_ENTIDADE", "size"), creche=("QT_MAT_INF_CRE", "sum"), pre=("QT_MAT_INF_PRE", "sum")).to_string())
    print(f"-> {saida.relative_to(BRUTOS.parent.parent)}")


if __name__ == "__main__":
    sys.exit(main())
