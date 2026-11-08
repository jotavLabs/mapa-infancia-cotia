# Escolha do índice: oferta de equipamentos para crianças nos territórios de Cotia

Versão de 07/11/2026. Decisão do Guilherme na seção 8. Este documento não traz resultado nem posição de território.

## 1. Resposta curta

**Nenhum índice existente pode ser aplicado ou adaptado com a nossa base.** Os candidatos brasileiros medem principalmente resultado de saúde e condição social (mortalidade, pré-natal, renda, violência). A nossa base mede onde estão os equipamentos públicos e quantas crianças moram em cada território. O candidato brasileiro com maior cobertura chega a 20% dos componentes, e o componente coberto é aproximado.

**Recomendação: opção C, um indicador composto próprio, sem inventar método.** Cada peça vem de uma fonte existente:

| Peça | De onde vem |
|---|---|
| Ordenação por postos, com sentido definido e leitura relativa | INVUPRIN, Prefeitura de São Paulo, 2025 |
| Definição das matrículas por crianças e peso analítico | IMAPI, Buccini et al., 2021/22 |
| UBS por população | Mapa da Desigualdade da Primeira Infância, Rede Nossa São Paulo |
| Raio de 1,5 km | Seção 9 do plano do mapa; o Mapa da Desigualdade usa o mesmo raio para escola e casa |
| Construção e teste de sensibilidade | Handbook OCDE/JRC, 2008 |

**Nome recomendado: Índice de Oferta e Acesso a Equipamentos para a Infância.**
O nome pedido era "Índice de Qualidade de Saúde Infantil no Bairro". Ele afirmaria três coisas que a base não sustenta:
- **Qualidade:** a base não mede equipe, horário nem fila.
- **Saúde:** a base não tem nenhum resultado de saúde, como mortalidade ou vacinação.
- **Bairro:** Cotia não tem limites oficiais de bairro. A unidade é o território de CRAS.

## 2. Tabela de aderência

A cobertura conta os componentes que a base atual consegue reproduzir. "Aproximado" significa que o conceito existe, mas a medida difere da original.

| Candidato | Quem, ano | Escala | Ainda é calculado? | Agregação | Cobertura por componentes | Cobertura por pesos |
|---|---|---|---|---|---|---|
| **IDI** | UNICEF; edições com dados de 1999 e 2004 | município e região | Sem edição recente localizada | Uma nota do IPECE descreve média ponderada; escala de 0 a 1. Pesos não obtidos | 1 de 5 (20%), aproximado | Não apurada |
| **IMAPI** | Buccini et al., 2021/22 | município | Dados de 2015–2019; atualização não confirmada | Padronização e pesos analíticos; escore de 0 a 100; fórmula no Apêndice S3, não lido | 2 de 31 (6,5%), ambos aproximados | 6,6% (7,76 de 118,35) |
| **INVUPRIN** | Prefeitura de SP, 2025 | distrito | Sim, ciclo 2025–2028 | Postos por indicador × peso por defasagem do dado; escala de 0 a 1 | 1 de 11 (9,1%), aproximado | 10,3% (1 de 9,75) |
| **Mapa da Desigualdade da Primeira Infância** | Rede Nossa São Paulo; 2017, 2020, 2026 | distrito | Sim | Comparação por indicador. Há ranking geral em 2026, com método não localizado | 1 de 26 com juízo de valor (3,8%): UBS por 10 mil habitantes | Sem pesos publicados |
| **INC** | FMCSV/Quantis, 2019; edição 2024 | estados e capitais | Sim | Soma de 4 grupos prioritários, em % das crianças de 0–3 | 0 de 4 | 0% |
| **IPVS 2022** | Fundação Seade, 2026 | setor censitário | Sim | Análise fatorial e agrupamento em grupos | 1 de 5 (20%), aproximado: crianças de 0–5 | Pesos não obtidos |
| **IPPI** | Fundação Seade | não confirmada | Não confirmado | Não localizada | Não apurada | Não apurada |
| **IDSUS** | Ministério da Saúde, 2012 | município | Medição interrompida, segundo uma fonte | Componentes principais e agrupamento k-means | Não apurada (24 indicadores) | Não apurada |
| **Child Opportunity Index 3.0** | Brandeis, 2024 | setor (EUA) | Sim | Pesos por poder preditivo de mobilidade e saúde adulta | Não apurada (44 indicadores); documento bloqueado | Não apurada |
| **2SFCA** | Luo e Wang, 2003 | flexível | É método, não índice | Razão oferta/demanda dentro de um raio | Calculável | Não se aplica |

### Componentes por candidato

O campo citado é o que a base tem. "Não" significa que o dado não existe na base.

