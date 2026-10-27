# Checklist da seção 8 — Parada 4 (27/10/2026)

Prévia privada (sem mapa de ruas e sem busca por endereço, que a hospedagem de prévias bloqueia): https://claude.ai/artifact/5ST1Rer3WrqB5fudPzsubU
Versão completa, local: `.venv/Scripts/python -m http.server 8765 --directory site` e http://localhost:8765

| Item | Situação | Onde conferir |
|---|---|---|
| As 9 camadas aparecem com pontos, legenda e ficha | Feito | mapa, painel “Camadas” |
| Todo ponto tem `fonte`, `fonte_url`, `data_coleta`, `coord_origem` e `verificacao`; nenhum está `pendente` | **Falta** — os campos estão preenchidos nos 132 pontos, mas 10 ainda estão `pendente` (no mapa, em posição aproximada) | `dados/verificacoes/pendentes.md`, `conferir-coordenadas.html` |
| `dados/verificacoes/conselhos-tutelares.md` documenta cada fonte consultada | Feito | o próprio arquivo |
| Os 7 territórios aparecem e abrem o painel com população e contagens | Feito | mapa, seletor “Território” |
| A soma da população fica a no máximo 1% do total oficial, com a diferença explicada | Feito: 274.163 × 274.413 (0,09%, setores em sigilo) | `dados/verificacoes/territorios.md`, metodologia |
| A tabela comparativa ordena por qualquer coluna | Feito | seção “Comparar os 7 territórios” |
| A metodologia lista as fontes com link e data, e as limitações | Feito; em 27/10 a API de dados abertos do Ministério da Saúde recusava conexões | `site/metodologia.html`, `links-metodologia.md` |
| Os downloads entregam `equipamentos.csv` e `territorios.geojson` | Feito na versão completa (na prévia, desligados) | seção “Baixar dados” |
| Funciona a 375 px sem rolagem horizontal | Feito (mapa, tabela e metodologia) | celular |
| Nenhum endereço de acolhimento e nenhum dado pessoal no repositório | Feito; o PDF do PMAS e o JSON completo do CNES ficam fora do Git | `.gitignore` |
| O `README.md` permite refazer os dados rodando os scripts na ordem | Feito: rodado do zero numa pasta limpa, os 5 arquivos de `site/data/` saíram idênticos | `README.md` |

## Para o João conferir

1. **13 pontos**: 10 com localização aproximada (5 CRAS, 2 CREAS, o Conselho Tutelar de Caucaia e 2 escolas) e 3 UBS com coordenada suspeita no CNES (Água Espraiada, Caputera e Cachoeira). Arraste ou aceite cada marcador em `conferir-coordenadas.html` e mande o texto do quadro.
2. **Fronteiras**: 60 setores marcados como duvidosos em `conferir-territorios.html` (use o controle de opacidade para sobrepor o mapa do PMAS) e 11 equipamentos cujo bairro aparece na lista de outro território (`territorio-equipamentos.md`), concentrados no Jardim Cláudio e no Parque Turiguara.
3. **Miolo sem CRAS**: com a regra “vizinho de maior fronteira dentro do mesmo distrito”, o miolo soma 1,72% da população, abaixo do limite de 2% do plano. Se preferir outro critério para a Reserva do Morro Grande, é só dizer.
