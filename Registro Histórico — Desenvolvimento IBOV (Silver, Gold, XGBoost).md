# Registro Histórico — Desenvolvimento IBOV (Silver, Gold, XGBoost)

**Período do chat:** Setembro/2025  
**Projeto:** BOLSA_2026  
**Ticker:** IBOV (^BVSP)

---

## 1. Silver (Normalização & Features)

- Partimos do Bronze validado (2012-01-03 a 2025-09-19, 3400 linhas).
    
- Aplicamos normalização **min–max [0,1]** em preços (`open`, `high`, `low`, `close`) e transformação log1p em `volume`.
    
- Foram geradas features adicionais:
    
    - `return_1d` (retorno diário).
        
    - `volatility_5d` (desvio-padrão móvel).
        
    - `sma_5`, `sma_20` e `sma_ratio`.
        
- **Validação**: presença de NaNs apenas na cauda, dentro do esperado (ex.: 1 para `return_1d`, 5 para `volatility_5d`, etc.).
    
- Auditoria de hashes (head/tail20) concluída, garantindo unicidade e reprodutibilidade.
    
- **Resultado:** dataset **Silver** consolidado em `/home/wrm/BOLSA_2026/silver/IBOV_silver.parquet`.
    

---

## 2. Gold (Rotulagem)

- Labels contínuos adicionados a partir do Silver:
    
    - `y_h1`, `y_h3`, `y_h5` (retornos acumulados 1, 3 e 5 dias à frente).
        
    - `y_h?_cls`: placeholders para classificação, mantidos em NaN neste estágio.
        
- Distribuição de retornos mostra valores próximos a zero na média, com caudas negativas e positivas, confirmando volatilidade típica.
    
- Persistência efetuada em `/home/wrm/BOLSA_2026/gold/IBOV_gold.parquet` (particionado por `year`).
    
- Validações pós-escrita confirmaram consistência:
    
    - Rows totais: 3400.
        
    - Período: 2012-01-03 a 2025-09-19.
        
    - Caudas de NaN esperadas (1,3,5).
        
- **Resultado:** dataset **Gold** consolidado e pronto para modelagem.
    

---

## 3. Splits Temporais

- Divisão realizada por ano:
    
    - **Train**: 2012–2021 (2470 linhas antes da limpeza).
        
    - **Validação**: 2022–2023 (498 linhas).
        
    - **Teste**: 2024–2025 (432 linhas).
        
- Features (X): `*_norm`, `sma_*`, `sma_ratio`, `volatility_5d`, `return_1d`.
    
- Labels (y): `y_h1`, `y_h3`, `y_h5`.
    
- Splits preparados tanto no formato **tabular** quanto em janelas sequenciais para LSTM (`20, 60, 120`).
    

---

## 4. Primeiras Interações com Modelos

### XGBoost

- Treinado para horizontes h=1,3,5 com early stopping em VAL.
    
- **Resultados VAL:**
    
    - h=1: R² ~0.99 (suspeita de vazamento).
        
    - h=3: R² ~0.10 (leve sinal).
        
    - h=5: R² negativo (pior que baseline).
        
- **Resultados TEST:**
    
    - h=1: R² ~1.0 (confirmado vazamento).
        
    - h=3: R² ~0.07 (ganho marginal).
        
    - h=5: R² negativo.
        
- Importância de features mostrou `return_1d` dominando fortemente, confirmando que o vazamento vinha dessa variável.
    

### Naive (baseline)

- Definição: previsão = 0 (sem retorno esperado).
    
- Resultados mostraram R² ≈ 0 em todos os horizontes, confirmando baseline honesta.
    
- Comparação XGB vs Naive revelou:
    
    - h=1: ΔR² ~ +1 (artificial, por vazamento).
        
    - h=3: ΔR² pequeno, mas positivo.
        
    - h=5: ΔR² negativo (XGB pior que naive).
        

### LSTM

- Backend não estava disponível no ambiente; não foi rodado neste estágio.
    
- Estruturas de janelas já estavam prontas em memória para futura execução.
    

---

## 5. Conclusões Parciais

- **Silver** e **Gold** concluídos com sucesso.
    
- **XGBoost** mostrou desempenho inflado em h=1 devido a `return_1d` (feature com vazamento).
    
- h=3 é o único horizonte com sinal marginal, mas ainda fraco.
    
- h=5 não apresentou valor preditivo.
    
- Próxima etapa definida: **4D-PATCH** → remover `return_1d`, reavaliar XGBoost contra baselines honestos (`naive_rw`, `naive_last`).
    

---

📌 **Checkpoint salvo:** encerramos este chat no ponto em que devemos refazer a modelagem sem `return_1d`, mantendo toda a linha do tempo registrada.

---

Quer que eu também prepare uma versão **curta e cronológica**, tipo linha do tempo com bullets, para ser usada como **timeline rápida de reentrada em novo chat**?