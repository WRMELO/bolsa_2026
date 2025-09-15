Perfeito — alinhando com sua preferência (direção do movimento > valor exato):

## O LSTM ainda é a melhor técnica?

Para **EOD diário com 15 lags** e sem features ricas, **nem sempre**. Em tabular “rasa” (lags, retornos, rolantes), **árvores impulsionadas** (LightGBM/XGBoost/CatBoost) costumam:

- aprender relações não lineares simples com **menos overfitting**,
    
- treinar **muito mais rápido**,
    
- entregar **boa acurácia direcional** com as features certas.
    

O **LSTM** volta a valer quando:

- há **sequências longas**/multi-resolução (intraday → diário),
    
- queremos **multi-horizontes acoplados** com dependência temporal explícita,
    
- usamos **exógenas sequenciais** (ex.: Brent minuto, dólar, futuros).
    

Como você quer **acertar direção**, recomendo **duas trilhas** em paralelo e comparáveis:

---

## Trilha A — Regressão em retorno (valor relativo) e sinal derivado

**Alvo:** rt+1=Closet+1−ClosetClosetr_{t+1} = \frac{Close_{t+1} - Close_t}{Close_t} (pode usar **log-return** também).  
**Modelo:** LSTM **ou** LightGBM Regressor.  
**Loss:** Huber (robusto).  
**Treino:** só **dias de pregão** (sem FF).  
**Escalas:** X → MinMax (ou Standard), y → Standard (para r).  
**Decisão de direção:** `sign( r̂_{t+1} )` com **limiar morto** ∣r^∣<ε|r̂|<ε → “neutro”.  
**Métrica principal:** **acurácia direcional** (↑/↓), **MCC**, **precision/recall** por classe (↑ e ↓).  
**Por que ajuda?** O modelo aprende **variação**, não nível — reduz a “persistência”.

---

## Trilha B — Classificação direcional pura (sobe/cai[/neutro])

**Alvo:** ycls∈{−1,+1}y_{cls} \in \{-1, +1\} (opcional classe 0 para |r| muito pequeno).  
**Modelo:** **LightGBMClassifier** (baseline fortíssimo) e um **cabeçalho de classificação** em cima do LSTM (multitarefa).  
**Loss:** BCE (ou **Focal Loss** se ↑/↓ desbalanceados).  
**Ponderação:** peso maior para amostras com |r| alto (menos “ruído”).  
**Threshold tuning:** escolher o limiar de prob. que **maximiza MCC** ou o **retorno esperado** sob custos.  
**Por que ajuda?** Otimiza diretamente o que você prioriza: **direção**.

---

## Extra — Multitarefa (o “meio-termo” que costumo preferir)

Um único modelo com **duas saídas**:

- **Cabeça regressão** → rt+1r_{t+1} (Huber).
    
- **Cabeça classificação** → 1[rt+1>0]\mathbb{1}[r_{t+1}>0] (BCE/Focal).
    
- **Loss total:** L=λregLHuber+λclsLBCE\mathcal{L} = \lambda_{reg}\mathcal{L}_{Huber} + \lambda_{cls}\mathcal{L}_{BCE}.  
    Isso força o modelo a captar **valor relativo** e **direção** simultaneamente — costuma melhorar o acerto ↑/↓ sem sacrificar muito a coerência do valor.
    

---

## Regras de dados (para evitar vieses que vimos)

- **Treinar só pregões**; para calendário, **dias sem pregão = regra Δ=0** fora do treino.
    
- **Corte temporal recente** (ex.: 2 anos) para aderir ao **regime atual**.
    
- **Walk-forward “purged”** (expanding window + embargo) ao avaliar.
    
- **Features úteis** (mesmo para árvores):
    
    - retornos rt−kr_{t-k}, **retornos cumulativos** (5/10/20d),
        
    - **volatilidade rolante**, ATR, **z-scores** de retornos,
        
    - razões Close/MAnClose/MA_{n}, **RSI** simples,
        
    - (opcional) exógenas: Brent, USD/BRL, IBOV, setor.
        

---

## Recomendo como próximo passo (objetivo: ganhar na direção)

1. **Criar alvo** rt+1r_{t+1} (e versão com classe ↑/↓/0 com ϵ\epsilon).
    
