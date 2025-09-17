# 1) Estrutura dos manifestos (campos essenciais)

## 1.1 `manifest_ssot.json` (global)

- `project`/`version`/`created_at`
    
- **Calendário e moeda**: `timezone`, `frequency="D"`, `carry_forward_last_close=true`, `currency="BRL"`, `close_adjusted=true`
    
- **Faixa temporal**: `date_start`, `date_end`
    
- **Fontes e artefatos**:
    
    - `root`, `dir_bronze`, `dir_silver`, `dir_gold`, `dir_ssot`
        
    - `ssot_path` (+ `ssot_md5`)
        
- **Tickers**: lista completa (23)
    
- **Política de atualização**: como atualizar diário (append + FF)
    
- **Auditoria**: por ticker → contagem de deltas `{D+1,D+3,D+5}` e hashes de arquivos de entrada/saída
    
- **Parâmetros comuns**: `lags=15`, `targets=[1,3,5]`
    
- **Proveniência**: quem gerou, versão do notebook, etc.
    

## 1.2 `manifest_gold_<TICKER>.json` (por ticker)

- `ticker`, `lags`, `features` (`X_0..X_14`), `targets` (definição em calendário), `ref_date_col`
    
- **Caminhos**: `silver_input`, `gold_output` (+ MD5)
    
- **Faixa temporal & tamanhos**: linhas, `start`, `end`
    
- **Auditoria**: `{Δ_D1: {1:...}, Δ_D3: {3:...}, Δ_D5: {5:...}}`
    
- **Políticas**: FF aplicado, ajuste de proventos, moeda
    
- **Reprodutibilidade**: `seed_default` (sugerido), `generated_at`
    

## 1.3 `manifest_train_<TICKER>_D+H.json` (por ticker e horizonte)

- `ticker`, `horizon`, `timesteps` (=lags), `seed`
    
- **Dados**: `gold_path`, `ref_date_col`, `feature_cols`, `target_col`, `date_target_col`
    
- **Splits**: datas **explícitas** (por padrão 70/15/15 por calendário, editável)
    
- **Scalers**: política (fit só no train), caminhos esperados
    
- **Modelo**: arquitetura (resumo), otimizador, lrs de fase 1/2, batch, callbacks, épocas
    
- **Saídas esperadas**: diretórios e nomes de artefatos (pesos, histórico, predições, relatório)