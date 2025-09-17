
---


## 1. Normalização dos GOLDs

- **Objetivo**: trazer todas as séries para uma escala comparável, evitando que tickers com preços em faixas diferentes distorçam o aprendizado.
    
- **Ajuste ao projeto**:
    
    - Normalizar **somente os campos numéricos** (`X_0..X_14`, `D+1`, `D+3`, `D+5`).
        
    - Manter as **datas e tickers** intactos.
        
    - Avaliar se a normalização deve ser **por ticker** (cada ativo normalizado no seu range) ou **global** (mesmo scaler para todos).
        

## 2. Split de treino/validação/teste

- **Objetivo**: separar períodos históricos para calibrar e avaliar o modelo.
    
- **Ajuste ao projeto**:
    
    - Usar separação temporal (não aleatória), preservando a ordem das séries.
        
    - Sugestão inicial: **70% treino, 15% validação, 15% teste** por ticker.
        
    - Guardar **datas de corte** para rastreabilidade (reports).
        

## 3. Preparação dos Tensores

- **Objetivo**: transformar cada GOLD em tensores de entrada e saída para a rede LSTM.
    
- **Ajuste ao projeto**:
    
    - `X` → matrizes de shape `(batch, 15, 1)` (janelas temporais).
        
    - `y` → vetores `(batch, 3)` para os três horizontes (`D+1, D+3, D+5`).
        
    - Concatenar todos os tickers em um único dataset ou treinar por ticker — a decidir na fase de design.
        

## 4. Arquitetura LSTM Multiativo

- **Objetivo**: redesenhar a LSTM que você já desenvolveu para suportar:
    
    - Entrada: sequência de 15 valores.
        
    - Saída: vetor de 3 previsões simultâneas.
        
- **Ajuste ao projeto**:
    
    - Usar pelo menos **duas camadas LSTM empilhadas**, seguidas de camadas densas.
        
    - Ativar _multi-output regression_.
        

## 5. Treinamento e Validação

- **Objetivo**: treinar o modelo em todos os tickers, monitorando métricas.
    
- **Ajuste ao projeto**:
    
    - Métricas principais: **MAE, RMSE, R²** (para cada horizonte).
        
    - Treinar com `EarlyStopping` e salvar checkpoints.
        
    - Usar **tensorboard/reports** para armazenar curvas de perda.
        

## 6. Avaliação Final

- **Objetivo**: medir desempenho em dados de teste nunca vistos.
    
- **Ajuste ao projeto**:
    
    - Gerar relatório por ticker e horizonte (`D+1`, `D+3`, `D+5`).
        
    - Comparar métricas com baseline (ex.: previsão de “último valor conhecido”).
        
    - Arquivar resultados em `/reports/avaliacao_lstm_multiativo.md`.
        

## 7. Próximos Relatórios

- **Checklist esperado no Drive**:
    
    - `/reports/normalizacao_scalers.pkl` → guardando os _scalers_ usados.
        
    - `/reports/split_dates.json` → cortes de treino/val/teste.
        
    - `/reports/metrics_lstm_multiativo.csv` → métricas finais.
        
    - `/reports/avaliacao_lstm_multiativo.md` → relatório interpretativo.
        

---

%% **Rodapé de arquivamento**  
ESSE DOCUMENTO GERADO DEVE SER AGRUPADO NA PASTA CHAMADA `/docs/fase0/`.  
E REFERE-SE AO PONTO **F0.3** DO PLANO **MASTER PLAN GPT-5 v2**. %%  

---
