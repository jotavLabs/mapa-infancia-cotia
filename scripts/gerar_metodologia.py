"""Gera site/metodologia.html a partir de scripts/modelo-metodologia.html, com os números dos relatórios.

Entradas: dados/verificacoes/territorios-resumo.json, dados/verificacoes/equipamentos-resumo.json,
          dados/educacao-inep.csv, dados/brutos/populacao-oficial-cotia-2022.json
"""
import json
import re
from datetime import date

import pandas as pd

from comum import BRUTOS, DADOS, RAIZ, VERIFICACOES

VERSAO_CSS = "7"


def br(n):
    return f"{int(round(n)):,}".replace(",", ".")


def pct(x):
    return f"{x:.2%}".replace(".", ",")


def main():
    terr = json.loads((VERIFICACOES / "territorios-resumo.json").read_text(encoding="utf-8"))
    eq = json.loads((VERIFICACOES / "equipamentos-resumo.json").read_text(encoding="utf-8"))
    oficial = json.loads((BRUTOS / "populacao-oficial-cotia-2022.json").read_text(encoding="utf-8"))
    educ = pd.read_csv(DADOS / "educacao-inep.csv", dtype=str).fillna("")
    m_px = terr["m_por_px"]
    res = terr["residuos_px"]
    valores = {
        "VERSAO": VERSAO_CSS,
        "DATA_ATUALIZACAO": date.fromisoformat(max(terr["data"], eq["data"])).strftime("%d/%m/%Y"),
        "DATA_CENSO": date.fromisoformat(oficial["data_coleta"]).strftime("%d/%m/%Y"),
        "N_TOTAL": br(eq["total"]),
        "N_CONVENIADAS_EDUC": str(int((educ.gestao == "conveniada").sum())),
        "N_INEP_COORD": str(int((educ.coord_origem == "inep").sum())),
        "POP_OFICIAL": br(oficial["populacao_2022"]),
        "SETORES": br(terr["setores"]),
        "IOU": f"{terr['iou'] * 100:.1f}%".replace(".", ","),
        "RES_OUTROS_M": br(round(max(res["norte"], res["oeste"], res["leste"]) * m_px, -1)),
        "RES_SUL_KM": f"{res['sul'] * m_px / 1000:.1f}".replace(".", ","),
        "SETORES_COR_SETOR": str(terr["setores_cor_do_setor"]),
        "SETORES_MIOLO": str(terr["setores_miolo"]),
        "POP_MIOLO": br(terr["pop_miolo"]),
        "PCT_MIOLO": pct(terr["pop_miolo"] / terr["populacao_oficial"]),
        "SETORES_DUVIDOSOS": str(terr["setores_duvidosos"]),
        "DIVERGENCIAS": str(eq["divergencias_bairro"]),
        "SOMA_SETORES": br(terr["soma_setores"]),
        "SIGILO_MORADORES": br(terr["moradores_em_sigilo"]),
        "PCT_SIGILO": pct(terr["moradores_em_sigilo"] / terr["populacao_oficial"]),
        "SETORES_SIGILO": str(terr["setores_sigilo"]),
    }
    for camada, n in eq["por_camada"].items():
        valores[f"N_{camada}"] = str(n)
    for origem in ("cnes", "inep", "nominatim", "pendente", "manual"):
        valores[f"ORIGEM_{origem}"] = str(eq["por_origem"].get(origem, 0))

    html = (RAIZ / "scripts" / "modelo-metodologia.html").read_text(encoding="utf-8")
    for chave, valor in valores.items():
        html = html.replace("{{" + chave + "}}", valor)
    faltando = sorted(set(re.findall(r"\{\{(\w+)\}\}", html)))
    if faltando:
        raise SystemExit(f"Marcadores sem valor: {faltando}")
    (RAIZ / "site" / "metodologia.html").write_text(html, encoding="utf-8")
    print("site/metodologia.html gerado:", {k: valores[k] for k in ("IOU", "RES_OUTROS_M", "RES_SUL_KM", "PCT_MIOLO", "PCT_SIGILO")})


if __name__ == "__main__":
    main()
