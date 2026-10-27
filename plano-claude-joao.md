# Plano de execução — Mapa Infância Cotia

Versão de 19/10/2026. Escrito pelo Guilherme para o Claude Code do João.

**Claude: este arquivo é a sua tarefa.** Leia tudo antes de agir, monte o plano em *plan mode* e execute as 6 fases na ordem. Ao fim de cada fase, pare no **PONTO DE PARADA** e espere o João aprovar antes de seguir. O João revisa e aprova, mas não faz nada fora do computador (telefonar, ir ao local). Tudo o que precisar ser descoberto, você descobre pela web.

```
PARÂMETROS
Nome provisório do site:  Mapa Infância Cotia  (sem logo, sem assinatura institucional)
Município:                Cotia (SP) — código IBGE 3513009 — código CNES 351300
Divisão territorial:      7 territórios de CRAS (Plano Municipal de Assistência Social 2026–2029)
Público:                  quem discute política pública em Cotia (diagnóstico, não guia de serviço)
Orçamento:                zero — sem servidor, sem API paga, sem domínio próprio
Hospedagem:               GitHub Pages
Mapa:                     Leaflet 1.9.4 + base OpenStreetMap
Idioma do site:           português
Insumos:                  ./insumos/ (enviados pelo Guilherme; não editar)
Data de corte dos dados:  a data em que você coletar cada fonte (registrar sempre)
```

---

## 1. Contexto e objetivo

O site mostra num mapa **onde estão e onde faltam** os equipamentos públicos que afetam a saúde das crianças de Cotia, território por território.

Ele responde: *"neste território de Cotia, quantas crianças moram e quantos equipamentos de saúde, educação infantil e proteção atendem essas crianças?"*

O recorte é intersetorial. Saúde da criança depende de renda, alimentação, violência e vínculos, e não só de atendimento clínico. Por isso o mapa junta SUS, SUAS (assistência social) e escola.

**Pronto significa:** o site está no ar no GitHub Pages e passa em todos os itens da seção 8.

---

## 2. Insumos (pasta `./insumos/`)

| Arquivo | O que é |
|---|---|
| `cnes-cotia-saude.csv` | 39 equipamentos de saúde ativos e públicos (+ APAE conveniada), extraídos da API do CNES em 19/10/2026, com coordenadas |
| `territorios-cras.md` | Os 7 territórios de CRAS: endereço, telefone e lista de bairros de cada um, transcritos do Plano Municipal de Assistência Social 2026–2029, com as divergências conhecidas |
| `mapa-territorios-cras-pmas-2026.png` | O mapa colorido oficial dos territórios, tirado do mesmo plano |

Se algum desses arquivos faltar, pare e avise o João.

---

## 3. Camadas do mapa

| # | Camada (`camada`) | O que entra | Fonte | Situação |
|---|---|---|---|---|
| 1 | `saude_atencao_basica` | 26 UBS | CNES | pronta no insumo |
| 2 | `saude_urgencia` | UPA Atalaia, PA Parque São George, PA Caucaia do Alto, Pronto Socorro Infantil | CNES | pronta. Funcionamento do PSI confirmado pela prefeitura em 09/10/2026; as 4 unidades são geridas pela OS AHBB desde abril de 2026 |
| 3 | `saude_hospital` | Hospital Regional de Cotia (gestão estadual) | CNES | pronta |
| 4 | `saude_mental` | CAPS Infantil, CAPS II adulto, CAPS AD | CNES | pronta. Destacar o CAPS Infantil; os outros dois em cor secundária |
| 5 | `saude_especializada` | Policlínica Portão, Clínica da Mulher | CNES | pronta |
| 6 | `reabilitacao` | CEFOR I, CEFOR V, APAE Cotia | CNES | pronta. APAE aparece como `conveniada` |
| 7 | `educacao_infantil` | creches e pré-escolas públicas em atividade | INEP (Censo Escolar) | **coletar na fase 2** |
| 8 | `assistencia_social` | 7 CRAS, CREAS Cotia, Unidade Avançada do CREAS em Caucaia | insumo + Carta de Serviços | **geocodificar na fase 2** |
| 9 | `protecao` | Conselho Tutelar Cotia, Conselho Tutelar Caucaia do Alto | web | **verificar na fase 2** |

