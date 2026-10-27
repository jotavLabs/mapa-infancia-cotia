"""Lista os pontos sem coordenada confiável e gera a página de conferência para o João.

Roda antes de montar_equipamentos.py (lê as camadas em dados/ e as coordenadas manuais já aprovadas).
Sai:
  dados/verificacoes/pendentes.md                  tabela para a revisão
  dados/verificacoes/coordenadas-provisorias.csv   sugestão de ponto para cada pendente (vai ao mapa como aproximado)
  dados/verificacoes/conferir-coordenadas.html     mapa com marcadores arrastáveis (servir por http://localhost)
Dois grupos:
  - pendente: sem coordenada precisa. A sugestão é um vizinho oficial, o ponto da rua (Nominatim) ou o do bairro.
  - a conferir: tem coordenada da fonte, mas há indício de erro (fora do limite municipal, longe do endereço).
O que o João aprovar ou corrigir vai para dados/verificacoes/coordenadas-manuais.csv.
"""
import json
import re

import pandas as pd

from comum import HOJE, SITE_DATA, VERIFICACOES
from geocodificar import geocodificar
from montar_equipamentos import aplicar_coordenadas_manuais, carregar_componentes

# Indícios levantados nas verificações (saude-cnes.md e cruzamento com o INEP)
A_CONFERIR = {
    "cnes-2746468": "O OpenStreetMap põe a Estrada da Água Espraiada a 3,2 km deste ponto (ver saude-cnes.md).",
    "cnes-2746514": "Fica 124 m fora do limite de Cotia. A EM do Bairro da Caputera, na mesma estrada (nº 4518, vizinho ao 4520 da UBS), está 2,6 km a sudoeste, em −23,688334, −46,916205, segundo o INEP.",
    "cnes-2746506": "Fica 619 m fora do limite de Cotia (divisa com São Lourenço da Serra).",
}
REFERENCIAS = {
    "cras-07": "Estrada do Caputera, 4.500. Na mesma região, a EM do Bairro da Caputera (Estrada da Ressaca, 4518) está em −23,688334, −46,916205 segundo o INEP, e a UBS Caputera (nº 4520) tem coordenada duvidosa no CNES.",
    "cras-04": "Mesmo endereço do CREAS Cotia (2º andar). A Clínica da Mulher fica no nº 843 da mesma avenida.",
    "creas-cotia": "Mesmo endereço do CRAS Central.",
    "cras-02": "Centro Humanizado de Proteção Social; mesmo endereço da unidade avançada do CREAS.",
    "creas-caucaia": "Centro Humanizado de Proteção Social; mesmo endereço do CRAS Caucaia do Alto.",
    "ct-caucaia": "Prédio da Rua Benedito Pires da Silva Sobrinho, 157, onde também está o Procon Caucaia desde set/2026.",
}


# Quando há um vizinho já localizado por fonte oficial, ele é uma sugestão melhor que o centro do bairro
SUGESTAO_POR_VIZINHO = {
    "cras-07": ("inep-35219836", "ponto da EM do Bairro da Caputera (INEP), no nº 4518 da mesma estrada (a Estrada da Ressaca é a Estrada Municipal do Caputera, segundo o próprio INEP)"),
    "ct-caucaia": ("cnes-2746522", "ponto da UBS Caucaia do Alto, no centro do distrito (a rua não está no OpenStreetMap)"),
}