2. **Treinar LightGBMClassifier** (baseline) para direção em **pregões 2y**.
    
3. Em paralelo, **LSTM multitarefa** (r + classe) nas mesmas janelas/sets.
    
4. **Avaliar**: acurácia direcional, **MCC**, ROC-AUC, precision/recall ↑/↓, e uma **curva acerto vs. limiar**.
    
5. **Escolher limiar** para maximizar **utilidade** (ex.: acerto de altas, ou retorno esperado com custos).
    

Se topar, eu já te entrego a **ETAPA E** com:

- (i) preparo do dataset em **retornos** + rótulo ↑/↓/0,
    
- (ii) **LightGBMClassifier** baseline,
    
- (iii) relatório de **acurácia direcional / MCC / matriz de confusão**,
    
- e (iv) a mesma avaliação aplicada sobre um **LSTM multitarefa** (cabeças gêmeas).
  
  
  
  Entendido. Aqui vai o **resumo de contexto para abertura do novo chat / notebook**, já preparado para que você (ou o modelo) recomece sabendo de onde partir:

---

## Checkpoint de Contexto — Projeto Multiativo (PETR4 e demais 22 tickers)

1. **Estrutura de diretórios no Google Drive**
    
    - Diretório raiz do novo projeto:
        
        ```
        /content/drive/Shared drives/BOLSA_2026/a_projeto_multiativo/LSTM/
        ```
        
    - Subpastas principais:
        
        - `bronze/<TICKER>/...` → dados brutos de leilão (últimos 5 anos).
            
        - `datasets_preparados/` → versões filtradas/transformadas (ex.: pregão, calendário 2 anos).
            
        - `experimentos/` → artefatos de treino/teste (modelos, históricos, predições, relatórios).
            
        - `manifests/` → metadados de runs e SSOT.
            
2. **Dados disponíveis**
    
    - **Base “antiga” calendarizada completa com FF:**
        
        ```
        /content/drive/Shared drives/BOLSA_2026/Projeto_LSTM_Multiativo/gold/PETR4/gold_lag15.parquet
        ```
        
        (equivalente ao usado no notebook original, dá R² ≈0,96 mas com viés de persistência).
        
    - **Bases derivadas preparadas recentemente:**
        
        ```
        /content/drive/Shared drives/BOLSA_2026/a_projeto_multiativo/LSTM/datasets_preparados/PETR4_d1_delta_pregao.parquet
        /content/drive/Shared drives/BOLSA_2026/a_projeto_multiativo/LSTM/datasets_preparados/PETR4_d1_calendario_2anos.parquet
        ```
        
        - `delta_pregao`: só dias de pregão, alvo Δ≠0.
            
        - `calendario_2anos`: recorte temporal para regime recente.
            
3. **Últimos resultados**
    
    - **D+1 Δ-pregão:** R² ~0.997, mas não superou naïve; acerto direcional ~46% (modelo colapsou para “queda constante”).
        
    - **Calendário 2 anos:** R² mais realista (~0.74), baseline naïve ainda superior.
        
    - **Notebook antigo (base completa com FF):** inflava R² (~0.96) mas falhava na direção.
        
4. **Próxima linha de pesquisa**
    
    - **Novo alvo:** retorno percentual
        
        rt+1=Closet+1−ClosetClosetr_{t+1} = \frac{Close_{t+1} - Close_t}{Close_t}
    - **Decisão:** direção = `sign(r_{t+1})` (↑ / ↓), opcional classe “neutro” para |r| < ε.
        
    - **Modelagem recomendada:**
        
        - Baseline: **LightGBMClassifier** (rápido, robusto).
            
        - Alternativa: **LSTM multitarefa** (saída regressão de r + saída classificação ↑/↓).
            
    - **Métrica central:** acurácia direcional, MCC, precision/recall ↑/↓.
        
    - **Regime de dados:** pregões dos últimos 2 anos → mais aderente ao presente.
        

---

👉 Esse é o **estado inicial que o novo chat deve saber**: onde estão os dados, como foram tratados até agora, e qual é o próximo objetivo (sair do valor absoluto para o retorno percentual, focando na direção).

---

Quer que eu já escreva também um **esqueleto inicial de notebook (Markdown + células)** para você colar no novo ambiente e começar direto dessa base?