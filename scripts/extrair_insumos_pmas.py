"""Extrai do PMAS de Cotia 2026–2029 os territórios de CRAS e o mapa, para conferir os insumos do Guilherme.

O que faz:
  1. Baixa o PDF do Plano Municipal de Assistência Social 2026–2029 (Resolução CMAS 298)
     para dados/brutos/pmas-2026-2029_<AAAA-MM-DD>.pdf (pula o download se o arquivo já existe).
  2. Extrai o texto da seção 3.6 TERRITORIALIZAÇÃO e imprime, em Markdown, os 7 territórios
     (nome, cor, endereço, telefone, bairros e página do PDF de cada dado).
  3. Extrai a imagem original do mapa dos territórios (embutida na página da seção 3.6) e grava
     dados/verificacoes/reconstrucao-pmas/mapa-territorios-cras-extraido.png. Se não houver imagem embutida, renderiza a área
     do mapa a 250 dpi.
  4. Com --carta, baixa a Carta de Serviços ao Usuário e compara os endereços dos CRAS (só imprime).

Uso (na raiz do projeto):
  .venv/Scripts/python.exe scripts/extrair_insumos_pmas.py [--data AAAA-MM-DD] [--forcar-download]
                                                           [--texto] [--carta]

Páginas são citadas como "p. N do PDF" (índice do arquivo, começando em 1). A numeração impressa
no rodapé do plano é N-1, porque a resolução do CMAS ocupa a primeira página.
"""

import argparse
import datetime
import hashlib
import html
import re
import sys
import unicodedata
from collections import Counter, defaultdict
from pathlib import Path

import pymupdf
import requests

RAIZ = Path(__file__).resolve().parent.parent
URL_PMAS = (
    "https://cotia.sp.gov.br/wp-content/uploads/2026/06/"
    "298-resolucao-cmas-aprova-o-plano-municipal-de-assistencia-social-2026-a-2029-.pdf"
)
URL_CARTA = "https://cotia.sp.gov.br/carta-de-servico-ao-usuario/"
SHA256_REFERENCIA = "f5f5f95b5d4470dad2c692982c7bf0f8c3636003ba8402a8c14adb708e982735"  # coleta de 2026-10-19
USER_AGENT = "MapaInfanciaCotia/0.1 (coleta de dados publicos para mapa de equipamentos)"
SAIDA_MAPA = RAIZ / "dados" / "verificacoes" / "reconstrucao-pmas" / "mapa-territorios-cras-extraido.png"
DPI_RENDER = 250

RE_CABECALHO = re.compile(r"^(\d)\.\s*CRAS\s+(.+?)\s*\((.+)\)\s*$")
RE_NUM_PAGINA = re.compile(r"^\s*\d{1,3}\s*$")
RE_RUA_NUMERO = re.compile(r"\b((?:Rua|Avenida|Av\.|Estrada)\b.+?),?\s+(\d[\d.]*)")

CHAVES_CARTA = {
    1: "JAPAO",
    2: "CAUCAIA",
    3: "MIRIZOLA",
    4: "MONTE SERRAT",
    5: "RECANTO SUAVE",
    6: "ARCO",
    7: "CAPUTERA",
}


def sem_acento(s):
    return "".join(c for c in unicodedata.normalize("NFD", s) if unicodedata.category(c) != "Mn")


def normalizar(s):
    s = sem_acento(s).lower()
    s = re.sub(r"[^a-z0-9 ]+", " ", s)
    return re.sub(r"\s+", " ", s).strip()


def baixar_pmas(destino, forcar):
    if destino.exists() and not forcar:
        print(f"PDF já existe, download pulado: {destino.relative_to(RAIZ)}")
    else:
        destino.parent.mkdir(parents=True, exist_ok=True)
        print(f"Baixando {URL_PMAS}")
        r = requests.get(URL_PMAS, headers={"User-Agent": USER_AGENT}, timeout=120)
        r.raise_for_status()
        if not r.content.startswith(b"%PDF"):
            sys.exit("A resposta não é um PDF; a URL pode ter mudado. Nada foi gravado.")
        tmp = destino.with_suffix(".part")
        tmp.write_bytes(r.content)
        tmp.replace(destino)
    dados = destino.read_bytes()
    sha = hashlib.sha256(dados).hexdigest()
    print(f"Tamanho: {len(dados):,} bytes | SHA-256: {sha}")
    if sha != SHA256_REFERENCIA:
        print("AVISO: o PDF difere da versão coletada em 2026-10-19. Confira se o plano foi republicado.")


