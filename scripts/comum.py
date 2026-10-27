import re
from datetime import date
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
INSUMOS = RAIZ / "insumos"
DADOS = RAIZ / "dados"
BRUTOS = DADOS / "brutos"
VERIFICACOES = DADOS / "verificacoes"
SITE_DATA = RAIZ / "site" / "data"

USER_AGENT = "MapaInfanciaCotia/0.1 (projeto sem fins lucrativos; github.com/jotavLabs)"
HOJE = date.today().isoformat()

CAMPOS_EQUIPAMENTO = [
    "id", "nome", "camada", "subtipo", "gestao", "endereco", "bairro", "telefone",
    "territorio", "lat", "lon", "coord_origem", "fonte", "fonte_url", "data_coleta",
    "verificacao", "observacao",
]

_MINUSCULAS = {"de", "da", "do", "das", "dos", "e", "em", "na", "no", "nas", "nos", "a", "o"}
_SIGLAS = {
    "UBS", "UPA", "PA", "PSI", "CAPS", "CAPSI", "AD", "II", "III", "IV", "APAE", "CEFOR",
    "SUS", "CRAS", "CREAS", "USF", "ESF", "SP", "KM", "CEI", "EMEI", "EMEF", "CEU", "AMA",
    "I", "V", "VI", "VII", "VIII", "IX", "X", "OS", "AHBB", "ABPA", "CESEP", "CAC",
}
_ABREVIACOES = {"JD": "Jd.", "PQ": "Pq.", "PRQ": "Pq.", "VL": "Vl.", "AV": "Av.", "ESTR": "Estr.", "DR": "Dr.", "DRA": "Dra.",
                "STA": "Sta.", "STO": "Sto.", "PROF": "Prof.", "PROFA": "Profa.", "ENG": "Eng.", "MTE": "Monte"}

# O CNES grava nomes sem acento. Restauramos só palavras de grafia inequívoca.
_ACENTOS = {
    "SAO": "São", "JAPAO": "Japão", "AGUA": "Água", "ALCOOL": "Álcool", "CLINICA": "Clínica",
    "POLICLINICA": "Policlínica", "PORTAO": "Portão", "MARIO": "Mário", "JOAO": "João",
    "PETROPOLIS": "Petrópolis", "CLAUDIO": "Cláudio", "ANGELA": "Ângela", "CASSIA": "Cássia",
    "IRIS": "Íris", "FLORENCIO": "Florêncio", "NUCLEO": "Núcleo", "TOPAZIO": "Topázio",
    "AZULAO": "Azulão", "QUITERIA": "Quitéria", "DEMETRIO": "Demétrio", "ANTONIO": "Antônio",
    "JOSE": "José", "CRIANCA": "Criança", "INTEGRACAO": "Integração", "REABILITACAO": "Reabilitação",
    "FISICA": "Física", "ATENCAO": "Atenção", "SAUDE": "Saúde", "SERVICO": "Serviço",
    "CONCEICAO": "Conceição", "SEBASTIAO": "Sebastião", "ESTACAO": "Estação", "PAROQUIA": "Paróquia",
    "MUNICIPIO": "Município", "VITORIA": "Vitória", "GLORIA": "Glória", "CANDIDO": "Cândido",
    "PLACIDO": "Plácido", "ARAUJO": "Araújo", "LOURENCO": "Lourenço",
    "GONCALVES": "Gonçalves", "CORACAO": "Coração", "REGIA": "Régia", "MENDONCA": "Mendonça",
    "AMBROSIO": "Ambrósio", "MOISES": "Moisés", "BELIZARIO": "Belizário", "IPES": "Ipês", "GRACAS": "Graças",
    "LAVAPES": "Lavapés", "BELEM": "Belém", "VALENCA": "Valença", "ILOPOLIS": "Ilópolis", "RIBEIRAO": "Ribeirão",
    "MARANHAO": "Maranhão", "INACIO": "Inácio", "JANUARIO": "Januário", "PATROCINIO": "Patrocínio",
    "ARCOIRIS": "Arco-Íris", "CHACARA": "Chácara", "TAQUARACU": "Taquaraçu", "JUNIOR": "Júnior", "DELIO": "Délio",
    "BARAUNA": "Baraúna", "MONTALVAO": "Montalvão", "ESTACIO": "Estácio", "EDUCACAO": "Educação",
}


def capitalizar(texto):
    """Title case em português, preservando siglas, acentos inequívocos e minúsculas de ligação."""
    if not texto:
        return ""
    palavras = re.split(r"(\s+|-|/)", texto.strip())
    saida = []
    primeira = True
    for p in palavras:
        if not p or re.fullmatch(r"\s+|-|/", p):
            saida.append(p)
            continue
        limpa = p.strip(".,()").upper()
        if limpa in _SIGLAS:
            saida.append(p.upper())
        elif limpa in _ABREVIACOES:
            saida.append(_ABREVIACOES[limpa])
        elif limpa in _ACENTOS:
            saida.append(_ACENTOS[limpa])
        elif not primeira and p.lower() in _MINUSCULAS:
            saida.append(p.lower())
        elif re.fullmatch(r"[\d.,ºª]+", p):
            saida.append(p)
        else:
            saida.append(p[:1].upper() + p[1:].lower())
        primeira = False
    return "".join(saida)


def formatar_telefone(bruto):
    """(11) 4703-5544 para fixos; (11) 9xxxx-xxxx para celulares. Devolve vazio se não reconhecer."""
    digitos = re.sub(r"\D", "", str(bruto or ""))
    if digitos.startswith("0"):
        digitos = digitos[1:]
    if len(digitos) == 8:
        digitos = "11" + digitos
    if len(digitos) == 10:
        return f"({digitos[:2]}) {digitos[2:6]}-{digitos[6:]}"
    if len(digitos) == 11:
        return f"({digitos[:2]}) {digitos[2:7]}-{digitos[7:]}"
    return str(bruto or "").strip()


def distancia_m(lat1, lon1, lat2, lon2):
    from math import asin, cos, radians, sin, sqrt
    dlat, dlon = radians(lat2 - lat1), radians(lon2 - lon1)
    a = sin(dlat / 2) ** 2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon / 2) ** 2
    return 2 * 6371000 * asin(sqrt(a))
