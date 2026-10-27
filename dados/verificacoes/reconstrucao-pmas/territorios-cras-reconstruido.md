# Territórios de CRAS — Cotia (PMAS 2026–2029)

Arquivo reconstruído em 2026-10-19 a partir de fonte pública (ver `LEIAME.md`).

- **Fonte:** Plano Municipal de Assistência Social de Cotia 2026–2029, anexo da Resolução CMAS nº 298, de 14/05/2026 — https://cotia.sp.gov.br/wp-content/uploads/2026/06/298-resolucao-cmas-aprova-o-plano-municipal-de-assistencia-social-2026-a-2029-.pdf
- **Cópia local:** `dados/brutos/pmas-2026-2029_2026-10-19.pdf` (52 páginas; SHA-256 `f5f5f95b5d4470dad2c692982c7bf0f8c3636003ba8402a8c14adb708e982735`).
- **Data da coleta:** 2026-10-19.
- **Seção usada:** 3.6 Territorialização (p. 14 a 16 do PDF).
- **Páginas:** "p. N" é a página N do arquivo PDF. A numeração impressa no rodapé do plano é N − 1, porque a resolução do CMAS ocupa a p. 1.
- **Como foi extraído:** `scripts/extrair_insumos_pmas.py` imprime os blocos dos 7 territórios direto do texto do PDF. As listas de bairros abaixo são cópia literal: grafia, maiúsculas, abreviações e ordem do PDF, sem correção.
- Campo sem dado na fonte: em branco, com a nota "não consta no PMAS".

## Resumo

| # | Território | Unidade CRAS (como no PMAS) | Endereço (PMAS) | Telefone (PMAS) | Nº de bairros | Págs. |
|---|---|---|---|---|---|---|
| 1 | Jd. Japão | CRAS JD. JAPÃO | Rua Frézia, 60 – Jardim Japão | 4611-2538 | 10 | 14 |
| 2 | Caucaia do Alto | CRAS CAUCAIA DO ALTO | Rua Benedito Pires da Silva Sobrinho, 157 – Planalto | 4242-1788 | 104 | 14–15 |
| 3 | Miguel Mirizola | CRAS MIGUEL MIRIZOLA | Rua Vicente Strifezi, 131 – Parque Miguel Mirizola | 4148-2921 | 27 | 15 |
| 4 | Central (Monte Serrat) | CRAS CENTRAL MONTE SERRAT | Avenida Professor José Pedroso, 1565 – Jardim Nomura | 4703-6779 / 4614-0663 | 83 | 15 |
| 5 | KM 21 / Granja Viana (antigo Recanto Suave) | CRAS REGIÃO KM 21 — atendimento provisório na UBS Jardim Santa Ângela | UBS Jardim Santa Ângela — Rua Francisco Pereira, A. Filho, 1.511 - Jardim Santa Ângela | (não consta no PMAS) | 48 | 15–16 |
| 6 | Jd. Arco-Íris / Jd. Sandra | CRAS JARDIM ARCO-ÍRIS (Nova Unidade) | Avenida Marabás, 700 – Jardim Arco Íris | 4934-2921 | 21 | 16 |
| 7 | Caputera | CRAS CAPUTERA | Estrada do Caputera, 4.500 – Caputera | 4617-3828 | 11 | 16 |

São 304 entradas de bairro no total, com repetições entre territórios (ver "Divergências conhecidas").

## Nomes e cores: PMAS, mapa e referência do plano (seção 3a)