def linhas_da_secao(doc):
    """Linhas (pagina_1based, texto) de '3.6 TERRITORIALIZAÇÃO' até o título da seção 4."""
    inicio = None
    for i, pagina in enumerate(doc):
        t = pagina.get_text()
        if "TERRITORIALIZA" in t and re.search(r"^1\.\s*CRAS", t, re.M):
            inicio = i
            break
    if inicio is None:
        sys.exit("Seção 3.6 TERRITORIALIZAÇÃO não encontrada no PDF.")
    linhas = []
    for i in range(inicio, min(inicio + 5, doc.page_count)):
        for bruta in doc[i].get_text().splitlines():
            texto = bruta.strip()
            if re.match(r"^4\s+PROTE", texto):
                return inicio, linhas
            if not texto or RE_NUM_PAGINA.match(texto):
                continue
            linhas.append((i + 1, texto))
    return inicio, linhas


def parsear_territorios(linhas):
    territorios = []
    atual = None
    campo = None
    for pagina, texto in linhas:
        m = RE_CABECALHO.match(texto)
        if m:
            atual = {
                "numero": int(m.group(1)),
                "nome_pmas": "CRAS " + m.group(2).strip(),
                "parenteses": m.group(3).strip(),
                "pag_cabecalho": pagina,
                "endereco": [],
                "pag_endereco": set(),
                "telefone": None,
                "pag_telefone": None,
                "bairros_txt": [],
                "pag_bairros": set(),
            }
            territorios.append(atual)
            campo = None
            continue
        if atual is None:
            continue
        if texto.startswith("Endereço:"):
            campo = "endereco"
            texto = texto[len("Endereço:"):].strip()
        elif texto.startswith("Telefone:"):
            atual["telefone"] = texto[len("Telefone:"):].strip()
            atual["pag_telefone"] = pagina
            campo = None
            continue
        elif "Bairros:" in texto:
            campo = "bairros"
            texto = texto.split("Bairros:", 1)[1].strip()
        if campo == "endereco":
            atual["endereco"].append(texto)
            atual["pag_endereco"].add(pagina)
        elif campo == "bairros":
            atual["bairros_txt"].append(texto)
            atual["pag_bairros"].add(pagina)
    for t in territorios:
        t["endereco"] = " ".join(t["endereco"])
        corrido = re.sub(r"\s+", " ", " ".join(t["bairros_txt"])).strip().rstrip(".")
        t["bairros"] = [b.strip() for b in corrido.split(",") if b.strip()]
        cor = re.search(r"Cor\s+(.+)$", t["parenteses"])
        t["cor"] = cor.group(1).strip() if cor else ""
    return territorios


def paginas(conj):
    conj = sorted(conj) if not isinstance(conj, int) else [conj]
    return ", ".join(str(p) for p in conj)


def imprimir_territorios(territorios):
    print("\n## Territórios extraídos da seção 3.6\n")
    for t in territorios:
        tel = t["telefone"] or "não consta no PMAS"
        pag_tel = f" (p. {t['pag_telefone']})" if t["pag_telefone"] else ""
        print(f"### {t['numero']}. {t['nome_pmas']} ({t['parenteses']}) — p. {t['pag_cabecalho']}")
        print(f"- Cor: {t['cor']}")
        print(f"- Endereço: {t['endereco']} (p. {paginas(t['pag_endereco'])})")
        print(f"- Telefone: {tel}{pag_tel}")
        print(f"- Bairros ({len(t['bairros'])}; p. {paginas(t['pag_bairros'])}):")
        for b in t["bairros"]:
            print(f"  - {b}")
        print()
    if len(territorios) != 7:
        print(f"AVISO: esperados 7 territórios, encontrados {len(territorios)}.")

    onde = defaultdict(list)
    for t in territorios:
        for b in t["bairros"]:
            onde[normalizar(b)].append((t["numero"], b))
    print("## Bairros com o mesmo nome (normalizado) em mais de um lugar\n")
    achou = False
    for chave, ocorr in sorted(onde.items()):
        if len(ocorr) > 1:
            achou = True
            print("- " + " | ".join(f"T{n}: {b}" for n, b in ocorr))
    if not achou:
        print("- nenhum")


def extrair_mapa(doc, indice_pagina):
    contagem = Counter()
    for pagina in doc:
        for img in pagina.get_images(full=True):
            contagem[img[0]] += 1
    pagina = doc[indice_pagina]
    candidatas = []
    for info in pagina.get_image_info(xrefs=True):
        xref = info["xref"]
        if xref and contagem[xref] == 1:
            candidatas.append((info["width"] * info["height"], xref, pymupdf.Rect(info["bbox"])))
    SAIDA_MAPA.parent.mkdir(parents=True, exist_ok=True)
    if candidatas:
        _, xref, bbox = max(candidatas)
        pix = pymupdf.Pixmap(doc, xref)
        if pix.alpha:
            pix = pymupdf.Pixmap(pix, 0)
        if pix.colorspace and pix.colorspace.n != 3:
            pix = pymupdf.Pixmap(pymupdf.csRGB, pix)
        pix.save(SAIDA_MAPA)
        dpi_efetivo = pix.width / (bbox.width / 72)
        print(
            f"\nMapa: imagem embutida xref {xref}, {pix.width}x{pix.height} px, "
            f"ocupa {bbox.width:.1f}x{bbox.height:.1f} pt na p. {indice_pagina + 1} "
            f"(~{dpi_efetivo:.0f} dpi efetivos na página). Original extraído, sem reamostragem."
        )
        proporcao_img = pix.width / pix.height
        proporcao_pag = bbox.width / bbox.height
        if abs(proporcao_img / proporcao_pag - 1) > 0.02:
            print(
                f"  Obs.: no PDF a imagem aparece com proporção {proporcao_pag:.3f}; a original é "
                f"{proporcao_img:.3f} (o PDF a exibe esticada). Vale a proporção original."
            )
    else:
        print(f"\nMapa: sem imagem embutida exclusiva na p. {indice_pagina + 1}; renderizando a {DPI_RENDER} dpi.")
        pagina.get_pixmap(dpi=DPI_RENDER).save(SAIDA_MAPA)
    print(f"Gravado: {SAIDA_MAPA.relative_to(RAIZ)}")