**Nunca mapeie serviços de acolhimento institucional de crianças (SAICA, abrigos).** A prefeitura diz que os endereços são sigilosos (Carta de Serviços ao Usuário, item 3.2). Se algum desses endereços aparecer em qualquer fonte, descarte. Na metodologia, cite só que Cotia tem 2 unidades, com 60 vagas no total.

---

## 4. Pilha técnica

- Site: HTML + CSS + JavaScript puro, sem framework, sem etapa de build.
- Leaflet **1.9.4** por CDN (cdnjs ou unpkg), com versão fixa na URL.
- Base: tiles do OpenStreetMap com a atribuição "© OpenStreetMap contributors" visível. Se a política de uso dos tiles virar problema, troque pela base Positron da CARTO.
- Dados estáticos em `site/data/` (GeoJSON e CSV). Sem API key, sem cookies, sem analytics de terceiros.
- Scripts de dados em Python 3 (`requests`, `pandas`, `geopandas`, `shapely`), com `requirements.txt`.
- Geocodificação: Nominatim, **no máximo 1 requisição por segundo**, com `User-Agent` identificando o projeto, e cache em `dados/cache-geocodificacao.csv` para nunca repetir consulta.
- Hospedagem: repositório público no GitHub, com GitHub Pages servindo `site/`.

Estrutura do repositório:

```
/
├── README.md                  ordem dos scripts e comando de cada um
├── requirements.txt
├── plano-claude-joao.md       este arquivo
├── insumos/                   o que veio do Guilherme (não editar)
├── dados/
│   ├── brutos/                arquivos originais baixados, com data no nome
│   ├── verificacoes/          relatórios de checagem (fase 2)
│   └── cache-geocodificacao.csv
├── scripts/
└── site/
    ├── index.html
    ├── metodologia.html
    ├── css/  js/
    └── data/
        ├── equipamentos.csv
        ├── equipamentos.geojson
        └── territorios.geojson
```

Arquivos grandes baixados (a malha do IBGE para SP, os microdados do INEP) ficam fora do Git: coloque no `.gitignore` e só versione o recorte de Cotia.

---

## 5. Esquema dos dados

### `site/data/equipamentos.csv` — uma linha por equipamento

| Campo | Regra |
|---|---|
| `id` | prefixo da fonte + código oficial (`cnes-6983138`, `inep-35xxxxxx`); `cras-01`, `ct-cotia` para quem não tem código |
| `nome` | como está na fonte, com capitalização corrigida |
| `camada` | um dos 9 valores da seção 3 |
| `subtipo` | texto curto (ex.: CAPSi, Creche, Pré-escola, Creche e pré-escola) |
| `gestao` | `municipal`, `estadual` ou `conveniada` |
| `endereco`, `bairro`, `telefone` | da fonte; vazio se a fonte não traz |
| `territorio` | preenchido por ponto-no-polígono (fase 3) |
| `lat`, `lon` | 6 casas decimais |
| `coord_origem` | `cnes`, `inep`, `nominatim`, `manual` ou `pendente` |
| `fonte`, `fonte_url`, `data_coleta` | sempre preenchidos; data em AAAA-MM-DD |
| `verificacao` | `confirmado` (fonte oficial de 2025 ou depois) ou `nao_confirmado` |
| `observacao` | divergências e avisos que aparecem na ficha do ponto |

### `site/data/territorios.geojson` — um polígono por território

Propriedades: `id`, `nome`, `cor`, `cras_referencia`, `pop_total`, `pop_0_4`, `pop_5_9`, `pop_10_14`, `pop_15_19`, `setores_com_sigilo`, `moradores_em_sigilo` e uma contagem por camada (`n_saude_atencao_basica`, …).

---

## 6. Fases

### Fase 1 — Esqueleto e saúde

1. Crie a estrutura da seção 4, o `.gitignore`, o `requirements.txt` e um `README.md` provisório.
2. Escreva `scripts/coletar_cnes.py`, que refaz a extração da saúde:
   - endpoint `https://apidadosabertos.saude.gov.br/cnes/estabelecimentos?codigo_municipio=351300&limit=20&offset=N`, paginando de 20 em 20 até a resposta vir vazia (Cotia tem cerca de 446 estabelecimentos);
   - mantenha só os de natureza jurídica começando com `1` (administração pública), mais a APAE;
   - descarte quem tem `codigo_motivo_desabilitacao_estabelecimento` preenchido;
   - tipos de unidade: 2 (UBS), 4 (só a Policlínica), 5 (hospital), 20 e 73 (pronto-socorro e pronto atendimento), 36 (só os CEFOR e a Clínica da Mulher), 70 (CAPS);
   - fora: vigilâncias, SAMU, farmácias, regulação, secretaria, medicina do trabalho e serviço de verificação de óbito.