| # | Referência do plano | Texto do PMAS | Rótulo no mapa (p. 14) | Cor no texto do PMAS | Cor medida no PNG (aprox.) |
|---|---|---|---|---|---|
| 1 | Jd. Japão — roxo | "CRAS JD. JAPÃO (Cor Roxa)" (p. 14) | CRAS JD. JAPÃO | Roxa | `#933057` (roxo-vinho) |
| 2 | Caucaia do Alto — verde-claro | "CRAS CAUCAIA DO ALTO (Cor Verde Claro)" (p. 14) | CRAS CAUCAIA | Verde Claro | `#aed258` |
| 3 | Miguel Mirizola — amarelo/dourado | "CRAS MIGUEL MIRIZOLA (Cor Amarelo/Dourado)" (p. 15); "CRAS Mirizola" (p. 19) | ilegível na resolução da imagem; posição e cor batem com Mirizola | Amarelo/Dourado | `#d2bb28` |
| 4 | Central (Monte Serrat) — azul-claro | "CRAS CENTRAL MONTE SERRAT (Cor Azul Claro)" (p. 15); "CRAS Central – Monte Serrate" (p. 18) | CRAS MONTE SERRAT | Azul Claro | `#54c4cc` (ciano) |
| 5 | KM 21 / Granja Viana (antigo Recanto Suave) — azul-escuro | "CRAS REGIÃO KM 21 (Antigo Recanto Suave - Cor Azul Escuro)" (p. 15) | CRAS RECANTO SUAVE | Azul Escuro | `#517383` (azul-acinzentado) |
| 6 | Jd. Arco-Íris / Jd. Sandra — laranja | "CRAS JARDIM ARCO-ÍRIS (Nova Unidade - Cor Laranja/Mescla)" (p. 16) | CRAS JD. SANDRA | Laranja/Mescla | `#cd7c2d` |
| 7 | Caputera — verde-limão | "CRAS CAPUTERA (Cor Verde Limão)" (p. 16) | CRAS CAPUTERA | Verde Limão | `#d6df22` |

Nomes e cores do PDF batem com a referência do plano. Diferenças de nomenclatura, sem efeito na divisão:

- Território 5: o texto chama a unidade de "CRAS REGIÃO KM 21", e o mapa ainda rotula "CRAS RECANTO SUAVE".
- Território 6: o texto chama a unidade de "CRAS JARDIM ARCO-ÍRIS", o mapa rotula "CRAS JD. SANDRA" e a cor é descrita como "Laranja/Mescla".
- Fora dos 7 territórios, o mapa usa um verde mais pálido (`#d2e387`): é a área sem CRAS (o miolo do município). Ele é diferente do verde de Caucaia (`#aed258`).
- As cores medidas são a mediana de uma janela de pixels no PNG. São aproximadas, porque a imagem original é um JPEG com ruído.

## Territórios — detalhe

### 1. Jd. Japão

- **Nome no PMAS:** CRAS JD. JAPÃO (Cor Roxa) — p. 14
- **Unidade CRAS:** CRAS Jd. Japão
- **Endereço:** Rua Frézia, 60 – Jardim Japão — p. 14
- **Telefone:** 4611-2538 — p. 14
- **Bairros (10) — p. 14:**

- Aguassaí
- Chác. Atalaia
- Chác. Fugimoto
- Chác. Granja Recreio
- Chác. Pavoeiro (parte)
- Chácara Tropical
- Jd. Japão
- Recanto do Mel
- Recreio Do Butiá
- Remanso

### 2. Caucaia do Alto

- **Nome no PMAS:** CRAS CAUCAIA DO ALTO (Cor Verde Claro) — p. 14
- **Unidade CRAS:** CRAS Caucaia do Alto
- **Endereço:** Rua Benedito Pires da Silva Sobrinho, 157 – Planalto — p. 14
- **Telefone:** 4242-1788 — p. 14
- **Bairros (104) — p. 15:**

