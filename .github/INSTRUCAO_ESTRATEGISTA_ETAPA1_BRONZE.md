# ESTRATEGISTA: INSTRUÇÃO PARA AGENTE – ETAPA 1 (BRONZE)

Objetivo: preparar uma célula Python que baixe a série histórica do índice IBOV (^BVSP) desde 2012-01-01 até a data atual, normalize o schema para Bronze e execute em modo dry_run.

Regras obrigatórias (não negociar):

1) Papéis
   - Estrategista: planeja e valida. Não gera código.
   - Agente: entrega apenas código Python pronto para colar em uma célula Jupyter.

2) Cabeçalho obrigatório
   - Todo texto desta instrução deve começar com exatamente o cabeçalho acima: "ESTRATEGISTA: INSTRUÇÃO PARA AGENTE – ETAPA 1 (BRONZE)".

3) Parâmetros e comportamento
   - Fonte: Série histórica do índice IBOV (^BVSP) desde 2012-01-01 até a data atual (runtime).
   - Schema fixo (exato, nessa ordem): date, open, high, low, close, volume
   - Descartar permanentemente qualquer coluna `adj_close`.
   - Colunas de preço (open, high, low, close) devem ser numéricas e sem timezone. Data em coluna `date` sem timezone (datetime64[ns]).
   - timezone: garantir UTC ou remover timezone info. A coluna `date` deve conter timestamps localizados em UTC ou tz-naive (preferencialmente tz-naive em UTC instant).

4) Execução inicial
   - `dry_run=True` por padrão na célula. Quando `dry_run=True` a célula NÃO deve persistir nenhum arquivo em disco.
      - Em dry_run a célula deve imprimir:
         - um `df.head()` (mostrando as primeiras linhas)
         - `df.info()` (para validar tipos e ausência de timezone)

5) Comentários no código
   - Incluir comentários marcando claramente onde a persistência em Bronze (CSV/Parquet) será ativada no futuro, com instruções para:
   - validar schema
   - escrever parquet com compressão snappy
   - gerar manifesto e SHA256

6) Segurança e reproduzibilidade
   - Não realizar chamadas de rede inseguras além do download do dado autorizado.
   - Não persistir credenciais ou tokens.

7) Formato de entrega do agente
   - O agente deve devolver um bloco de código Python pronto para colar em uma célula Jupyter.
   - O código deve ser auto-contido: incluir os imports necessários e parâmetros.
   - NÃO incluir `if __name__ == "__main__":` ou `argparse`.

8) Observação final
   - Esta instrução assume que o projeto está na Etapa 1 (Bronze). A criação de Silver/Gold seguirá regras diferentes e só será executada após validação do Bronze.

---

Instrução pronta. Agent: gerar agora a célula Python conforme especificado (dry_run=True). Se desejar que eu formate esta instrução no estilo final do `.github/copilot-instructions.md`, responda indicando "formatar".
