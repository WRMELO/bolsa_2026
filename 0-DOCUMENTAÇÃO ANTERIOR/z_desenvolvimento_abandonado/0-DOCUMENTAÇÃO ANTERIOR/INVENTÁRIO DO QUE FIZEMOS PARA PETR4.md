\\

# 📑 INVENTÁRIO_PETR4.md

## 🚩 Status: Pipeline PETR4.SA Congelado — Etapas, Função e Localização

Este documento detalha **cada célula do fluxo PETR4**, explicando **o que foi feito**, **para que serve**, **qual artefato gerou** e **onde está salvo**.  
É o checkpoint oficial para iniciar a fase multiativo de forma 100% rastreável.

---

### 1️⃣ Montagem do Drive & Imports

**Função:**  
- Monta `/Projeto_B3` no Google Drive.
- Importa `pandas`, `numpy`, `scipy`, `tqdm`, `Path`.

📂 **Artefato:** Nenhum — pré-requisito de ambiente.

---

### 2️⃣ Criação do Dataset Contínuo

**Função:**  
- Une `original-treino.csv` + `original-teste.csv` para PETR4.
- Cria `Fonte` (`Treino` / `Teste`).
- Gera calendário contínuo `Date` com `Close` forward-filled.

📂 **Salvo em:** `/bases_criadas/features_petr4_diario.csv`

---

### 3️⃣ Feature Builder (Slope, Vol, Zscore)

**Função:**  
- Calcula `slope_15d`, `vol_15d`, `zscore_15d` com janela real de 15 dias.
- Usa `linregress` e `std` seguros para evitar `NaN` indevidos.

📂 **Mantido em:** `/bases_criadas/features_petr4_diario.csv`

---

### 4️⃣ LSTM Multihorizonte

**Função:**  
- Roda janela de 15 dias para prever t, t+2, t+4 (`pred_d1`, `pred_d3`, `pred_d5`).
- Usa scaler específico (`scaler_close_PETR4.joblib`).
- Modelos salvos em formato `.keras`.

📂 **Modelos:**  
- `/modelos/modelo_LSTM_PETR4.keras`
- `/modelos/modelo_LSTM_t2_PETR4.keras`
- `/modelos/modelo_LSTM_t4_PETR4.keras`

📂 **Scaler:** `/scalers/scaler_close_PETR4.joblib`

📂 **Previsões:** `/bases_criadas/predictions_petr4.csv`

---

### 5️⃣ Consolidação Features + Previsões

**Função:**  
- Faz `merge` de `features_petr4_diario.csv` com `predictions_petr4.csv` pela coluna `Date`.

📂 **Salvo em:** `/bases_criadas/final_consolidado_petr4.csv`

---

### 6️⃣ Criação do `Signal` Buy | Hold | Sell

**Função:**  
- Aplica regra de threshold: +0.5% → `Buy`; -0.5% → `Sell`; entre eles → `Hold`.
- Verifica `value_counts` para rastrear distribuição.

📂 **Incluído em:** `/bases_criadas/final_consolidado_petr4.csv`

---

### 7️⃣ Preparação do Dataset X/y

**Função:**  
- Define `X` com features: `Close`, `slope_15d`, `vol_15d`, `zscore_15d`, `pred_d1`, `pred_d3`, `pred_d5`.
- Codifica `y`: `Sell`=0, `Hold`=1, `Buy`=2.
- Remove `NaN` residuais.

📂 **Mantido em memória** para split.

---

### 8️⃣ Split Treino/Teste

**Função:**  
- 70% treino, 30% teste com `stratify` de `Signal`.
- Valida `Fonte` original (`Treino`/`Teste`).

📂 **Mantido em memória.**

---

### 9️⃣ Tuning Final XGBoostClassifier

**Função:**  
- GridSearch com `n_estimators`, `max_depth`, `learning_rate`, `subsample`, `colsample_bytree`.
- Mantém Recall forte em `Sell` (~0.89).
- Matriz de confusão validada.

📂 **Salvo em:** `/modelos/xgb_classifier_petr4.joblib`

---

### 🔟 Logs, Git e Congelamento

**Função:**  
- Logs dos shapes, matriz de confusão, config do `best_estimator_` e métricas salvas.
- Ação recomendada: atualizar `controles/log_arquivos_gerados.csv` e commitar `/models/` no Git.

---

## ✅ Estrutura final de artefatos

```

/Projeto_B3/  
├── bases_criadas/  
	│ ├── features_petr4_diario.csv  
	│ ├── predictions_petr4.csv  
	│ ├── final_consolidado_petr4.csv  
├── modelos/  
	│ ├── modelo_LSTM_PETR4.keras  
	│ ├── modelo_LSTM_t2_PETR4.keras  
	│ ├── modelo_LSTM_t4_PETR4.keras  
	│ ├── xgb_classifier_petr4.joblib  
├── scalers/  
	│ ├── scaler_close_PETR4.joblib  
├── controles/  
	│ ├── log_arquivos_gerados.csv

```

---

## 🟢 Pronto para:

1️⃣ **Travamento oficial PETR4.**  
2️⃣ **Generalização notebook ➜ ticker-agnóstico.**  
3️⃣ **Execução para os outros 9 ativos.**


