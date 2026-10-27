# Reconstrução dos insumos a partir de fontes públicas — conferência

Em 2026-10-19 a pasta `insumos/` do Guilherme ainda não tinha chegado. Os insumos foram reconstruídos de fontes públicas e, quando os originais chegaram no mesmo dia, comparados com eles. **Os originais estão em `insumos/` e são a referência.** Esta pasta guarda só a conferência.

| Insumo original | Reconstrução | Resultado |
|---|---|---|
| `insumos/cnes-cotia-saude.csv` | `scripts/coletar_cnes.py` (API do CNES) | Mesmas 39 unidades, mesmas camadas e datas de atualização; maior diferença de coordenada 0,07 m (arredondamento) |
| `insumos/territorios-cras.md` | `territorios-cras-reconstruido.md` (PMAS, p. 14–16 do PDF) | Mesmos 7 territórios, endereços e telefones; as 304 entradas de bairro são idênticas, território a território |
| `insumos/mapa-territorios-cras-pmas-2026.png` | `mapa-territorios-cras-extraido.png` (imagem embutida na p. 14 do PDF) | Mesma imagem, 620 × 526 px; diferenças só de compressão |

O arquivo reconstruído traz informação que não está no original e que será usada nas fases seguintes:

- **Página de cada dado.** O original cita as p. 13–15, pela numeração impressa no rodapé; a reconstrução cita as p. 14–16, pela numeração do arquivo PDF. São as mesmas páginas.
- **Bairros repetidos ou divididos entre territórios.**
  - Repetidos: Jd. Nara Lúcia (2 e 3), Pq. Monjolo (3 e 4) e Santana (2 e 5).
  - Marcados como "(parte)": Pavoeiro (1 e 5) e Lagos (7 e 5).
- **Endereço do CREAS.** O PMAS (p. 22) põe o CREAS Central na Av. Prof. Manoel José Pedroso, 1565, Jd. Nomura. A Carta de Serviços, citada no plano, põe na Rua Água Marinha, 39.
- **Inscritos no CadÚnico por território e faixa etária** (p. 33).
- **Acolhimento.** O PMAS publica os endereços das 2 unidades de acolhimento. Eles foram omitidos de propósito.

Para refazer a extração: `.venv/Scripts/python.exe scripts/extrair_insumos_pmas.py --data 2026-10-19 [--carta]`.