- Água Espraiada
- Altos De Caucaia
- Altos do Pereiras
- Apache
- Areião
- Avelino Pires De Oliveira
- Bairro Dos Nunes
- Bela Vista
- Bosque Dos Pereiras
- Bosque Dos Pires
- Brotas
- Cachoeira
- Campininha
- Cândido Pinto
- Centro (Caucaia)
- Chác. dos Amigos
- Chác. dos Coqueiros
- Chác. dos Sonhos
- Chácara Remanso
- Cia. dos Bichos
- Cipó
- Colina
- Colonial Village
- Comercial
- Correias
- Cruzeiro
- Da Capelinha
- Do Apache
- Do Tijuco Preto
- Dos Mendes
- Dos Neves
- Dos Pereiras
- Dos Pires
- Esmeralda Park
- Evaristo
- Fazenda Ajapi
- Graças
- Granja Hotsu
- Grilos
- Jd. Agreste
- Jd. Ana Cristina
- Jd. Arabutan
- Jd. Camargo
- Jd. Cláudia
- Jd. d'Abril
- Jd. das Antilhas
- Jd. das Oliveiras
- Jd. dos Palmares
- Jd. dos Pereiras
- Jd. Gilda Maria
- Jd. Ipê
- Jd. Maísa
- Jd. Monte Verde
- Jd. Nara Lúcia
- Jd. Paulistano
- Jd. Planalto
- Jd. Primavera
- Jd. Rosa Azul
- Jd. San Ressore
- Jd. Santa Paula
- Jd. Sítio Branco
- Jd. Sítio Verde
- Jd. Suíço
- Jd. Vista Alegre
- Los Álamos
- Morro Preto
- Mulatas
- Nhambuca
- Parque Do Agreste
- Parque Doutor Mendonça Cortez
- Parque Vicente Celestino
- Pastoreiro
- Pinheiro Tênis Village
- Planalto De Caucaia
- Portal Do Areião
- Portal Do Quilombo
- Portal Santa Paula
- Pq. Caucaia
- Pq. Realeza
- Projeto Jardim
- Pununduva
- Quinta de Caucaia
- Recanto Paraíso
- Recanto Topázio
- Res. Araucária
- Res. Vila Real
- Residencial Caucaia
- Residencial Pastoreiro
- San Resore
- Santana
- São Benedito
- Sebastião Nunes
- Sítio Evaristo
- Sítio São Francisco
- Terras De San Felipe
- Tijuco Preto
- Vila Alcina
- Vila de Fátima
- Vila Dos Palmares
- Vila Paraíso
- Vila Santa Catarina
- Vila Santa Clara
- Vila São Benedito
- Vila São Roque

### 3. Miguel Mirizola

- **Nome no PMAS:** CRAS MIGUEL MIRIZOLA (Cor Amarelo/Dourado) — p. 15
- **Unidade CRAS:** CRAS Miguel Mirizola
- **Endereço:** Rua Vicente Strifezi, 131 – Parque Miguel Mirizola — p. 15
- **Telefone:** 4148-2921 — p. 15
- **Bairros (27) — p. 15:**

- Bairro das Pitas
- Chácara Novo Horizonte
- Chácara Roselândia
- Chácara Vista Alegre
- Colinas São Fernando
- Condomínio dos Palmares
- Granja Caiapiá
- Granja Carneiro Viana
- Haras Terra Branca
- Jd. Coimbra
- Jd. Dinorah
- Jd. Estela Maris
- Jd. Nara Lúcia
- Jd. Nova Vida
- Jd. Rosemary
- Lajeado
- Morada do Rei
- Parque das Rosas
- Portal Roselândia
- Pq. Miguel Mirizola
- Pq. Monjolo
- Pq. Rizzo
- Pq. Turiguara
- Recanto Vista Alegre
- Residencial Palma de Maiorca
- San Fernando Park
- Vila Clara

### 4. Central (Monte Serrat)

- **Nome no PMAS:** CRAS CENTRAL MONTE SERRAT (Cor Azul Claro) — p. 15
- **Unidade CRAS:** CRAS Central Monte Serrat
- **Endereço:** Avenida Professor José Pedroso, 1565 – Jardim Nomura — p. 15. Ver "Inconsistências internas do PMAS" sobre o nome da avenida.
- **Telefone:** 4703-6779 / 4614-0663 — p. 15
- **Bairros (83) — p. 15:**

