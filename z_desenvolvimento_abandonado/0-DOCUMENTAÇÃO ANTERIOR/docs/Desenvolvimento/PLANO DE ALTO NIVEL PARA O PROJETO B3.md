
# 🗺️ Plano de Alto Nível — Sistema **Previsão → Decisão** de _Buy | Hold | Sell_

> Este documento resume, em passos executáveis, como transformar as previsões LSTM multihorizonte em um **motor de decisão operacional**.  
> Ele serve como roteiro de implementação, documentação para Obsidian e guia de alinhamento entre times.

---

## 1. Objetivo

> **Construir um pipeline diário que recebe dados de mercado, gera previsões para D+1 / D+3 / D+5, consolida múltiplos modelos de decisão (heurístico, ML supervisionado, RL) e devolve uma recomendação Buy | Hold | Sell, monitorada por métricas-chave de retorno e risco.**

---

## 2. Indicadores-meta de sucesso

|Métrica|Meta 12 m|Janela de avaliação|
|---|---|---|
|_Annual Return_|≥ CDI + 3 p.p.|Rolling 12 m|
|_Sharpe Ratio_|≥ 1.0|Mensal|
|_Max Drawdown_|≤ 15 %|Diário|
|_Win Rate_|≥ 55 %|Trade|
|_Profit Factor_|≥ 1.5|Trade|

---

## 3. Visão-geral da Arquitetura





![](../../imagens/Editor%20_%20Mermaid%20Chart-2025-06-27-165741.svg)



---

## 4. Fases de Desenvolvimento

| Fase                              | Objetivo                                                               | Principais Entregáveis                                  | Ferramentas                         |
| --------------------------------- | ---------------------------------------------------------------------- | ------------------------------------------------------- | ----------------------------------- |
| **0. Kick-off**                   | Alinhar escopo, papéis e ambiente                                      | Documento de requisitos, repositório Git                | Obsidian, GitHub                    |
| **1. Ingestão & Storage**         | Pipeline para coletar EOD (End-Of-Day) e armazenar em PostgreSQL/MinIO | Tabela `prices_raw`, rotinas de ETL                     | Python, SQLAlchemy, Airflow/Prefect |
| **2. Previsões LSTM**             | Automatizar inferência diária dos três modelos treinados               | Função `run_lstm_predict()`, tabela `predictions_tbl`   | PyTorch, Jupyter, VS Code           |
| **3. Feature Builder**            | Gerar deltas, slopes, convexidade, volatilidade, etc.                  | Notebook `feature_builder.ipynb`, tabela `features_tbl` | Pandas, NumPy                       |
| **4. Camadas de Decisão**         | Implementar Score, Classificador ML (GBM), Agente RL (PPO)             | Pacotes `score.py`, `ml_classifier.py`, `rl_agent.py`   | Scikit-learn, SB3, MLflow           |
| **5. Ensemble & Regras de Risco** | Voting ponderado, hard-veto de volatilidade                            | Módulo `ensemble.py`, YAML de limiares de risco         | Python                              |
| **6. Backtest & Validação**       | Walk-forward, métricas, stress-test                                    | Relatório `backtest_report.md`, plots                   | VectorBT / Backtrader               |
| **7. Deploy & Monitoramento**     | Agendador diário + dashboard                                           | Job cron/Airflow, painel Grafana ou Streamlit           | Docker, Grafana, Prometheus         |
| **8. Governança & Auditoria**     | Logs, versionamento de dados/modelos                                   | Tabela `decision_log`, modelo MLflow registry           | MLflow, Postgres                    |

---

## 5. Papéis & Responsabilidades

|Papel|Responsável|Missões-chave|
|---|---|---|
|**Product Owner**|Usuário / PMO|Priorizar backlog, validar entregas|
|**Data Engineer**|—|Ingestão, ETL, storage|
|**ML Engineer**|—|Manter modelos LSTM & ML|
|**RL Researcher**|—|Treinar agente PPO/DQN|
|**DevOps**|—|CI/CD, contêineres, monitoramento|
|**QA / Risk**|—|Testes, validação de métricas|

_(“—” indica vagas a definir ou acumuladas por membros atuais.)_

---

## 6. DevOps & Ferramentas

- **Versionamento:** Git + GitHub-Flow
    
- **Contêineres:** Docker-Compose; nomes padrão `projeto-containerA-ingestor-1`, etc.
    
- **Orquestração:** Airflow (ETL & jobs diários) ou Prefect
    
- **Experiment Tracking:** MLflow (param, metrics, artefacts)
    
- **Infra de Log & Métrica:** Prometheus + Grafana, log para PostgreSQL
    
- **Ambientes:**
    
    - _Dev_ — VS Code Remote Containers (CPU)
        
    - _Train_ — Google Colab GPU L4 (montagem Drive obrigatória)
        
    - _Prod_ — Container permanente em servidor (CPU/GPU)
        

---

## 7. Gestão de Risco & Qualidade

1. **Hard-veto** automático se volatilidade 1 d > p95 ou divergência > θ.
    
2. **Testes unitários** para cada módulo (`pytest`).
    
3. **Backtest walk-forward** com _slippage_ e custos B³.
    
4. **Shadow live-tracking** de 30 pregões antes de capital real.
    
5. **Revisão trimestral** dos pesos do ensemble e limiares de risco.
    

---

## 8. Cronograma Macro (exemplo)

|Mês|0|1|2|3|4|5|
|---|---|---|---|---|---|---|
|Kick-off|█||||||
|Ingestão & Storage||█|█||||
|Previsões LSTM||█|█||||
|Feature Builder|||█|█|||
|Camadas de Decisão||||█|█||
|Backtest & Validação|||||█|█|
|Deploy & Monitor.||||||█|

_(“█” = período ativo; ajustar conforme recursos.)_

---

## 9. Próximas Ações Imediatas

1. **Reunião de Kick-off** — validar escopo, times e calendário (⚠️ protocolo de um passo por vez).
    
2. **Configurar repositório Git & estrutura de pastas** (`/data`, `/notebooks`, `/src`, `/docker`).
    
3. **Criar notebook de ingestão inicial** para popular `prices_raw` com histórico PETR4.SA.
    
4. **Documentar variáveis-meta** no vault Obsidian.
    
5. **Definir limiares iniciais de risco** (θ, p95 volatilidade) e registrar em YAML.
    

> **Obs.** Cada etapa de código será entregue em notebooks separados, seguindo o protocolo de execução passo a passo, com barras de progresso `tqdm`, cabeçalhos `# 🔧 ETAPA: …` e impressão de `head(20)` quando novos DataFrames forem criados.

---

_Após concluir essas ações, validamos e avançamos para a Fase 1._