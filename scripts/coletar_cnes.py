"""Extrai da API de dados abertos do CNES os equipamentos públicos de saúde de Cotia.

Saídas:
  dados/brutos/cnes-cotia-<data>.json           resposta completa da API (fora do Git: inclui consultórios
                                                privados com e-mails e nomes de profissionais)
  dados/brutos/cnes-cotia-publicos-<data>.json  retrato versionado: só estabelecimentos públicos e a APAE
  dados/saude-cnes.csv                          equipamentos filtrados, no esquema de equipamentos
Sem --rebaixar, o script reaproveita a extração mais recente já salva, e a data de coleta é a dela.
"""
import json
import re
import sys
import time

import pandas as pd
import requests

from comum import BRUTOS, DADOS, HOJE, INSUMOS, USER_AGENT, capitalizar, formatar_telefone

API = "https://apidadosabertos.saude.gov.br/cnes/estabelecimentos"
CODIGO_MUNICIPIO = 351300
PAGINA = 20

TIPOS_UNIDADE = {2, 4, 5, 20, 73, 36, 70}


def baixar_tudo():
    sessao = requests.Session()
    sessao.headers["User-Agent"] = USER_AGENT
    todos = []
    offset = 0
    while True:
        for tentativa in range(5):
            try:
                r = sessao.get(API, params={"codigo_municipio": CODIGO_MUNICIPIO, "limit": PAGINA, "offset": offset}, timeout=60)
                r.raise_for_status()
                break
            except requests.RequestException as e:
                print(f"  offset {offset}: {e}; nova tentativa", file=sys.stderr)
                time.sleep(3 * (tentativa + 1))
        else:
            raise SystemExit(f"API do CNES não respondeu no offset {offset}")
        lote = r.json().get("estabelecimentos", [])
        if not lote:
            break
        todos.extend(lote)
        offset += PAGINA
        time.sleep(0.3)
    return todos


def classificar(e):
    """Devolve (camada, subtipo) ou None se o estabelecimento fica fora do mapa."""
    tipo = e["codigo_tipo_unidade"]
    nome = (e.get("nome_fantasia") or "").upper()
    if tipo == 2:
        return "saude_atencao_basica", "UBS"
    if tipo in (20, 73):
        if "INFANTIL" in nome:
            return "saude_urgencia", "Pronto-socorro infantil"
        if "UPA" in nome:
            return "saude_urgencia", "UPA"
        return "saude_urgencia", "Pronto atendimento"
    if tipo == 5:
        return "saude_hospital", "Hospital geral"
    if tipo == 70:
        if "INFANT" in nome or re.match(r"CAPS\s*IJ?\b", nome) and not re.match(r"CAPS\s*II", nome):
            return "saude_mental", "CAPSi"
        if " AD" in nome or "ALCOOL" in nome or "ÁLCOOL" in nome:
            return "saude_mental", "CAPS AD"
        return "saude_mental", "CAPS adulto"
    if tipo == 4 and "POLICLINICA" in nome.replace("Í", "I"):
        return "saude_especializada", "Policlínica"
    if tipo == 36:
        if "CEFOR" in nome:
            return "reabilitacao", "Centro de reabilitação"
        if "MULHER" in nome:
            return "saude_especializada", "Clínica da Mulher"
    return None


def e_apae(e):
    nomes = f"{e.get('nome_fantasia') or ''} {e.get('nome_razao_social') or ''}".upper()
    return "APAE" in nomes or "PAIS E AMIGOS DOS EXCEPCIONAIS" in nomes


def gestao(e, apae):
    if apae:
        return "conveniada"
    esfera = (e.get("descricao_esfera_administrativa") or "").upper()
    if esfera.startswith("ESTADUAL") or e.get("tipo_gestao") == "E":
        return "estadual"
    return "municipal"


def endereco(e):
    partes = [capitalizar(e.get("endereco_estabelecimento") or "")]
    numero = (e.get("numero_estabelecimento") or "").strip()
    if numero and numero.upper() not in {"S/N", "SN", "0"}:
        partes.append(numero)
    elif numero:
        partes.append("s/n")
    return ", ".join(p for p in partes if p)


