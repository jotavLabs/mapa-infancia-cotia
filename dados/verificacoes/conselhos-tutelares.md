# Verificação dos Conselhos Tutelares e do CREAS — 2026-10-19

Fase 2c do plano (Conselhos Tutelares), estendida às duas unidades do CREAS com o mesmo método. Só pesquisa: nenhum endereço foi geocodificado.

## Conclusões

| id | Endereço escolhido | Bairro | Telefone | Verificação | Fonte escolhida | Data da fonte |
|---|---|---|---|---|---|---|
| `ct-cotia` | Rua Jorge Caixe, 306 (prédio 306-A, térreo) | Jardim Nomura | (11) 4703-1618 (fonte mais recente; o Regimento de 2025 traz também (11) 4703-5813, registrado na observação) | confirmado | Página da Secretaria Municipal de Desenvolvimento Social | 2026-07-14 |
| `ct-caucaia` | Rua Benedito Pires da Silva Sobrinho, 157 | Jardim Planalto, Caucaia do Alto | (11) 4242-0110 / (11) 4611-1793 | confirmado | Página da Secretaria Municipal de Desenvolvimento Social | 2026-07-14 |
| `creas-cotia` | Avenida Professor Manoel José Pedroso, 1565 (2º andar) | Jardim Nomura | (11) 4614-5622 | confirmado | Página da Secretaria Municipal de Desenvolvimento Social | 2026-07-14 |
| `creas-caucaia` | Rua Benedito Ferreira das Dores, 289 | Vila Santa Catarina, Caucaia do Alto | sem telefone na fonte | confirmado | Página da Secretaria Municipal de Desenvolvimento Social | 2026-07-14 |

Dados prontos para a junção: `dados/verificacoes/enderecos-protecao-creas.csv`.

## Método

- Data das consultas: 2026-10-19.
- Notícias e páginas da prefeitura foram lidas pela API WordPress (`/wp-json/wp/v2/posts`, `/pages`, `/media`), que devolve o texto completo. A data de uma notícia é a data de publicação (`date`). A data de uma página fixa é a da última modificação (`modified`), porque a API não mostra qual trecho foi alterado.
- Documentos da prefeitura com data de 2025 ou depois foram baixados para uma pasta temporária, fora do projeto: 74 PDFs (atas e resoluções do CMDCA, editais). O texto foi extraído com pymupdf e as buscas foram feitas por endereço, telefone, "sede" e "mudança".
- Regra aplicada: fonte oficial com data de 2025 ou depois confirma o endereço. Quando fontes oficiais divergem, vale a mais recente, e as duas ficam registradas aqui.
- Os nomes de conselheiros, servidores e outras pessoas que aparecem nas fontes foram omitidos. Endereços de serviços de acolhimento também foram omitidos.

### Correção de uma premissa da tarefa

A tarefa dizia que o Procon "saiu" do prédio da Rua Benedito Pires da Silva Sobrinho, 157 em setembro de 2026. As fontes mostram o contrário: o Procon de Caucaia **entrou** nesse prédio em 17/09/2026. Antes disso, ele funcionava na Rua Manoel Ferraz de Almeida, 38 (notícias de 04/12/2025 e 23/07/2026).

- https://cotia.sp.gov.br/rocon-de-caucaia-atende-em-novo-endereco-a-partir-desta-quinta-feira-17/ (2026-09-15): "A partir desta quinta-feira (17), o Procon de Caucaia do Alto passa a atender em novo endereço: Rua Benedito Pires da Silva Sobrinho, nº 157".
- https://cotia.sp.gov.br/procon-de-cotia-orienta-consumidores-sobre-praticas-proibidas-pelo-codigo-do-consumidor/ (2026-09-17): Procon Caucaia na Benedito Pires da Silva Sobrinho, 157, tel. (11) 4242-3759.

A mudança relevante no prédio do nº 157 é outra. O CRAS e a unidade avançada do CREAS saíram de lá em 30/05/2026 e foram para o Centro Humanizado de Proteção Social, na Rua Benedito Ferreira das Dores, 289. O Conselho Tutelar de Caucaia continua listado no nº 157 (ver seção 2).

---

