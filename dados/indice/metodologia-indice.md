# Índice de Oferta e Acesso a Equipamentos para a Infância: metodologia

> Este índice compara a oferta e o acesso a equipamentos públicos para crianças entre os 7 territórios de Cotia. Não mede a qualidade do atendimento, a saúde das crianças nem a rede particular.

Versão de 09/11/2026. O cálculo está em `scripts/montar_indice.py`. A escolha do índice, com as fontes consultadas, está em [escolha-do-indice.md](escolha-do-indice.md).

## 1. O que é

O índice resume num valor de 0 a 100, por território de CRAS, oito indicadores de oferta e de acesso a equipamentos públicos para crianças, em três dimensões:

- educação infantil;
- saúde;
- assistência social e proteção.

O valor é uma régua entre os 7 territórios de Cotia e não tem sentido fora dessa comparação. Por isso o site não mostra o valor nem a posição de cada território, e sim uma **faixa**:

- **alta:** os 2 territórios com o índice mais alto;
- **média:** os 3 seguintes;
- **baixa:** os 2 com o índice mais baixo.

A seção 5 explica por que o site mostra faixas.

**Por que um índice próprio.** Nenhum índice publicado para a infância pode ser refeito com esta base. Os candidatos medem sobretudo resultado de saúde e condição social, como mortalidade, pré-natal, renda e violência. A base do mapa mede onde ficam os equipamentos públicos e quantas crianças moram em cada território.

Por isso o índice é um cálculo próprio, montado com peças de métodos publicados. A comparação está nas seções 1 a 3 de `escolha-do-indice.md`.

## 2. Os 8 indicadores

**Crianças** são as pessoas de 0 a 14 anos do Censo 2022. Todas as fontes são as da página de metodologia do site.

| # | Indicador | Como se calcula | Leitura | Fonte e data |
|---|---|---|---|---|
| E1 | Matrículas em creche | matrículas em creche nas escolas do território ÷ crianças de 0 a 4 anos × 100 | quanto maior, mais oferta | matrículas: Censo Escolar 2025 (INEP), coleta em 19/10/2026; crianças: Censo 2022 (IBGE), coleta em 27/10/2026 |
| E2 | Matrículas em pré-escola | matrículas em pré-escola nas escolas do território ÷ crianças de 0 a 4 anos × 100 | quanto maior, mais oferta | as mesmas de E1 |
| S1 | UBS por crianças | UBS no território ÷ crianças de 0 a 14 anos × 10.000 | quanto maior, mais oferta | UBS: CNES, coleta em 19/10/2026; crianças: Censo 2022 |
| S2 | Crianças perto de UBS | crianças dos setores a até 1.500 m da UBS mais próxima ÷ crianças do território × 100 | quanto maior, mais acesso | 26 UBS do CNES (19/10/2026); setores e crianças: Censo 2022 |
| S3 | Distância à urgência | distância média até o mais próximo dos 5 pontos: 4 de urgência e o Hospital Regional | quanto menor, mais acesso | CNES, coleta em 19/10/2026 |
| S4 | Distância ao CAPS Infantil | distância média até o único CAPS Infantil | quanto menor, mais acesso | CNES, coleta em 19/10/2026 |
| A1 | Distância ao CRAS | distância média até o mais próximo dos 7 CRAS | quanto menor, mais acesso | página da Secretaria de Desenvolvimento Social (modificada em 14/07/2026, coletada em 19/10/2026) e PMAS 2026–2029 |
| A2 | Distância ao Conselho Tutelar | distância média até o mais próximo dos 2 Conselhos Tutelares | quanto menor, mais acesso | página da Secretaria de Desenvolvimento Social, a mesma de A1 |

**Como as distâncias são medidas:**
- **Crianças por setor:** soma das faixas de 0 a 4, 5 a 9 e 10 a 14 anos (V01031, V01032 e V01033) de cada setor censitário.
  - Se o IBGE esconde qualquer uma das faixas com um "X", o setor inteiro fica de fora, e não vale zero.
