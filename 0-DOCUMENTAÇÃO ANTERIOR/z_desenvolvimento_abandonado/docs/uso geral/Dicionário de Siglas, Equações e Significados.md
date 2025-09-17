


| Sigla / Símbolo | Nome / Equação | Significado e Interpretação | Exemplo Numérico |
|-----------------|----------------|-----------------------------|------------------|
| LSTM | Long Short-Term Memory | Rede neural recorrente para prever séries temporais, captando dependências longas e curtas. | Treinado em preços de PETR4, prevê retornos futuros com base em histórico de 60 dias. |
| D+1, D+3, D+5 | Horizonte de previsão | Previsão do retorno do ativo para 1, 3 ou 5 pregões à frente. | Se PETR4 fecha hoje a R$ 40, previsão D+1 = R$ 40,50 (+1,25%). |
| $\hat{\mu}_h$ | Retorno médio/mediano previsto no horizonte $h$ | Valor central esperado da distribuição preditiva. | Para D+3, $\hat{\mu}_{3} = +0,9\%$. |
| $q_{5\%}, q_{95\%}$ | Quantis previstos (5% e 95%) | Delimitam o intervalo preditivo (PI). | D+1: $q_{5\%} = -1,2\%$, $q_{95\%} = +2,0\%$. |
| PI90 | Intervalo preditivo de 90% | $[q_{5\%}, q_{95\%}]$. Mede a incerteza prevista. | PI90(D+1) = [–1,2%, +2,0%]. |
| $p_h$ | Probabilidade direcional | $\Pr(\Delta_h > 0)$ = probabilidade de alta no horizonte $h$. | D+1: $p_1 = 0,72$ (72% de chance de subir). |
| $\text{VaR}^{pred}_\alpha$ | Value at Risk preditivo | Perda máxima esperada com nível de confiança $\alpha$. | D+1, $\alpha=5\%$: $\text{VaR}^{pred}_{5\%} = -1,5\%$. |
| $\text{ES}^{pred}_\alpha$ | Expected Shortfall preditivo | Perda média esperada, dado que ultrapassa o VaR. | D+1, $\alpha=5\%$: $\text{ES}^{pred}_{5\%} = -2,0\%$. |
| MaxDD | Máx. Drawdown (realizado) | Pior perda acumulada pico-vale da carteira (ex-post). | Carteira foi de +10% para –5% antes de recuperar → MaxDD = –15%. |
| $\hat{\sigma}_h$ | Volatilidade prevista | Desvio padrão dos retornos previstos no horizonte $h$. | D+3: $\hat{\sigma}_3 = 1,1\%$. |
| SCP | Score de Convicção Preditiva | Combina direção, magnitude, probabilidade e incerteza. | A: $\hat{\mu}_1=+0,5\%$, $p_1=0,70$, PI estreito → SCP alto. |
| RL | Reinforcement Learning | Agente que aprende política ótima de alocação sequencial. | Agente decide aumentar PETR4 de 20%→30% porque maximiza retorno ajustado a risco. |
| PPO | Proximal Policy Optimization | Algoritmo de RL estável para políticas contínuas. | Treina agente a ajustar pesos sem grandes saltos entre iterações. |
| CPO | Constrained Policy Optimization | Variante do PPO que impõe restrições explícitas. | Mantém $\text{ES}^{pred}$ da carteira ≤ –8% sempre. |
| Soft veto | Regra de redução parcial | Reduz posição (–33% a –50%) sob incerteza/divergência. | C tem PI90 = [–3%, +4%] → reduz de 25% → 12,5%. |
| Hard veto | Regra de venda total | Zera ativo sob risco de cauda inaceitável e coerência negativa. | B com $\text{ES}^{pred}_{5\%} = -4\%$ → venda total. |
| Cooldown | Período mínimo após venda | Ativo só volta a ser elegível após X janelas semanais. | Hard veto → cooldown 2 semanas; Soft veto → 1 semana. |
| Ensemble | Voto ponderado | Combina sinais de SCP, ML, RL e Bayesiana. | Para A: Heurística=Buy, ML=Buy, RL=Buy → consenso = Buy. |
| Winkler Score | Métrica de intervalo | Penaliza intervalos largos e falhas de cobertura. | PI previsto [–1%, +2%], valor real = +3% → Score ruim. |
| CRPS | Continuous Ranked Probability Score | Mede a qualidade de toda a distribuição prevista. | CRPS baixo → previsão bem calibrada; CRPS alto → distribuição ruim. |
| Cobertura | Taxa de acerto de PI | % de vezes em que o valor real ficou dentro do PI. | Se PI90 cobre 87% dos casos → cobertura próxima da meta (90%). |
