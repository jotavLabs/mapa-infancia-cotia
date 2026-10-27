"""Baixa o contorno oficial de Cotia da API de malhas do IBGE.

Saídas:
  dados/brutos/ibge-malha-cotia-<data>.geojson
  site/data/cotia.geojson
Sem --rebaixar, reaproveita o download mais recente já salvo, e a data de coleta é a dele.
"""
import json
import re
import sys

import requests

from comum import BRUTOS, HOJE, SITE_DATA, USER_AGENT

URL = "https://servicodados.ibge.gov.br/api/v3/malhas/municipios/3513009"


def main():
    BRUTOS.mkdir(parents=True, exist_ok=True)
    salvos = sorted(BRUTOS.glob("ibge-malha-cotia-*.geojson"))
    if salvos and "--rebaixar" not in sys.argv:
        bruto = salvos[-1]
        print(f"Usando {bruto.name} já salvo; passe --rebaixar para baixar de novo.")
    else:
        r = requests.get(URL, params={"formato": "application/vnd.geo+json", "qualidade": "maxima"},
                         headers={"User-Agent": USER_AGENT}, timeout=60)
        r.raise_for_status()
        bruto = BRUTOS / f"ibge-malha-cotia-{HOJE}.geojson"
        bruto.write_text(json.dumps(r.json()), encoding="utf-8")
    data = re.search(r"(\d{4}-\d{2}-\d{2})", bruto.name).group(1)
    gj = json.loads(bruto.read_text(encoding="utf-8"))
    for f in gj["features"]:
        f["properties"] = {"nome": "Cotia", "codigo_ibge": "3513009", "fonte": "IBGE — API de malhas v3",
                           "fonte_url": f"{URL}?formato=application/vnd.geo%2Bjson&qualidade=maxima", "data_coleta": data}
    SITE_DATA.mkdir(parents=True, exist_ok=True)
    (SITE_DATA / "cotia.geojson").write_text(json.dumps(gj, ensure_ascii=False), encoding="utf-8")
    print(f"Contorno de Cotia ({data}) -> site/data/cotia.geojson")


if __name__ == "__main__":
    main()
