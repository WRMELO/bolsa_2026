
**Mudando para THINKING por comando do usuário.**

Você foi direto: quer um desenho completo que **obrigatoriamente** incorpore **RL** e as demais camadas descritas na “Reflexão Representativa”, tratando **decisão** como um problema **prediction-first** (LSTM D+1/D+3/D+5) e não como “análise do passado”. Abaixo está o **MASTER PLAN v2 — Prediction-First + RL** reescrito do zero, fiel ao documento que você apontou e com críticas pontuais onde cabem.

---

# MASTER PLAN v2 — Prediction-First + RL (definitivo)

## 0) Princípios

- **Paradigma:** toda decisão **Buy | Hold | Sell** nasce **exclusivamente** das previsões LSTM D+1/D+3/D+5 e **suas incertezas** (intervalos/quantis).
    
- **Arquitetura híbrida (acoplada, não sequencial):**  
    **(a)** Heurística multi-horizonte (transparência) → **(b)** Classificador ML (padrões não-lineares) → **(c)** **Agente RL** (otimização sequencial de portfólio e execução) → **(d)** Camada Bayesiana de decisão (limiar de confiança) → **(e)** Ensemble de voto com **veto de segurança**. Isso está exatamente no espírito do seu MD.
    
- **Capital fechado:** 10 ativos core + 2–3 reservas; compras só com **caixa de vendas**.
    
- **Risco antes de retorno:** piso **CDI+3%**; meta **~CDI+8%**; **soft/hard veto** condicionados à **distribuição prevista** (não ao histórico).
    
- **Disciplina operacional:** vendas (EOD), compras semanais com mini-janelas anti cash-drag; **cooldown por janelas**.
    
- **Governança:** versionamento de dados/modelos, logs e rastreabilidade total.
    

---

## 1) Camada de Previsão (LSTM multi-horizonte)

**Saídas por ativo:** μ^h\hat\mu_h (média/mediana prevista), **quantis** (q5,q50,q95)(q_{5}, q_{50}, q_{95}), ph=Pr⁡(Δh>0)p_h=\Pr(\Delta_h>0) para h∈{1,3,5}h\in\{1,3,5\}.  
**Como obter incerteza preditiva (obrigatória):**