- Altos de Cotia
- Bairro Das Pedras
- Bairro Novo
- Centro (Cotia)
- Chácara N. Senhora De Fátima
- Chácara Recanto Verde
- Chácara Santa Maria
- Chácara São Luiz
- Colinas De Cotia
- Cotia Park
- Granja Carolina
- Granja Clotilde
- Honória
- Jardim Barro Branco
- Jardim Caiapiá
- Jardim Honória
- Jardim São Pedro
- Jd. Acoty
- Jd. Atalaia
- Jd. Belizário
- Jd. Cláudio
- Jd. Do Rio Cotia
- Jd. Pioneira
- Jd. Sabiá
- Jd. Vale Verde
- Jd. Adelina
- Jd. Carmel
- Jd. Central
- Jd. Cotia
- Jd. Dos Ipês
- Jd. Eliane
- Jd. Elias
- Jd. Empírio
- Jd. Isis
- Jd. Leonor
- Jd. Lina
- Jd. Maranhão
- Jd. Maria Tereza
- Jd. Miranda
- Jd. Monte Santo
- Jd. Nomura
- Jd. Nova Coimbra
- Jd. Rio Das Pedras
- Jd. Rosalina
- Morada Santa Fé
- Morro Do Céu
- Morro Grande
- Nakamura Park
- Outeiro De Passárgada
- Paisagem Casa Grande
- Paisagem Van Gogh
- Parque Paulistano
- Parque Rincão I e II
- Parque São Vitor
- Portal Primavera
- Portão
- Pq. Bahia
- Pq. Dom Henrique
- Pq. Isaac Pires
- Pq. Mirante Da Mata
- Pq. Monjolo
- Pq. Santa Rita De Cássia
- Quinta Dos Angicos
- Recanto Dos Victors
- Recanto Maria Tereza
- Recanto Suíço
- Recanto Verde
- Residencial Palma Da Mata
- Residencial Recanto Verde
- Santa Cristina
- Sítio Boa Vista
- Sítio Mandu
- Taboleiro Verde
- Vila Dos Pobres
- Vila Jovina
- Vila Maria
- Vila Monte Serrat
- Vila Nova
- Vila Olaria
- Vila Santa Terezinha
- Vila Santo Antônio Do Portão
- Vila São Francisco
- Vila São Joaquim

### 5. KM 21 / Granja Viana (antigo Recanto Suave)

- **Nome no PMAS:** CRAS REGIÃO KM 21 (Antigo Recanto Suave - Cor Azul Escuro) — p. 15
- **Unidade CRAS:** CRAS Região KM 21, em atendimento provisório numa sala da UBS Jardim Santa Ângela. O CRAS Recanto Suave encerrou as atividades em 2022, e o atendimento foi retomado em 2025 nesse espaço cedido pela Saúde (p. 17). O PMAS tem como metas um CRAS no Instituto Federal (KM 21) e um CRAS Granja Viana em unidade definitiva (p. 36).
- **Endereço:** "UBS Jardim Santa Ângela" / "Rua Francisco Pereira, A. Filho, 1.511 - Jardim Santa Ângela" (duas linhas no PDF) — p. 15
- **Telefone:** (em branco — não consta no PMAS)
- **Bairros (48) — p. 15 e 16:**

- Algarve
- Bosque Do Viana
- Chácara Canta Galo
- Chácara Do Refúgio
- Chácara Dos Lagos
- Chácara Eliana
- Chácara Granja Velha
- Chácara Pavoeiro
- Chácara Recanto
- Chácara São Carlos
- Chácara Terra Nobre
- Gramado
- Granja Poty
- Granja Viana (I e II)
- Horizontal Park
- Jardim Tomé
- Jd. Barbacena
- Jd. Capuava
- Jd. Circular
- Jd. Colibri (I e II)
- Jd. Da Glória
- Jd. Do Engenho
- Jd. Fontana
- Jd. Guerreiro
- Jd. Lambreta
- Jd. Mediterrânio
- Jd. Passárgada
- Jd. Rebelato
- Jd. Recanto Suave
- Jd. Santa Ângela
- Jd. Santa Isabel
- Jd. Santa Maria
- Jd. São Vicente
- Jd. Semiramis
- Jd. Terra Nobre
- Jd. Torino
- Moinho Velho
- Paisagem Renoir
- Palos Verde
- Pinus Park
- Pq. Alexandre
- Pq. Frondoso
- Pq. Rincão
- Pq. São George
- San Diego Park
- Santana
- Vila Boa Vista
- Vila Santo Antônio

### 6. Jd. Arco-Íris / Jd. Sandra

- **Nome no PMAS:** CRAS JARDIM ARCO-ÍRIS (Nova Unidade - Cor Laranja/Mescla) — p. 16
- **Unidade CRAS:** CRAS Jardim Arco-Íris
- **Endereço:** Avenida Marabás, 700 – Jardim Arco Íris — p. 16
- **Telefone:** 4934-2921 — p. 16
- **Bairros (21) — p. 16:**

