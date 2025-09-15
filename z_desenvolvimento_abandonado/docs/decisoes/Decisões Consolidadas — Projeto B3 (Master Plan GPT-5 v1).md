
# 10/09/2025 

# Decisões Consolidadas — Projeto B3 (Master Plan GPT-5 v2)

## Premissas Gerais

- Framework em simulação (paper trading) até cumprir critérios de prontidão.
    
- Piso de retorno anualizado: **CDI +3%**.
    
- Meta de retorno anualizado: **~CDI +8%**.
    
- Prioridade absoluta: **minimizar risco de perda**. Ganhos devem vir de estratégias firmes e coerentes.
    
- Decisões sempre **prediction-first**: baseadas em previsões LSTM D+1, D+3 e D+5.
    
- Arquitetura híbrida consolidada: **Heurística (SCP)** → **Classificador ML** → **Agente RL (PPO/CPO)** → **Camada Bayesiana (VaR/ES preditivos)** → **Ensemble de voto com veto de segurança**.
    

## Arquitetura de Carteira

- Sistema fechado: **10 ativos principais (core)**.
    
- Reservas: **2–3 ativos em observação** (sempre com dados e previsões calculadas).
    
- Compras apenas com **caixa proveniente de vendas efetivas**.
    
- Substituição disciplinada: venda de ativo core → reforço em um dos 9 restantes ou promoção de reserva.
    

## Rotina Operacional

### Vendas (diárias)

- Avaliação EOD dos 10 ativos, com base em previsões e métricas de risco preditivas.
    
- **Hard veto preditivo:** risco de cauda fora do orçamento e coerência negativa nos três horizontes → **venda total imediata**. Cooldown = 2 janelas.
    
- **Soft veto preditivo:** alta incerteza ou divergência de horizontes → **redução parcial** (–33% a –50%). Cooldown = 1 janela.
    

### Compras (semanais)

- Análise e alocação **1x por semana** (janela fixa).
    
- Ranking de candidatos: ativos core remanescentes + reservas (fora de cooldown).
    
- Ensemble decide entradas; RL define pesos alvo, respeitando limites de ativo, setor, correlação e custos.
    
- Caixa acumulado distribuído entre os melhores candidatos.
    

### Mini-janelas de exceção

- Disparadas se:
    
    - Caixa > 15–20% do patrimônio, ou
        
    - Número de ativos < 8.
        
- Permitem alocar **parcialmente** o caixa em candidatos fortes, mantendo disciplina.
    

## Cooldown

- **Regra base:** ativo vendido não entra na **primeira janela semanal** após venda.
    
- **Hard veto:** cooldown de **2 janelas**.
    
- **Soft veto:** cooldown de **1 janela**.
    

## Governança

- Reprodutibilidade garantida: versionamento de dados, modelos, previsões e relatórios.
    
- Logs obrigatórios: previsões, distribuições, sinais de veto, decisões do ensemble, votos do RL/ML/heurística.
    
- Rastreabilidade total: todo resultado deve ser reconstruível a partir de versões e manifestos.
    
- PETR4 baseline congelado como estudo de caso.
    

---

%% **Rodapé de arquivamento**  
ESSE DOCUMENTO GERADO DEVE SER AGRUPADO NA PASTA CHAMADA `/docs/decisoes/`.  
E REFERE-SE AO PONTO **F0.1–F0.5** DO PLANO **MASTER PLAN GPT-5 v2**. %%
---