- **Ponto do setor:** ponto interno do polígono do setor, calculado em UTM 23S (SIRGAS 2000, EPSG 31983).
- **Distância:** linha reta do ponto do setor até o equipamento, em metros, na mesma projeção.
- **Distância média do território:** soma de (crianças do setor × distância) ÷ soma das crianças dos setores.

## 3. Como o valor é calculado

1. **Posto.** Em cada indicador, os 7 territórios recebem um posto de 1 a 7. O posto 1 vai para a maior oferta ou a menor distância. Territórios empatados dividem o mesmo posto.
2. **Pontos.** Cada posto vira pontos pela conta (7 − posto) ÷ 6 × 100. O posto 1 vale 100 e o posto 7 vale 0.
3. **Pesos.** Cada dimensão vale 1/3, dividido igualmente entre os seus indicadores:

   | Indicadores | Dimensão | Peso de cada um |
   |---|---|---|
   | E1, E2 | Educação infantil | 1/6 (16,67%) |
   | S1, S2, S3, S4 | Saúde | 1/12 (8,33%) |
   | A1, A2 | Assistência e proteção | 1/6 (16,67%) |

4. **Índice.** É a soma ponderada dos pontos e vai de 0 a 100.
5. **Faixa.** Os territórios são ordenados pelo índice: alta para os 2 primeiros, média para os 3 seguintes e baixa para os 2 últimos.

**De onde vem cada peça:**

| Peça | De onde vem |
|---|---|
| Ordenação por postos, com sentido definido e leitura relativa | 3º Diagnóstico Territorial da Primeira Infância (INVUPRIN), Prefeitura de São Paulo, 2025 |
| Matrículas de creche e de pré-escola divididas pelas crianças | Buccini et al. (IMAPI), Box 1: matrículas ÷ população com menos de 5 anos |
| UBS por população | Mapa da Desigualdade da Primeira Infância 2020, Rede Nossa São Paulo |
| Raio de 1,5 km | Seção 9 do plano do mapa; o Mapa da Desigualdade usa o mesmo raio entre escola e casa |
| Construção e teste de sensibilidade | Handbook on Constructing Composite Indicators, OCDE/JRC, 2008 |
| 2SFCA, usado num cenário de sensibilidade | Luo e Wang, 2003 |

A conversão do posto em pontos é deste projeto. O INVUPRIN não detalha o escalonamento final.

## 4. Resultado

O site mostra só a faixa. As tabelas abaixo ficam aqui para quem quiser conferir a conta.

| Território | Faixa | Índice (0 a 100) |
|---|---|---|
| Central (Monte Serrat) | alta | 76,4 |
| Caucaia do Alto | alta | 59,7 |
| Miguel Mirizola | média | 58,3 |
| Jd. Japão | média | 52,8 |
| Jd. Arco-Íris / Jd. Sandra | média | 48,6 |
| KM 21 / Granja Viana | baixa | 38,9 |
| Caputera | baixa | 15,3 |

A coluna Cotia usa as mesmas bases para a cidade inteira. Nas distâncias, ela é a média de todas as crianças de Cotia.

| Indicador | Unidade | Jd. Japão | Caucaia do Alto | Miguel Mirizola | Central (Monte Serrat) | KM 21 / Granja Viana | Jd. Arco-Íris / Jd. Sandra | Caputera | Cotia |
|---|---|---|---|---|---|---|---|---|---|
| E1 | matrículas por 100 crianças de 0–4 | 32,2 | 37,0 | 33,6 | 45,8 | 29,4 | 22,3 | 0,0 | 33,4 |
| E2 | matrículas por 100 crianças de 0–4 | 34,7 | 46,2 | 28,5 | 43,7 | 24,2 | 23,3 | 17,1 | 33,8 |
| S1 | UBS por 10 mil crianças de 0–14 | 6,03 | 5,11 | 3,12 | 3,14 | 7,10 | 3,87 | 4,80 | 4,53 |
| S2 | % das crianças a até 1,5 km de uma UBS | 81,3 | 66,0 | 84,3 | 85,8 | 89,7 | 96,4 | 19,4 | 82,4 |
| S3 | m, média por crianças | 5.827 | 2.422 | 2.596 | 1.521 | 2.354 | 2.120 | 8.817 | 2.454 |
| S4 | m, média por crianças | 17.231 | 13.860 | 2.891 | 2.297 | 7.050 | 3.198 | 9.169 | 6.104 |
| A1 | m, média por crianças | 984 | 2.334 | 989 | 1.607 | 3.125 | 1.115 | 1.538 | 1.849 |
| A2 | m, média por crianças | 5.846 | 2.517 | 2.783 | 2.464 | 6.254 | 4.074 | 9.296 | 3.884 |

