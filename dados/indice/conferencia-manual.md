# Conferência à mão e pontos de atenção — Parada 1

Complementa `parada-1.md`, que é gerado por `scripts/montar_indice.py`. Feita em 08/11/2026.

## Recálculo independente de Jd. Japão e Central

Os oito indicadores dos dois territórios foram refeitos por outro caminho. A conta foi feita linha a linha, somando as faixas à mão. As distâncias foram medidas com `distancia_m` de `scripts/comum.py` (fórmula de haversine, em latitude e longitude), em vez da distância em UTM usada no script.

| Território | Indicador | Recálculo | `montar_indice.py` | Diferença |
|---|---|---:|---:|---:|
| Jd. Japão | E1 | 32,24 | 32,24 | 0 |
| Jd. Japão | E2 | 34,75 | 34,75 | 0 |
| Jd. Japão | S1 | 6,03 | 6,03 | 0 |
| Jd. Japão | S2 | 81,33 | 81,33 | 0 |
| Jd. Japão | S3 | 5.822,7 m | 5.826,7 m | −0,07% |
| Jd. Japão | S4 | 17.214,0 m | 17.231,1 m | −0,10% |
| Jd. Japão | A1 | 985,3 m | 984,5 m | +0,09% |
| Jd. Japão | A2 | 5.842,0 m | 5.845,9 m | −0,07% |
| Central | E1 | 45,77 | 45,77 | 0 |
| Central | E2 | 43,72 | 43,72 | 0 |
| Central | S1 | 3,14 | 3,14 | 0 |
| Central | S2 | 85,81 | 85,81 | 0 |
| Central | S3 | 1.522,0 m | 1.521,1 m | +0,06% |
| Central | S4 | 2.296,4 m | 2.297,2 m | −0,04% |
| Central | A1 | 1.608,2 m | 1.607,2 m | +0,06% |
| Central | A2 | 2.462,5 m | 2.463,7 m | −0,05% |

- Contagens e razões batem exatamente.
- As distâncias diferem menos de 0,1% entre haversine e UTM, sem mudar nenhum posto.
- O índice refeito a partir dos pontos dá 52,7778 para Jd. Japão e 76,3889 para Central, iguais ao script.

## Empates apertados

Menor diferença entre territórios vizinhos no posto, em cada indicador:

| Indicador | Vizinhos mais próximos | Diferença |
|---|---|---:|
| A1 | Jd. Japão (984 m) × Miguel Mirizola (989 m) | 0,5% |
| S1 | Central (3,14) × Miguel Mirizola (3,12) | 0,7% |
| S2 | Central (85,8%) × Miguel Mirizola (84,3%) | 1,7% |
| A2 | Central (2.464 m) × Caucaia do Alto (2.517 m) | 2,2% |
| S3 | KM 21 (2.354 m) × Caucaia do Alto (2.422 m) | 2,9% |
| E2 | KM 21 (24,2) × Jd. Arco-Íris (23,3) | 3,8% |
| E1 | Miguel Mirizola (33,6) × Jd. Japão (32,2) | 4,1% |
| S4 | Miguel Mirizola (2.891 m) × Jd. Arco-Íris (3.198 m) | 10,6% |

O caso de A1 é frágil:
- O CRAS Jd. Japão tem ponto aproximado (centro do bairro no OpenStreetMap).
- Uma diferença de 5 m entre os dois territórios cabe nessa incerteza.
- Se os dois trocassem de posto em A1, Jd. Japão perderia 2,8 pontos e Mirizola ganharia 2,8. Mirizola (61,1) passaria Caucaia do Alto (59,7) e as duas trocariam as posições 2 e 3.
- Com isso, as faixas das duas também se inverteriam: Mirizola iria para "alta" e Caucaia para "média". A fronteira entre essas faixas depende de 5 m num ponto aproximado.

## Valores que merecem atenção

1. **Jd. Japão varia de 1º a 6º.** É o território mais instável:
   - fica em 1º em `sem_municipais`, porque A1 passa a valer sozinho a dimensão de assistência, e ali Jd. Japão é o 1º, com o ponto aproximado citado acima;
   - cai para 6º em `pesos_imapi`, que dá menos peso à educação e mais às distâncias, e Jd. Japão é o mais distante do CAPS Infantil (17,2 km).
2. **Caucaia do Alto cai de 2º para 5º** em `pesos_imapi`, `sem_municipais` e `sem_A2`. Isso acontece porque ela é forte em educação infantil e em A2. O Conselho Tutelar de Caucaia também tem ponto aproximado: está no ponto da UBS Caucaia do Alto, à espera da sua conferência.
3. **KM 21 / Granja Viana é 1º em UBS por crianças (S1) e 6º no índice.** Ele tem as matrículas mais baixas depois de Arco-Íris e Caputera, e é o mais distante de um CRAS (3,1 km). O CRAS dele funciona provisoriamente na UBS Jardim Santa Ângela, no extremo leste.
4. **Caputera é 7º nos 17 cenários.**
   - Tem 0 matrícula em creche pública (caso conhecido).
   - Só 19,4% das crianças estão a até 1,5 km de uma UBS. Esse número depende do ponto da UBS Caputera no CNES, um dos 3 pontos suspeitos à espera de conferência: ele fica fora do limite de Cotia e a 2,6 km da escola vizinha de numeração.
   - Com a UBS no ponto da EM do Bairro da Caputera, S2 subiria para 53,7%. Mesmo assim continuaria em 7º, porque o 6º tem 66,0%.
5. **Central é 1º em 16 dos 17 cenários e 2º em `sem_municipais`.** Era o esperado, porque o Central fica perto de quase todos os equipamentos municipais.
6. **No 2SFCA, a UBS Cachoeira fica fora**, porque não há ponto de setor a até 1,5 km dela. O ponto dela no CNES fica 619 m fora do limite de Cotia (outro dos 3 pontos suspeitos).
7. **Duas bases de crianças.** E1, E2 e S1 usam os campos do `territorios.geojson` (57.452 crianças). S2 a A2 usam a soma por setor, em que um "X" tira o setor (57.157). A diferença por território vai de 8 crianças (Jd. Japão) a 109 (KM 21).