- Centreville
- Condomínio das Graças
- Furquim
- Jardim Vila Maria
- Jd das Graças
- Jd. Arco Íris
- Jd. Araruama
- Jd. Arco Verde
- Jd. das Cruzadas
- Jd. Museu
- Jd. Nossa Senhora das Graças
- Jd. Nova Cotia
- Jd. Panorama
- Jd. Petrópolis
- Jd. Sandra
- Jd. Santana
- Jd. São Miguel
- Jd. Lavapés das Graças
- Recanto Arco Verde
- Recanto da Mata
- Vila Nova São Miguel

### 7. Caputera

- **Nome no PMAS:** CRAS CAPUTERA (Cor Verde Limão) — p. 16
- **Unidade CRAS:** CRAS Caputera
- **Endereço:** Estrada do Caputera, 4.500 – Caputera — p. 16
- **Telefone:** 4617-3828 — p. 16
- **Bairros (11) — p. 16:**

- Caputera
- Chác. Lagos (parte)
- Jd. Colinas
- Jd. São Luiz
- Pq. das Nascentes
- Res. Recanto Verde
- Jd. Rosa Branca
- Jd. Das Cerejeiras
- Parque Dos Manacás
- Ressaca
- Samambaia

## Dados por território que constam no PMAS

### Pessoas inscritas no CadÚnico, por território de CRAS e faixa etária — p. 33

A tabela é uma imagem no PDF, transcrita à mão e conferida linha a linha. A fonte citada é a Vigilância Socioassistencial. A data de referência dos dados não consta no PMAS. A p. 32 anuncia "o total de famílias cadastradas", mas a tabela traz **pessoas**: o número de famílias por território não consta no PMAS.

| Idade | Caputera | Caucaia do Alto | Mirizola | Central | Recanto Suave | Jardim Arco Iris | Jardim Japão | Total geral |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 0 a 4 | 277 | 1293 | 1262 | 1854 | 896 | 1446 | 45 | 7073 |
| 5 a 6 | 164 | 768 | 663 | 982 | 484 | 753 | 22 | 3836 |
| 7 a 15 | 727 | 3192 | 2632 | 3892 | 2062 | 3350 | 129 | 15984 |
| 16 a 17 | 134 | 568 | 463 | 758 | 422 | 664 | 26 | 3035 |
| 18 a 24 | 289 | 1267 | 1095 | 1740 | 892 | 1442 | 53 | 6778 |
| 25 a 34 | 376 | 1888 | 1713 | 2511 | 1290 | 1898 | 59 | 9735 |
| 35 a 39 | 1985 | 1011 | 832 | 1299 | 657 | 1000 | 44 | 5038 |
| 40 a 44 | 221 | 995 | 778 | 1251 | 647 | 991 | 62 | 4945 |
| 45 a 49 | 165 | 825 | 598 | 1062 | 623 | 788 | 45 | 4106 |
| 50 a 54 | 149 | 691 | 485 | 887 | 501 | 609 | 19 | 3341 |
| 55 a 59 | 151 | 611 | 436 | 858 | 454 | 527 | 33 | 3070 |
| 60 a 64 | 150 | 596 | 426 | 946 | 550 | 531 | 29 | 3228 |
| 65 + | 283 | 1731 | 939 | 2353 | 1645 | 1210 | 99 | 8260 |
| **Total de pessoas inscritas** | **5071** | **15436** | **12322** | **20393** | **11123** | **15209** | **665** | **78429** |

Conferência das somas:

- Todas as colunas somam o total da própria coluna.
- Todas as linhas somam o "Total geral", menos a de 35 a 39 anos. Nessa linha os territórios somam 6828, e o total geral diz 5038, uma diferença de 1790.
- A causa provável é a célula Caputera/35 a 39 (1985): com 195, a linha fecharia. O total da coluna Caputera (5071) já inclui 1985. Por isso a soma dos 7 totais por território dá 80219, e não 78429. Os valores foram transcritos como estão.
- Jardim Japão tem só 665 inscritos, muito abaixo dos demais territórios. O valor foi transcrito como está.

### Vagas do SCFV de 6 a 15 anos por território — p. 18

O PMAS informa "480 vagas de 6 a 15 anos" na última distribuição por chamamento público:

| Território (como no PMAS) | Vagas |
|---|---:|
| Caucaia | 110 |
| Arco Iris | 130 |
| Monte Serrat | 40 |
| Recanto Suave | 70 |
| Jardim Japão | 50 |
| Miguel Mirizola | 40 |
| Caputera | (não consta no PMAS) |