## 1. Conselho Tutelar de Cotia (`ct-cotia`)

### Fontes oficiais consultadas

| Data da fonte | Fonte | O que diz | Oficial |
|---|---|---|---|
| 2026-07-14 (modificação) | Página da Secretaria Municipal de Desenvolvimento Social — https://cotia.sp.gov.br/desenvolvimento-social-2025/ | Rua Jorge Caixe, 306 – CESEP; tel. (11) 4703-1618; atendimento das 8h às 17h. A página já mostra o CRAS e o CREAS de Caucaia no endereço novo de maio de 2026, então foi revisada depois dessa data. | sim (prefeitura) |
| 2026-05-21 (modificação) | Página do CMDCA — https://cotia.sp.gov.br/conselho-municipal-dos-direitos-da-crianca-e-do-adolescente/ | Rua Jorge Caixe, 306 – CESEP; tel. (11) 4703-1618. | sim (CMDCA/prefeitura) |
| 2025-04-09 (publicada no site em 2025-05-20) | Resolução CMDCA nº 113/2025, que aprova o Regimento Interno do Conselho Tutelar (art. 2º, parágrafo único) — https://cotia.sp.gov.br/wp-content/uploads/2025/05/resolua%E2%94%9Co-113-cmdca-aprova-o-regimento-do-conselho-tutelar-.pdf | "Conselho Tutelar de Cotia (Sede): CAM - Rua Jorge Caixe, 306-A - térreo - Jardim Nomura, Cotia - SP, 06716-900 - Telefone: (11) 4703-5813." | sim (CMDCA) |
| 2026-01-27 (ata de 18/12/2025) | Ata da 282ª reunião ordinária do CMDCA — https://cotia.sp.gov.br/wp-content/uploads/2026/01/ata-cmdca-282a-2025.pdf | Item 2, "linhas telefônicas dos Conselhos Tutelares de Cotia e Caucaia do Alto": os problemas administrativos com as linhas foram resolvidos e a "institucionalização definitiva" estava em andamento. Não traz números nem endereço. | sim (CMDCA) |
| 2026-05-15 | Notícia "Maio Laranja" — https://cotia.sp.gov.br/cotia-promove-acoes-de-conscientizacao-no-maio-laranja-e-reforca-combate-ao-abuso-e-a-exploracao-sexual-infantil/ | Confirma que o nº 306 da Rua Jorge Caixe é o Centro Administrativo de Cotia (CAC). Não traz o endereço do Conselho. | sim |
| 2024-03-01 | Notícia sobre a posse dos conselheiros 2024–2028 — https://cotia.sp.gov.br/conselheiros-tutelares-de-cotia-tomaram-posse-nesta-quarta-feira-10-01/ | Rua Jorge Caixe, 306 – Portão; tel. (11) 4703-1618. | sim, mas anterior a 2025 |
| 2024-02-21 | Notícia sobre ação do CREAS com o Conselho Tutelar — https://cotia.sp.gov.br/creas-em-parceria-com-o-conselho-tutelar-realiza-acao-de-enfrentamento-ao-trabalho-infantil/ | Rua Jorge Caixe, 306 – CESEP; tel. (11) 4703-1618. | sim, mas anterior a 2025 |
| 2021-02-03 | Notícia de partida — https://cotia.sp.gov.br/sds-entrega-novos-equipamentos-e-mobiliario-para-o-conselho-tutelar-de-caucaia/ | Rua Jorge Caixe, 306, Jardim Nomura; tel. 4703-1618 e 4703-5813. | sim, mas anterior a 2025 |
| 2017-08-08 | Notícia sobre a reforma do Conselho — https://cotia.sp.gov.br/prefeitura-de-cotia-concluiu-reforma-das-instalacoes-do-conselho-tutelar/ | Rua Jorge Caixe, 306, Jardim Nomura; tel. 4703-5813. | sim, histórico |

