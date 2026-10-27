# Territórios de CRAS — Parada 3 (2026-10-27)

## Georreferenciamento do mapa do PMAS

- Ajuste do contorno de Cotia (setores do IBGE) sobre a mancha colorida do mapa: **IoU 0,957** (1 = sobreposição perfeita).
- Rotação -1.65°; escala 60.2 m/px na horizontal e 51.5 m/px na vertical.
- Pontos de controle (extremos do município), distância entre o contorno ajustado e a borda do mapa: norte 3.0 px (~179 m); sul 23.5 px (~1418 m); oeste 2.8 px (~166 m); leste 4.1 px (~247 m).

## População por território (Censo 2022)

| # | Território | Setores | Moradores | 0–4 | 5–9 | 10–14 | 15–19 | Crianças 0–14 | Setores em sigilo | Setores do miolo herdados |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | Jd. Japão | 18 | 7.320 | 518 | 593 | 547 | 555 | 1.658 | 1 | 4 |
| 2 | Caucaia do Alto | 128 | 44.398 | 2.995 | 3.463 | 3.320 | 3.210 | 9.778 | 2 | 3 |
| 3 | Miguel Mirizola | 72 | 28.218 | 1.925 | 2.306 | 2.179 | 2.020 | 6.410 | 1 | 0 |
| 4 | Central (Monte Serrat) | 215 | 81.352 | 4.874 | 5.663 | 5.370 | 5.468 | 15.907 | 5 | 0 |
| 5 | KM 21 / Granja Viana | 175 | 60.319 | 3.288 | 3.973 | 4.010 | 3.748 | 11.271 | 7 | 0 |
| 6 | Jd. Arco-Íris / Jd. Sandra | 120 | 43.823 | 3.189 | 3.761 | 3.396 | 3.389 | 10.346 | 2 | 2 |
| 7 | Caputera | 26 | 8.733 | 648 | 742 | 692 | 727 | 2.082 | 1 | 7 |

- Soma dos setores: **274.163** moradores. Total oficial de Cotia (SIDRA, tabela 4709): **274.413**. Diferença: 250 (0,09%), que corresponde aos 19 setores em sigilo (menos de 5 domicílios, valores "X" do IBGE). Limite do plano: 1%.
- Setores sem nenhum registro na tabela de demografia (sem moradores): 14.
- Miolo sem CRAS (verde-pálido): 16 setores e 4.725 moradores (1,72% de Cotia). Abaixo de 2%: cada setor foi para o vizinho com a maior fronteira comum.

## Setores de fronteira duvidosos

Critérios: setor do miolo ou sem cor no mapa (herdou o vizinho), cor sob o ponto diferente da cor dominante do polígono, ou menos de 60% de votos na janela do ponto.

