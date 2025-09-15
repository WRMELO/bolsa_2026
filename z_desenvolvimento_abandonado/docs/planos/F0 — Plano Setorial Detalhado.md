
**Mudando para THINKING por comando do usuário.**

Você pediu a **reescrita do F0 — Plano Setorial Detalhado**, agora **coerente com o MASTER PLAN v2 Prediction-First + RL**, e já corrigindo os pontos que evoluímos no chat (abandono da v1, incorporação de RL, foco em previsões D+1/D+3/D+5, ensemble híbrido, soft/hard veto preditivo etc.).

Vou entregar uma versão **sequencial, detalhada, progressiva** que substitui a anteriore está alinhada com a reflexão central do seu documento.

---

# F0 — Plano Setorial Detalhado (versão v2 definitiva)

## 🎯 Objetivo da Fase 0

- Consolidar os **fundamentos conceituais** do projeto, agora sob o paradigma **prediction-first** (decisão baseada nas previsões D+1/D+3/D+5).
    
- Definir como cada camada da arquitetura híbrida (Heurística, ML, RL, Bayesiana, Ensemble) será usada.
    
- Estabelecer as **métricas de risco condicionadas à previsão**, os critérios de soft/hard veto, benchmarks e regras de governança.
    
- Produzir entregáveis documentados que servirão de insumo direto para F1 (Dados & Governança).
    

---

## 📂 Estrutura de F0 (subfases e entregáveis)

### **F0.1 — Regras e Fundamentos Gerais**

**Tarefas**

- Formalizar o paradigma **prediction-first**.
    
- Definir meta/piso: **CDI+3% piso, meta ~CDI+8%**.
    
- Registrar os papéis das camadas (Heurística → ML → RL → Bayesiana → Ensemble).
    
- Documentar a política de OOS: mínimo 6 meses, dados nunca vistos.
    
- Fixar comparações contra **CDI e gestores profissionais**.
    

**Entregável**

- `Fundamentos_e_Regras_v2.md` (substitui v1).
    

**Critério de Aceite**

- Documento validado, com rodapé de arquivamento.
    

---

### **F0.2 — Especificação de Dados**

**Tarefas**

- Definir fontes: sandbox (Yahoo/B3 histórico) e oficiais (B3, APIs).
    
- Granularidade: **EOD (diário)**.
    
- Ajustes: **splits, dividendos, feriados, calendário B3**.
    
- Estrutura de partições: `ticker/year/month`.
    
- Formato: **Parquet particionado**.
    
- Política de snapshots versionados.
    

**Entregável**

- `Especificacao_Dados_v2.md`.
    

---

### **F0.3 — Ferramentas e Abordagem de Modelagem**

**Tarefas**

- Documentar o uso de **LSTM quantílico + MC Dropout** para previsão D+1/D+3/D+5.
    
- Explicar o papel de **classificador supervisionado (ex.: XGBoost)**.
    
- Definir o escopo do **RL (PPO/CPO)**: otimização de alocação multiativo e execução sequencial.
    
- Detalhar a **camada Bayesiana**: VaR/ES preditivos como filtro de risco.
    
- Justificar o ensemble: voto ponderado + veto de segurança.
    

**Entregável**

- `Ferramentas_Modelagem_v2.md`.
    

---

### **F0.4 — Métricas de Risco & Benchmarks**

**Tarefas**

- Migrar métricas para o contexto **preditivo**:
    
    - Volatilidade prevista (σ^h\hat\sigma_h).
        
    - VaRpred_{pred}, ESpred_{pred}.
        
    - Cobertura de intervalos (PI).
        
    - Winkler/CRPS como métricas de calibração.
        
- Definir **soft/hard veto preditivo** (ativo e carteira).
    
- Estabelecer benchmarks: **CDI + carteira profissional de referência**.
    

**Entregável**

- `Metricas_Risco_Benchmarks_v2.md`.
    

---

### **F0.5 — Roteiro de Validação**

**Tarefas**

- Criar checklist de OOS prediction-first (sem vazamento).
    
- Checklist de logs: previsões, distribuições, vetos aplicados, votos do ensemble.
    
- Plano de “cartão vermelho”: se calibração cair (cobertura PI < limiar), **hard veto de modelo** até retreino.
    

**Entregável**

- `Roteiro_Validacao_v2.md`.
    

---

## 📅 Cronograma sugerido (3h/dia, dias úteis)

- **Semana 1:** F0.1 (Fundamentos v2) + início F0.2 (Dados).
    
- **Semana 2:** Concluir F0.2 + F0.3 (Ferramentas híbridas).
    
- **Semana 3:** F0.4 (Métricas preditivas & Benchmarks).
    
- **Semana 4:** F0.5 (Validação) + revisão geral.
    

Entrega final: ~1 mês (≈60h de dedicação vespertina).

---

## 📌 Observações críticas

1. **RL ausente no plano anterior** → agora é **pilar central** da Fase 0: vamos decidir como será treinado, recompensas e restrições.
    
2. **Métricas de risco não podem ser históricas** → agora são **condicionadas às previsões** (VaR/ES preditivo, CRPS, Winkler).
    
3. **Abordagem híbrida está fixada**: heurística (explicável), ML (padrões), RL (sequencial), Bayesiana (confiança), Ensemble (robustez).
    
4. **Rodapé obrigatório de arquivamento** continua regra para este projeto, mas **não faz parte do protocolo global**.
    

---

