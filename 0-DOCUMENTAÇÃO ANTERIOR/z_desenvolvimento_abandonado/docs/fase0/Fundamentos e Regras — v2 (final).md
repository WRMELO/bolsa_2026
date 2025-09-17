
---

## 1. Objetivo do Framework

- Desenvolver um sistema disciplinado de decisão **Buy | Hold | Sell** que opere exclusivamente em simulação até cumprir critérios de prontidão.
    
- **Paradigma prediction-first**: todas as decisões são baseadas **somente** nas previsões LSTM D+1, D+3 e D+5 e suas incertezas (intervalos preditivos, quantis, probabilidades direcionais).
    
- **Metas financeiras:**
    
    - Piso de retorno anualizado: **CDI +3%** (mínimo aceitável).
        
    - Meta de retorno anualizado: **~CDI +8%** (objetivo alvo).
        
- **Prioridade absoluta:** preservação do capital e controle de risco. O retorno é consequência de estratégias firmes, coerentes e disciplinadas.
    

---

## 2. Arquitetura de Decisão

O processo decisório é estruturado em **camadas complementares**, formando uma arquitetura híbrida:

1. **Heurística (SCP):** consolida sinais de D+1/D+3/D+5 em score de convicção preditiva.
    
2. **Classificador supervisionado (ML):** identifica padrões não-lineares a partir das previsões e auxilia a refinar sinais.
    
3. **Agente de Reforço (RL - PPO/CPO):** otimiza alocação sequencial e pesos de carteira, respeitando restrições de risco.
    
4. **Camada Bayesiana:** calcula risco de cauda (VaR/ES preditivos) e impõe limites intransponíveis.
    
5. **Ensemble final:** voto ponderado entre as camadas, com **veto de segurança** (hard sempre prevalece).
    

---

## 3. Sistema de Carteira

- Estrutura **fechada**: sempre **10 ativos core**.
    
- **Reservas:** 2–3 ativos em observação contínua (previsões já calculadas).
    
- **Liquidez:** só se compra com caixa oriundo de vendas efetivas.
    
- **Rotatividade disciplinada:** saída de um ativo implica reforço em outro core ou promoção de reserva.
    

---

## 4. Critérios de Veto

### Nível do ativo

- **Hard veto preditivo:** $\text{ES}^{pred}$ acima do limite e coerência negativa nos três horizontes → **venda total**; cooldown = 2 janelas.
    
- **Soft veto preditivo:** PI muito largo, divergência entre horizontes ou edge baixo → **redução parcial (–33% a –50%)**; cooldown = 1 janela.
    

### Nível da carteira

- Soma de $\text{ES}^{pred}$ acima do orçamento → congelar compras e/ou rotacionar piores contribuintes.
    
- Concentração setorial ou correlação excessiva → restrição de novos aumentos.
    

---

## 5. Comparativos e Benchmarks

- Benchmark principal: **CDI**.
    
- Benchmark secundário: carteira de gestor profissional de referência (a definir).
    
- O desempenho será avaliado **ajustado a risco**, não apenas em termos absolutos de retorno.
    

---

## 6. Regras Transversais de Governança

- **Versionamento obrigatório:** dados, modelos, previsões e relatórios.
    
- **Logs diários:** previsões, intervalos, decisões de veto, votos do ensemble, pesos definidos pelo RL.
    
- **Rastreabilidade total:** qualquer resultado deve ser reconstituído a partir de versões.
    
- **Baseline PETR4:** mantido como estudo de caso fixo para calibrar e validar procedimentos.
    

---

%% **Rodapé de arquivamento**  
ESSE DOCUMENTO GERADO DEVE SER AGRUPADO NA PASTA CHAMADA `/docs/fase0/`.  
E REFERE-SE AO PONTO **F0.1** DO PLANO **MASTER PLAN GPT-5 v2**.
 %%


---
