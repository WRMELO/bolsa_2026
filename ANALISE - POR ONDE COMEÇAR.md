# Análise Detalhada — Por Onde Começar

Segue a análise detalhada, direta ao ponto e alinhada ao seu objetivo (decisão prática). Eu separei em: sumário executivo, achados, problemas detectados (com evidências), hipóteses de causa, correções imediatas e proposta de decisão para o próximo run.

# Sumário executivo

- **Dados/SSOT OK**: IBOV GOLD lido com 3.400 linhas, 2012-01-03 → 2025-09-19.

- **Labels**: D+1/D+3/D+5 gerados (classificação binária por direção do retorno futuro).

- **Validação**: walk-forward com 10 folds (treino expansivo; val 3m; teste 6m).

- **Previsão (teste)**: tanto **XGBoost** quanto **LSTM** ficaram **≈ aleatório** (AUC perto de 0,5) na maior parte das combinações; validação > teste → **instabilidade**.

- **Operacional (teste)**: muitos cenários **sem trades** por threshold alto (hit_rate NaN), e resultados **inconsistentes**; há dobras pontuais boas no XGBoost, mas sem robustez.

- **Estado atual**: **nenhum vencedor válido** foi declarado por **erro no formatter** ao imprimir o “vencedor” (bug de string format); checklist falhou por conta disso — não por falta de métricas.

Minha leitura: com o setup atual (features/labels/thresholds), **não há evidência de alfa estável** out-of-sample. O **XGBoost** se sai “menos mal” que o LSTM, mas ainda **insuficiente** para decisão operacional.

---

# Achados (com evidências do seu log)

1. **Leitura e rótulos**

- Caminho: `/home/wrm/BOLSA_2026/gold/IBOV_gold.parquet` (GOLD).

- `date_min=2012-01-03`, `date_max=2025-09-19`, `rows=3400`.

- Rótulos D+1/D+3/D+5 foram **gerados** (não nativos).

2. **Desempenho de previsão — teste (médias por família)**

- **LSTM** (exemplos):

  - h=1, w=5: AUC_test=0,488; ACC_test=0,488; F1_test=0,261

  - h=3, w=5: AUC_test=0,449; ACC_test=0,463

  - h=5, w=10: AUC_test=0,446; ACC_test=0,447

- **XGBoost** (exemplos):

  - h=1, w=5: AUC_test=0,504; ACC_test=0,495; F1_test=0,166

  - h=3, w=15: AUC_test=0,495; ACC_test=0,494

  - h=5, w=10: AUC_test=0,485; ACC_test=0,476

→ **Todos muito próximos de 0,50** (aleatório) no teste.

3. **Gap val → teste (instabilidade)**

- Várias combinações têm **validação melhor que teste** (ex.: XGB h=5 w=10: val AUC≈0,536 vs test AUC≈0,485; LSTM h=5 w=10: val AUC≈0,572 vs test AUC≈0,446).  
    → Sinal clássico de **overfitting/instabilidade** ou **mudança de regime** entre períodos.

4. **Métricas operacionais (teste)**

- Muitos blocos com **ann_return=0** e **hit_rate NaN** (ex.: LSTM h=1 w=5 em vários folds), indicando **nenhum trade** para o threshold adotado (0,55 ou 0,50).

- Alguns resultados do XGBoost sugerem janelas/folds com Sharpe positivo, mas **não é consistente** ao longo dos folds e horizontes.

- **maxdd** aparece com sinal inconsistente (alguns positivos, outros negativos). Precisamos **padronizar** a convenção (magnitude positiva ou negativa — mas consistente).

5. **Erros e avisos**

- **TensorFlow retracing**: retrabalho de grafo (lento/ruidoso) por construir o modelo na iteração/fold.

- **CUDA init error (303)**: tentativa de inicializar GPU quando indisponível. É só ruído, mas convém silenciar.

- **Bug de formatação**: `Invalid format specifier` ao imprimir hit_rate no resumo do vencedor → travou a seleção final, gerando `CHECKLIST_FAILURE`.

---

# Problemas detectados (evidência → impacto)

1. **Threshold muito alto → nenhum trade**  
    Evidência: muitas linhas com `ann_return=0`, `hit_rate=NaN`, `turnover=0` para LSTM (vários folds).  
    Impacto: **operacional “mudo”**; não há como avaliar estratégia.

2. **Seleção do vencedor quebrou por bug de string**  
    Evidência: `Invalid format specifier '.1% if not pd.isna(top['hit_rate']) ...'`  
    Impacto: **Checklist reprovado** apesar de métricas existirem.

3. **Instabilidade val/teste** (provável overfitting, normalização/feature leakage ou regime shift)  
    Evidência: AUC_val sistematicamente > AUC_test.  
    Impacto: **Generalização fraca**; risco de “ganho de papel”.

4. **Padronização do max drawdown**  
    Evidência: `maxdd` com sinais mistos (às vezes positivo, às vezes negativo).  
    Impacto: dificulta comparar e ordenar cenários.

5. **LSTM configurado de forma “tímida” e pouco diferenciadora**  
    Evidência: features por passo = só 3 (`ret1`, média e desvio 5d), igual para todas janelas; mesma arquitetura em todos os horizontes.  
    Impacto: **LSTM sem insumo rico**, pouca chance de bater XGBoost (e não bateu).

6. **Retracing e GPU noise**  
    Evidência: warnings TF e erro cuInit(303).  
    Impacto: ruído de log, potencial lentidão, mas não muda o resultado.