**IDI (5 componentes)**
| Componente | Temos? | Campo |
|---|---|---|
| Crianças até 6 anos com mãe com menos de 4 anos de estudo | Não | |
| Crianças até 6 anos com pai com menos de 4 anos de estudo | Não | |
| Cobertura vacinal em menores de 1 ano | Não | |
| Mães com mais de seis consultas de pré-natal | Não | |
| Crianças matriculadas na pré-escola | Aproximado | `_mat_pre`, só rede pública |

**IMAPI (31 indicadores; 30 no escore geral)**
| Componente | Temos? | Campo |
|---|---|---|
| Cobertura de creche e pré-escola | Aproximado | `_mat_creche`, `_mat_pre`, `pop_0_4`; só rede pública |
| Cobertura de atenção primária | Aproximado | `n_saude_atencao_basica`; o IMAPI conta equipes, nós contamos UBS |
| Os outros 29, como pré-natal, mortalidade, vacinação, alunos por profissional, recursos da escola, Bolsa Família e violência | Não | |

**INVUPRIN (11 indicadores)**
| Componente | Peso | Temos? | Campo |
|---|---|---:|---|
| Taxa de universalização da educação infantil (creche) | 1 | Aproximado | `_mat_creche`; o original inclui rede particular |
| Famílias com crianças no Bolsa Família; mortalidade infantil; pré-natal; mães adolescentes; baixo peso; mortalidade materna; idade média ao morrer; violência no SINAN | 1 cada | Não | |
| Domicílios em favelas | 0,5 | Não | |
| População em situação de rua | 0,25 | Não | |

**Mapa da Desigualdade, edição 2020 (28 indicadores, 2 só de contexto)**
| Componente | Temos? | Campo |
|---|---|---|
| Unidades Básicas de Saúde ÷ população total × 10.000 | Sim | `n_saude_atencao_basica`, `pop_total` |
| População total (contexto) | Sim | `pop_total` |
| População de 0–6 anos (contexto) | Aproximado | faixas do Censo não fecham em 6 anos |
| Creche: demanda atendida, tempo de espera, alunos por turma; pré-escola: alunos por turma | Não | exigem fila e turmas |
| Os demais, de saúde, urbanos e de violência | Não | |

**INC (4 componentes):** pobreza, monoparentalidade, mães ou cuidadores economicamente ativos e deficiência, todos para crianças de 0–3. Nenhum está na base. A nossa matrícula só serviria para comparar com a necessidade, que precisaria ser obtida fora.

**IPVS 2022 (5 variáveis visíveis no informe da Prefeitura de SP):** renda média do responsável, alfabetização, mulheres responsáveis de 15–29 anos, responsáveis de 15–29 anos e crianças de 0–5. Só a última existe, de forma aproximada.

## 3. Por que A e B não servem

- **A. Aplicar na íntegra:** impossível. Nenhum candidato tem seus componentes completos na base.
- **B. Adaptar:** um cálculo com 20% de um índice ou menos não mede o mesmo que ele. Usar o nome seria enganoso, e a restrição do projeto já proíbe isso.
- **C. Composto próprio:** é o único caminho que descreve corretamente o que a base mede.

## 4. Indicadores propostos

Oito indicadores em três dimensões, que seguem o recorte do mapa: escola, SUS e SUAS com proteção. Todos usam só dados já existentes no repositório.

| # | Indicador | Fórmula | Denominador | Por que entra |
|---|---|---|---|---|
| **Educação infantil** | | | | |
| E1 | Matrículas em creche | `_mat_creche` ÷ `pop_0_4` × 100 | crianças de 0–4 | Definição próxima à do IMAPI; separa o caso de território sem creche pública |
| E2 | Matrículas em pré-escola | `_mat_pre` ÷ `pop_0_4` × 100 | crianças de 0–4 | Idem. Leitura relativa, porque a pré-escola atende 4–5 anos |
| **Saúde** | | | | |
| S1 | UBS por crianças | `n_saude_atencao_basica` ÷ crianças de 0–14 × 10.000 | crianças de 0–14 | Fórmula do Mapa da Desigualdade, com o denominador já usado no site |
| S2 | Crianças perto de uma UBS | crianças em setores a até 1,5 km da UBS mais próxima ÷ crianças de 0–14 × 100 | crianças de 0–14 | Corrige a distorção dos territórios pequenos e extensos; está na seção 9 do plano |
| S3 | Distância à urgência | distância média ponderada por crianças até o ponto mais próximo de urgência ou o hospital | crianças de 0–14 | Unidades servem a mais de um território; a contagem local distorce |
| S4 | Distância ao CAPS Infantil | distância média ponderada por crianças até o único CAPSi | crianças de 0–14 | Serviço municipal único; saúde mental é eixo da pesquisa de saúde infantil |
| **Assistência e proteção** | | | | |
| A1 | Distância ao CRAS | distância média ponderada por crianças até o CRAS mais próximo | crianças de 0–14 | Substitui "crianças por CRAS", que só repete a população |
| A2 | Distância ao Conselho Tutelar | distância média ponderada por crianças até o Conselho mais próximo | crianças de 0–14 | Os dois Conselhos atendem a cidade |