def filtrar(todos, data_coleta):
    linhas = []
    for e in todos:
        if e.get("codigo_motivo_desabilitacao_estabelecimento"):
            continue
        natureza = str(e.get("descricao_natureza_juridica_estabelecimento") or "")
        apae = e_apae(e)
        if not (natureza.startswith("1") or apae):
            continue
        if apae:
            camada, subtipo = "reabilitacao", "APAE"
        else:
            if e["codigo_tipo_unidade"] not in TIPOS_UNIDADE:
                continue
            c = classificar(e)
            if c is None:
                continue
            camada, subtipo = c
        lat, lon = e.get("latitude_estabelecimento_decimo_grau"), e.get("longitude_estabelecimento_decimo_grau")
        cnes = e["codigo_cnes"]
        linhas.append({
            "id": f"cnes-{cnes:07d}",
            "nome": capitalizar(e.get("nome_fantasia") or e.get("nome_razao_social")),
            "camada": camada,
            "subtipo": subtipo,
            "gestao": gestao(e, apae),
            "endereco": endereco(e),
            "bairro": capitalizar(e.get("bairro_estabelecimento") or ""),
            "telefone": formatar_telefone(e.get("numero_telefone_estabelecimento")),
            "territorio": "",
            "lat": round(lat, 6) if lat is not None else "",
            "lon": round(lon, 6) if lon is not None else "",
            "coord_origem": "cnes" if lat is not None else "pendente",
            "fonte": "CNES — API de dados abertos do Ministério da Saúde",
            "fonte_url": f"https://cnes.datasus.gov.br/pages/estabelecimentos/ficha/index.jsp?coUnidade={CODIGO_MUNICIPIO}{cnes:07d}",
            "data_coleta": data_coleta,
            "verificacao": "confirmado" if str(e.get("data_atualizacao") or "") >= "2025" else "nao_confirmado",
            "observacao": "",
            "_tipo_unidade": e["codigo_tipo_unidade"],
            "_natureza": natureza,
            "_cep": e.get("codigo_cep_estabelecimento") or "",
            "_data_atualizacao": e.get("data_atualizacao") or "",
        })
    df = pd.DataFrame(linhas).sort_values(["camada", "nome"]).reset_index(drop=True)
    notas = notas_do_insumo()
    df["observacao"] = df["id"].map(notas).fillna("")
    return df


def notas_do_insumo():
    """Observações factuais do insumo do Guilherme; frases que são instrução de exibição ("Mostrar…") ficam fora."""
    caminho = INSUMOS / "cnes-cotia-saude.csv"
    if not caminho.exists():
        return {}
    notas = {}
    for r in pd.read_csv(caminho, dtype=str).fillna("").itertuples():
        frases = [f for f in re.split(r"(?<=\.)\s+", r.observacao.strip()) if f and not f.startswith("Mostrar")]
        if frases:
            notas[f"cnes-{r.cnes.zfill(7)}"] = " ".join(frases)
    return notas


def e_publico_ou_apae(e):
    return str(e.get("descricao_natureza_juridica_estabelecimento") or "").startswith("1") or e_apae(e)


def ultima_extracao():
    """Extração mais recente salva: a completa (local) ou o retrato público (versionado). Devolve (registros, data)."""
    candidatos = sorted(BRUTOS.glob("cnes-cotia-*.json"), key=lambda p: re.search(r"(\d{4}-\d{2}-\d{2})", p.name).group(1))
    if not candidatos:
        return None, None
    data = re.search(r"(\d{4}-\d{2}-\d{2})", candidatos[-1].name).group(1)
    completa = BRUTOS / f"cnes-cotia-{data}.json"
    arquivo = completa if completa.exists() else BRUTOS / f"cnes-cotia-publicos-{data}.json"
    return json.loads(arquivo.read_text(encoding="utf-8")), data


def main():
    BRUTOS.mkdir(parents=True, exist_ok=True)
    todos, data = (None, None) if "--rebaixar" in sys.argv else ultima_extracao()
    if todos is None:
        print("Baixando estabelecimentos de Cotia do CNES...")
        todos, data = baixar_tudo(), HOJE
        (BRUTOS / f"cnes-cotia-{data}.json").write_text(json.dumps(todos, ensure_ascii=False, indent=1), encoding="utf-8")
    else:
        print(f"Usando a extração de {data} já salva; passe --rebaixar para baixar de novo.")
    publicos = [e for e in todos if e_publico_ou_apae(e)]
    (BRUTOS / f"cnes-cotia-publicos-{data}.json").write_text(json.dumps(publicos, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"  {len(todos)} estabelecimentos lidos; {len(publicos)} públicos ou APAE no retrato versionado")

    df = filtrar(todos, data)
    saida = DADOS / "saude-cnes.csv"
    df.to_csv(saida, index=False, encoding="utf-8")
    print(f"  {len(df)} equipamentos públicos de saúde -> {saida.relative_to(DADOS.parent)}")
    print(df.groupby("camada").size().to_string())


if __name__ == "__main__":
    main()
