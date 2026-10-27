"""Censo 2022 (IBGE): setores censitários de Cotia e população por faixa etária.

Downloads (ficam fora do Git):
  dados/brutos/SP_setores_CD2022.gpkg                        malha de setores de SP (~180 MB)
  dados/brutos/Agregados_por_setores_demografia_BR.zip       agregados de demografia (~22 MB)
  dados/brutos/dicionario_agregados_setores_20260520.xlsx    dicionário de variáveis
Saídas (versionadas):
  dados/brutos/setores-cotia-2022.geojson     setores de Cotia (EPSG:4326)
  dados/brutos/demografia-cotia-2022.csv      V01006 e faixas etárias por setor, com "X" preservado
  dados/brutos/populacao-oficial-cotia-2022.json  total oficial do município (SIDRA, tabela 4709)
"""
import io
import json
import sys
import zipfile

import geopandas as gpd
import pandas as pd
import requests

from comum import BRUTOS, HOJE, USER_AGENT

BASE = "https://ftp.ibge.gov.br/Censos/Censo_Demografico_2022/Agregados_por_Setores_Censitarios"
MALHA = f"{BASE}/malha_com_atributos/setores/gpkg/UF/SP/SP_setores_CD2022.gpkg"
DEMOGRAFIA = f"{BASE}/Agregados_por_Setor_csv/Agregados_por_setores_demografia_BR.zip"
DICIONARIO = f"{BASE}/dicionario_de_dados_agregados_por_setores_censitarios_20260520.xlsx"
SIDRA = "https://apisidra.ibge.gov.br/values/t/4709/n6/3513009/v/93/p/2022"
CD_MUN = "3513009"
VARIAVEIS = ["V01006", "V01031", "V01032", "V01033", "V01034"]


def baixar(url, destino):
    if destino.exists():
        return destino
    print(f"Baixando {url.rsplit('/', 1)[-1]} ...", flush=True)
    with requests.get(url, headers={"User-Agent": USER_AGENT}, stream=True, timeout=300) as r:
        r.raise_for_status()
        parcial = destino.with_suffix(destino.suffix + ".parcial")
        with parcial.open("wb") as f:
            for bloco in r.iter_content(1 << 20):
                f.write(bloco)
        parcial.replace(destino)
    return destino


def conferir_dicionario(caminho):
    """Imprime a descrição de cada variável usada, para conferir contra o plano."""
    achadas = {}
    for aba, df in pd.read_excel(caminho, sheet_name=None, header=None, dtype=str).items():
        for linha in df.fillna("").itertuples(index=False):
            celulas = [c.strip() for c in linha if c and c.strip()]
            for v in VARIAVEIS:
                if v in celulas and v not in achadas:
                    achadas[v] = (aba, " | ".join(celulas)[:200])
    for v in VARIAVEIS:
        print(f"  {v}: {achadas.get(v, ('?', 'NÃO ENCONTRADA NO DICIONÁRIO'))[1]}")
    return achadas


def main():
    BRUTOS.mkdir(parents=True, exist_ok=True)

    dic = baixar(DICIONARIO, BRUTOS / "dicionario_agregados_setores_20260520.xlsx")
    print("Variáveis no dicionário:")
    conferir_dicionario(dic)

    gpkg = baixar(MALHA, BRUTOS / "SP_setores_CD2022.gpkg")
    setores = gpd.read_file(gpkg, where=f"CD_MUN = '{CD_MUN}'").to_crs(4326)
    setores.to_file(BRUTOS / "setores-cotia-2022.geojson", driver="GeoJSON")
    print(f"Setores de Cotia: {len(setores)}; colunas: {list(setores.columns)[:25]}")

    zp = baixar(DEMOGRAFIA, BRUTOS / "Agregados_por_setores_demografia_BR.zip")
    with zipfile.ZipFile(zp) as z:
        nome = next(n for n in z.namelist() if n.lower().endswith(".csv"))
        with z.open(nome) as f:
            dem = pd.read_csv(io.TextIOWrapper(f, encoding="iso-8859-1"), sep=";", dtype=str)
    dem.columns = [c.strip() for c in dem.columns]
    cod = next(c for c in dem.columns if c.upper() == "CD_SETOR")
    dem = dem[dem[cod].str.startswith(CD_MUN)][[cod] + VARIAVEIS].rename(columns={cod: "CD_SETOR"})
    dem.to_csv(BRUTOS / "demografia-cotia-2022.csv", index=False, encoding="utf-8")
    print(f"Demografia: {len(dem)} setores de Cotia; com sigilo (X) em V01006: {(dem.V01006 == 'X').sum()}")

    oficial = BRUTOS / "populacao-oficial-cotia-2022.json"
    if not oficial.exists() or "--rebaixar" in sys.argv:
        r = requests.get(SIDRA, headers={"User-Agent": USER_AGENT}, timeout=60)
        r.raise_for_status()
        oficial.write_text(json.dumps({"municipio": "Cotia", "codigo_ibge": CD_MUN, "populacao_2022": int(r.json()[1]["V"]),
                                       "fonte": SIDRA, "data_coleta": HOJE}, ensure_ascii=False, indent=1), encoding="utf-8")
    total = json.loads(oficial.read_text(encoding="utf-8"))["populacao_2022"]
    print(f"População oficial de Cotia (Censo 2022, SIDRA 4709): {total}")


if __name__ == "__main__":
    main()
