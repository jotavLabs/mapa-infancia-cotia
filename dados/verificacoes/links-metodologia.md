# Links da metodologia — conferência de 27/10/2026

Cada link externo de `site/metodologia.html` e `site/index.html` foi aberto com `curl -L`.

| Status | Link |
|---|---|
| 200 | https://apisidra.ibge.gov.br/values/t/4709/n6/3513009/v/93/p/2022 |
| 200 | https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/leaflet.min.css |
| 200 | https://cotia.sp.gov.br/carta-de-servico-ao-usuario/ |
| 200 | https://cotia.sp.gov.br/desenvolvimento-social-2025/ |
| 200 | https://cotia.sp.gov.br/wp-content/uploads/2026/06/298-resolucao-cmas-aprova-o-plano-municipal-de-assistencia-social-2026-a-2029-.pdf |
| 200 | https://ftp.ibge.gov.br/Censos/Censo_Demografico_2022/Agregados_por_Setores_Censitarios/ |
| 200 | https://servicodados.ibge.gov.br/api/v3/malhas/municipios/3513009?formato=application/vnd.geo%2Bjson&qualidade=maxima |
| 200 | https://www.gov.br/inep/pt-br/acesso-a-informacao/dados-abertos/inep-data/catalogo-de-escolas |
| 200 | https://www.gov.br/inep/pt-br/acesso-a-informacao/dados-abertos/microdados/censo-escolar |
| 200 | https://www.openstreetmap.org/copyright |
| sem resposta | https://apidadosabertos.saude.gov.br/cnes/estabelecimentos?codigo_municipio=351300&limit=20&offset=0 |

## Ocorrência: API de dados abertos do Ministério da Saúde fora do ar

Em 27/10/2026, todo o host `apidadosabertos.saude.gov.br` recusou conexões ("Connection was reset"), inclusive a raiz. Em 19/10/2026 a mesma API respondeu normalmente e a extração usada no site é dessa data (retrato em `dados/brutos/cnes-cotia-publicos-2026-10-19.json`). O site do CNES (`cnes.datasus.gov.br`), usado nas fichas de cada unidade, respondeu 200. O link foi mantido na metodologia porque é o endereço oficial da fonte; vale testar de novo antes da publicação.
