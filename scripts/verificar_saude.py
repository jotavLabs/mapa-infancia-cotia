"""Confere a extração do CNES (Fase 1) e gera dados/verificacoes/saude-cnes.md.

Checagens:
  1. Lista nominal esperada pela seção 3 do plano.
  2. Diferenças contra o insumo do Guilherme, insumos/cnes-cotia-saude.csv
     (unidades que entraram ou saíram; coordenadas que andaram mais de 100 m).
  3. Coordenadas: dentro do contorno de Cotia; pontos colados entre unidades diferentes;
     distância até o que o OpenStreetMap (Nominatim) acha pelo nome e pelo endereço.
"""
import json
import re

import pandas as pd
from shapely.geometry import Point, shape

from comum import DADOS, HOJE, INSUMOS, SITE_DATA, VERIFICACOES, distancia_m
from geocodificar import geocodificar

ESPERADO = [
    ("saude_urgencia", r"^UPA Atalaia"),
    ("saude_urgencia", r"Pronto Atendimento Parque São George"),
    ("saude_urgencia", r"Pronto Atendimento Caucaia do Alto"),
    ("saude_urgencia", r"Pronto Socorro Infantil"),
    ("saude_hospital", r"Hospital Regional de Cotia"),
    ("saude_mental", r"CAPS Infantil"),
    ("saude_mental", r"CAPS II"),
    ("saude_mental", r"CAPS Álcool e Drogas"),
    ("saude_especializada", r"Policlínica Portão"),
    ("saude_especializada", r"Clínica da Mulher"),
    ("reabilitacao", r"^CEFOR I "),
    ("reabilitacao", r"^CEFOR V "),
    ("reabilitacao", r"^APAE"),
]
ESPERADO_UBS = 26
LIMITE_MOVIMENTO_M = 100
LIMITE_OSM_M = 1500


