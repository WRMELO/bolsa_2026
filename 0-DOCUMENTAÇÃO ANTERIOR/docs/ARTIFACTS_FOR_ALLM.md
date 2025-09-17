# Artefatos e instruções para AL/LLM — Projeto BOLSA_2026

Este documento descreve, em nível operacional, os artefatos que já existem no workspace e instruções claras sobre quais usar para os próximos passos.

Uso esperado: copie/cole trechos Python nos notebooks ou execute células quando indicado. Não execute comandos de shell sem autorização explícita do operador humano.

---

## Localização principal dos dados e runs

- Bronze (raw Parquet + manifesto):
  - Diretório: `/home/wrm/BOLSA_2026/dados_originais`
  - Manifesto: `/home/wrm/BOLSA_2026/dados_originais/manifesto_dados_originais_3y.csv`

- Silver (normalizados / alinhados) — runs:
  - Run original (problemático): `/home/wrm/BOLSA_2026/intermediarios/silver/run_20250915_114709`
  - Run fix (corrigido): `/home/wrm/BOLSA_2026/intermediarios/silver/run_fixed_20250915_121821`
  - Run promovido (stable): `/home/wrm/BOLSA_2026/intermediarios/silver/run_stable_20250915_152222`
  - Manifesto global atualizado: `/home/wrm/BOLSA_2026/intermediarios/manifesto_silver.csv`
  - Arquivo de proveniência (sugerido/gerado): `.../run_stable_20250915_152222/PROVENANCE.txt`

- Arquivos de apoio e notebooks:
  - Notebook principal de ingestão/execution: `/home/wrm/BOLSA_2026/notebooks/ingesta_executed.ipynb`
  - Scripts auxiliares: `scripts/` (se existirem) e `requirements-*.txt` na raiz

---

## Objetivo imediato para a AL/LLM

1. Validar o `run_stable` recém-promovido como fonte canônica (Silver oficial).
2. Gerar/atualizar artefatos de proveniência (PROVENANCE.txt, manifestos) e criar um relatório de validação por arquivo Parquet.
3. Preparar a etapa Gold (conversão para dataset prontos para modelagem) — listar tarefas necessárias.

As instruções a seguir estão escritas para você executar como LLM-assistant produzindo células Python (o humano executa as células no notebook).

---

## Células / comandos Python sugeridos (copiar/colar no notebook)

1) Resumo rápido dos manifests (compara run antigo x run_fixed x run_stable):

```python
from pathlib import Path
import pandas as pd

runA = Path("/home/wrm/BOLSA_2026/intermediarios/silver/run_20250915_114709")
runB = Path("/home/wrm/BOLSA_2026/intermediarios/silver/run_fixed_20250915_121821")
runStable = Path("/home/wrm/BOLSA_2026/intermediarios/silver/run_stable_20250915_152222")

def read_manifest(p):
    m = p / "manifesto_silver.csv"
    m2 = p / "manifesto_silver_fixed.csv"
    if m.exists():
        return pd.read_csv(m)
    if m2.exists():
        return pd.read_csv(m2)
    return pd.DataFrame()

dfA = read_manifest(runA)
dfB = read_manifest(runB)
dfS = read_manifest(runStable)
print('len A,B,S:', len(dfA), len(dfB), len(dfS))
```

2) Validação por arquivo (gera CSV de relatório):

Use a célula de validação que existe no notebook `ingesta_executed.ipynb` (busque a célula com o título "Validação de Parquets Silver") — ou cole e execute a versão abaixo (ajuste o `MANIFEST_PATH` para o manifesto do run_stable):

```python
# (colar o validador que foi entregue previamente; exemplo resumido abaixo)
MANIFEST_PATH = Path("/home/wrm/BOLSA_2026/intermediarios/silver/run_stable_20250915_152222/manifesto_silver_fixed.csv")
# ... copiar função de validação e executar
```

Saída esperada: um CSV `report_parquet_validation_<ts>.csv` dentro do diretório do run com colunas `ticker,file_path,exists,ok,messages`.

3) Criar/atualizar PROVENANCE.txt (registro de promoção do run)

```python
from pathlib import Path
from datetime import datetime
import getpass, platform

stable = Path("/home/wrm/BOLSA_2026/intermediarios/silver/run_stable_20250915_152222")
prov = stable / "PROVENANCE.txt"
note = f"run_id: {stable.name}\norigin: run_fixed_20250915_121821\npromoted_at: {datetime.now()}\npromoted_by: {getpass.getuser()}@{platform.node()}\n"
prov.write_text(note)
print('Wrote', prov)
```

4) (Opcional) criar `run_stable` como cópia estável e atualizar `intermediarios/manifesto_silver.csv` — já foi feito, mas registrar no Git e no PROVENANCE garante rastreabilidade.

---

## Critérios de aceitação / sucesso

- Validação: pelo menos 90% dos arquivos do `run_stable` devem sair com `ok == True` no relatório (ajustável).
- Todos os arquivos devem conter `date`, `ticker` e ao menos uma coluna de preço (open/high/low/close/adj_close).
- O manifesto global (`/home/wrm/BOLSA_2026/intermediarios/manifesto_silver.csv`) deve conter as mesmas entradas (tickers) que o `run_stable`.
- `PROVENANCE.txt` presente no `run_stable` com timestamp e origem do run.

---

## Artefatos que a AL/LLM pode (e deve) usar para os próximos passos

- `manifesto_dados_originais_3y.csv` — fonte de verdade dos Bronze; usar para reprocessamentos ou auditoria.
- Parquets Bronze em `/home/wrm/BOLSA_2026/dados_originais` — para re-rodagens localizadas (se precisar reparar ticker por ticker).
- `run_fixed_*` — contém a correção aplicada; usar como base para validação e para promover se for correto.
- `run_stable_*` — run promovido; usar como Silver oficial para a etapa de Gold / preparação de features.
- Notebooks em `/home/wrm/BOLSA_2026/notebooks` — especialmente `ingesta_executed.ipynb` que contém funções utilitárias: `enforce_schema_flat`, validação, escrita de parquet e funções de hash.

---

## Próximos passos recomendados (priorizados)

1. Executar a validação completa no `run_stable` e revisar o relatório.
2. Se houver falhas isoladas, reprocessar apenas os tickers afetados (usar o Bronze original e a função `normalize_schema`/`enforce_schema_flat`).
3. Após validação OK, preparar a etapa Gold: (a) consolidar colunas, (b) escolher janela temporal de treino/val/test, (c) exportar dataset model-ready (csv/parquet), (d) acrescentar metadados (manifesto + PROVENANCE).
4. Adicionar uma célula de teste automatizado no notebook que execute validação e falhe claramente se a qualidade for menor que o limiar.

---

Se precisar, eu (AL/LLM) posso:
- gerar as células JSON prontas para inserir no `ingesta_executed.ipynb` (se você preferir que eu edite o notebook direto),
- criar o `PROVENANCE.txt` com detalhes por arquivo (lista de arquivos + hashes),
- preparar o pipeline Gold com a primeira rotina de extração de features.

Indique qual das ações prefere que eu execute: (A) gerar célula JSON no notebook, (B) criar PROVENANCE com hashes, (C) gerar célula de reprocessamento por ticker, (D) preparar skeleton Gold pipeline.