Postos e pontos de cada indicador: `indice-territorios.csv` e `parada-1.md`.

## 5. Sensibilidade

O cálculo foi refeito em 17 cenários. Em cada um, só muda o que está descrito:

| Cenário | O que muda |
|---|---|
| `base` | o cálculo da seção 3 |
| `pesos_por_indicador` | os 8 indicadores com o mesmo peso |
| `pesos_imapi` | E1 e E2 dividem 3,79; S1 vale 3,97; os outros 5 valem 3,82 |
| `norm_minmax` | escala de 0 a 100 entre o menor e o maior valor, no lugar dos postos |
| `norm_zscore` | z-score (desvio padrão populacional), no lugar dos postos |
| `sem_municipais` | S3 sem o Hospital Regional; S4 e A2 fora |
| `sem_E1` a `sem_A2` | retira um indicador; o peso dele passa aos outros da mesma dimensão (8 cenários) |
| `s2_1km`, `s2_2km` | S2 com raio de 1.000 m e de 2.000 m |
| `s2_2sfca` | S2 trocado pelo 2SFCA: raio de 1.500 m, capacidade 1 por UBS, média pelas crianças |

**Pesos do IMAPI**, conferidos em 08/11/2026 no artigo de Buccini et al. (https://pmc.ncbi.nlm.nih.gov/articles/PMC8968942):
- Tabela 1: cobertura de creche e pré-escola pesa 3,79, e cobertura de atenção primária, 3,97.
- Os 31 pesos da tabela somam 118,35. A média, 3,82, vale para os 5 indicadores que o IMAPI não tem.

**Escolhas que a skill deixou em aberto:**
- Quando um indicador sai, o peso da dimensão se divide igualmente entre os que sobram. Em `sem_municipais`, S1, S2 e S3 ficam com 1/9 cada, e A1 com 1/3.
- No z-score, só a posição é comparada.
- No min-max, um indicador com o mesmo valor em todos os territórios valeria 100 para todos; isso não ocorreu.
- No 2SFCA, a UBS sem nenhuma criança a até 1,5 km do ponto de algum setor não entra. É o caso de 1 das 26, a UBS Cachoeira.

**Amplitude.** É a diferença entre a posição mais alta e a mais baixa de cada território nos 17 cenários.

| Território | Posições nos 17 cenários | Amplitude |
|---|---|---|
| Central (Monte Serrat) | 1º a 2º | 1 |
| Caucaia do Alto | 2º a 5º | 3 |
| Miguel Mirizola | 2º a 4º | 2 |
| Jd. Japão | 1º a 6º | 5 |
| Jd. Arco-Íris / Jd. Sandra | 2º a 5º | 3 |
| KM 21 / Granja Viana | 4º a 6º | 2 |
| Caputera | 7º em todos | 0 |

Os cenários que mais mexem na ordem:

| Cenário | Soma das mudanças de posição |
|---|---|
| `pesos_imapi` | 10 |
| `sem_municipais` | 8 |
| `pesos_por_indicador` | 6 |
| `sem_A2` | 6 |

A soma junta a diferença de posição de cada território em relação ao cálculo-base. A posição de cada território em cada cenário está em `sensibilidade.csv`, e o valor do índice em `sensibilidade-valores.csv`.

**Por que faixas.** A regra combinada com o Guilherme é mostrar faixas quando algum território varia 3 ou mais posições entre os cenários. Três territórios variam isso ou mais: Jd. Japão (5), Caucaia do Alto (3) e Jd. Arco-Íris / Jd. Sandra (3). As faixas foram a recomendação da Parada 1 e são o formato que o site usa.

## 6. Limitações, com números

- **Duas bases de crianças:**
  - E1, E2 e S1 usam os campos dos territórios, que somam 57.452 crianças de 0 a 14 anos.
  - S2 a A2 usam a soma por setor, que dá 57.157. Ficam de fora:
    - os 39 setores com alguma faixa escondida pelo IBGE, que têm 295 crianças publicadas;
    - outros 35 setores sem nenhuma faixa publicada.
- **Onde a matrícula é contada.** A matrícula conta onde fica a escola, não onde a criança mora: uma criança que estuda no território vizinho conta para o vizinho.
  - Em Cotia são 5.832 matrículas em creche e 5.895 em pré-escola, em 82 escolas públicas e conveniadas.
- **Faixas de idade.** O Censo junta as idades de 0 a 4 e de 5 a 9 anos, o que não coincide com creche (0 a 3) nem com pré-escola (4 e 5). Por isso E1 e E2 são medidas relativas, e não taxas de cobertura.
- **Caputera tem 0 matrícula em creche**, porque as suas 2 escolas públicas constam só como pré-escola no INEP. A base não vê creche particular nem criança matriculada em outro território.
- **Distâncias em linha reta**, não pelo caminho das ruas. Em setores rurais grandes, o ponto interno representa mal onde as crianças moram.
- **Coordenadas aproximadas:**
  - em A1, 5 dos 7 CRAS;
  - em A2, 1 dos 2 Conselhos Tutelares;
  - em S2, S3 e S4, nenhuma: as 26 UBS e os pontos de saúde têm a coordenada do CNES.
  - O efeito aparece nos cenários `sem_A1` e `sem_A2`.
- **Limites dos territórios.** São uma aproximação do mapa do PMAS: 60 setores têm fronteira duvidosa, e 11 dos 132 equipamentos têm bairro listado em outro território.
- **Equipamentos que atendem a cidade toda.** O Hospital Regional, o CAPS Infantil e o Conselho Tutelar de Cotia ficam no território Central, que por isso tem distâncias curtas até eles. O cenário `sem_municipais` mostra o efeito: Central passa ao 2º lugar.
- **Só 7 territórios.** Um único equipamento pode mudar uma posição.

## 7. O que o índice não permite afirmar

- **Como é o atendimento.** O índice não mede equipe, horário, fila nem capacidade. Uma UBS grande e uma pequena contam igual.
- **A saúde das crianças.** Nenhum resultado de saúde entra no cálculo. Faixa alta não quer dizer que as crianças daquele território têm mais saúde.
- **Falta de atendimento.** Só a rede pública e as escolas conveniadas entram. Num território com muita escola ou clínica particular, pouca oferta pública não quer dizer criança sem atendimento, e a base não tem renda para corrigir isso.
- **Desempenho de gestão.** O índice descreve onde ficam os equipamentos. Ele não avalia gestão.

## 8. Como reproduzir

Com o ambiente do `README.md` pronto, rode de dentro de `scripts/`:

```bash
../.venv/Scripts/python montar_indice.py
../.venv/Scripts/python gerar_metodologia.py
```

O script não acessa a rede.

**Conferências.** O script para com erro se alguma destas contas não fechar:
- 754 setores;
- 57.157 crianças por setor e 57.452 por território;
- 274.163 moradores;
- 132 equipamentos, todos com território e coordenada;
- 82 escolas;
- 5.832 matrículas em creche e 5.895 em pré-escola;
- 26 UBS, 5 pontos de urgência e hospital, 1 CAPS Infantil, 7 CRAS e 2 Conselhos Tutelares.

Duas rodadas seguidas produzem arquivos idênticos.

**Saídas:**

| Arquivo | Conteúdo |
|---|---|
| `dados/indice/indice-territorios.csv` | valor, posto e pontos de cada indicador; índice, posição e faixa |
| `dados/indice/sensibilidade.csv` | posição de cada território nos 17 cenários e amplitude |
| `dados/indice/sensibilidade-valores.csv` | valor do índice nos 17 cenários |
| `dados/indice/parada-1.md` | resumo da Parada 1, com todas as tabelas |
| `site/data/indice.json` | o que o site mostra: indicadores, índice e faixa de cada território, e o valor de Cotia |
