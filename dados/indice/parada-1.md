# Índice de Oferta e Acesso a Equipamentos para a Infância — Parada 1

> Este índice compara a oferta e o acesso a equipamentos públicos para crianças entre os 7 territórios de Cotia. Não mede a qualidade do atendimento, a saúde das crianças nem a rede particular.

Gerado por `scripts/montar_indice.py`. O valor do índice vai de 0 a 100 e é uma régua entre os 7 territórios, sem sentido absoluto.

## Resultado do cálculo-base

| Posição | Território | Índice | Faixa (2 · 3 · 2) |
|---|---|---|---|
| 1 | Central (Monte Serrat) | 76,4 | alta |
| 2 | Caucaia do Alto | 59,7 | alta |
| 3 | Miguel Mirizola | 58,3 | média |
| 4 | Jd. Japão | 52,8 | média |
| 5 | Jd. Arco-Íris / Jd. Sandra | 48,6 | média |
| 6 | KM 21 / Granja Viana | 38,9 | baixa |
| 7 | Caputera | 15,3 | baixa |

## Indicadores: valor e posto (1 = melhor)

| Indicador | Unidade | Melhor | Jd. Japão | Caucaia do Alto | Miguel Mirizola | Central (Monte Serrat) | KM 21 / Granja Viana | Jd. Arco-Íris / Jd. Sandra | Caputera |
|---|---|---|---|---|---|---|---|---|---|
| E1 Matrículas em creche | matrículas por 100 crianças de 0–4 | maior | 32,2 (4º) | 37,0 (2º) | 33,6 (3º) | 45,8 (1º) | 29,4 (5º) | 22,3 (6º) | 0,0 (7º) |
| E2 Matrículas em pré-escola | matrículas por 100 crianças de 0–4 | maior | 34,7 (3º) | 46,2 (1º) | 28,5 (4º) | 43,7 (2º) | 24,2 (5º) | 23,3 (6º) | 17,1 (7º) |
| S1 UBS por crianças | UBS por 10 mil crianças de 0–14 | maior | 6,03 (2º) | 5,11 (3º) | 3,12 (7º) | 3,14 (6º) | 7,10 (1º) | 3,87 (5º) | 4,80 (4º) |
| S2 Crianças perto de UBS | % das crianças a até 1,5 km de uma UBS | maior | 81,3 (5º) | 66,0 (6º) | 84,3 (4º) | 85,8 (3º) | 89,7 (2º) | 96,4 (1º) | 19,4 (7º) |
| S3 Distância à urgência | m, média ponderada por crianças | menor | 5.827 (6º) | 2.422 (4º) | 2.596 (5º) | 1.521 (1º) | 2.354 (3º) | 2.120 (2º) | 8.817 (7º) |
| S4 Distância ao CAPS Infantil | m, média ponderada por crianças | menor | 17.231 (7º) | 13.860 (6º) | 2.891 (2º) | 2.297 (1º) | 7.050 (4º) | 3.198 (3º) | 9.169 (5º) |
| A1 Distância ao CRAS | m, média ponderada por crianças | menor | 984 (1º) | 2.334 (6º) | 989 (2º) | 1.607 (5º) | 3.125 (7º) | 1.115 (3º) | 1.538 (4º) |
| A2 Distância ao Conselho Tutelar | m, média ponderada por crianças | menor | 5.846 (5º) | 2.517 (2º) | 2.783 (3º) | 2.464 (1º) | 6.254 (6º) | 4.074 (4º) | 9.296 (7º) |

## Pontos por indicador e pesos

Pontos = (7 − posto) ÷ 6 × 100. Pesos: cada dimensão vale 1/3, dividido igualmente entre seus indicadores.

