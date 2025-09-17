

## 0) Preparação e SSOT
- **Universo**: 24 tickers balanceados + IBOV como referência.  
- **Diretórios padrão**  
  - Raw: `/home/wrm/BOLSA_2026/dados_originais`  
  - Bronze/Silver: `/home/wrm/BOLSA_2026/intermediarios`  
  - Gold: `/home/wrm/BOLSA_2026/gold`  
  - Modelos e artefatos: `/home/wrm/BOLSA_2026/modelos`  
  - Relatórios/plots: `/home/wrm/BOLSA_2026/relatorios`  
- **Manifests e logs**: cada etapa gera `manifesto_*.csv` e usa `tqdm` para acompanhamento.  
- **Execução**: CPU suficiente; GPU apenas acelera tuning. TPU não aplicável.

---

## 1) Coleta e Padronização
- Download de **3 anos** para 24 tickers e o IBOV.  
- Padronização: `date, open, high, low, close, adj_close, volume, ticker`.  
- Calendário unificado de pregões da B3.  
- Manter `close` como base para features; `adj_close` apenas para auditoria.  
- Manifesto: `manifesto_dados_originais_3y.csv`.

---

## 2) Engenharia de Features
- **Preço e volume**: `close, volume`  
- **Retornos**: `ret_1d, ret_3d, ret_5d, ret_10d`  
- **Médias móveis**: `ma_5, ma_10, ma_20`, `ma_5_z`  
- **Bandas**: `bb_pos`  
- **Volatilidades**: `std_ret_10, std_ret_15, std_ret_20`, `atr_pct_14`  
- **Indicadores técnicos**: `rsi_14, %K_14, %D_3`  
- **Com IBOV**: `ibov_ret_1d, ibov_std_15, corr_20_ibov, adj_regime`  
- **Calendário**: `dow, dom, month, is_month_end, is_quarter_end`

---

## 3) Definição dos Labels
Para cada horizonte \( h \in \{1,3,5\} \):

1. **Retorno relativo**:
   $$
   r_{t,h} = \frac{Close_{t+h} - Close_t}{Close_t}
   $$

2. **Volatilidade rolante**: janelas de 10, 15 e 20 pregões.

3. **Zona neutra**:
   $$
   y_{t,h} =
   \begin{cases}
   0 & \text{se } |r_{t,h}| \leq k_h \cdot \sigma_{t,h} \\
   +1 & \text{se } r_{t,h} > k_h \cdot \sigma_{t,h} \\
   -1 & \text{se } r_{t,h} < -k_h \cdot \sigma_{t,h}
   \end{cases}
   $$

4. **Alvo de proporção neutra**:
   - D+1: 45–55%  
   - D+3: 38–45%  
   - D+5: 30–38%  

5. **Ajuste híbrido (opcional)**:
   $$
   \text{limiar}_{ativo,h} = k_h \cdot \sigma_{ativo,h} \cdot \frac{\sigma_{IBOV,h}}{\text{mediana}(\sigma_{IBOV,h})}
   $$

---

## 4) Gold Dataset
- **Grão**: uma linha por ativo por pregão.  
- **Chaves**: `ticker, ref_date`.  
- **Formato**: Parquet particionado.  
- **Campos**: todas as features + labels + retornos auxiliares.  
- **Manifesto Gold**: resumo de datas, linhas e distribuição de classes.

---

## 5) Particionamento Temporal
- Walk-forward em 6–8 blocos.  
- Embargo de pelo menos 5 pregões.  
- Modelos: global (com `ticker` como feature) + teste por ticker.  
- Métricas:  
  - Acurácia balanceada  
  - MCC macro  
  - F1 ↑ / F1 ↓  
  - Hit rate direcional (fora dos neutros)

---

## 6) Modelo Base
- Algoritmo: **XGBoost multiclass (softprob)**.  
- Pesos de classe: punir falsos-↑.  
- Tuning em duas fases: grid + bayesiana (Optuna).  
- Regularização: `lambda, alpha, gamma`.  
- Seleção de features via SHAP.

---

## 7) Calibração e Decisão
- Calibração: Platt ou Isotonic.  
- **Zona neutra probabilística**:
  $$
  \hat{y}_{t,h} =
  \begin{cases}
  0 & \text{se } \max(p_{↑}, p_{↓}) < \tau_h \\
  \arg\max(p_{↑}, p_{↓}) & \text{caso contrário}
  \end{cases}
  $$
- Ajuste de \(\tau_h\) para manter proporção neutra alvo.  
- Matriz de custo assimétrica: falsos-↑ mais caros.

---

## 8) Robustez
- Avaliar por setor e por ativo.  
- Separar regimes (bull, bear, lateral) usando `adj_regime`.  
- Rolling-window das métricas para detectar drift.

---

## 9) Backtest Simples (sem RL)
- Política:  
  - Compra: D+1 ↑ e D+3 ↑ e D+5 ≠ ↓  
  - Venda: D+1 ↓ ou D+3 ↓  
  - Neutro: esperar  
- Métricas: CAGR, vol, Sharpe, Calmar, max drawdown, turnover.  
- Comparação com IBOV buy-and-hold.

---

## 10) Seleção Final
- Critérios:  
  - Acurácia balanceada acima do baseline.  
  - Proporções neutras dentro dos intervalos alvo.  
  - Estabilidade ao longo do tempo.  
  - Backtest com drawdown reduzido.  
- Congelamento de modelos (`modelo_trend_d1.xgb`, etc.), thresholds \(\tau_h\), versão do Gold.

---

## 11) Entregáveis
1. Gold dataset em Parquet.  
2. Modelos calibrados por horizonte.  
3. Relatórios de métricas e backtest.  
4. Documentação reprodutível.

---

## 12) Critérios de Aceitação
- Faixa neutra atingida:  
  - D+1: 45–55%  
  - D+3: 38–45%  
  - D+5: 30–38%  
- Acurácia balanceada superior ao baseline em [INFORMAÇÃO AUSENTE – PRECISAR PREENCHER] pontos.  
- MCC positivo em todos os blocos.  
- Drawdown não pior que benchmark para a mesma exposição média.  
- Reprodutibilidade comprovada.

---
