# 📈 

Este documento define as **métricas de sucesso** utilizadas como critérios de avaliação de desempenho de estratégias financeiras. Todas as métricas abaixo fazem parte do protocolo ativo e são obrigatórias em avaliações finais de modelos.

---

## 🎯 Target Metrics (Metas)
```python
target_metrics = {
    'annual_return': 'CDI + 3%',
    'sharpe_ratio': '> 1.0',
    'max_drawdown': '< 15%',
    'win_rate': '> 55%',
    'profit_factor': '> 1.5'
}
````

---

## 📘 Definição e Interpretação de Cada Métrica

### 📌 `annual_return` — Retorno Anualizado

- **O que é**: Média anual de rentabilidade da estratégia simulada.
    
- **Meta**: Superar o CDI (índice de referência de renda fixa no Brasil) em pelo menos 3 pontos percentuais ao ano.
    
- **Interpretação**: Demonstra o ganho médio esperado em um ano. Um retorno de “CDI + 3%” indica consistência acima do mercado conservador.
    

---

### 📌 `sharpe_ratio` — Índice de Sharpe

- **O que é**: Relação entre retorno excedente e volatilidade (risco).
    
- **Meta**: Superior a 1.0
    
- **Interpretação**: Indica eficiência da estratégia ao gerar retorno ajustado ao risco. Um valor > 1 significa que o risco foi bem recompensado.
    

---

### 📌 `max_drawdown` — Máxima Perda Acumulada

- **O que é**: Maior queda percentual observada entre um topo e um fundo durante a simulação.
    
- **Meta**: Inferior a 15%
    
- **Interpretação**: Mede a pior sequência de perdas. Protege contra estratégias com quedas profundas, mesmo que tenham bom retorno.
    

---

### 📌 `win_rate` — Taxa de Acertos

- **O que é**: Percentual de operações positivas (lucro) em relação ao total.
    
- **Meta**: Superior a 55%
    
- **Interpretação**: Indica a consistência da estratégia. Uma taxa acima de 55% é estatisticamente confiável e acima da aleatoriedade.
    

---

### 📌 `profit_factor` — Fator de Lucro

- **O que é**: Razão entre o total ganho nas operações vencedoras e o total perdido nas operações perdedoras.
    
- **Meta**: Superior a 1.5
    
- **Interpretação**: Para cada 1 real perdido, espera-se ganhar 1,5 ou mais. Representa a robustez e o equilíbrio do sistema como um todo.
    

---

📄 **Versão:** Protocolo V5.1 Universal  
📆 **Data de Consolidação:** 2025-06-25  
👤 **Aplicável a todas as avaliações quantitativas do usuário `wrmelo`**