| Setor | Distrito | Território | Como | Cor sob o ponto | Cor dominante do polígono | Moradores |
|---|---|---|---|---|---|---:|
| 351300910000092 | Caucaia do Alto | Jd. Japão | miolo sem CRAS → vizinho | miolo | miolo | 753 |
| 351300910000099 | Caucaia do Alto | Jd. Japão | cor sob o ponto interno | Jd. Japão | Jd. Japão |  |
| 351300910000100 | Caucaia do Alto | Jd. Japão | miolo sem CRAS → vizinho | miolo | miolo | 64 |
| 351300910000102 | Caucaia do Alto | Jd. Japão | miolo sem CRAS → vizinho | miolo | miolo | 203 |
| 351300910000140 | Caucaia do Alto | Jd. Japão | miolo sem CRAS → vizinho | miolo | miolo | 584 |
| 351300910000156 | Caucaia do Alto | Jd. Japão | cor dominante do setor | miolo | Jd. Japão | 568 |
| 351300905000356 | Cotia | Caucaia do Alto | cor sob o ponto interno | Caucaia do Alto | Central (Monte Serrat) | 139 |
| 351300905000397 | Cotia | Caucaia do Alto | cor sob o ponto interno | Caucaia do Alto | Central (Monte Serrat) | 326 |
| 351300905000721 | Cotia | Caucaia do Alto | cor sob o ponto interno | Caucaia do Alto | Caucaia do Alto | 201 |
| 351300905000747 | Cotia | Caucaia do Alto | cor sob o ponto interno | Caucaia do Alto | Miguel Mirizola | 109 |
| 351300905000819 | Cotia | Caucaia do Alto | cor dominante do setor | miolo | Caucaia do Alto | 102 |
| 351300910000019 | Caucaia do Alto | Caucaia do Alto | miolo sem CRAS → vizinho | miolo | miolo |  |
| 351300910000118 | Caucaia do Alto | Caucaia do Alto | cor dominante do setor | miolo | Caucaia do Alto | 47 |
| 351300910000139 | Caucaia do Alto | Caucaia do Alto | cor sob o ponto interno | Caucaia do Alto | miolo | 333 |
| 351300910000165 | Caucaia do Alto | Caucaia do Alto | miolo sem CRAS → vizinho | miolo | miolo | 361 |
| 351300910000176 | Caucaia do Alto | Caucaia do Alto | cor sob o ponto interno | Caucaia do Alto | Caucaia do Alto |  |
| 351300910000188 | Caucaia do Alto | Caucaia do Alto | cor dominante do setor | miolo | Caucaia do Alto | 161 |
| 351300910000189 | Caucaia do Alto | Caucaia do Alto | miolo sem CRAS → vizinho | miolo | miolo | 53 |
| 351300910000191 | Caucaia do Alto | Caucaia do Alto | cor sob o ponto interno | Caucaia do Alto | Jd. Japão | 381 |
| 351300910000204 | Caucaia do Alto | Caucaia do Alto | cor dominante do setor | miolo | Caucaia do Alto | 177 |
| 351300905000368 | Cotia | Miguel Mirizola | cor sob o ponto interno | Miguel Mirizola | Miguel Mirizola | 188 |
| 351300905000482 | Cotia | Miguel Mirizola | cor sob o ponto interno | Miguel Mirizola | Miguel Mirizola | 558 |
| 351300905000536 | Cotia | Miguel Mirizola | cor dominante do setor | miolo | Miguel Mirizola | 121 |
| 351300905000641 | Cotia | Miguel Mirizola | cor sob o ponto interno | Miguel Mirizola | Miguel Mirizola | 417 |
| 351300905000864 | Cotia | Miguel Mirizola | cor sob o ponto interno | Miguel Mirizola | Miguel Mirizola |  |
| 351300905000193 | Cotia | Central (Monte Serrat) | cor sob o ponto interno | Central (Monte Serrat) | Central (Monte Serrat) | 603 |
| 351300905000247 | Cotia | Central (Monte Serrat) | cor sob o ponto interno | Central (Monte Serrat) | Miguel Mirizola | 377 |
| 351300905000263 | Cotia | Central (Monte Serrat) | cor sob o ponto interno | Central (Monte Serrat) | miolo | 225 |
| 351300905000266 | Cotia | Central (Monte Serrat) | cor sob o ponto interno | Central (Monte Serrat) | Central (Monte Serrat) | 359 |
| 351300905000494 | Cotia | Central (Monte Serrat) | cor dominante do setor | miolo | Central (Monte Serrat) | 153 |
| 351300905000497 | Cotia | Central (Monte Serrat) | cor dominante do setor | miolo | Central (Monte Serrat) | 489 |
| 351300905000708 | Cotia | Central (Monte Serrat) | cor sob o ponto interno | Central (Monte Serrat) | Central (Monte Serrat) | 769 |
| 351300905000763 | Cotia | Central (Monte Serrat) | cor sob o ponto interno | Central (Monte Serrat) | KM 21 / Granja Viana | 261 |
| 351300905000829 | Cotia | Central (Monte Serrat) | cor sob o ponto interno | Central (Monte Serrat) | Jd. Arco-Íris / Jd. Sandra | 74 |
| 351300905000831 | Cotia | Central (Monte Serrat) | cor sob o ponto interno | Central (Monte Serrat) | Jd. Arco-Íris / Jd. Sandra | 262 |
| 351300905000840 | Cotia | Central (Monte Serrat) | cor sob o ponto interno | Central (Monte Serrat) | Central (Monte Serrat) |  |
| 351300910000159 | Caucaia do Alto | Central (Monte Serrat) | cor sob o ponto interno | Central (Monte Serrat) | Caucaia do Alto | 288 |
| 351300905000106 | Cotia | KM 21 / Granja Viana | cor sob o ponto interno | KM 21 / Granja Viana | KM 21 / Granja Viana | 334 |
| 351300905000259 | Cotia | Jd. Arco-Íris / Jd. Sandra | cor sob o ponto interno | Jd. Arco-Íris / Jd. Sandra | Central (Monte Serrat) | 451 |
| 351300905000316 | Cotia | Jd. Arco-Íris / Jd. Sandra | cor sob o ponto interno | Jd. Arco-Íris / Jd. Sandra | Central (Monte Serrat) | 539 |
| 351300905000384 | Cotia | Jd. Arco-Íris / Jd. Sandra | cor sob o ponto interno | Jd. Arco-Íris / Jd. Sandra | Jd. Arco-Íris / Jd. Sandra | 75 |
| 351300905000547 | Cotia | Jd. Arco-Íris / Jd. Sandra | cor sob o ponto interno | Jd. Arco-Íris / Jd. Sandra | Jd. Arco-Íris / Jd. Sandra | 386 |
| 351300905000740 | Cotia | Jd. Arco-Íris / Jd. Sandra | cor sob o ponto interno | Jd. Arco-Íris / Jd. Sandra | Central (Monte Serrat) | 384 |
| 351300905000797 | Cotia | Jd. Arco-Íris / Jd. Sandra | cor sob o ponto interno | Jd. Arco-Íris / Jd. Sandra | Central (Monte Serrat) | 103 |
| 351300905000820 | Cotia | Jd. Arco-Íris / Jd. Sandra | cor sob o ponto interno | Jd. Arco-Íris / Jd. Sandra | Jd. Arco-Íris / Jd. Sandra | 119 |
| 351300905000822 | Cotia | Jd. Arco-Íris / Jd. Sandra | miolo sem CRAS → vizinho | miolo | miolo | 119 |
| 351300905000823 | Cotia | Jd. Arco-Íris / Jd. Sandra | miolo sem CRAS → vizinho | miolo | miolo | 105 |
| 351300905000824 | Cotia | Jd. Arco-Íris / Jd. Sandra | cor sob o ponto interno | Jd. Arco-Íris / Jd. Sandra | Jd. Arco-Íris / Jd. Sandra | 322 |
| 351300905000832 | Cotia | Jd. Arco-Íris / Jd. Sandra | cor dominante do setor | miolo | Jd. Arco-Íris / Jd. Sandra | 54 |
| 351300905000865 | Cotia | Jd. Arco-Íris / Jd. Sandra | cor dominante do setor | miolo | Jd. Arco-Íris / Jd. Sandra | 127 |
| 351300905000523 | Cotia | Caputera | miolo sem CRAS → vizinho | miolo | miolo | 973 |
| 351300905000806 | Cotia | Caputera | miolo sem CRAS → vizinho | miolo | miolo | 129 |
| 351300905000809 | Cotia | Caputera | miolo sem CRAS → vizinho | miolo | miolo | 447 |
| 351300905000810 | Cotia | Caputera | miolo sem CRAS → vizinho | miolo | miolo | 629 |
| 351300905000848 | Cotia | Caputera | miolo sem CRAS → vizinho | miolo | miolo | 44 |
| 351300905000849 | Cotia | Caputera | cor dominante do setor | miolo | Caputera |  |
| 351300905000850 | Cotia | Caputera | cor sob o ponto interno | Caputera | Caputera | 279 |
| 351300905000851 | Cotia | Caputera | cor dominante do setor | miolo | Caputera | 232 |
| 351300905000863 | Cotia | Caputera | miolo sem CRAS → vizinho | miolo | miolo | 133 |
| 351300905000866 | Cotia | Caputera | miolo sem CRAS → vizinho | miolo | miolo | 128 |

## Listas de bairros do PMAS

O IBGE não tem bairros cadastrados para Cotia, então os setores não trazem nome de bairro para conferir contra as listas. A conferência por bairro é feita nos equipamentos (bairro do endereço × lista do território), no relatório `territorio-equipamentos.md`.

- Jd. Japão: 10 bairros na lista
- Caucaia do Alto: 104 bairros na lista
- Miguel Mirizola: 27 bairros na lista
- Central (Monte Serrat): 83 bairros na lista
- KM 21 / Granja Viana: 48 bairros na lista
- Jd. Arco-Íris / Jd. Sandra: 21 bairros na lista
- Caputera: 11 bairros na lista