As parcelas somam 440, e não 480. A diferença de 40 vagas não é explicada no PMAS. As demais vagas (80 de 15 a 17 anos, 30 de 18 a 59, 240 de idosos e 280 do SINPcD) são de âmbito municipal, sem divisão por território (p. 18).

### Serviços referenciados a cada CRAS — p. 18 a 21

Contagem das organizações listadas nas tabelas das seções 4.1 a 4.7. Os nomes e endereços das organizações não foram transcritos aqui.

| CRAS (seção do PMAS) | Organizações referenciadas | Observação |
|---|---:|---|
| Central – Monte Serrat (4.1, p. 18) | 3 | convivência para crianças de 6 a 15, crianças e adolescentes de 6 a 14 e idosos |
| Mirizola (4.2, p. 19) | 0 | "dispõe de serviços realizados na unidade" |
| Jardim Arco-íris (4.3, p. 19) | 1 | convivência para crianças de 6 a 15 |
| Caucaia do Alto (4.4, p. 19) | 3 | convivência para crianças de 6 a 15 e para 15 a 17 |
| Jardim Japão (4.5, p. 20) | 0 no território | crianças e adolescentes atendidos por organização em Caucaia, com transporte |
| Caputera (4.6, p. 20) | 0 no território | crianças e adolescentes atendidos por casa de apoio na Granja Viana, com transporte |
| Região KM 21 (4.7, p. 20–21) | 9 | 6 de convivência ou profissionalizante e 3 do SINPcD (pessoas com deficiência) |

### População por território

Não consta no PMAS. O plano traz só totais do município: 274.413 habitantes no Censo 2022 (p. 10) e um gráfico por faixa etária de 2000, 2010 e 2022 para o município inteiro (p. 11).

## Outros equipamentos citados no PMAS (úteis na fase 2b)

- **CREAS Central:** Avenida Professor Manoel José Pedroso, 1565 – Jardim Nomura; tel. 4614-5622 (p. 22).
- **Unidade Avançada CREAS:** Rua Benedito Pires da Silva Sobrinho, 157 – Jardim Planalto (p. 23); telefone: não consta no PMAS. É o mesmo endereço do CRAS Caucaia do Alto.
- **Acolhimento institucional de crianças e adolescentes (SAICA):** 2 unidades (p. 25). Vagas: não consta no PMAS. O PMAS publica os endereços, que foram **omitidos aqui de propósito** por regra do projeto. A Carta de Serviços (item 3.2) diz "02 unidades", "totalizando 60 vagas", e que os endereços são sigilosos.

## Divergências conhecidas

Fontes comparadas:

- **PMAS 2026–2029:** aprovado em 14/05/2026 e publicado em 06/2026. URL: https://cotia.sp.gov.br/wp-content/uploads/2026/06/298-resolucao-cmas-aprova-o-plano-municipal-de-assistencia-social-2026-a-2029-.pdf
- **Carta de Serviços ao Usuário:** página modificada em 2025-08-27, segundo o metadado `dateModified` do HTML, consultada em 2026-10-19. URL: https://cotia.sp.gov.br/carta-de-servico-ao-usuario/ (seção Proteção Social Básica → PAIF → "Unidades de atendimento do PAIF, execução direta"; o mesmo bloco se repete em SCFV, Bolsa Família, BPC e Cadastro Único).

**Regra:** vale o PMAS, que é a fonte oficial mais recente.

### Endereços dos CRAS: PMAS × Carta de Serviços

Os 3 CRAS com endereço diferente:

| CRAS | Endereço no PMAS (vale) | Endereço na Carta | Telefone PMAS × Carta |
|---|---|---|---|
| 4. Central Monte Serrat | Avenida Professor José Pedroso, 1565 – Jardim Nomura (p. 15) | "CRAS MONTE SERRAT" — Rua Professor José Barreto, 355 – Centro | 4703-6779 / 4614-0663 nas duas |
| 3. Miguel Mirizola | Rua Vicente Strifezi, 131 – Parque Miguel Mirizola (p. 15) | "CRAS MIRIZOLA" — Rua Jorge Rizzo, 266 – Pq Miguel Mirizola | 4148-2921 × 4148-3472 (diferente) |
| 5. Região KM 21 (antigo Recanto Suave) | UBS Jardim Santa Ângela — Rua Francisco Pereira, A. Filho, 1.511 - Jardim Santa Ângela (p. 15) | "CRAS RECANTO SUAVE" — Rua Monet, 584- Horizontal Park – Recanto Suave | não consta no PMAS × 4777-0093 |

