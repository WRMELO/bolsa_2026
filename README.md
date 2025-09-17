# Projeto BOLSA_2026 — Reinício da Solução

## Contexto
Após a primeira rodada de experimentos com o IBOV (3 anos de dados), identificamos problemas metodológicos:
- **Dupla neutralidade**: o modelo aplicava neutro no dataset e de novo na decisão final, distorcendo as classes.
- **Dados limitados**: 3 anos de IBOV não capturavam regimes de mercado suficientes, causando blocos sem classes completas e métricas instáveis.

Essas lições foram documentadas em `0-documentação-anterior/`.  
A partir de agora, iniciamos um **novo ciclo de solução** dentro do diretório `BOLSA_2026/`.

---

## Nova Arquitetura

### 1. Dados
- **Ampliar horizonte temporal**: usar 8–12 anos de dados (quando disponíveis).
- **Expandir ativos**: após estabilizar IBOV, aplicar em 24 tickers + IBOV.
- **Camadas**:
  - **Bronze**: extração bruta.
  - **Prata**: séries persistidas, alinhadas por pregão/leilão.
  - **Ouro (Gold)**: features técnicas + rótulos (↓, 0, ↑) por horizonte D+1/D+3/D+5.

### 2. Modelagem
- **Classes fixas**: dataset Gold com 3 classes, decisão final sempre = `argmax(p↓, p0, p↑)` (sem banda neutra adicional).
- **Modelos candidatos**: XGBoost (baseline), CatBoost, LogReg multinomial.
- **Métricas**: MCC macro, Acurácia Balanceada, F1(↑), F1(↓), proporção de neutro prevista vs real.

### 3. Política de Negócio
- **Venda compulsória**: alta sensibilidade a sinais de ↓ (preservação de capital).
- **Compra opcional**: exige consistência de ↑ em D+1/D+3, ausência de ↓ em D+5 e expectativa ≥ 8% a.a. pró-rata.
- **Objetivo**: nunca cair abaixo de **+3%**, meta de **+8% a.a.**.
- **Overlay de risco**: CPPI leve, position sizing por volatilidade, “kill switch” em caso de risco de quebra de piso.

---

## Critérios de Aceitação
- **Modelo (técnico)**:
  - MCC macro > 0 em todos blocos.
  - Acurácia Balanceada > trivial.
  - F1(↑), F1(↓) > 0.
- **Política (negócio)**:
  - Nenhuma violação do piso de +3%.
  - Retorno ≥ trajetória de 8% a.a. em rolling 12 meses.
  - Turnover/custos controlados.

---

## Fluxo de Trabalho
- **Um passo por vez**: orientações ao agente sempre incrementais, revisadas antes de execução.
- **Protocolo LLM↔LLM** em vigor:
  - Labels definem neutralidade (proibido redefinir na decisão).
  - Decisão multiclasses = argmax.
  - Checklists obrigatórios antes de concluir uma tarefa.
  - Nenhuma heurística nova sem aprovação explícita no chat principal.

---

## Próximos Passos
1. **Rebuild Gold do IBOV** com mais anos de dados (8–12 anos).
2. **Rodar OptA baseline** no IBOV expandido (walk-forward com embargo + N_min por classe).
3. **Benchmark de modelos** (XGB vs CatBoost vs LogReg).
4. **Incorporação da política de negócio** (venda compulsória, compra opcional, overlay de risco).
5. **Backtest completo** e validação contra critérios de aceitação.

