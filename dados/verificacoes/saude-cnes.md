# Verificação da saúde (CNES) — 2026-10-27

## 1. Lista esperada pelo plano (seção 3)

- OK — UBS: 26 (esperado 26)
- OK — `saude_urgencia`: UPA Atalaia Dra. Rita de Cássia Sorio (cnes-7522738)
- OK — `saude_urgencia`: Pronto Atendimento Parque São George (cnes-2746794)
- OK — `saude_urgencia`: Pronto Atendimento Caucaia do Alto (cnes-6212573)
- OK — `saude_urgencia`: PSI Pronto Socorro Infantil (cnes-4540891)
- OK — `saude_hospital`: Hospital Regional de Cotia (cnes-2792141)
- OK — `saude_mental`: CAPS Infantil (cnes-6983138)
- OK — `saude_mental`: CAPS II Cotia Adulto (cnes-5680328)
- OK — `saude_mental`: CAPS Álcool e Drogas Dr. João Olavo do Canto Neto (cnes-6981763)
- OK — `saude_especializada`: Policlínica Portão Antônio de Camargo (cnes-2746786)
- OK — `saude_especializada`: Clínica da Mulher (cnes-6768849)
- OK — `reabilitacao`: CEFOR I Centro de Fisioterapia e Ortopedia (cnes-2746344)
- OK — `reabilitacao`: CEFOR V Centro de Fisioterapia Caucaia do Alto (cnes-5992621)
- OK — `reabilitacao`: APAE Cotia (cnes-7323980)

Total: 39 equipamentos; 0 divergência(s) com o plano.

## 2. Comparação com o insumo do Guilherme

Insumo: `cnes-cotia-saude.csv` (39 linhas).

- Nenhuma diferença.

## 3. Coordenadas

- Fora do contorno de Cotia: 2
  - UBS Cachoeira
  - UBS Caputera
- Pares de unidades a menos de 30 m: 4
  - CEFOR V Centro de Fisioterapia Caucaia do Alto × UBS Caucaia do Alto: 21 m (endereços diferentes)
  - CEFOR V Centro de Fisioterapia Caucaia do Alto × Pronto Atendimento Caucaia do Alto: 22 m (endereços diferentes)
  - UBS Caucaia do Alto × Pronto Atendimento Caucaia do Alto: 20 m (mesmo endereço)
  - CAPS Infantil × CAPS Álcool e Drogas Dr. João Olavo do Canto Neto: 30 m (endereços diferentes)

### Distância até o OpenStreetMap (alerta acima de 1500 m)

O Nominatim é consultado pelo nome da unidade e pelo endereço. Para cada unidade vale a menor distância.
Endereço que o OSM só acha pela rua devolve um ponto qualquer da rua, então a distância é um indício, não prova.