3. Compare o resultado com `insumos/cnes-cotia-saude.csv`. Liste as unidades que entraram ou saíram e as coordenadas que mudaram mais de 100 m.
4. Monte um `site/index.html` mínimo com o contorno de Cotia e os pontos de saúde.

**PONTO DE PARADA 1:** mostre ao João o mapa simples e o relatório de diferenças contra o insumo. Se houver diferença, explique a provável causa (unidade nova, desativada, mudança de endereço).

### Fase 2 — Demais camadas e verificação

**2a. Educação infantil (camada 7)**

1. Baixe os microdados do Censo Escolar mais recente: https://www.gov.br/inep/pt-br/acesso-a-informacao/dados-abertos/microdados/censo-escolar
2. Leia o dicionário de dados que vem no pacote e confirme o nome das variáveis antes de filtrar. Os nomes esperados são `CO_MUNICIPIO`, `TP_DEPENDENCIA` (2 estadual, 3 municipal), `TP_SITUACAO_FUNCIONAMENTO` (1 em atividade), `IN_INF_CRE`, `IN_INF_PRE`, as matrículas `QT_MAT_INF_CRE` e `QT_MAT_INF_PRE` e os campos de endereço.
3. Filtre Cotia (`CO_MUNICIPIO = 3513009`), escolas públicas em atividade e com creche ou pré-escola. Salve o recorte em `dados/brutos/inep-cotia-<ano>.csv`.
4. Guarde as matrículas de creche e de pré-escola de cada escola. Elas não aparecem na versão 1, mas servem para a versão 2.
5. Para conveniadas (privadas que recebem vaga pública), use o campo de convênio do dicionário. Se ele não existir, deixe as conveniadas fora e registre isso na metodologia.
6. Os microdados não trazem coordenadas, então geocodifique pelo endereço (seção 4). Tente também o Catálogo de Escolas do INEP (https://www.gov.br/inep/pt-br/acesso-a-informacao/dados-abertos/inep-data/catalogo-de-escolas), que pode trazer latitude e longitude. Se o painel exigir interação que você não consegue fazer, siga só com a geocodificação.

**2b. Assistência social (camada 8)**

1. Use os endereços dos 7 CRAS em `insumos/territorios-cras.md`. Três CRAS têm endereço diferente na Carta de Serviços: vale o Plano 2026, com a divergência em `observacao`.
2. CREAS, segundo a Carta de Serviços (https://cotia.sp.gov.br/carta-de-servico-ao-usuario/):
   - CREAS Cotia: Rua Água Marinha, 39, Jd. Nomura, tel. 4614-5622;
   - Unidade Avançada do CREAS: Rua Benedito Pires da Silva Sobrinho, 157, Jd. Planalto, Caucaia do Alto.
3. Geocodifique os dois.

**2c. Verificação dos Conselhos Tutelares (camada 9)**

O único endereço encontrado até agora é de uma notícia da prefeitura de 03/02/2021 (https://cotia.sp.gov.br/sds-entrega-novos-equipamentos-e-mobiliario-para-o-conselho-tutelar-de-caucaia/):

- Conselho Tutelar Cotia: Rua Jorge Caixe, 306, Jardim Nomura, tel. 4703-1618 / 4703-5813;
- Conselho Tutelar Caucaia do Alto: Rua Benedito Pires da Silva Sobrinho, 157, Jd. Planalto, tel. 4242-0110 / 4611-1793.

Há dois sinais de que esses endereços podem ter mudado. A Rua Jorge Caixe, 306 hoje é o Centro Administrativo de Cotia (CAC). E o Procon saiu do prédio da Benedito Pires, 157 em setembro de 2026.

Verifique cada conselho nesta ordem, parando quando achar uma fonte oficial com data de 2025 ou depois:

1. Notícias da prefeitura pela API do site (a página HTML esconde o texto, mas a API devolve o conteúdo):
   `https://cotia.sp.gov.br/wp-json/wp/v2/posts?search=conselho%20tutelar&after=2025-01-01T00:00:00&per_page=50&_fields=date,link,content`
   Repita com `search=tutelar`, `search=CMDCA` e `search=rede%20de%20prote%C3%A7%C3%A3o`, e procure endereço ou telefone no texto.
2. Documentos da prefeitura pela mesma API: `https://cotia.sp.gov.br/wp-json/wp/v2/media?search=conselho%20tutelar&per_page=50`. Procure PDFs de 2025 ou depois (resoluções do CMDCA, editais, planos); baixe e leia os que citarem endereço.
3. A Carta de Serviços ao Usuário (link acima) e páginas do Ministério Público de SP ou do Tribunal de Justiça que listem a rede de proteção de Cotia.
4. Busca geral na web por "Conselho Tutelar Cotia endereço" e "Conselho Tutelar Caucaia do Alto endereço", priorizando resultados de 2025 em diante.

Regras de decisão:

- **Confirmado:** endereço em fonte oficial (prefeitura, CMDCA, MP, Judiciário, governo) com data de 2025 ou depois. Use esse endereço, `verificacao = confirmado`, e a fonte em `fonte_url`.
- **Fonte não oficial** (Google Maps, guia comercial, rede social): não confirma. Registre em `dados/verificacoes/conselhos-tutelares.md` como indício.
- **Nada confirmado:** o ponto entra com o endereço de 2021, `verificacao = nao_confirmado` e `observacao = "Endereço publicado pela prefeitura em 2021; não há confirmação oficial mais recente."`. A ficha do ponto mostra esse aviso.
- **Fontes oficiais recentes que divergem:** use a mais recente e registre as duas.

Salve o relatório em `dados/verificacoes/conselhos-tutelares.md`: cada fonte consultada, com URL, data da fonte, o que dizia e a conclusão.

**2d. Junção**

1. Escreva `scripts/montar_equipamentos.py`, que junta as 9 camadas no esquema da seção 5.
2. Pontos que o Nominatim devolveu só com a rua, ou que caíram fora de Cotia, ficam `coord_origem = pendente`. Para cada um, tente outra grafia do endereço, o CEP ou um ponto de referência citado na fonte. Se ainda falhar, liste para o João.

**PONTO DE PARADA 2:** mostre ao João:
- a contagem de equipamentos por camada;
- o relatório dos Conselhos Tutelares;
- a lista de pontos `pendente`, com a sugestão de coordenada para cada um, para ele aprovar ou corrigir.

### Fase 3 — Territórios e população

**3a. Polígonos.** Cotia não tem limites de bairro oficiais: o IBGE não tem bairros cadastrados para o município, e não há lei de abairramento publicada. Os 7 territórios de CRAS são a única divisão com mapa e lista de bairros. Os polígonos serão uma aproximação:

1. Baixe a malha de setores do Censo 2022 para SP (GeoPackage, ~180 MB):
   `https://ftp.ibge.gov.br/Censos/Censo_Demografico_2022/Agregados_por_Setores_Censitarios/malha_com_atributos/setores/gpkg/UF/SP/SP_setores_CD2022.gpkg`
   Filtre `CD_MUN = 3513009` e salve em `dados/brutos/setores-cotia-2022.geojson`.
2. Georreferencie `insumos/mapa-territorios-cras-pmas-2026.png` sobre os setores, com 4 ou mais pontos de controle reconhecíveis (bordas do município, a Raposo Tavares, a represa).
3. Atribua cada setor ao território cuja cor cai sob o centroide dele.
4. Use as listas de bairros de `insumos/territorios-cras.md` para checar os setores de fronteira, comparando com os nomes de bairro do OpenStreetMap.
5. Setores do miolo verde-claro do mapa (Morro Grande, área de reserva sem CRAS) vão para o território vizinho que tiver acesso viário.
6. Dissolva os setores por território: o resultado é `site/data/territorios.geojson`.
7. Use estes nomes e cores de referência:

| # | Território | Cor no mapa oficial |
|---|---|---|
| 1 | Jd. Japão | roxo |
| 2 | Caucaia do Alto | verde-claro |
| 3 | Miguel Mirizola | amarelo/dourado |
| 4 | Central (Monte Serrat) | azul-claro |
| 5 | KM 21 / Granja Viana (antigo Recanto Suave) | azul-escuro |
| 6 | Jd. Arco-Íris / Jd. Sandra | laranja |
| 7 | Caputera | verde-limão |

**3b. População.**

1. Baixe `https://ftp.ibge.gov.br/Censos/Censo_Demografico_2022/Agregados_por_Setores_Censitarios/Agregados_por_Setor_csv/Agregados_por_setores_demografia_BR.zip`. O dicionário está em `.../Agregados_por_Setores_Censitarios/dicionario_de_dados_agregados_por_setores_censitarios_20260520.xlsx`.
2. Variáveis: `V01006` (moradores), `V01031` (0–4 anos), `V01032` (5–9), `V01033` (10–14), `V01034` (15–19). O arquivo está em ISO-8859-1, separado por `;`.
3. Valores `X` são sigilo do IBGE (setores com menos de 5 domicílios). Trate como ausentes, nunca como zero, e conte quantos setores e moradores ficaram de fora.
4. Some por território. Compare o total de moradores com o total oficial de Cotia no Censo 2022 (https://cidades.ibge.gov.br/brasil/sp/cotia). Uma diferença acima de 1% indica erro na junção: investigue antes de seguir.
5. No site, "crianças" é a faixa de 0–14 anos. A faixa de 15–19 aparece à parte, como "adolescentes (15–19)", porque o Censo não separa 0–17.

**3c. Território de cada equipamento.** Atribua o território por ponto-no-polígono. Depois cruze com as listas de bairros. Se o bairro do equipamento pertence a outro território na lista oficial, registre em `observacao` e liste o caso.

**PONTO DE PARADA 3:** mostre ao João:
- o mapa de conferência dos setores coloridos;
- a tabela de população por território, com o total conferido;
- os setores de fronteira duvidosos;
- os equipamentos com território divergente.

Se os setores do miolo de reserva somarem mais de 2% da população de Cotia, peça ao João uma decisão sobre onde colocá-los.

### Fase 4 — Site

Implemente:

1. **Mapa** com os 7 territórios coloridos e o contorno de Cotia.
2. **Camadas que ligam e desligam**, uma por camada da seção 3, cada uma com ícone e cor próprios e legenda visível. Pontos `nao_confirmado` aparecem com um marcador distinto.
3. **Ficha do ponto**: nome, subtipo, gestão, endereço, telefone, território, fonte (com link), data da coleta e `observacao`.
4. **Ficha do território** (painel lateral; em tela estreita, gaveta de baixo):
   - população 0–4, 5–9, 10–14 e 15–19;
   - quantos equipamentos de cada camada;
   - crianças de 0–14 por equipamento, para UBS, CRAS e educação infantil;
   - comparação com a média de Cotia (ex.: "1 UBS para cada 2.300 crianças; média de Cotia: 1 para 1.900").
5. **Tabela comparativa** dos 7 territórios, ordenável por qualquer coluna.
6. **`metodologia.html`**: cada fonte com link e data de coleta, como os territórios foram desenhados, a regra de verificação dos Conselhos Tutelares e as limitações:
   - os limites dos territórios são uma aproximação do mapa oficial, montada a partir de setores censitários;
   - a população é do Censo 2022, e áreas que cresceram depois aparecem subestimadas;
   - setores em sigilo ficam fora da contagem (com os números);
   - contar equipamentos não mede qualidade, equipe nem fila;
   - o CNES depende do que a prefeitura declara;
   - a Saúde de Cotia usa outra divisão interna, que não coincide com os territórios de CRAS.
7. **Download** de `equipamentos.csv` e `territorios.geojson`.
8. **Linguagem neutra.** O site mostra números. Não elogia nem critica a gestão, não aponta culpados, não cita partido nem político.

### Fase 5 — Revisão

1. Teste numa largura de 375 px, sem rolagem horizontal.
2. Abra cada link da metodologia e confirme que responde.
3. Procure no repositório inteiro qualquer endereço de acolhimento, nome de servidor, de conselheiro ou de paciente. Não pode haver nenhum.
4. Rode os scripts do zero, numa pasta limpa, seguindo o `README.md`, e confirme que os arquivos de `site/data/` saem iguais.
5. Passe pelo checklist da seção 8.

**PONTO DE PARADA 4:** publique uma prévia (GitHub Pages num branch de prévia, ou abrir localmente) e entregue ao João o link e o checklist preenchido. Ele leva ao Guilherme.

### Fase 6 — Publicação

Só depois que o João disser que o Guilherme aprovou:

1. Publique no GitHub Pages.
2. Confira que o site abre no endereço público e que os downloads funcionam.

---

## 7. Regras para quando travar

- **Nenhum dado inventado.** Equipamento sem fonte não entra. Número que não fecha leva a parar e mostrar ao João.
- **Cada ponto e cada número tem fonte e data**, na ficha e na metodologia.
- **Se uma fonte oficial sair do ar** ou mudar de formato, registre o que aconteceu, tente a fonte alternativa citada no plano e, se não houver, pare e avise o João.
- **Se duas fontes oficiais divergirem**, use a mais recente e registre as duas.
- **Se precisar de ação humana fora do computador**, não peça. Registre a lacuna, siga com a melhor informação documentada e marque o ponto como `nao_confirmado`.
- **Na dúvida sobre escopo** (incluir uma camada nova, mudar a divisão territorial), pare e pergunte ao João.

---

## 8. Critério de pronto

- [ ] As 9 camadas aparecem com pontos, legenda e ficha.
- [ ] Todo ponto tem `fonte`, `fonte_url`, `data_coleta`, `coord_origem` e `verificacao`; nenhum está `pendente`.
- [ ] `dados/verificacoes/conselhos-tutelares.md` existe e documenta cada fonte consultada.
- [ ] Os 7 territórios aparecem, e clicar em cada um abre o painel com população e contagens.
- [ ] A soma da população dos territórios fica a no máximo 1% do total oficial de Cotia, e a metodologia explica a diferença.
- [ ] A tabela comparativa ordena por qualquer coluna.
- [ ] A metodologia lista todas as fontes com link e data, e as limitações da fase 4.
- [ ] Os downloads entregam `equipamentos.csv` e `territorios.geojson`.
- [ ] Funciona a 375 px sem rolagem horizontal.
- [ ] Nenhum endereço de acolhimento e nenhum dado pessoal no repositório.
- [ ] O `README.md` permite a outra pessoa refazer os dados rodando os scripts na ordem.

---

## 9. Ideias para a versão 2 (não fazer agora)

- Percentual de crianças morando a mais de 1,5 km da UBS mais próxima.
- Taxa de atendimento em creche: matrículas (já guardadas na fase 2) ÷ população de 0–4 anos, por território.
- Cobertura vacinal e mortalidade infantil por território, se houver dado.
- Escolas de ensino fundamental (Programa Saúde na Escola).
- Territórios da Saúde, se a Secretaria publicar a área de abrangência das UBS.

---

## 10. Fontes de partida (acessadas em 19/10/2026)

- CNES — API de dados abertos: https://apidadosabertos.saude.gov.br/cnes/estabelecimentos
- Plano Municipal de Assistência Social 2026–2029 (Resolução CMAS 298): https://cotia.sp.gov.br/wp-content/uploads/2026/06/298-resolucao-cmas-aprova-o-plano-municipal-de-assistencia-social-2026-a-2029-.pdf
- Carta de Serviços ao Usuário: https://cotia.sp.gov.br/carta-de-servico-ao-usuario/
- Relatório Anual de Gestão da Saúde 2023: https://cotia.sp.gov.br/wp-content/uploads/2026/05/rag-2023.pdf
- Funcionamento do PSI no feriado de 12/10 (09/10/2026): https://cotia.sp.gov.br/feriado-de-12-de-outubro-confira-o-funcionamento-dos-servicos-de-cotia/
- OS AHBB na gestão da urgência (18/03/2026): https://cotia.sp.gov.br/saude-de-cotia-tera-nova-organizacao-social-para-gestao-de-prontos-atendimentos/
- Conselhos Tutelares (03/02/2021): https://cotia.sp.gov.br/sds-entrega-novos-equipamentos-e-mobiliario-para-o-conselho-tutelar-de-caucaia/
- IBGE — Censo 2022, agregados por setores e malha: https://ftp.ibge.gov.br/Censos/Censo_Demografico_2022/Agregados_por_Setores_Censitarios/
- INEP — microdados do Censo Escolar: https://www.gov.br/inep/pt-br/acesso-a-informacao/dados-abertos/microdados/censo-escolar
- INEP — Catálogo de Escolas: https://www.gov.br/inep/pt-br/acesso-a-informacao/dados-abertos/inep-data/catalogo-de-escolas
- Nominatim — política de uso: https://operations.osmfoundation.org/policies/nominatim/
- Tiles do OpenStreetMap — política de uso: https://operations.osmfoundation.org/policies/tiles/
