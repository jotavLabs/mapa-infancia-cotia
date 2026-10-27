"""Geocodificação pelo Nominatim (OSM) com cache local.

Política de uso: no máximo 1 requisição por segundo e User-Agent identificado.
https://operations.osmfoundation.org/policies/nominatim/
Toda consulta fica em dados/cache-geocodificacao.csv e nunca é repetida.
"""
import csv
import time

import requests

from comum import DADOS, HOJE, USER_AGENT

CACHE = DADOS / "cache-geocodificacao.csv"
CAMPOS_CACHE = ["consulta", "lat", "lon", "tipo", "nome_encontrado", "data"]
URL = "https://nominatim.openstreetmap.org/search"
# Caixa de Cotia com folga (oeste, norte, leste, sul)
VIEWBOX = "-47.20,-23.48,-46.75,-23.88"

# Tipos de resultado precisos o bastante para marcar o ponto (edifício, lugar ou número da rua)
TIPOS_PRECISOS = {"building", "amenity", "house", "place", "office", "healthcare", "school", "government", "social_facility"}

_cache = None
_ultima = 0.0


def _carregar():
    global _cache
    if _cache is None:
        _cache = {}
        if CACHE.exists():
            with CACHE.open(encoding="utf-8", newline="") as f:
                for linha in csv.DictReader(f):
                    _cache[linha["consulta"]] = linha
    return _cache


def _gravar(linha):
    novo = not CACHE.exists()
    with CACHE.open("a", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=CAMPOS_CACHE)
        if novo:
            w.writeheader()
        w.writerow(linha)


def geocodificar(consulta):
    """Devolve dict com lat, lon, tipo e nome_encontrado; lat vazio quando não encontra."""
    global _ultima
    cache = _carregar()
    if consulta in cache:
        return cache[consulta]
    espera = 1.1 - (time.monotonic() - _ultima)
    if espera > 0:
        time.sleep(espera)
    r = requests.get(URL, params={
        "q": consulta, "format": "jsonv2", "limit": 1, "countrycodes": "br",
        "viewbox": VIEWBOX, "bounded": 1, "addressdetails": 0,
    }, headers={"User-Agent": USER_AGENT, "Accept-Language": "pt-BR"}, timeout=60)
    _ultima = time.monotonic()
    r.raise_for_status()
    res = r.json()
    if res:
        h = res[0]
        linha = {"consulta": consulta, "lat": h["lat"], "lon": h["lon"],
                 "tipo": h.get("addresstype") or h.get("type", ""), "nome_encontrado": h.get("display_name", ""), "data": HOJE}
    else:
        linha = {"consulta": consulta, "lat": "", "lon": "", "tipo": "", "nome_encontrado": "", "data": HOJE}
    cache[consulta] = linha
    _gravar(linha)
    return linha


def preciso(resultado):
    return bool(resultado.get("lat")) and resultado.get("tipo") in TIPOS_PRECISOS
