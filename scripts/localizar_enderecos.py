"""Camadas 8 e 9 — CRAS, CREAS e Conselhos Tutelares.

Os endereços vêm de listas verificadas à mão contra fontes oficiais (fase 2b e 2c do plano):
  dados/verificacoes/enderecos-cras.csv            7 CRAS (PMAS 2026–2029 + página da Secretaria, jul/2026)
  dados/verificacoes/enderecos-protecao-creas.csv  2 CREAS e 2 Conselhos Tutelares (ver conselhos-tutelares.md)
O ponto no mapa sai, nesta ordem:
  1. de um equipamento já mapeado no mesmo prédio (ex.: CRAS KM 21 dentro da UBS Jardim Santa Ângela);
  2. de outro equipamento desta lista no mesmo endereço;
  3. do Nominatim, aceitando só resultado preciso (prédio, lugar ou número);
  4. senão fica coord_origem = pendente; listar_pendentes.py gera a sugestão para a revisão do João.
Coordenadas conferidas à mão (dados/verificacoes/coordenadas-manuais.csv) são aplicadas em montar_equipamentos.py.
Saídas: dados/assistencia-social.csv, dados/protecao.csv
"""
import pandas as pd

from comum import CAMPOS_EQUIPAMENTO, DADOS, VERIFICACOES
from geocodificar import geocodificar, preciso

ENTRADAS = ["enderecos-cras.csv", "enderecos-protecao-creas.csv"]
DATA_COLETA = "2026-10-19"

# Equipamentos que funcionam dentro de outro já mapeado
MESMO_PREDIO = {"cras-05": "cnes-2746824"}


def coordenadas_conhecidas():
    saude = pd.read_csv(DADOS / "saude-cnes.csv", dtype=str).fillna("")
    return {r.id: (float(r.lat), float(r.lon)) for r in saude.itertuples()}


def main():
    df = pd.concat([pd.read_csv(VERIFICACOES / n, dtype=str).fillna("") for n in ENTRADAS], ignore_index=True)
    conhecidas = coordenadas_conhecidas()
    por_endereco = {}
    linhas = []
    for r in df.itertuples():
        lat = lon = ""
        origem = "pendente"
        if r.id in MESMO_PREDIO:
            lat, lon = conhecidas[MESMO_PREDIO[r.id]]
            origem = "cnes"
        elif r.endereco in por_endereco:
            lat, lon, origem = por_endereco[r.endereco]
        else:
            for c in (f"{r.nome}, Cotia, SP", f"{r.endereco}, {r.bairro}, Cotia, SP", f"{r.endereco}, Cotia, SP"):
                g = geocodificar(c)
                if preciso(g):
                    lat, lon, origem = float(g["lat"]), float(g["lon"]), "nominatim"
                    break
        if origem != "pendente":
            por_endereco.setdefault(r.endereco, (lat, lon, origem))
        linhas.append({
            "id": r.id, "nome": r.nome, "camada": r.camada, "subtipo": r.subtipo, "gestao": r.gestao,
            "endereco": r.endereco, "bairro": r.bairro, "telefone": r.telefone, "territorio": "",
            "lat": round(lat, 6) if lat != "" else "", "lon": round(lon, 6) if lon != "" else "",
            "coord_origem": origem, "fonte": r.fonte, "fonte_url": r.fonte_url, "data_coleta": DATA_COLETA,
            "verificacao": r.verificacao, "observacao": r.observacao,
        })

    out = pd.DataFrame(linhas)[CAMPOS_EQUIPAMENTO]
    out[out.camada == "assistencia_social"].to_csv(DADOS / "assistencia-social.csv", index=False, encoding="utf-8")
    out[out.camada == "protecao"].to_csv(DADOS / "protecao.csv", index=False, encoding="utf-8")
    print(out[["id", "coord_origem", "lat", "lon"]].to_string(index=False))


if __name__ == "__main__":
    main()