def sugerir(r, eq):
    """Vizinho oficial; ponto da rua certa (o nome da rua tem de aparecer no resultado); centro do bairro."""
    if r.id in SUGESTAO_POR_VIZINHO:
        viz, texto = SUGESTAO_POR_VIZINHO[r.id]
        v = eq[eq.id == viz].iloc[0]
        return float(v.lat), float(v.lon), texto, ""
    sem_numero = re.sub(r",\s*[\w/.-]+$", "", r.endereco)
    nome_rua = re.sub(r"^(Rua|Avenida|Estrada( Municipal)?|Alameda|Travessa)\s+", "", sem_numero).split()[-1].lower()
    for consulta in (f"{r.endereco}, {r.bairro}, Cotia, SP", f"{sem_numero}, {r.bairro}, Cotia, SP", f"{sem_numero}, Cotia, SP"):
        g = geocodificar(consulta)
        if g.get("lat") and nome_rua in g["nome_encontrado"].lower():
            return float(g["lat"]), float(g["lon"]), "ponto da rua no OpenStreetMap", g["nome_encontrado"]
    for parte in [p.strip() for p in r.bairro.split(",")][::-1]:
        g = geocodificar(f"{parte}, Cotia, SP")
        if g.get("lat"):
            return float(g["lat"]), float(g["lon"]), f"centro do bairro {parte} no OpenStreetMap (a rua não está mapeada)", g["nome_encontrado"]
    return -23.6040, -46.9190, "centro de Cotia (nem a rua nem o bairro foram achados)", ""


def main():
    eq = aplicar_coordenadas_manuais(carregar_componentes())
    itens, provisorias = [], []
    for r in eq[eq.coord_origem == "pendente"].itertuples():
        lat, lon, base, achado = sugerir(r, eq)
        itens.append({"id": r.id, "nome": r.nome, "camada": r.camada, "endereco": f"{r.endereco} — {r.bairro}",
                      "grupo": "pendente", "lat": round(lat, 6), "lon": round(lon, 6),
                      "motivo": f"Sem coordenada precisa. Sugestão = {base}; o número exato não está mapeado.",
                      "referencia": REFERENCIAS.get(r.id, ""), "osm": achado})
        provisorias.append({"id": r.id, "lat": round(lat, 6), "lon": round(lon, 6),
                            "base": re.sub(r"\s*\(.*\)$", "", base)})
    pd.DataFrame(provisorias, columns=["id", "lat", "lon", "base"]).to_csv(
        VERIFICACOES / "coordenadas-provisorias.csv", index=False, encoding="utf-8")
    for id_, motivo in A_CONFERIR.items():
        if eq.loc[eq.id == id_, "coord_origem"].iloc[0] == "manual":
            continue
        r = eq[eq.id == id_].iloc[0]
        itens.append({"id": id_, "nome": r.nome, "camada": r.camada, "endereco": f"{r.endereco} — {r.bairro}",
                      "grupo": "a conferir", "lat": float(r.lat), "lon": float(r.lon), "motivo": motivo,
                      "referencia": "", "osm": ""})

    linhas = [f"# Pontos para conferir — {HOJE}", "",
              "Abra `conferir-coordenadas.html` por um servidor local (`.venv/Scripts/python -m http.server 8766 --directory dados/verificacoes` e depois http://localhost:8766/conferir-coordenadas.html), arraste cada marcador para o lugar certo (ou aceite a sugestão) "
              "e copie o resultado para `coordenadas-manuais.csv`.", "",
              "| Grupo | id | Equipamento | Endereço | Sugestão (lat, lon) | Por quê |", "|---|---|---|---|---|---|"]
    for i in itens:
        ref = f" {i['referencia']}" if i["referencia"] else ""
        linhas.append(f"| {i['grupo']} | `{i['id']}` | {i['nome']} | {i['endereco']} | {i['lat']:.6f}, {i['lon']:.6f} | {i['motivo']}{ref} |")
    (VERIFICACOES / "pendentes.md").write_text("\n".join(linhas) + "\n", encoding="utf-8")

    modelo = (VERIFICACOES.parent.parent / "scripts" / "modelo-conferencia.html").read_text(encoding="utf-8")
    contorno = (SITE_DATA / "cotia.geojson").read_text(encoding="utf-8")
    html = (modelo.replace("/*DADOS*/[]", json.dumps(itens, ensure_ascii=False))
            .replace("/*CONTORNO*/null", contorno).replace("{{HOJE}}", HOJE))
    (VERIFICACOES / "conferir-coordenadas.html").write_text(html, encoding="utf-8")
    n_p = sum(i["grupo"] == "pendente" for i in itens)
    print(f"{n_p} pendente(s) e {len(itens) - n_p} a conferir -> dados/verificacoes/pendentes.md e conferir-coordenadas.html")


if __name__ == "__main__":
    main()
