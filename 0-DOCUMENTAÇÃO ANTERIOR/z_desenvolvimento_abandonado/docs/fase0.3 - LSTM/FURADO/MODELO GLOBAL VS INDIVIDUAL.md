
DUVIDA: EU VOU SABER COMO CADA UM DOS TICKERS TERÁ REAGIDO INDIVIDUALMENTE? OU APÓS O MODELAMENTO, VOLTAMOS PARA TESTAR QUAL O COMPORTAMENTO PARA CADA UM? NA PRATICA DO DIA A DIA, UM UNICO MODELO DEVE ATENDER A QUALQUER UM DOS 23 TICKRES?


Resposta direta:

1. **Você vai saber como cada ticker reagiu?**  
    Sim. Mesmo com **um único modelo global**, nós **medimos e registramos desempenho por ticker** (e por horizonte D+1/D+3/D+5). Depois do treino, rodamos inferência em Val/Test **separando por ticker** e geramos um relatório com métricas por ativo.
    
2. **Um único modelo atende a todos os 23 tickers?**
    

- **Na prática, sim** — como baseline. Um modelo global aprende padrões gerais de mercado e costuma **generalizar melhor** que 23 modelos pequenos (evita sobreajuste, usa mais dados, captura regimes amplos).
    
- Para capturar diferenças entre ativos, usamos dois cuidados:
    
    - **Sinalização do ativo** (ex.: um ID/embedding de ticker como feature; se ainda não adicionamos, podemos incluir no próximo ciclo).
        
    - **Avaliação por ticker** para identificar **onde o global vai bem ou mal**. Se alguns forem consistentemente piores, abrimos opções: **fine-tuning por ticker**, **grupos de ativos (clusters)** ou **mixture-of-experts**.
        

3. **Quando e como saber o comportamento individual?**  
    Após o treino do global, executamos a **ETAPA: avaliação por ticker**, que produz, para cada ativo e para cada horizonte:
    

- **MAE, RMSE, MAPE**;
    
- **Calibração** (cobertura de PIs, se estivermos gerando quantis/intervalos);
    
- **Resumo CSV** e ranking de melhores/piores;
    
- (Opcional) gráficos rápidos de resíduos.
    

Resumo da estratégia:

- **Baseline**: **modelo único global**.
    
- **Governança**: **relatório por ticker** sempre.
    
- **Ação corretiva**: só especializamos (fine-tune/experts) se o relatório apontar **laggards** persistentes.
    

Próximo passo (agora): **treinar o LSTM global multi-horizonte** com os tensores prontos. Em seguida, executaremos a **avaliação por ticker** com exportação de métricas para CSV.


FEITO TUDO OS RESULTADO INDIVIDUAIS S FICARAM MUITO RUINS

ADOTADO FAZER INDIVIDUAL

Desnormalizando e avaliando (TEST): 100%|██████████| 23/23 [00:01<00:00, 13.11it/s]

Tabela (R² e MaxRelErr%) salva em: /content/drive/Shared drives/BOLSA_2026/Projeto_LSTM_Multiativo/reports/metrics/metrics_R2_real_TEST_20250912_171121.csv
Tickers selecionados p/ gráficos: ['KLBN11', 'BMOB3', 'RAIZ4']
Figura salva: /content/drive/Shared drives/BOLSA_2026/Projeto_LSTM_Multiativo/reports/figures/curvas_real_vs_prev_KLBN11_TEST_20250912_171121.png
Figura salva: /content/drive/Shared drives/BOLSA_2026/Projeto_LSTM_Multiativo/reports/figures/curvas_real_vs_prev_BMOB3_TEST_20250912_171121.png
Figura salva: /content/drive/Shared drives/BOLSA_2026/Projeto_LSTM_Multiativo/reports/figures/curvas_real_vs_prev_RAIZ4_TEST_20250912_171121.png

Prévia (head) da tabela R²/ErroMax%:

||ticker|split|horizon|R2|MaxRelErr_%|n|
|---|---|---|---|---|---|---|
|0|ABEV3|TEST|D+1|0.335191|7.267644|127|
|1|ABEV3|TEST|D+3|0.869536|6.798348|127|
|2|ABEV3|TEST|D+5|0.812798|9.835609|127|
|3|AGRO3|TEST|D+1|0.616810|5.019796|127|
|4|AGRO3|TEST|D+3|0.618826|6.417080|127|
|5|AGRO3|TEST|D+5|0.516772|6.166079|127|
|6|AURE3|TEST|D+1|0.937919|8.032018|127|
|7|AURE3|TEST|D+3|0.609254|16.900320|127|
|8|AURE3|TEST|D+5|0.683505|14.998726|127|
|9|B3SA3|TEST|D+1|0.564228|16.017648|127|
|10|B3SA3|TEST|D+3|0.685203|15.685489|127|
|11|B3SA3|TEST|D+5|0.432897|14.834861|127|