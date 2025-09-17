
## Contexto
No notebook `xgboost.ipynb` foram identificadas duas camadas distintas de neutralidade aplicadas **em série**:

1. **Neutralidade no dataset (Gold)**  
   Labels multiclasses (−1, 0, +1) já definem a classe **0 (neutro)** a partir do retorno futuro:

   $$
   r_{t,h} = \frac{Close_{t+h} - Close_t}{Close_t}
   $$

   com comparação contra o limiar:

   $$
   \text{limiar}_{t,h} = k_h \cdot \sigma_{t,h}
   $$

   A regra de rotulagem é:

   $$
   y_{t,h} =
   \begin{cases}
   0 & \text{se } |r_{t,h}| \leq k_h \cdot \sigma_{t,h} \\
   +1 & \text{se } r_{t,h} > k_h \cdot \sigma_{t,h} \\
   -1 & \text{se } r_{t,h} < -k_h \cdot \sigma_{t,h}
   \end{cases}
   $$

2. **Neutralidade na decisão do modelo**  
   A regra pós-modelo ignorava $p_0$ (probabilidade da classe 0) e criava uma banda neutra adicional baseada apenas em $p_{\uparrow}$ e $p_{\downarrow}$ com um limiar $\tau$.  
   Isto é, uma **segunda neutralização** aplicada sobre o resultado já multiclasses.

Essa combinação levou a um **inchaço artificial da classe neutra** (proporções muito acima das calibradas no Gold).

---

## Decisão
- **Abandonar** o notebook `xgboost.ipynb` (arquivar como `deprecated`).  
- **Recomeçar** o baseline IBOV com a **Opção A (consistente)**:  
  - Treinar e decidir em **3 classes (↓, 0, ↑)**.  
  - **Decisão final = argmax** entre $p_{\downarrow}, p_{0}, p_{\uparrow}$ após calibração de probabilidades.  
  - **Não** aplicar nova banda neutra que ignore $p_0$.  
  - (Opcional) registrar a **margem de incerteza** $p_{(1)} - p_{(2)}$ apenas para diagnóstico, sem alterar a classe prevista.

---

## Racional
- A classe 0 já foi cuidadosamente definida na etapa Gold via $k_h \cdot \sigma_{t,h}$, calibrada para faixas-alvo de neutros.  
- Reaplicar neutralidade na decisão **duplica o conceito** e distorce a distribuição.  
- Manter a tarefa como **multiclasse pura** melhora a coerência estatística e a interpretabilidade dos resultados.

---

## Ações
1. Arquivar `xgboost.ipynb` como obsoleto.  
2. Criar novo notebook `ibov_baseline_optA.ipynb`.  
3. Reexecutar baseline IBOV sob a **Opção A**.  
4. Atualizar `PROVENANCE_IBOV.txt` documentando esta mudança.

---

## Critérios de Aceitação
- Modelo treinado e avaliado em **3 classes (↓,0,↑)**.  
- Decisão **por argmax** (após calibração).  
- Proporções de 0 (neutro) compatíveis com as obtidas na rotulagem do Gold.  
- MCC macro > 0 em todos os blocos.  
- Acurácia balanceada superior ao baseline trivial.