**Como calcular:**
- **Crianças de 0–14:** soma de `V01031`, `V01032` e `V01033`, por setor, em `dados/verificacoes/setores-territorio.csv`. Setor em sigilo fica como ausente, nunca zero.
- **Distância:** do ponto interno do setor até o equipamento, em linha reta, com `distancia_m` de `scripts/comum.py`.
- **Normalização:** posto de 1 a 7 em cada indicador, com empate no mesmo posto, como no INVUPRIN. Nos indicadores de distância, menor é melhor.
- **Pesos:** as três dimensões valem o mesmo, e os indicadores dividem igualmente o peso dentro de cada uma.
- **Escala:** de 0 a 100. O INVUPRIN não detalha o escalonamento final, então esta parte é nossa e será declarada.
- **Leitura:** o valor é uma régua entre os 7 territórios, sem sentido absoluto.

**Por que postos:** com 7 unidades, um valor extremo dominaria uma escala min-max ou z-score. Os postos também lidam com o zero de creche em Caputera sem tratamento especial. As duas outras normalizações entram na sensibilidade.

**Sensibilidade:**
- pesos iguais por dimensão, iguais por indicador e com os pesos do IMAPI nos indicadores que ele tem;
- postos, min-max e z-score;
- com e sem equipamentos municipais (S3 sem o hospital, S4 e A2 fora);
- retirando um indicador de cada vez;
- S2 com raio de 1 km e 2 km e com 2SFCA.

## 5. Equipamentos de abrangência municipal

Eles não entram em contagem por território. Hospital, CAPS Infantil e Conselhos Tutelares entram por distância, porque atendem moradores de outros territórios. O CREAS e as outras camadas de especialidade (CAPS adulto e AD, Policlínica, Clínica da Mulher, reabilitação) ficam fora do índice e seguem visíveis no mapa.

O território Central ficará perto de quase todos eles. Isso é uma condição real de acesso, mas também faz o índice favorecê-lo. Por isso o cenário sem equipamentos municipais é obrigatório.

## 6. O que o índice não permite afirmar

- **Qualidade do atendimento:** ele não mede equipe, horário, fila nem capacidade. Uma UBS grande e uma pequena contam igual.
- **Saúde das crianças:** nenhum resultado de saúde entra no cálculo. Uma posição alta não quer dizer que as crianças daquele território têm mais saúde.
- **Falta de atendimento em geral:** só a rede pública é contada. Em território com muita escola ou clínica particular, pouca oferta pública não significa criança sem atendimento. A base não tem renda para corrigir isso.
- **Desempenho da gestão:** o índice descreve localização de equipamentos e não avalia gestão.
- **Diferenças pequenas:** com 7 territórios, uma posição de distância pode mudar com um único equipamento. Se a sensibilidade mostrar instabilidade, a recomendação será usar faixas, não posições.

**Limitações que afetam os números:**
- Matrícula é contada onde fica a escola, não onde a criança mora.
- O Censo agrupa 0–4 e 5–9, o que não coincide com creche e pré-escola. E1 e E2 são medidas relativas, não taxas de cobertura.
- Distâncias são em linha reta. Em setores rurais grandes, o ponto interno representa mal onde as crianças moram.
- 7 dos 9 pontos de assistência social e 1 dos 2 Conselhos Tutelares têm coordenada aproximada. O efeito sobre A1 e A2 aparece no teste que retira cada indicador. As 26 UBS e os pontos de urgência vêm do CNES.
- Os limites dos territórios são aproximados: 60 setores têm fronteira duvidosa e 11 equipamentos têm bairro listado em outro território.
- Caputera tem 0 matrícula em creche nos dados do INEP: suas duas escolas públicas constam como pré-escola. A base não vê creche particular, nem criança matriculada em outro território.

## 7. Lacunas de fonte

Nenhuma muda a recomendação, porque os componentes ausentes já excluem esses índices. Mas nenhum destes pontos pode ser citado como fato antes de conferir:

| Índice | O que faltou |
|---|---|
| IMAPI | Fórmula no Apêndice S3, não lido. Os artigos falam em 31 e 30 indicadores, e os pesos da dimensão de segurança parecem deslocados na tabela lida |
| IDI | Pesos e fórmula. O relatório do UNICEF de 2006 não foi lido; a nota do IPECE veio só em trecho de busca. Os componentes vêm de Kappel (2007) |
| INC | Notas metodológicas, com acesso bloqueado (HTTP 403). Os componentes vêm do resumo de 2024 da FMCSV |
| IPVS 2022 | Anexo metodológico do Seade não lido. A lista vem de informe da Prefeitura de SP, e a tabela foi lida com o texto cortado na margem |
| IPPI | Nenhum documento do Seade localizado |
| IDSUS | Lista dos 24 indicadores não conferida. A interrupção da medição vem de uma única fonte |
| COI 3.0 | Documento técnico bloqueado (HTTP 403). Dados vêm dos resumos de busca |
| Mapa da Desigualdade 2026 | Método do ranking geral não localizado. A edição de 2020 diz "26 indicadores" numa página e "28" em outra |

## 8. Decisão

O Guilherme pediu, em 07/11/2026, a implementação do que foi levantado aqui:
1. **Opção:** C.
2. **Nome:** Índice de Oferta e Acesso a Equipamentos para a Infância.
3. **Indicadores:** os 8 da seção 4.

**Para depois:** o IPVS 2022 é publicado por setor censitário e poderia corrigir o maior ponto cego, que é o da rede particular em áreas de renda alta. Isso amplia a base, então fica de fora agora.

## 9. Fontes

Consultadas em 07/11/2026. "Leitura" indica o que foi efetivamente acessado.

| Fonte | Leitura | Link |
|---|---|---|
| Prefeitura de São Paulo. 3º Diagnóstico Territorial da Primeira Infância (INVUPRIN) | Seção de método e Quadro 1 | https://prefeitura.sp.gov.br/documents/d/secretaria_executiva_de_projetos_estrategicos/3-diagnostico-territorial-da-primeira-infancia |
| Rede Nossa São Paulo. Mapa da Desigualdade da Primeira Infância 2020 | Metodologia e fórmulas | https://www.nossasaopaulo.org.br/wp-content/uploads/2020/02/Mapa_PrimeiraInfancia-2020-completo.pdf |
| Prefeitura de São Paulo. Notícia sobre o 3º Mapa (2026) | Notícia | https://prefeitura.sp.gov.br/web/secretaria_executiva_de_projetos_estrategicos/w/3%C2%BA-mapa-da-desigualdade-da-primeira-inf%C3%A2ncia-refor%C3%A7a-diagn%C3%B3sticos-territoriais-realizados-pela-prefeitura-de-s%C3%A3o-paulo |
| TVT News. Reportagem sobre o Mapa 2026 | Notícia | https://tvtnews.com.br/mapa-desigualdade-primeira-infancia-sao-paulo/ |
| Buccini et al. Nurturing care indicators for the IMAPI | Resumo automático da tabela; conferir antes de citar | https://pmc.ncbi.nlm.nih.gov/articles/PMC8968942 |
| Buccini et al. Sociodemographic inequities in nurturing care | Resumo automático; sem o Apêndice S3 | https://pmc.ncbi.nlm.nih.gov/articles/PMC8968940 |
| IMAPI dataset (Mendeley Data) | Página descritiva | https://data.mendeley.com/datasets/8cy7v679zv/4 |
| Kappel, D. B. Índice de desenvolvimento infantil no Brasil. Revista Brasileira de Educação, 2007 | Trechos sobre composição | https://www.redalyc.org/pdf/275/27503504.pdf |
| IPECE. Nota Técnica 13, 2005 | Só trecho de busca; PDF ilegível | https://www.ipece.ce.gov.br/wp-content/uploads/sites/45/2012/12/NT_13.pdf |
| FMCSV/Quantis. INC Estados e Capitais, 2024 | Resumo de 2 páginas | https://biblioteca.fmcsv.org.br/wp-content/uploads/2024/09/INC_V3_final.pdf |
| Prefeitura de São Paulo. Informe Urbano 74 sobre o IPVS | Quadro de variáveis e método | https://prefeitura.sp.gov.br/web/licenciamento/w/74-din%C3%A2mica-da-vulnerabilidade-social-na-cidade-de-s%C3%A3o-paulo-uma-an%C3%A1lise-a-partir-do-ipvs-entre-2000-e-2022 |
| Ministério da Saúde. Apresentação do IDSUS, 2012 | Só trecho de busca | https://materiais.ead.fiocruz.br/especializacao/gestao-em-saude/percurso/documents/IDSUS_PARA_UA5_BIBLIOTECA.pdf |
| Brandeis. COI 3.0 Technical Documentation | Só trecho de busca | https://www.diversitydatakids.org/research-library/coi-30-technical-documentation |
| Aplicação do 2SFCA a UBS (REFACS, 2024) | Só trecho de busca | https://seer.uftm.edu.br/revistaeletronica/index.php/refacs/article/view/7747 |
| OCDE/JRC. Handbook on Constructing Composite Indicators, 2008 | Registro do catálogo | https://publications.jrc.ec.europa.eu/repository/handle/JRC47008 |