- **Quantile loss (Pinball)** para treinar quantis e formar **intervalos de previsão** (Winkler/IS depois avalia qualidade). ([Scores](https://scores.readthedocs.io/en/stable/tutorials/Quantile_Interval_And_Interval_Score.html?utm_source=chatgpt.com "Quantile Interval Score and Interval Score — scores 2.2.0 documentation"))
    
- **MC Dropout** em inferência para capturar **incerteza de modelo** (aprox. Bayesiana). ([Proceedings of Machine Learning Research](https://proceedings.mlr.press/v48/gal16?utm_source=chatgpt.com "Dropout as a Bayesian Approximation: Representing Model Uncertainty in Deep Learning"), [arXiv](https://arxiv.org/abs/1506.02142?utm_source=chatgpt.com "[1506.02142] Dropout as a Bayesian Approximation: Representing Model Uncertainty in Deep Learning"))
    

**Crítica pertinente:** sem **distribuições** (e só ponto), não existe controle de cauda/risco ex-ante; por isso quantis/PI são mandatórios.

---

## 2) Calibração Probabilística (gate de segurança)

**Métricas núcleo:** **Cobertura** dos PI (ex.: 90% nominal ≈ 90% observada), **Interval/Winkler Score** e **CRPS** (avalia a distribuição inteira). Se a cobertura degrada (ex.: 90% → 75%), **hard veto de modelo** (congelar compras) até recalibrar. ([Epiforecasts](https://epiforecasts.io/scoringutils/reference/interval_score.html?utm_source=chatgpt.com "Interval score — interval_score • scoringutils"), [Tom Monks](https://tommonks.github.io/forecast-tools/content/02a_coverage_metrics.html?utm_source=chatgpt.com "Evaluating a prediction interval — forecast-tools"), [CRAN](https://cran.r-project.org/web/packages/scoringutils/vignettes/metric-details.html?utm_source=chatgpt.com "Details on the metrics implemented in scoringutils"))

---

## 3) Score de Convicção Preditiva (SCP)

Um **score único** por ativo que entrará no ensemble:

- **Direção:** acordo de sinal em ≥2 horizontes (3/3 = bônus).
    
- **Magnitude:** combinação ponderada de μ^h\hat\mu_h.
    
- **Incerteza:** penalização por **largura do PI**; divergência entre horizontes reduz SCP.
    
- **Probabilidade:** agregação de php_h.
    

> O SCP é a “voz transparente” e dirige a heurística.

---

## 4) Classificador Supervisionado (ML)

**Entrada:** vetor das previsões/quantis/consistência, + auxiliares (vol/liquidez/custos).  
**Saída:** probas para ações {Buy, Hold, Sell}.  
**Papel:** aprender **padrões não-lineares** entre D+1/D+3/D+5 e o que historicamente **funcionou** quando só essas previsões estavam disponíveis (sem olhar futuro).

---

## 5) Camada Bayesiana (limiar de confiança)

Converte distribuição prevista em **probabilidade de perda exceder orçamento** (VaR/ES **preditivos**).

- Se ESpredES^{pred} do ativo **> teto por ativo** → **veto (soft/hard)** antes de qualquer compra.
    
- Na carteira, **soma de ESpred_{pred}** não pode violar orçamento global → congela compras/rotaciona piores contribuições.
    

> VaR/ES **são calculados da distribuição prevista**, não do histórico. (Propriedades de risco de cauda ex-ante).

---

## 6) Agente RL (coração da **otimização sequencial**)

**Papel:** decidir **alocação** e **execução** ao longo do tempo (sequência), **respeitando restrições**.

- **Estado sts_t:** previsões e incertezas por ativo (D+1/D+3/D+5), SCP, probas do classificador, posição atual, caixa, custos estimados, limites e **sinais de veto**.
    
- **Ações ata_t:** vetor de pesos alvo nos 10 ativos + caixa (respeitando limites por ativo/setor/correlação).
    
- **Recompensa rtr_t:** retorno **ajustado a risco** (penaliza MaxDD realizado, turnover e custo), **com restrições duras** (orçamento de ESpred_{pred}).
    
- **Algoritmos:**
    
    - **PPO** para estabilidade e simplicidade. ([export.arxiv.org](https://export.arxiv.org/abs/1707.06347v1?utm_source=chatgpt.com "[1707.06347v1] Proximal Policy Optimization Algorithms"))
        
    - **CPO** quando queremos **garantias de restrição** (ex.: manter ESpred_{pred} ≤ teto a cada passo). ([Proceedings of Machine Learning Research](https://proceedings.mlr.press/v70/achiam17a?utm_source=chatgpt.com "Constrained Policy Optimization"))
        
- **Modo de treinamento:** **offline/OOS**: o agente só enxerga **informação ex-ante**; o “ambiente” usa **retornos realizados** para computar o PnL das ações simuladas (com custos).
    
- **Crítica pertinente:** RL sem **restrições explícitas** tende a “forçar risco” pelo objetivo de retorno; por isso **CPO/penalidades** são parte mandatória. ([arXiv](https://arxiv.org/abs/1705.10528?utm_source=chatgpt.com "[1705.10528] Constrained Policy Optimization"))
    

---

## 7) Ensemble & Veto de Segurança

- **Ensemble de voto ponderado** entre: **Heurística(SCP)**, **Classificador ML** e **RL**.
    
- **Regras:**
    
    - Para **abrir/aumentar** posição: exigir concordância mínima (ex.: 2 de 3) **e** passar na **camada Bayesiana** (confiança).
        
    - **Veto hard** sempre domina: se Bayesiano aponta risco de cauda fora do orçamento, **impede** a ação (inclusive RL).
        
- **Soft/Hard veto preditivo (final):**
    
    - **Soft:** PI largo/divergência de horizontes/edge baixo → **redução de 33–50%** + cooldown 1 janela.
        
    - **Hard:** ESpredES^{pred} > teto **e** coerência negativa nos 3 horizontes → **zerar** + cooldown 2 janelas.
        

---

## 8) Rotina Operacional

- **Diário (EOD):** recalcular previsões/PI; avaliar **soft/hard vetos**; executar vendas (hard = total; soft = parcial).
    
- **Semanal (janela fixa):** ensemble decide **compras/alocações**; **RL** define pesos alvo sob restrições;
    
- **Exceções anti cash-drag:** mini-janela se **cash > 15–20%** ou #ativos < 8.
    
- **Cooldown por janelas:** 1 (soft), 2 (hard); opcional: ampliar se incerteza subir.
    

---

## 9) Backtest Ex-Ante e Calibração Contínua

- **Backtest ex-ante:** toda decisão usa **apenas** informações disponíveis no timestamp.
    
- **Métricas de desempenho:** retorno vs CDI, MaxDD realizado, turnover, custo, **e** qualidade probabilística (**Cobertura/Winkler/CRPS**). ([Epiforecasts](https://epiforecasts.io/scoringutils/reference/interval_score.html?utm_source=chatgpt.com "Interval score — interval_score • scoringutils"), [Tom Monks](https://tommonks.github.io/forecast-tools/content/02a_coverage_metrics.html?utm_source=chatgpt.com "Evaluating a prediction interval — forecast-tools"), [CRAN](https://cran.r-project.org/web/packages/scoringutils/vignettes/metric-details.html?utm_source=chatgpt.com "Details on the metrics implemented in scoringutils"))
    
- **Monitores de drift:** queda de cobertura, PI estreitando/largando demais, dispersão de MC-Dropout/Ensemble subindo; se disparar, **hard veto de modelo**. ([Proceedings of Machine Learning Research](https://proceedings.mlr.press/v48/gal16?utm_source=chatgpt.com "Dropout as a Bayesian Approximation: Representing Model Uncertainty in Deep Learning"))
    

---

## 10) Entregáveis por Fase (resumo enxuto)

- **F1 Dados & Governança:** pipelines, manifests, splits OOS.
    
- **F2 LSTM+Incerteza:** quantis/PI + MC-Dropout; artefatos versionados. ([Proceedings of Machine Learning Research](https://proceedings.mlr.press/v48/gal16?utm_source=chatgpt.com "Dropout as a Bayesian Approximation: Representing Model Uncertainty in Deep Learning"))
    
- **F3 Calibração:** relatórios de Cobertura/Winkler/CRPS e gates. ([Epiforecasts](https://epiforecasts.io/scoringutils/reference/interval_score.html?utm_source=chatgpt.com "Interval score — interval_score • scoringutils"), [CRAN](https://cran.r-project.org/web/packages/scoringutils/vignettes/metric-details.html?utm_source=chatgpt.com "Details on the metrics implemented in scoringutils"))
    
- **F4 SCP & Heurística:** função de score transparente.
    
- **F5 Classificador ML:** probas {B/H/S}, explicabilidade (importâncias/SHAP).
    
- **F6 Camada Bayesiana:** VaR/ES **preditivos** por ativo e carteira.
    
- **F7 RL (PPO/CPO):** política com restrições; simulação OOS; pesos alvo. ([export.arxiv.org](https://export.arxiv.org/abs/1707.06347v1?utm_source=chatgpt.com "[1707.06347v1] Proximal Policy Optimization Algorithms"), [arXiv](https://arxiv.org/abs/1705.10528?utm_source=chatgpt.com "[1705.10528] Constrained Policy Optimization"))
    
- **F8 Ensemble & Veto:** voto ponderado + hard/soft veto final.
    
- **F9 Backtest ex-ante:** relatório de performance + qualidade probabilística.
    
- **F10 Gate:** só avança se **desempenho** + **calibração** passarem.
    

---

## Críticas pertinentes (e por que esta v2 corrige sua “fragilidade” apontada)

1. **RL ausente na v1:** agora ele é **peça central** para **alocação e execução sequencial** — com **CPO** para respeitar restrições de risco **a cada iteração** (e não apenas “em média”). ([arXiv](https://arxiv.org/abs/1705.10528?utm_source=chatgpt.com "[1705.10528] Constrained Policy Optimization"))
    
2. **Decisão realmente prediction-first:** todas as camadas consomem **somente** as previsões/PI; o histórico serve **apenas** para treinar e **auditar a calibração**.
    
3. **Risco de cauda explícito ex-ante:** **VaR/ES preditivos** e **veto Bayesiano** são gates de segurança antes de qualquer ordem.
    
4. **Robustez por diversidade:** Heurística (explicável) + ML (padrões) + **RL** (ótimo sequencial) + veto Bayesiano (segurança) → **reduz overfitting** de qualquer camada isolada — exatamente a “abordagem híbrida” defendida na sua reflexão.
    

---

## Fechamento

Este é o **plano completo** que respeita **o que já está escrito** e coloca **RL** no lugar certo: **otimizador sequencial com restrições**, sob um **ensemble com veto Bayesiano** e **controle de calibração**. Se der ok, prossigo — **aqui no chat** — com a **especificação técnica detalhada do RL (estado/ação/recompensa, PPO vs CPO, restrições implementáveis)** e a **receita de avaliação/calibração**, tudo já alinhado às pastas/dados que você mostrou.