A Carta de Serviços ao Usuário (https://cotia.sp.gov.br/carta-de-servico-ao-usuario/, modificada em 2025-08-27) não traz o endereço do Conselho Tutelar.

### Indícios não oficiais

Nenhum foi encontrado. A busca geral na web não devolveu guia comercial, mapa nem rede social com o endereço do Conselho.

### Conclusão

**Confirmado: Rua Jorge Caixe, 306, Jardim Nomura**, no Centro Administrativo de Cotia (prédio 306-A, térreo; CEP 06716-900).

- O sinal de mudança da tarefa ("o nº 306 hoje é o CAC") não indica mudança. O próprio Regimento de 2025 põe a sede do Conselho dentro do centro administrativo, no térreo do 306-A.
- Duas fontes de 2025 ou depois confirmam o endereço: o Regimento (abril de 2025) e a página da Secretaria (revisada em 2026).
- **Telefone.** A fonte mais recente (página da Secretaria, 2026) traz (11) 4703-1618. O Regimento (2025) traz (11) 4703-5813. A notícia de 2021 traz os dois. Os dois números entraram no CSV, com o da fonte mais recente primeiro.
- **Bairro.** As fontes usam "Jardim Nomura" (Regimento 2025 e a maioria das notícias sobre o CAC) e, às vezes, "Portão" (notícia de 2024). Ficou "Jardim Nomura".
- "CESEP" e "CAM" aparecem nas fontes como nomes do prédio, mas nenhuma delas explica as siglas.

---

## 2. Conselho Tutelar de Caucaia do Alto (`ct-caucaia`)

### Fontes oficiais consultadas

| Data da fonte | Fonte | O que diz | Oficial |
|---|---|---|---|
| 2026-07-14 (modificação) | Página da Secretaria Municipal de Desenvolvimento Social — https://cotia.sp.gov.br/desenvolvimento-social-2025/ | Rua Benedito Pires da Silva Sobrinho, 157; tel. (11) 4242-0110 / (11) 4611-1793; e-mail institucional. Na mesma página, o CRAS e o CREAS de Caucaia já aparecem no endereço novo (Benedito Ferreira das Dores, 289), e o Conselho Tutelar continua no 157. | sim (prefeitura) |
| 2026-05-21 (modificação) | Página do CMDCA — https://cotia.sp.gov.br/conselho-municipal-dos-direitos-da-crianca-e-do-adolescente/ | Rua Benedito Pires da Silva Sobrinho, 157; tel. (11) 4242-0110 / (11) 4611-1793. | sim (CMDCA/prefeitura) |
| 2025-04-09 (publicada no site em 2025-05-20) | Resolução CMDCA nº 113/2025, Regimento Interno do Conselho Tutelar (art. 2º) — mesmo PDF da seção 1 | "Conselho Tutelar Distrito Caucaia do Alto: Rua Benedito Pires da Silva Sobrinho, nº157, no Centro de Caucaia do Alto – Telefone: 4242-0110/4611-1793." | sim (CMDCA) |
| 2026-09-15 e 2026-09-17 | Notícias do Procon (links na seção "Correção de uma premissa") | O Procon de Caucaia passou a funcionar no nº 157 em 17/09/2026. As notícias não falam do Conselho Tutelar. | sim |
| 2024-03-01 e 2024-02-21 | Notícias de 2024 (links na seção 1) | Rua Benedito Pires da Silva Sobrinho, 157; tel. (11) 4242-0110 / (11) 4611-1793. | sim, mas anteriores a 2025 |
| 2021-02-03 | Notícia de partida (link na seção 1) | Rua Benedito Pires da Silva Sobrinho, 157, Jd. Planalto; tel. 4242-0110 / 4611-1793. | sim, mas anterior a 2025 |
| 2018-11-26 | https://cotia.sp.gov.br/prefeitura-entrega-novas-instalacoes-do-cras-caucaia-do-alto-conselho-tutelar-e-uma-unidade-avancada-do-creas/ | O prédio do nº 157 foi reformado e passou a reunir o CRAS Caucaia, a unidade avançada do CREAS e o Conselho Tutelar. | sim, histórico |

### Indícios não oficiais

Nenhum foi encontrado. A busca na web por "Conselho Tutelar Caucaia do Alto" devolve sobretudo resultados de Caucaia, no Ceará.

### Conclusão

**Confirmado: Rua Benedito Pires da Silva Sobrinho, 157, Jardim Planalto, Caucaia do Alto.**

- Todas as fontes oficiais de 2025 e 2026 dão o mesmo endereço e os mesmos telefones.
- A página da Secretaria foi atualizada depois da mudança do CRAS e do CREAS e manteve o Conselho no 157. Isso indica que o Conselho não acompanhou a mudança.
- **Ressalva.** O Procon entrou no prédio em 17/09/2026, depois da data da fonte (14/07/2026). Nenhuma fonte diz que o Conselho saiu. Por isso a observação da ficha ficou vazia, e o Procon aparece só como ponto de referência.
- **Bairro.** As fontes usam "Jardim Planalto" (página da Secretaria, PMAS e notícias) e "Centro de Caucaia do Alto" (Regimento). Ficou "Jardim Planalto, Caucaia do Alto".

---

## 3. CREAS Cotia (`creas-cotia`)

### Fontes oficiais consultadas

| Data da fonte | Fonte | O que diz | Oficial |
|---|---|---|---|
| 2026-07-14 (modificação) | Página da Secretaria Municipal de Desenvolvimento Social — https://cotia.sp.gov.br/desenvolvimento-social-2025/ | CREAS Cotia: Avenida Professor Manoel José Pedroso, 1565 – Jd. Nomura; tel. 4614-5622. | sim (prefeitura) |
| 2026-06-11 | Notícia "Cotia entra em campo contra o trabalho infantil" — https://cotia.sp.gov.br/cotia-entra-em-campo-contra-o-trabalho-infantil/ | CREAS Cotia: Av. Prof. Manoel José Pedroso, 1.565, 2º andar, Jardim Nomura; fone 4614-5622; e-mail institucional. | sim |
| 2026-05-14 | PMAS 2026–2029, aprovado pela Resolução CMAS nº 298 (arquivo `dados/brutos/pmas-2026-2029_2026-10-19.pdf`, p. 22 do PDF, item 4.8) | "CREAS Central — Avenida Professor Manoel José Pedroso, 1565 – Jardim Nomura — Telefone: 4614-5622". O texto descreve "um equipamento de CREAS na região Central [...] e 1 (uma) unidade Avançada no Distrito de Caucaia". O mesmo PMAS põe o CRAS Central no nº 1565 (p. 15 do PDF, escrito "Avenida Professor José Pedroso"). | sim (CMAS) |
| 2025-08-27 (modificação) | Carta de Serviços ao Usuário — https://cotia.sp.gov.br/carta-de-servico-ao-usuario/ | CREAS Cotia: Rua Água Marinha, 39, Jd. Nomura; tel. 4614-5622. O endereço se repete em todas as seções do CREAS na Carta. | sim, mas desatualizada (ver conclusão) |
| 2025-06-16 e 2025-06-25 | Notícias "Junho Violeta" — https://cotia.sp.gov.br/cotia-participa-de-campanha-nacional-de-enfrentamento-a-violencia-contra-a-pessoa-idosa/ e https://cotia.sp.gov.br/com-previsao-de-chuva-para-o-dia-27-sdsp-adia-mobilizacao-da-campanha-junho-violeta/ | CREAS Cotia: Avenida Professor Manoel José Pedroso, 1565 – Jd. Nomura; tel. 4614-5622. | sim |
| 2025-05-20 (modificação) | Página do Fundo Social — https://cotia.sp.gov.br/fundo-social/ | CREAS Central: avenida Professor Manoel José Pedroso, 1565 – Jd. Nomura. | sim |
| 2024-02-21 | Notícia sobre trabalho infantil (link na seção 1) | CREAS: Av. Prof. Manoel José Pedroso, 1565, Jd. Nomura; tel. 4614-5622. | sim, anterior a 2025 |
| 2022-09-01 | https://cotia.sp.gov.br/agosto-lilas-cotia-participou-de-encontro-regional-de-politicas-para-mulheres-2/ | É a primeira notícia encontrada com o CREAS no nº 1565 (tel. 4614-5622). | sim, histórico |
| 2018-06-15 | https://cotia.sp.gov.br/idosos-sao-tratados-com-carinho-e-respeito-em-cotia/ | "O CREAS fica na Rua Água Marinha, 39, Jardim Nomura". É a notícia mais recente encontrada com esse endereço. | sim, histórico |

### Indícios não oficiais

Nenhum foi encontrado. A busca na web por "CREAS Cotia endereço" não devolveu listagens.

### Conclusão

**Confirmado: Avenida Professor Manoel José Pedroso, 1565, 2º andar, Jardim Nomura**, tel. (11) 4614-5622.

- Seis fontes oficiais de 2025 e 2026 dão esse endereço: a página da Secretaria (jul. 2026), uma notícia (jun. 2026), o PMAS (mai. 2026), duas notícias de junho de 2025 e a página do Fundo Social.
- A Carta de Serviços (modificada em ago. 2025) traz a Rua Água Marinha, 39. É o endereço que a prefeitura publicava até 2018. Desde 2022, todas as outras fontes dão o nº 1565.
- Pela regra da fonte mais recente, vale o nº 1565. A divergência com a Carta ficou registrada na observação.
- O nº 1565 também é o endereço do CRAS Central (PMAS e página da Secretaria). Segundo a notícia de jun. 2026, o CREAS fica no 2º andar.

---

## 4. Unidade Avançada do CREAS — Caucaia do Alto (`creas-caucaia`)

### Fontes oficiais consultadas

| Data da fonte | Fonte | O que diz | Oficial |
|---|---|---|---|
| 2026-07-14 (modificação) | Página da Secretaria Municipal de Desenvolvimento Social — https://cotia.sp.gov.br/desenvolvimento-social-2025/ | "UNIDADE AVANÇADA DO CREAS CAUCAIA DO ALTO — Endereço: Rua Benedito Ferreira das Dores, 289 – Vila Santa Catarina". Sem telefone. O CRAS Caucaia aparece no mesmo endereço, com tel. 4242-1788. | sim (prefeitura) |
| 2026-05-31 | Notícia da inauguração — https://cotia.sp.gov.br/caucaia-do-alto-recebe-centro-humanizado-de-protecao-social-e-amplia-rede-de-atendimento-a-populacao/ | Desde sábado (30/05/2026), o Centro Humanizado de Proteção Social, na Vila Santa Catarina, reúne os atendimentos do CRAS, do CREAS e do Cadastro Único. | sim |
| 2026-05-27 | Notícia de anúncio — https://cotia.sp.gov.br/caucaia-do-alto-ganha-centro-humanizado-de-protecao-social/ | O Centro Humanizado fica na Rua Benedito Ferreira das Dores, nº 289, Vila Santa Catarina. Entre os serviços do local estão o CRAS e o CREAS. | sim |
| 2026-05-14 | PMAS 2026–2029 (p. 23 do PDF, item 4.9) | "Unidade Avançada CREAS — Rua Benedito Pires da Silva Sobrinho, 157 – Jardim Planalto". Sem telefone. Foi aprovado duas semanas antes da inauguração. | sim, superado pelas fontes posteriores |
| 2025-08-27 (modificação) | Carta de Serviços ao Usuário | Unidade Avançada do CREAS: Rua Benedito Pires da Silva Sobrinho, 157 – Jd. Planalto – Caucaia do Alto. Sem telefone. | sim, superada |
| 2025-06-16 e 2025-06-25 | Notícias "Junho Violeta" (links na seção 3) | Unidade Avançada do CREAS Caucaia do Alto: Rua Benedito Pires da Silva Sobrinho, 157 – Jd. Planalto. | sim, superadas |
| 2025-03-14 | https://cotia.sp.gov.br/prefeitura-segue-com-a-obra-de-construcao-do-novo-cras-creas-caucaia-do-alto/ | Obra da nova unidade do CRAS e do CREAS de Caucaia na Rua Benedito Ferreira das Dores, 289. Antes disso, os dois funcionavam em imóvel alugado. | sim |

### Indícios não oficiais

Nenhum foi encontrado. A busca na web por "Centro Humanizado de Proteção Social" devolve resultados de Caucaia, no Ceará.

### Conclusão

**Confirmado: Rua Benedito Ferreira das Dores, 289, Vila Santa Catarina, Caucaia do Alto**, no Centro Humanizado de Proteção Social. A unidade funciona lá desde 30/05/2026.

- O PMAS (14/05/2026) e a Carta de Serviços ainda trazem o nº 157 da Benedito Pires da Silva Sobrinho. As três fontes posteriores (duas notícias de maio de 2026 e a página da Secretaria) trazem o nº 289. Pela regra da fonte mais recente, vale o 289, e a divergência ficou na observação.
- Nenhuma fonte dá telefone próprio da unidade, por isso o campo ficou vazio. O único número no endereço é o do CRAS Caucaia (4242-1788), que não foi usado.
- Atenção a duas grafias parecidas. "Rua Benedito Ferreira das Dores, 289" (endereço novo) e "Rua Benedito Pires da Silva Sobrinho, 157" (endereço antigo) são ruas diferentes. Uma notícia de 13/08/2026 escreve "Rua Benedito Pires das Dores, 289, Planalto", que parece misturar as duas. Para geocodificar, use a grafia da página da Secretaria.

---

## 5. Buscas feitas, com o resultado de cada uma

### API de notícias (posts), filtro `after=2025-01-01`

| Consulta | Notícias | Resultado |
|---|---|---|
| `search=conselho tutelar` | 10 | nenhum endereço de Conselho Tutelar |
| `search=tutelar` | 10 | nenhum endereço de Conselho Tutelar |
| `search=CMDCA` | 12 | nenhum endereço de Conselho Tutelar; endereços dos locais das pré-conferências (não usados) |
| `search=rede de proteção` | 38 | endereço do CREAS Cotia (2025-06 e 2026-06-11) |
| `search=CREAS` | 13 | CREAS Cotia; unidade avançada no 157 (2025-06); Centro Humanizado (2025-03, 2026-05) |
| `search=Caucaia do Alto serviços` | 69 | mudança do Procon para o 157 (2026-09); antigo endereço do Procon (Manoel Ferraz de Almeida, 38) |

### API de notícias sem filtro de data (para achar a fonte oficial mais recente)

| Consulta | Notícias | Resultado |
|---|---|---|
| `search=conselho tutelar` | 61 | as últimas com endereço são de 2024-02-21 e 2024-03-01 |
| `search=4703-1618` | 3 | 2021, 2024-02, 2024-03 |
| `search=4703-5813` | 4 | 2017 a 2021 |
| `search=4242-0110` | 4 | 2020 a 2024-03 |
| `search=4611-1793` | 2 | 2020 e 2021 |
| `search=Jorge Caixe` | 179 | confirma que o nº 306/306-A é o CAC; nenhuma notícia de 2025 ou depois cita o Conselho nesse endereço |
| `search=Benedito Pires da Silva Sobrinho` | 27 | a última citação do CREAS no 157 é de 2025-06; depois, só o Procon (2026-09) |
| `search=Água Marinha` | 16 | a última citação do CREAS nesse endereço é de 2018-06-15 |
| `search=Benedito Ferreira das Dores` | 51 | Centro Humanizado (2026-05 em diante); obra do CRAS/CREAS (2025-03) |
| `search=Centro Humanizado` | 24 | nenhuma notícia cita o Conselho Tutelar no Centro Humanizado |

### API de páginas fixas (pages)

| Consulta | Páginas | Resultado |
|---|---|---|
| `search=conselho tutelar` | 4 | página da Secretaria (fonte escolhida), página do CMDCA, Carta de Serviços |
| `search=tutelar` | 5 | as mesmas |
| `search=CREAS` | 4 | página da Secretaria, Carta de Serviços, Fundo Social |
| `search=desenvolvimento social` | 25 | só a página da Secretaria tem os endereços |
| `search=CMDCA` | 3 | página do CMDCA |

### API de documentos (media)

| Consulta | Arquivos | Resultado |
|---|---|---|
| `search=conselho tutelar` | 21 (2 PDFs de 2025) | Resolução CMDCA 113/2025, com os endereços dos dois Conselhos. O PDF "Substituição membros Conselho Tutelar – CACS" é digitalizado, sem texto, e trata do conselho do FUNDEB, não do Conselho Tutelar. |
| `search=CMDCA` | 86 (73 PDFs de 2025 ou depois) | Atas 261 a 285, resoluções 89 a 128 e editais 2025–2026. Só a Resolução 113 traz endereços. A ata 282 (18/12/2025) fala das linhas telefônicas, sem números. |
| `search=CREAS` | 13 (só imagens) | sem documentos |
| `search=tutelar` | 24 (4 PDFs de 2025) | os PDFs de `conselho tutelar` e as Resoluções CMDCA 92 e 103 (comissões eleitorais), que já estavam no grupo `CMDCA` e não trazem endereço |

No grupo `CMDCA`, o edital da eleição suplementar de 2026 e o edital de 09/02/2026 não trazem o endereço do Conselho Tutelar. Nenhum edital do processo de escolha de 2027 foi encontrado no site.

### Busca geral na web

| Consulta | Resultado |
|---|---|
| "Conselho Tutelar Cotia endereço telefone" | sem resultado (só outras cidades) |
| "Conselho Tutelar Caucaia do Alto endereço" | sem resultado (só Caucaia, no Ceará) |
| "CREAS Cotia endereço Manoel José Pedroso 1565" | sem resultado |
| "Ministério Público SP Cotia rede de proteção conselho tutelar endereço" | sem resultado de MP ou TJ; só PDFs da prefeitura já lidos |
| "Conselho Tutelar" Cotia "Jorge Caixe" 2026 | sem resultado novo |
| "Centro Humanizado de Proteção Social" Caucaia do Alto CREAS | sem resultado (só Caucaia, no Ceará) |
| CadSUAS CREAS Cotia SP endereço equipamento | sem resultado; a consulta pública do CadSUAS é interativa e não foi usada |
| cadastro nacional conselhos tutelares MDHC Cotia SP | sem resultado específico de Cotia |
| CONDECA SP relação conselhos tutelares endereços Cotia | sem resultado; só atas do CMDCA |
| "conselho tutelar" "Benedito Pires da Silva Sobrinho" | sem resultado |
| "CREAS" Cotia "Água Marinha" OR "Manoel José Pedroso" telefone 4614-5622 | sem resultado |
| Cotia conselho tutelar (domínios mpsp.mp.br, tjsp.jus.br, sp.gov.br) | só páginas da prefeitura, já lidas; nada do MPSP nem do TJSP |
| "Conselho Tutelar de Cotia" OR "Conselho Tutelar Caucaia do Alto" … guia | sem resultado em guia comercial |

---

## 6. Pontos para o João decidir

1. **Telefone do CT Cotia.** O CSV traz os dois números, (11) 4703-1618 (página da Secretaria, 2026) e (11) 4703-5813 (Regimento, 2025). Se preferir seguir à risca a regra da fonte mais recente, deixe só o 4703-1618 e mencione o outro na observação.
2. **CT Caucaia e o Procon.** O Procon entrou no prédio do nº 157 em 17/09/2026, depois da fonte que confirma o Conselho (14/07/2026). A ficha ficou sem aviso porque nenhuma fonte diz que o Conselho saiu. Se quiser cautela, a observação pode dizer: "Endereço confirmado em julho de 2026; o prédio passou a abrigar também o Procon em setembro de 2026."
3. **Datas das páginas fixas.** Nas páginas da prefeitura, a data registrada é a da última modificação (2026-07-14), não a de publicação do trecho. Isso deve aparecer na metodologia.

## 7. Achados fora do escopo, que afetam a fase 2b (CRAS)

- **O CRAS Caucaia do Alto mudou.** O endereço em `insumos/territorios-cras.md` e no PMAS (Rua Benedito Pires da Silva Sobrinho, 157) está superado. Desde 30/05/2026, o CRAS funciona na **Rua Benedito Ferreira das Dores, 289, Vila Santa Catarina**, tel. 4242-1788. Fontes: página da Secretaria (mod. 2026-07-14) e notícias de 2026-05-27 e 2026-05-31. A regra da 2b ("vale o Plano 2026") daria um endereço antigo para esse CRAS.
- **Telefone do CRAS Central.** A página da Secretaria (2026-07-14) traz (11) 4616-3191. O PMAS traz 4703-6779 / 4614-0663.
