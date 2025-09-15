# Objetivo: replicar e validar a metodologia LSTM (baseline PETR4) em 20 tickers da seed list.

---

## Seed list
- [ ] PETR4
- [ ] VALE3
- [ ] ITUB4
- [ ] BBDC4
- [ ] SANB11
- [ ] ABEV3
- [ ] WEGE3
- [ ] KLBN11
- [ ] SUZB3
- [ ] JBSS3
- [ ] B3SA3
- [ ] BPAC11
- [ ] RAIZ4
- [ ] LREN3
- [ ] VIVT3
- [ ] HAPV3
- [ ] TOTS3
- [ ] LWSA3
- [ ] AGRO3
- [ ] BMOB3
- [ ] BLAU3
- [ ] SOJA3
- [ ] AURE3

---

## 1. Preparação
- [x] Definir diretório raiz (`/workspace/lstm_multiativo/`)
- [x] Criar estrutura de pastas por ativo (`/dados/<TICKER>/`, `/modelos/<TICKER>/`)
- [x] Confirmar versões de bibliotecas e fixar seeds de reprodutibilidade

## 2. Ingestão de dados
- [x] Coletar séries históricas (mínimo 5 anos)
- [x] Padronizar schema: Data, Open, High, Low, Close, Volume
- [x] Salvar em parquet (Silver), mantendo Bronze/Silver/Ouro

## 3. Pré-processamento
- [ ] Selecionar `Close` ajustado
- [ ] Ajustar timezone para UTC-3
- [ ] Dividir treino e teste (80/20 ou último ano como teste)
- [ ] Aplicar MinMaxScaler ao treino e salvar por ticker

## 4. Janelamento
- [ ] Criar função para gerar X e y (janelas de 15 dias)
- [ ] Definir saídas D+1, D+3 e D+5 (sem usar previsões no input)

## 5. Treinamento
- [ ] Treinar 3 modelos por ativo (D+1, D+3, D+5)
- [ ] Arquitetura: LSTM(64) → Dense(1)
- [ ] Hiperparâmetros: epochs=30, batch=32, Adam
- [ ] Salvar modelos em `.keras` ou `.h5`

## 6. Inferência e consolidação
- [ ] Rodar previsões no conjunto de teste
- [ ] Consolidar resultados em `previsao_teste_consolidado.csv`
- [ ] Incluir colunas: Data, Previsao_D+1, Previsao_D+3, Previsao_D+5
- [ ] Salvar métricas calculadas

## 7. Avaliação
- [ ] Calcular MAE, RMSE, R², Correlação, Bias
- [ ] Comparar desempenho entre ativos e horizontes
- [ ] Validar consistência geral

## 8. Entregáveis
- [ ] Modelos treinados (3 por ticker)
- [ ] Scalers salvos
- [ ] Previsões consolidadas por ativo
- [ ] Relatório comparativo com métricas
- [ ] Registro de logs/manifests de execução