| Unidade | Distância (m) | Achado por | O que o OSM achou |
|---|---:|---|---|
| APAE Cotia | 93 | endereço (road) | Rua Euricledes Formiga, Jardim Claúdio, Paisagem Renoir, Cotia, São Paulo, 06714 |
| CEFOR I Centro de Fisioterapia e Ortopedia | 901 | endereço (road) | Avenida Vasco Massafeli, Vila Santo Antônio do Portão, Jardim Rosalina, Cotia, S |
| CEFOR V Centro de Fisioterapia Caucaia do Alto | 37 | endereço (road) | Avenida Roque Celestino Pires, Jardim São Luiz, Centro, Caucaia do Alto, Cotia,  |
| UBS Arco Íris | 565 | endereço (road) | Estrada Velha da Olaria, Jardim Panorama, Jardim Arco Iris, Cotia, São Paulo, 06 |
| UBS Assa | 0 | endereço (office) | ASSA - Assistência Social Santo Antônio, 406, Rua Santo Antônio, Vila Santo Antô |
| UBS Atalaia Dr. Mário Aguiar Filho | 2 | endereço (road) | Rua Demétrio Calfat, Atalaia, Cotia, São Paulo, 06700-595 |
| UBS Cachoeira | 402 | endereço (road) | Estrada da Cachoeira, Caucaia do Alto, São Lourenço da Serra, São Paulo |
| UBS Caputera | 66 | endereço (road) | Estrada da Ressaca, Ressaca, Cotia, Itapecerica da Serra, São Paulo, 06724-100 |
| UBS Caucaia do Alto | 195 | endereço (road) | Avenida Roque Celestino Pires, Jardim São Luiz, Centro, Caucaia do Alto, Cotia,  |
| UBS Jardim Coimbra | 12 | endereço (road) | Rua Azulão, Vila Santo Antônio do Portão, Jardim Cotia, Cotia, São Paulo, 06703- |
| UBS Jardim Japão Alvaro Pedroso | — | não achado | — |
| UBS Jardim Petrópolis | 67 | nome (amenity) | Unidade Básica de Saúde Jardim Petrópolis, 401, Rua Ameixeiras, Jardim Panorama, |
| UBS Jardim Sandra | 6 | nome (amenity) | Unidade Básica de Saúde Jardim Sandra, 1927, Estrada dos Fischer's, Jardim São M |
| UBS Jardim São Miguel | 2 | endereço (road) | Rua Santa Adelaide, Jardim São Miguel Arcanjo, Bairro das Graças, Cotia, São Pau |
| UBS Jardim das Oliveiras Benedito Florêncio da Costa | 0 | endereço (amenity) | Unidade Básica de Saúde Benedito Florêncio da  Costa, 105, Rua Urupema, Jardim d |
| UBS Jardim do Engenho | 154 | endereço (road) | Rua das Doninhas, Jardim do Engenho, Cotia, São Paulo, 06711-280 |
| UBS Jd. São Vicente | 138 | endereço (road) | Estrada do Embu, Jardim Torino, Granja Viana, Cotia, São Paulo, 06713-100 |
| UBS Mendes | 14 | endereço (amenity) | Paróquia Nossa Senhora Imaculada Conceição, 105, Rua José Manoel de Oliveira, Ja |
| UBS Miguel Mirizola | 45 | endereço (road) | Rua Jorge Rizzo, Parque Miguel Mirizola, Cotia, São Paulo, 06704-220 |
| UBS Mirante da Mata | 8 | endereço (road) | Rua Francisco Alves, Parque Mirante da Mata, Cotia, São Paulo, 06719-690 |
| UBS Morro Grande | — | não achado | — |
| UBS Parque Alexandre | 139 | endereço (road) | Rua José de Andrade, Jardim Claúdio, Residence Park, Cotia, São Paulo, 06714-190 |
| UBS Parque São George | 3 | endereço (road) | Rua Karan, Jardim Torino, Parque São Jorge, Cotia, São Paulo, 06708-230 |
| UBS Parque Turiguara | 88 | nome (amenity) | Unidade Básica de Saúde Turiguara, 10, Rua Natal, Jardim Estela Mari, Parque Tur |
| UBS Portão | 0 | endereço (amenity) | Unidade de Pronto Atendimento Portão, 350, Avenida Vasco Massafeli, Vila Santo A |
| UBS Recanto Suave Francisco de Paula Silva | 0 | endereço (road) | Rua Mendes Pimentel, Jardim Lambreta, Jardim Rebelato, Cotia, São Paulo, 06710-5 |
| UBS Rio Cotia | 0 | nome (amenity) | Unidade Básica de Saúde Rio Cotia, 12, Rua Pedro Rodrigues, Rio Cotia, Jardim Be |
| UBS Santa Ângela | — | não achado | — |
| UBS Água Espraiada ⚠ | 3170 | endereço (road) | Estrada da Água Espraiada, Água Espraiada, Caucaia do Alto, Cotia, São Paulo, 06 |
| Clínica da Mulher | — | não achado | — |
| Policlínica Portão Antônio de Camargo | 12 | endereço (road) | Rua Vasco Massafeli, Parque Rincão, Cotia, São Paulo, 06705-490 |
| Hospital Regional de Cotia | 14 | nome (amenity) | Hospital de Regional Cotia, 171, Avenida Doutor Odair Pacheco Pedroso, Jardim No |
| CAPS II Cotia Adulto | 205 | endereço (amenity) | Centro de Atenção Psicossocial III Cotia Adulto, 96, Rua Topázio, Jardim Normura |
| CAPS Infantil | 29 | endereço (road) | Rua Topázio, Jardim Normura, Recanto dos Victors, Cotia, São Paulo, 06717-235 |
| CAPS Álcool e Drogas Dr. João Olavo do Canto Neto | 0 | endereço (road) | Rua Topázio, Jardim Normura, Recanto dos Victors, Cotia, São Paulo, 06717-235 |
| PSI Pronto Socorro Infantil | 225 | endereço (road) | Rua Engenheiro Leon Psanquevich, Jardim Dinorah, Vila Mont Serrat, Cotia, São Pa |
| Pronto Atendimento Caucaia do Alto | 193 | endereço (road) | Avenida Roque Celestino Pires, Jardim São Luiz, Centro, Caucaia do Alto, Cotia,  |
| Pronto Atendimento Parque São George | 147 | endereço (road) | Avenida Denne, Jardim Torino, Parque São Jorge, Cotia, São Paulo, 06708-230 |
| UPA Atalaia Dra. Rita de Cássia Sorio | 0 | endereço (amenity) | Unidade de Pronto Atendimento Atalaia, 326, Estrada do Morro Grande, Atalaia, Co |

Alertas: 1

- **UBS Água Espraiada** — CNES: -23.672713, -47.040391 (Estrada Água Espraiada, s/n, Água Espraiada). OSM: -23.646568, -47.052807 a 3170 m.
