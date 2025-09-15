# Relatório do Pipeline de Dados – Projeto LSTM Multiativo (BOLSA_2026)

## 1. Origem dos Dados
Os dados brutos foram obtidos a partir da **B3 (Bolsa de Valores do Brasil)**, em formato diário (EOD – *End of Day*).  
Esses dados incluem informações como **data, preço de fechamento (close), preço de abertura, máxima, mínima, volume** etc.  

---

## 2. Estrutura de Armazenamento no Google Drive
Todo o projeto está organizado dentro do Google Drive em:

```
/content/drive/Shared drives/BOLSA_2026/Projeto_LSTM_Multiativo/
```

Com as seguintes pastas principais:

- **bronze/** → onde inicialmente seriam salvos os dados crus (*raw*).  
- **silver/** → dados padronizados e limpos, armazenados por ticker em formato `parquet`.  
- **gold/** → dados finais preparados para modelagem preditiva.  
- **reports/** → relatórios, validações e outputs auxiliares.

---

## 3. Camada Silver
Para cada ticker da *seed list* oficial, foi criado um arquivo em:

```
/silver/<TICKER>/eod.parquet
```

Exemplo:  
- `silver/PETR4/eod.parquet`  
- `silver/VALE3/eod.parquet`

### Estrutura típica de colunas em cada Silver:
- `date` → data da observação (datetime).  
- `close` → preço de fechamento ajustado.  
- `adj_close`, `high`, `low`, `open`, `volume` → demais campos auxiliares.  
- `date_local`, `ticker`, `tz` → metadados.

Esses arquivos já estavam prontos antes do início do trabalho com GOLD.

---

## 4. Camada Gold
O objetivo foi transformar cada série temporal em um conjunto de treinamento adequado para modelos de Deep Learning (ex.: LSTM).

Cada arquivo GOLD é salvo em:

```
/gold/<TICKER>/gold_lag15.parquet
```

### Estrutura das colunas no GOLD:
- **Independentes (features)**  
  `X_0, X_1, ..., X_14` → 15 últimos preços de fechamento consecutivos.

- **Alvos (targets)**  
  `D+1`, `D+3`, `D+5` → valores reais do fechamento futuro em 1, 3 e 5 pregões à frente.

- **Datas de referência**  
  `ref_date` → data correspondente a `X_14`.  
  `date_D+1`, `date_D+3`, `date_D+5` → datas reais dos alvos.

- **Identificação**  
  `ticker` → código do ativo.

### Regras aplicadas:
- **Janela (lag)** de 15 dias.  
- **Horizontes de previsão**: 1, 3 e 5 pregões futuros.  
- **Sobrescrita habilitada**: arquivos antigos em GOLD foram substituídos.  
- **Barra de progresso (`tqdm`)** usada no loop de geração.  

---

## 5. Seed List Oficial
Conjunto de ativos processados:

```
PETR4, VALE3, ITUB4, BBDC4, SANB11, ABEV3, WEGE3, KLBN11, SUZB3, BRFS3,
B3SA3, BPAC11, RAIZ4, LREN3, VIVT3, HAPV3, TOTS3, LWSA3, AGRO3, BMOB3,
BLAU3, SOJA3, AURE3
```

---

## 6. Estado Atual
- Todos os tickers da seed list possuem agora um arquivo GOLD unificado pronto.  
- Cada GOLD contém uma tabela completa e autocontida, adequada para alimentar modelos de séries temporais (LSTM ou similares).  
- O pipeline está, portanto, pronto para a **etapa de pré-processamento para treino do LSTM**.

---

%% ## Rodapé de Arquivamento
**Projeto:** BOLSA DE VALORES EM 2026  
**Pipeline:** Bronze → Silver → Gold  
**Documento:** relatorio_pipeline_gold.md  
**Local de Arquivamento:** `/fase0.3-LSTM/` dentro de  
`/content/drive/Shared drives/BOLSA_2026/Projeto_LSTM_Multiativo/`  
**Data de geração:** 12/09/2025  %%


---
