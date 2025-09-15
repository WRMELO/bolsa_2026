# ATA DE DECISÃO — REINÍCIO DO PROJETO (PREVISÕES DIÁRIAS EM CALENDÁRIO)

## 1) Contexto e problema

- As séries usadas em **PETR4** para treinar D+1/D+3/D+5 foram geradas em **dias de pregão** (leilão/úteis), mas o **manifesto** declara **calendário diário com forward-fill**.
    
- Auditoria de deltas mostrou variações (ex.: D+5 com 7–13 dias), evidenciando **inconsistência estrutural** e explicando o **deslocamento visual** e a queda de R².
    

## 2) Conclusão

- O arquivo `gold_lag15.parquet` está **incompatível** com o protocolo (targets em pregões, e não em calendário).
    
- **Decisão**: **refazer a base “ouro” do zero em calendário diário** e **reiniciar** o pipeline de previsão com essa SSOT como fonte única de verdade.
    

## 3) SSOT “OURO” (Single Source of Truth) — desenho

- **Linhas**: datas **em calendário corrido** (freq “D”), cobrindo o intervalo comum aos 23 ativos.
    
- **Colunas por ticker**: `Close_<TICKER>`, `Volume_<TICKER>` (mínimo).
    
- **Preenchimento**: **forward-fill** do último valor válido (sábados, domingos e feriados).
    
- **Validação embutida**: checagem de monotonia do calendário, ausência de buracos e estatísticas básicas por ativo.
    
- **Atualização diária**: append da data nova + FF; SSOT é persistida versionada (parquet).
    

## 4) Geração de alvos e artefatos derivados

- Para cada ticker, gerar **targets em calendário**:
    
    - `D+1 = Close(t+1)`, `D+3 = Close(t+3)`, `D+5 = Close(t+5)`.
        
    - Registrar também `date_D+1 = t+1`, `date_D+3 = t+3`, `date_D+5 = t+5` (delta fixo 1/3/5).
        
- **Lags**: `X_0..X_{L-1}` produzidos **no calendário** (ex.: L=15 → X_0=t-14 … X_14=t).
    
- **Padrão de arquivo por ticker** (para treino/serving): `gold_<ticker>_lag<L>.parquet` (calendário).
    

## 5) Modelagem (política)

- **Single-target por horizonte** (D+1, D+3, D+5), cada um com **scalers, pesos e manifesto próprios** (sem multi-saída, sem loss compartilhado).
    
- **Splits temporais** por datas do calendário (`ref_date`).
    
- **Sem janela deslizante** quando os lags já vierem como colunas (uma linha = um exemplo).
    
- **Manifests imutáveis** registrando: caminho da SSOT, janela de lags, splits, seed, features, targets e artefatos.
    

## 6) Validação e reporting

- Tabela de **validação diária** por data `t`:
    
    - `real(t)`, `estimado_D+1(t)`, `estimado_D+3(t)`, `estimado_D+5(t)`
        
    - Comparação oficial: `estimado_D+h(t)` vs `real(t+h)` (sempre calendário).
        
- **Plots canônicos**: série temporal alinhada por `date_D+h`, dispersão `y_true` vs `y_pred`, resíduos vs tempo.
    
- **Checagem automática de deltas** (devem ser {1,3,5}). Quebra → bloqueio de publicação.
    

## 7) Versionamento, rastreabilidade e disciplina

- **Estrutura de diretórios (sugestão)**
    
    - `/raw/<TICKER>/*.csv` (pregões originais)
        
    - `/ssot/ouro.ssot.parquet` (todos os 23 ativos, calendário diário)
        
    - `/gold/<TICKER>/gold_<TICKER>_lag<L>.parquet` (derivado da SSOT)
        
    - `/manifests/<TICKER>/D+{1|3|5}/manifesto.json`
        
    - `/models/<TICKER>/D+{1|3|5}/…` (pesos, histórico, métricas, predições)
        
- **Regra HF-000 (travada)**: se faltar dado/arquivo → **[INFORMAÇÃO AUSENTE]** e aborta, sem “gap-fill” inventado.
    

## 8) Plano de reinício — etapas (do zero)

**ETAPA 0 — Construção da SSOT OURO (23 ativos)**

1. Ingerir RAW por ticker; normalizar schema (date, close, volume, …).
    
2. Construir **calendário diário** global; fazer join por ticker + **forward-fill**.
    
3. Persistir SSOT (`ouro.ssot.parquet`) + relatório de auditoria.
    

**ETAPA 1 — Derivação GOLD por ticker**  
4. A partir da SSOT, gerar `X_0..X_{L-1}`, `D+1/D+3/D+5`, `date_D+*`.  
5. Persistir `gold_<ticker>_lag<L>.parquet` + checagem de deltas {1,3,5}.

**ETAPA 2 — Treino single-target por horizonte**  
6. Para cada horizonte, scaler/modelo/manifesto próprios; treinar/validar/testar.  
7. Salvar pesos, métricas e predições (com datas).

**ETAPA 3 — Consolidação diária (serving/monitoramento)**  
8. Produzir **tabela diária** `real(t)` + `estimado_D+h(t)`; publicar figuras e métricas.

## 9) Riscos e mitigação

- **Divergências de ajuste (proventos/splits)**: padronizar “Close ajustado” na SSOT.
    
- **Datas faltantes em RAW**: FF resolverá; manter lista de feriados para diagnose.
    
- **Drift**: monitorar MAPE/R² por janela móvel e por regime de volatilidade.
    

---

### Decisão final

- **Aprovar** a reconstrução **SSOT OURO em calendário** e **reiniciar** o pipeline completo a partir das **ETAPAS 0–3** acima.
    
- **Descontinuar** o uso dos `gold_lag15` atuais (em pregões) para modelagem calendarizada.
    

Se concorda, sigo com a **ETAPA 0 — Construção da SSOT OURO** (23 ativos), já entregando o esqueleto de diretórios, schema e a primeira versão do código de consolidação.