def main():
    df = pd.read_csv(DADOS / "saude-cnes.csv", dtype=str).fillna("")
    df["lat"] = df["lat"].astype(float)
    df["lon"] = df["lon"].astype(float)
    linhas = [f"# Verificação da saúde (CNES) — {HOJE}", ""]

    # 1. Lista nominal
    linhas += ["## 1. Lista esperada pelo plano (seção 3)", ""]
    falhas = 0
    n_ubs = (df.camada == "saude_atencao_basica").sum()
    ok = n_ubs == ESPERADO_UBS
    falhas += not ok
    linhas.append(f"- {'OK' if ok else 'DIVERGE'} — UBS: {n_ubs} (esperado {ESPERADO_UBS})")
    usados = set()
    for camada, padrao in ESPERADO:
        achados = df[(df.camada == camada) & df.nome.str.contains(padrao, regex=True)]
        if len(achados) == 1:
            usados.add(achados.id.iloc[0])
            linhas.append(f"- OK — `{camada}`: {achados.nome.iloc[0]} ({achados.id.iloc[0]})")
        else:
            falhas += 1
            linhas.append(f"- DIVERGE — `{camada}` /{padrao}/: {len(achados)} resultado(s)")
    extras = df[(df.camada != "saude_atencao_basica") & ~df.id.isin(usados)]
    for _, r in extras.iterrows():
        falhas += 1
        linhas.append(f"- EXTRA — `{r.camada}`: {r.nome} ({r.id}), não previsto no plano")
    linhas += ["", f"Total: {len(df)} equipamentos; {falhas} divergência(s) com o plano.", ""]

    # 2. Retrato de referência
    linhas += ["## 2. Comparação com o insumo do Guilherme", ""]
    ref_path = INSUMOS / "cnes-cotia-saude.csv"
    if not ref_path.exists():
        raise SystemExit("Falta insumos/cnes-cotia-saude.csv (enviado pelo Guilherme). Pare e avise o João.")
    else:
        ref = pd.read_csv(ref_path, dtype=str).fillna("")
        if "id" not in ref.columns:
            ref["id"] = "cnes-" + ref["cnes"].str.zfill(7)
        entraram = df[~df.id.isin(ref.id)]
        sairam = ref[~ref.id.isin(df.id)]
        linhas.append(f"Insumo: `{ref_path.name}` ({len(ref)} linhas).")
        linhas.append("")
        for _, r in entraram.iterrows():
            linhas.append(f"- ENTROU: {r.nome} ({r.id}, `{r.camada}`)")
        for _, r in sairam.iterrows():
            linhas.append(f"- SAIU: {r.nome} ({r.id}, `{r.camada}`)")
        juntos = df.merge(ref[["id", "lat", "lon"]], on="id", suffixes=("", "_ref"))
        movidos = 0
        for _, r in juntos.iterrows():
            if r.lat_ref and r.lon_ref:
                d = distancia_m(r.lat, r.lon, float(r.lat_ref), float(r.lon_ref))
                if d > LIMITE_MOVIMENTO_M:
                    movidos += 1
                    linhas.append(f"- MUDOU DE LUGAR ({d:.0f} m): {r.nome} ({r.id})")
        if entraram.empty and sairam.empty and not movidos:
            linhas.append("- Nenhuma diferença.")
        linhas.append("")

    # 3. Coordenadas
    linhas += ["## 3. Coordenadas", ""]
    cotia = shape(json.loads((SITE_DATA / "cotia.geojson").read_text(encoding="utf-8"))["features"][0]["geometry"])
    fora = df[[not cotia.contains(Point(lo, la)) for la, lo in zip(df.lat, df.lon)]]
    linhas.append(f"- Fora do contorno de Cotia: {len(fora)}" + "".join(f"\n  - {r.nome}" for _, r in fora.iterrows()))

    colados = []
    regs = list(df.itertuples())
    for i, a in enumerate(regs):
        for b in regs[i + 1:]:
            d = distancia_m(a.lat, a.lon, b.lat, b.lon)
            if d < 30:
                colados.append(f"  - {a.nome} × {b.nome}: {d:.0f} m ({'mesmo endereço' if a.endereco == b.endereco else 'endereços diferentes'})")
    linhas.append(f"- Pares de unidades a menos de 30 m: {len(colados)}" + ("\n" + "\n".join(colados) if colados else ""))
    linhas.append("")

    linhas += [
        f"### Distância até o OpenStreetMap (alerta acima de {LIMITE_OSM_M} m)", "",
        "O Nominatim é consultado pelo nome da unidade e pelo endereço. Para cada unidade vale a menor distância.",
        "Endereço que o OSM só acha pela rua devolve um ponto qualquer da rua, então a distância é um indício, não prova.", "",
        "| Unidade | Distância (m) | Achado por | O que o OSM achou |", "|---|---:|---|---|",
    ]
    alertas = []
    for r in df.itertuples():
        candidatos = []
        for como, consulta in (("nome", f"{r.nome}, Cotia, SP"), ("endereço", f"{r.endereco}, Cotia, SP")):
            g = geocodificar(consulta)
            if g.get("lat"):
                candidatos.append((distancia_m(r.lat, r.lon, float(g["lat"]), float(g["lon"])), como, g))
        if not candidatos:
            linhas.append(f"| {r.nome} | — | não achado | — |")
            continue
        d, como, g = min(candidatos, key=lambda c: c[0])
        resumo = re.sub(r",\s*(Região|Microrregião|Mesorregião|Região Metropolitana|Região Imediata|Região Intermediária|Brasil)[^,]*", "", g["nome_encontrado"])[:80]
        marca = " ⚠" if d > LIMITE_OSM_M else ""
        linhas.append(f"| {r.nome}{marca} | {d:.0f} | {como} ({g['tipo']}) | {resumo} |")
        if d > LIMITE_OSM_M:
            alertas.append((r, d, g))
    linhas += ["", f"Alertas: {len(alertas)}", ""]
    for r, d, g in alertas:
        linhas.append(f"- **{r.nome}** — CNES: {r.lat:.6f}, {r.lon:.6f} ({r.endereco}, {r.bairro}). "
                      f"OSM: {float(g['lat']):.6f}, {float(g['lon']):.6f} a {d:.0f} m.")

    VERIFICACOES.mkdir(parents=True, exist_ok=True)
    saida = VERIFICACOES / "saude-cnes.md"
    saida.write_text("\n".join(linhas) + "\n", encoding="utf-8")
    print(f"Relatório em {saida.relative_to(DADOS.parent)}: {falhas} divergência(s) com o plano, {len(fora)} fora de Cotia, {len(alertas)} alerta(s) de coordenada.")


if __name__ == "__main__":
    main()
