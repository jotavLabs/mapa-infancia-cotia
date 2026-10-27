# Mapa Infância Cotia

Mapa de onde estão, e onde faltam, os equipamentos públicos de saúde, educação infantil, assistência social e proteção que atendem as crianças de Cotia (SP), território por território.

Site publicado: https://jotavlabs.github.io/mapa-infancia-cotia/

Site estático (HTML, CSS e JavaScript, com Leaflet 1.9.4 e OpenStreetMap), sem servidor, sem chave de API e sem cookies. Os dados saem de fontes oficiais abertas e são montados pelos scripts em `scripts/`. A metodologia completa está em `site/metodologia.html`.

## Estrutura

```
insumos/        o que veio do Guilherme (não editar)
dados/brutos/   downloads originais com data no nome (os grandes e os sensíveis ficam fora do Git)
dados/          camadas intermediárias (saude-cnes.csv, educacao-inep.csv, ...)
dados/verificacoes/  relatórios de conferência e páginas de revisão
scripts/        coleta, conferência e montagem
site/           o que vai para o GitHub Pages
```

## Preparar o ambiente

```bash
python -m venv .venv
.venv/Scripts/python -m pip install -r requirements.txt
```

## Refazer os dados

Rode de dentro de `scripts/`, nesta ordem. Os scripts de coleta reaproveitam o download mais recente já salvo em `dados/brutos/`; passe `--rebaixar` para baixar de novo.

| # | Script | O que faz | Saída |
|---|---|---|---|
| 1 | `baixar_contorno.py` | Contorno de Cotia da API de malhas do IBGE | `site/data/cotia.geojson` |
| 2 | `coletar_cnes.py` | Estabelecimentos de Cotia na API do CNES; filtra os equipamentos públicos de saúde | `dados/saude-cnes.csv` |
| 3 | `verificar_saude.py` | Confere a saúde contra o plano, o insumo do Guilherme e o OpenStreetMap | `dados/verificacoes/saude-cnes.md` |
| 4 | `coletar_inep.py` | Microdados do Censo Escolar 2025 (~540 MB, fora do Git); recorta as escolas de Cotia com creche ou pré-escola | `dados/brutos/inep-cotia-2025.csv` |
| 5 | `montar_educacao.py` | Junta o recorte do INEP com as fichas do Catálogo de Escolas | `dados/educacao-inep.csv` |
| 6 | `localizar_enderecos.py` | Localiza CRAS, CREAS e Conselhos Tutelares a partir das listas verificadas | `dados/assistencia-social.csv`, `dados/protecao.csv` |
| 7 | `coletar_censo.py` | Setores e demografia do Censo 2022 (~200 MB, fora do Git) e o total oficial do SIDRA | `dados/brutos/setores-cotia-2022.geojson`, `demografia-cotia-2022.csv` |
| 8 | `desenhar_territorios.py` | Encaixa o mapa do PMAS nos setores e desenha os 7 territórios com população | `dados/territorios-base.geojson`, `dados/verificacoes/territorios.md`, `conferir-territorios.html` |
| 9 | `listar_pendentes.py` | Lista pontos sem coordenada confiável, sugere um ponto provisório e gera a página de conferência | `dados/verificacoes/pendentes.md`, `coordenadas-provisorias.csv`, `conferir-coordenadas.html` |
| 10 | `montar_equipamentos.py` | Junta as 9 camadas, liga cada ponto ao território e conta equipamentos por território | `site/data/equipamentos.csv`, `.geojson`, `territorios.geojson`, `bairros.json` |
| 11 | `gerar_metodologia.py` | Preenche a página de metodologia com os números dos relatórios | `site/metodologia.html` |

Conferência opcional: `extrair_insumos_pmas.py` extrai do PDF do PMAS os territórios e o mapa, para comparar com `insumos/`.

A geocodificação usa o Nominatim (no máximo 1 requisição por segundo), com cache versionado em `dados/cache-geocodificacao.csv`: refazer os dados não repete consultas.

### Etapas que não são script

- **Catálogo de Escolas do INEP** (`dados/brutos/inep-catalogo-escolas-cotia-2026-10-19.psv`): os microdados de 2025 não trazem mais endereço nem coordenadas. Esses campos foram lidos da ficha de cada escola no Catálogo de Escolas, um painel interativo (Oracle Analytics) que só funciona no navegador. A URL de cada ficha está em `montar_educacao.py` (`CATALOGO`).
- **Endereços verificados** (`dados/verificacoes/enderecos-cras.csv` e `enderecos-protecao-creas.csv`): conferidos à mão contra o PMAS 2026–2029, a página da Secretaria de Desenvolvimento Social e as fontes listadas em `dados/verificacoes/conselhos-tutelares.md`.
- **Coordenadas conferidas** (`dados/verificacoes/coordenadas-manuais.csv`): o que o João aprovar ou corrigir em `conferir-coordenadas.html` (colunas `id,lat,lon,justificativa`). Elas prevalecem sobre as provisórias.

## Ver o site localmente

```bash
.venv/Scripts/python -m http.server 8765 --directory site
```

Depois abra http://localhost:8765. As páginas de conferência ficam em `dados/verificacoes/` e também precisam ser abertas por um servidor local (os tiles do OpenStreetMap exigem endereço http).

## Publicação

O workflow `.github/workflows/pages.yml` publica a pasta `site/` no GitHub Pages a cada push nas branches `publicacao-v1` e `main`.

## Créditos

Feito por João Bento em colaboração com o Claude Code (Anthropic), a partir do plano e dos insumos preparados pelo Guilherme. Dados públicos de CNES, INEP, IBGE e Prefeitura de Cotia; mapa-base e geocodificação © colaboradores do OpenStreetMap (ODbL).