| Indicador | Peso | Jd. Japão | Caucaia do Alto | Miguel Mirizola | Central (Monte Serrat) | KM 21 / Granja Viana | Jd. Arco-Íris / Jd. Sandra | Caputera |
|---|---|---|---|---|---|---|---|---|
| E1 | 16,67% | 50,0 | 83,3 | 66,7 | 100,0 | 33,3 | 16,7 | 0,0 |
| E2 | 16,67% | 66,7 | 100,0 | 50,0 | 83,3 | 33,3 | 16,7 | 0,0 |
| S1 | 8,33% | 83,3 | 66,7 | 0,0 | 16,7 | 100,0 | 33,3 | 50,0 |
| S2 | 8,33% | 33,3 | 16,7 | 50,0 | 66,7 | 83,3 | 100,0 | 0,0 |
| S3 | 8,33% | 16,7 | 50,0 | 33,3 | 100,0 | 66,7 | 83,3 | 0,0 |
| S4 | 8,33% | 0,0 | 16,7 | 83,3 | 100,0 | 50,0 | 66,7 | 33,3 |
| A1 | 16,67% | 100,0 | 16,7 | 83,3 | 33,3 | 0,0 | 66,7 | 50,0 |
| A2 | 16,67% | 33,3 | 83,3 | 66,7 | 100,0 | 16,7 | 50,0 | 0,0 |

## Sensibilidade: posição em cada um dos 17 cenários

| Cenário | O que muda | Jd. Japão | Caucaia do Alto | Miguel Mirizola | Central (Monte Serrat) | KM 21 / Granja Viana | Jd. Arco-Íris / Jd. Sandra | Caputera |
|---|---|---|---|---|---|---|---|---|
| base | postos, pesos iguais por dimensão | 4 | 2 | 3 | 1 | 6 | 5 | 7 |
| pesos_por_indicador | os 8 indicadores com o mesmo peso | 5 | 2 | 2 | 1 | 5 | 2 | 7 |
| pesos_imapi | E1 e E2 dividem 3,79; S1 = 3,97; os outros 5 = 3,82 | 6 | 5 | 3 | 1 | 4 | 2 | 7 |
| norm_minmax | min-max de 0 a 100 no lugar dos postos | 5 | 3 | 2 | 1 | 6 | 4 | 7 |
| norm_zscore | z-score (ddof=0) no lugar dos postos | 5 | 3 | 2 | 1 | 6 | 4 | 7 |
| sem_municipais | S3 sem o hospital; S4 e A2 fora | 1 | 5 | 3 | 2 | 6 | 4 | 7 |
| sem_E1 | retira E1; o peso passa aos outros da dimensão | 3 | 2 | 3 | 1 | 6 | 5 | 7 |
| sem_E2 | retira E2; o peso passa aos outros da dimensão | 4 | 3 | 2 | 1 | 6 | 5 | 7 |
| sem_S1 | retira S1; o peso passa aos outros da dimensão | 5 | 3 | 2 | 1 | 6 | 4 | 7 |
| sem_S2 | retira S2; o peso passa aos outros da dimensão | 4 | 2 | 3 | 1 | 6 | 5 | 7 |
| sem_S3 | retira S3; o peso passa aos outros da dimensão | 4 | 3 | 2 | 1 | 6 | 5 | 7 |
| sem_S4 | retira S4; o peso passa aos outros da dimensão | 3 | 2 | 4 | 1 | 6 | 5 | 7 |
| sem_A1 | retira A1; o peso passa aos outros da dimensão | 5 | 2 | 3 | 1 | 5 | 4 | 7 |
| sem_A2 | retira A2; o peso passa aos outros da dimensão | 2 | 5 | 3 | 1 | 6 | 4 | 7 |
| s2_1km | S2 com raio de 1.000 m | 4 | 2 | 3 | 1 | 6 | 5 | 7 |
| s2_2km | S2 com raio de 2.000 m | 4 | 3 | 2 | 1 | 6 | 5 | 7 |
| s2_2sfca | S2 trocado por 2SFCA (raio de 1.500 m, capacidade 1 por UBS) | 3 | 2 | 4 | 1 | 6 | 5 | 7 |

### Amplitude por território

| Território | Posição-base | Faixa de posições | Amplitude | Melhor posição | Pior posição |
|---|---|---|---|---|---|
| Central (Monte Serrat) | 1 | 1º a 2º | 1 | — | 2º em: sem_municipais |
| Caucaia do Alto | 2 | 2º a 5º | 3 | — | 5º em: pesos_imapi, sem_municipais, sem_A2 |
| Miguel Mirizola | 3 | 2º a 4º | 2 | 2º em: pesos_por_indicador, norm_minmax, norm_zscore, sem_E2, sem_S1, sem_S3, s2_2km | 4º em: sem_S4, s2_2sfca |
| Jd. Japão | 4 | 1º a 6º | 5 | 1º em: sem_municipais | 6º em: pesos_imapi |
| Jd. Arco-Íris / Jd. Sandra | 5 | 2º a 5º | 3 | 2º em: pesos_por_indicador, pesos_imapi | — |
| KM 21 / Granja Viana | 6 | 4º a 6º | 2 | 4º em: pesos_imapi | — |
| Caputera | 7 | 7º a 7º | 0 | — | — |