Os outros quatro:

- **1. Jd. Japão:** mesmo endereço e telefone. A Carta escreve "Rua Frezia, 60 – Jd Japão", sem acento.
- **2. Caucaia do Alto:** mesmo endereço e telefone.
- **7. Caputera:** mesmo endereço e telefone. A Carta chama a unidade de "UNIDADE AVANÇADA CAPUTERA", e não de CRAS.
- **6. Jardim Arco-Íris:** não aparece na Carta. O PMAS a chama de "Nova Unidade".

### CREAS: PMAS × Carta de Serviços

Fora dos 7 CRAS, mas afeta a fase 2b do plano:

| Unidade | PMAS | Carta |
|---|---|---|
| CREAS Central / CREAS Cotia | Avenida Professor Manoel José Pedroso, 1565 – Jardim Nomura; tel. 4614-5622 (p. 22) | Rua Água Marinha, 39- Jd Nomura – Cotia; tel. 4614-5622 |
| Unidade Avançada do CREAS | Rua Benedito Pires da Silva Sobrinho, 157 – Jardim Planalto (p. 23) | Rua Benedito Pires da Silva Sobrinho, 157- Jd Planalto – Caucaia do Alto (igual) |

O plano (fase 2b) usa o endereço da Carta para o CREAS Cotia. Pela regra "vale a mais recente", o endereço do PMAS teria precedência. Fica para decisão do João.

### Inconsistências internas do PMAS

- **Nome da avenida do CRAS Central:** "Avenida Professor José Pedroso, 1565" (p. 15). Para o CREAS Central, no mesmo número, o PMAS escreve "Avenida Professor Manoel José Pedroso, 1565" (p. 22). Provavelmente falta "Manoel" na linha do CRAS. Transcrito como está.
- **Endereço do CRAS KM 21:** "Rua Francisco Pereira, A. Filho, 1.511" tem vírgula e abreviação estranhas. O nome completo da rua não consta no PMAS. Transcrito como está.
- **Grafia do nome:** "Monte Serrat" (p. 15) e "Monte Serrate" (p. 18).
- **Número de territórios:** a seção 3.2 (p. 10) diz que o município é "administrativamente dividido em seis territórios", mas lista quatro itens: Caucaia do Alto; Granja Viana; Caputera; "Central, Jardim Panorama e Parque Miguel Mirizola". A p. 13 repete "seis territórios". Isso não bate com os 7 territórios de CRAS da seção 3.6.
- **População de Cotia:** 274.413 (p. 10) e 274.443 (p. 11).
- **Contagem de CRAS:** a p. 17 fala em "7 (sete) Centros de Referência de Assistência Social – CRAS, considerando emergencialmente 1(um) Atendimento Provisório no território da Granja Viana".
- **Tabela do CadÚnico:** linha de 35 a 39 anos não fecha (ver acima).

### Bairros que aparecem em mais de um território

Mesmo nome exato:

| Bairro | Territórios |
|---|---|
| Jd. Nara Lúcia | 2 Caucaia do Alto e 3 Miguel Mirizola |
| Pq. Monjolo | 3 Miguel Mirizola e 4 Central |
| Santana | 2 Caucaia do Alto e 5 KM 21 (e "Jd. Santana" no 6 Arco-Íris) |

Divididos de forma explícita pelo PDF, com "(parte)":

- **Pavoeiro:** "Chác. Pavoeiro (parte)" no 1 Jd. Japão e "Chácara Pavoeiro" no 5 KM 21.
- **Lagos:** "Chác. Lagos (parte)" no 7 Caputera e "Chácara Dos Lagos" no 5 KM 21. Provavelmente é o mesmo loteamento.

Nomes parecidos em territórios diferentes, que podem ser o mesmo lugar e devem ser checados na fase 3:

- **Remanso:** "Remanso" (1) e "Chácara Remanso" (2).
- **Rincão:** "Parque Rincão I e II" (4) e "Pq. Rincão" (5).
- **Recanto Verde:** "Recanto Verde", "Chácara Recanto Verde" e "Residencial Recanto Verde" (4); "Res. Recanto Verde" (7).
- **Vila Maria:** "Vila Maria" (4) e "Jardim Vila Maria" (6).
- **Atalaia:** "Chác. Atalaia" (1) e "Jd. Atalaia" (4).
- **Caiapiá:** "Granja Caiapiá" (3) e "Jardim Caiapiá" (4).
- **Passárgada:** "Jd. Passárgada" (5) e "Outeiro De Passárgada" (4).
- **Vista Alegre:** "Jd. Vista Alegre" (2); "Chácara Vista Alegre" e "Recanto Vista Alegre" (3).
- **Graças:** "Graças" (2); "Condomínio das Graças", "Jd das Graças", "Jd. Nossa Senhora das Graças" e "Jd. Lavapés das Graças" (6).

Outros pontos sobre os bairros:

- **Morro Grande** está na lista do território 4 (Central). Na fase 3a, o plano trata o Morro Grande como área de reserva sem CRAS (o miolo verde-claro do mapa).
- **Possíveis duplicatas dentro do mesmo território** (cada grafia conta como uma entrada separada no total de bairros):
  - 2: "Jd. San Ressore" e "San Resore"; "Apache" e "Do Apache"; "Tijuco Preto" e "Do Tijuco Preto"; "Evaristo" e "Sítio Evaristo"; "São Benedito" e "Vila São Benedito"; "Pastoreiro" e "Residencial Pastoreiro"; "Dos Pereiras" e "Jd. dos Pereiras".
  - 4: "Honória" e "Jardim Honória".
  - 6: "Jd das Graças" e "Jd. Nossa Senhora das Graças".
- **Nomes duvidosos ou difíceis de localizar:**
  - Grafias incomuns: "Jd. Mediterrânio" (5; provável "Mediterrâneo"), "Jd. Empírio" (4) e "Palos Verde" (5).
  - Fragmentos sem tipo de logradouro no território 2: "Comercial", "Colina", "Cruzeiro", "Da Capelinha", "Dos Mendes", "Dos Neves", "Dos Pires", "Graças" e "Mulatas".
  - "Santana", sem qualificador, em dois territórios.

## Notas sobre o mapa (`mapa-territorios-cras-pmas-2026.png`)

- O mapa é uma imagem embutida na p. 14 (JPEG de 620 × 526 px). O PNG é a imagem original extraída, sem reamostragem. Renderizar a 250 dpi só ampliaria os pixels: a imagem ocupa cerca de 110 dpi efetivos na página.
- No PDF, a imagem aparece esticada na horizontal: proporção 1,266 contra 1,179 da original. O PNG mantém a proporção original.
- **Sem legenda.** Os 7 territórios são identificados por rótulos brancos ("CRAS …") e pela cor. Os nomes de bairro escritos dentro de cada mancha estão ilegíveis nesta resolução. O rótulo da mancha dourada (Mirizola) também está ilegível.
- O logotipo da Prefeitura e da Secretaria de Desenvolvimento Social está dentro da própria imagem, no canto inferior direito. Não foi recortado, porque um recorte retangular cortaria o mapa.
- **Caucaia (verde):** além do corpo principal, tem uma faixa estreita que sobe pela divisa oeste até encostar no Monte Serrat, a oeste do Jd. Sandra. A faixa está ligada ao corpo principal.
- **Fundo verde-pálido** (`#d2e387`, área sem CRAS): ocupa o miolo e também aparece como franjas finas entre territórios.
- Há pixels laranja/vermelhos espalhados na divisa sudoeste, no extremo sul de Caucaia. Parecem artefato de desenho e não correspondem a nenhum território.
- A capa do PMAS (p. 2) traz outro mapa: um coroplético por setores, sem legenda. Ele não é o mapa dos territórios de CRAS e não foi usado.
- Não foi encontrada versão de maior resolução na biblioteca de mídia do site da prefeitura. A busca na API WordPress por "cras", "mapa cras" e "territorializacao" não achou.