def html_para_linhas(s):
    s = re.sub(r"(?is)<(script|style|noscript)[^>]*>.*?</\1>", " ", s)
    s = re.sub(r"(?i)<br\s*/?>|</p>|</li>|</h\d>|</div>|</tr>|</td>", "\n", s)
    s = html.unescape(re.sub(r"<[^>]+>", " ", s))
    return [re.sub(r"[ \t ]+", " ", l).strip() for l in s.splitlines() if l.strip()]


def chave_endereco(endereco):
    m = RE_RUA_NUMERO.search(endereco or "")
    if not m:
        return None
    rua = normalizar(m.group(1))
    rua = re.sub(r"^(rua|avenida|av|estrada) ", "", rua)
    return rua, m.group(2).replace(".", "")


def comparar_carta(territorios):
    print(f"\n## Comparação com a Carta de Serviços ({URL_CARTA})\n")
    r = requests.get(URL_CARTA, headers={"User-Agent": USER_AGENT}, timeout=60)
    r.raise_for_status()
    modificada = re.search(r'"dateModified":"([^"]+)"', r.text)
    print(f"Página modificada em: {modificada.group(1) if modificada else 'data não encontrada no HTML'}")
    linhas = html_para_linhas(r.text)
    blocos = {}
    for i, l in enumerate(linhas):
        if re.match(r"^•?\s*(CRAS|UNIDADE AVAN[ÇC]ADA)\s+(?!E\b)[A-ZÁÂÃÉÊÍÓÔÕÚÇ ]+$", l):
            nome = l.lstrip("• ").strip()
            if nome in blocos:
                continue
            end = tel = None
            for seg in linhas[i + 1:i + 4]:
                if seg.startswith("Telefone"):
                    tel = seg.split(":", 1)[1].strip()
                    break
                if end is None:
                    end = seg.replace("Endereço:", "").strip()
            blocos[nome] = (end, tel)
    for t in territorios:
        chave = CHAVES_CARTA[t["numero"]]
        achados = [(n, v) for n, v in blocos.items() if chave in sem_acento(n).upper()]
        print(f"- T{t['numero']} {t['nome_pmas']}")
        print(f"  PMAS : {t['endereco']} | tel. {t['telefone'] or 'não consta'}")
        if not achados:
            print("  Carta: não consta")
            continue
        for nome, (end, tel) in achados:
            igual_end = chave_endereco(end) == chave_endereco(t["endereco"])
            dig = lambda s: re.sub(r"\D", "", s or "")
            igual_tel = dig(tel) == dig(t["telefone"])
            print(f"  Carta: {nome}: {end} | tel. {tel or 'não consta'}")
            print(f"  -> endereço {'igual' if igual_end else 'DIFERENTE'}; telefone {'igual' if igual_tel else 'DIFERENTE'}")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--data", default=datetime.date.today().isoformat(), help="data da coleta no nome do PDF")
    ap.add_argument("--forcar-download", action="store_true", help="baixa de novo mesmo se o PDF já existe")
    ap.add_argument("--texto", action="store_true", help="imprime o texto integral do PDF, página a página")
    ap.add_argument("--carta", action="store_true", help="compara endereços com a Carta de Serviços (só imprime)")
    args = ap.parse_args()
    sys.stdout.reconfigure(encoding="utf-8")

    pdf =RAIZ / "dados" / "brutos" / f"pmas-2026-2029_{args.data}.pdf"
    baixar_pmas(pdf, args.forcar_download)

    doc = pymupdf.open(pdf)
    print(f"Páginas: {doc.page_count}")
    if args.texto:
        for i, pagina in enumerate(doc):
            print(f"\n===== p. {i + 1} do PDF =====\n{pagina.get_text()}")

    indice, linhas = linhas_da_secao(doc)
    territorios = parsear_territorios(linhas)
    imprimir_territorios(territorios)
    extrair_mapa(doc, indice)
    if args.carta:
        comparar_carta(territorios)


if __name__ == "__main__":
    main()
