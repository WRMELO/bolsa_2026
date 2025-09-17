## Metodologia LSTM já desenvolvida (Baseline)

Esta subseção documenta a metodologia LSTM já criada, validada e utilizada como núcleo preditivo do Framework Prediction-First + RL.  

### Escopo
- **Modelo:** LSTM univariado, com previsões independentes em três horizontes (D+1, D+3, D+5).  
- **Baseline:** validado em PETR4, com resultados de alta acurácia e calibração.  
- **Entrada:** janelas deslizantes de 15 dias de preços reais (sem uso de valores previstos).  
- **Saídas:** previsões pontuais e distribuições probabilísticas para cada horizonte.  
- **Normalização:** MinMaxScaler salvo em `.joblib`.  
- **Artefatos:** modelos salvos em `.keras`/`.h5`, previsões consolidadas em `.csv`.

### Arquitetura
- Camada LSTM (64 unidades) → camada densa de saída.  
- Treinamento: 30 épocas, batch size 32, otimizador Adam.  
- Três modelos distintos: `t`, `t+2`, `t+4`.  

### Garantias de realismo
- Nenhum insumo de previsão entra nas janelas; apenas dados reais.  
- Escaler reaplicado corretamente sobre treino+teste.  
- Controle rígido de índices para evitar contaminação.

### Resultados empíricos (PETR4 baseline, OOS)
- **D+1:** R² ≈ 0,987 | Correlação ≈ 0,997 | MAE ≈ 0,56.  
- **D+3:** R² ≈ 0,975 | Correlação ≈ 0,995 | MAE ≈ 0,77.  
- **D+5:** R² ≈ 0,962 | Correlação ≈ 0,991 | MAE ≈ 0,94.  

### Integração no Framework
- O LSTM é o **núcleo preditivo** do sistema.  
- Todas as demais camadas (ML, RL, Bayesiana, Ensemble) consomem estas previsões.  
- A metodologia não será substituída: é o baseline oficial, a ser replicado para todos os tickers da carteira.  
---

%% **Rodapé de arquivamento**  
ESSE DOCUMENTO GERADO DEVE SER AGRUPADO NA PASTA CHAMADA `/docs/fase0/`.  
E REFERE-SE AO PONTO **F0.3** DO PLANO **MASTER PLAN GPT-5 v2**. %%


---