---

# Hipóteses de causa (prováveis)

- **Thresholds fixos (0,55/0,50)** escolhidos globalmente, sem grid por fold via **validação** → desativa trades em muitos períodos.

- **Calibração de probabilidade ausente** (Platt/Isotonic) → scores mal calibrados, o que estraga a seleção de threshold.

- **Normalização/rolling dentro do fold** pode não estar 100% “leak-safe” (checar se médias/STD são **fitadas só no treino** e aplicadas em val/teste).

- **Features insuficientes** para LSTM (e até para XGB): usar apenas retornos e estatísticas de 5d é pouco; o IBOV tem regimes longos e não-estacionariedades.

- **Folds e blocos temporais**: 6 meses de teste pode ser curto para IBOV em certos regimes; tentar 9–12 meses ajuda a reduzir variância.

- **Classe desbalanceada** (direção do próximo retorno ≈ 50/50, mas com leve viés e autocorrelação baixa); AUC tende a ~0,5 sem features informativas.

---

# Correções imediatas (cirúrgicas, sem voltar ao Bronze)

1. **Consertar o “vencedor” (bug de formatação)**

    - Calcular `hit_rate_display = f"{hit_rate:.1%}"` **apenas se** não for NaN; caso contrário, `"-"`.

    - Separar lógica de formatação da string f-string (nada de condicional dentro do format specifier).

2. **Thresholds data-driven por fold**

    - Para cada modelo/horizonte/janela, **grid** de thresholds em **validação do fold** (p.ex., 0,50→0,70 passo 0,01), selecionando o que maximiza Sharpe (ou retorno com DD limite).

    - **Aplicar o threshold escolhido** no **teste do mesmo fold** (sem recalcular).

    - **Regra de fallback**: if “nenhum trade” → reduzir threshold até o mínimo (0,50) ou adotar **min_trades** por período (ex.: ≥ 4 entradas no semestre).

3. **Padronizar max drawdown**

    - Definir **positiva** (magnitude) ou **negativa** (queda) e manter igual em todos os relatórios. Sugiro **positiva = magnitude do drawdown** (0,00 = sem perda; maior = pior).

4. **Calibração de probabilidades** (XGBoost e LSTM)

    - Em cada fold, **calibrar no conjunto de validação** (Platt/Isotonic conforme amostra).

    - Aplicar calibração congelada no **teste**.

    - Isso melhora muito a escolha de thresholds.

5. **Checagem de vazamento**

    - Garantir que **rolling stats** e **scalers** sejam fitados **exclusivamente** no treino; aplicar em val/teste sem refit.

    - **Z-score** por janela: compute a média/STD **do treino** e aplique adiante.

6. **LSTM: ajustes mínimos**

    - Evitar retracing: construir o grafo/modelo **uma vez por combinação** (fora do loop de batches).

    - Desativar GPU caso não disponível (`tf.config.set_visible_devices([], 'GPU')`).

    - Incluir 1–2 features a mais por passo (ex.: `sma_ratio` 5/20, `volatility_10d`), mantendo o modelo **enxuto**.

7. **Revisar blocos de teste**

    - Teste de **9–12 meses** por fold (em vez de 6) para reduzir variância, mantendo val em 3 meses.

    - Alternativa: **Purged k-fold temporal** (com “gap”) para mitigar overlap.

8. **Relato operacional**

    - Sempre mostrar **n_trades** por fold; se 0, sinalizar explicitamente “sem operações” e aplicar fallback de threshold.

---

# Decisão para o próximo run (pragmática)

- **Mantemos XGBoost como baseline** e **rodamos LSTM enxuto só para comparação**, **após** aplicar as correções acima.

- Critério de vitória **operacional** no período de teste mais recente (fold final):

  - **Sharpe** maior, **DD** padronizado abaixo de um teto (ex.: ≤ 15% anualizado de magnitude), **n_trades** mínimo por semestre (ex.: ≥ 6).

  - Se empatar, vence **menor turnover** (menos custo/fricção).

- Se, mesmo com thresholds calibrados e correções, o LSTM **não bater** o XGBoost **com estabilidade entre folds**, **ficamos com XGBoost**.

---

# O que eu espero ver no próximo relatório (checklist objetivo)

1. **Winner fix**: relatório final com um **vencedor declarado** sem erro de formatação.

2. **Sem “folds mudos”**: n_trades ≥ mínimo em **>80%** dos folds (após grid de thresholds).

3. **Calibração**: curvas de calibração (ou pelo menos Brier score) **por modelo** em validação.

4. **Desempenho teste**: tabelas com **Sharpe, DD, ann_return, n_trades** por fold e agregados; maxdd padronizado.

5. **Estabilidade**: desvio-padrão entre folds **aceitável**; nada de “um fold salva o resto”.

---

# Observação final (importante)

Os números atuais **não justificam** virar money-on-the-line. Eles mostram que a metodologia está **funcionando tecnicamente** (pipeline, validação, métricas), mas **ainda sem alfa estável**. As correções propostas são de **governança e método**, não de “mais dados”: só com **thresholds calibrados**, **probabilidades calibradas**, **min_trades** e **DD padronizado** já dá para ter uma leitura muito mais fiel do que realmente funciona.

Se quiser, eu já deixo **as instruções precisas** para o Agente aplicar **exatamente** as 8 correções acima no próximo run (dry_run novamente).