### Cenários que mais mexem na ordem

Soma, nos 7 territórios, da diferença de posição em relação ao cálculo-base.

| Cenário | Soma das mudanças |
|---|---|
| pesos_imapi | 10 |
| sem_municipais | 8 |
| pesos_por_indicador | 6 |
| sem_A2 | 6 |
| norm_zscore | 4 |
| sem_S1 | 4 |
| norm_minmax | 4 |
| sem_A1 | 3 |

## Recomendação: posições ou faixas

**Mostrar faixas, não posições.** Pela regra da skill, basta um território variar 3 ou mais posições entre os cenários, e aqui variam: Jd. Japão (5), Caucaia do Alto (3), Jd. Arco-Íris / Jd. Sandra (3). Faixas pelo cálculo-base: alta para os 2 maiores índices, média para os 3 seguintes e baixa para os 2 menores.

## Base de crianças

E1, E2 e S1 usam os campos de `territorios.geojson`. S2 a A2 usam a soma por setor, em que um "X" do IBGE em qualquer faixa tira o setor inteiro.

| Território | 0–14 no geojson (E1, E2, S1) | 0–14 por setor (S2 a A2) | Setores com faixa escondida |
|---|---|---|---|
| Jd. Japão | 1.658 | 1.650 | 1 |
| Caucaia do Alto | 9.778 | 9.736 | 6 |
| Miguel Mirizola | 6.410 | 6.395 | 2 |
| Central (Monte Serrat) | 15.907 | 15.831 | 11 |
| KM 21 / Granja Viana | 11.271 | 11.162 | 13 |
| Jd. Arco-Íris / Jd. Sandra | 10.346 | 10.314 | 4 |
| Caputera | 2.082 | 2.069 | 2 |
| Cotia | 57.452 | 57.157 | 39 |

## IMAPI

Conferido em 08/11/2026 em https://pmc.ncbi.nlm.nih.gov/articles/PMC8968942 (Buccini et al.). Tabela 1: 31 pesos analíticos, que somam 118,35 (média 3,818). Cobertura de creche e pré-escola pesa 3,79, e cobertura de atenção primária, 3,97. Box 1: a cobertura soma as matrículas de creche e de pré-escola e divide pela população com menos de 5 anos. Aqui creche e pré-escola são dois indicadores com o mesmo denominador (0–4 anos), e S1 conta UBS, enquanto o IMAPI mede a população coberta por equipes. O cenário `pesos_imapi` foi mantido.

## Pontos de atenção

- Valores zero: E1 = 0 em Caputera.
- Empates de posto no cálculo-base: nenhum.
- No 2SFCA, 1 das 26 UBS não tem criança a até 1,5 km do ponto de algum setor e fica fora: UBS Cachoeira.
- 7 dos 9 pontos de assistência social e 1 dos 2 Conselhos Tutelares têm coordenada aproximada, o que afeta A1 e A2. O efeito aparece nos cenários `sem_A1` e `sem_A2`.
- O território Central fica perto de quase todos os equipamentos municipais; por isso existe o cenário `sem_municipais`.

## Conferências que passaram

- 754 setores casados entre o CSV e o GeoJSON.
- Crianças de 0–14: 57.157 somando setores (um X tira o setor) e 57.452 somando os 7 territórios. A diferença de 295 são as crianças publicadas nos 39 setores com faixa escondida; outros 35 setores não têm nenhuma faixa publicada.
- 274.163 moradores em territorios.geojson.
- 132 equipamentos, todos com território e coordenada; 82 escolas casadas por id.
- 5.832 matrículas em creche e 5.895 em pré-escola.
- Pontos: 26 UBS, 5 pontos de urgência e hospital, 4 pontos de urgência sem o hospital, 1 CAPSi, 7 CRAS, 2 Conselhos Tutelares.
