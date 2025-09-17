1. Delivery format

	- Sempre responder com um único bloco de código Python (```python ... ```) pronto para colar em uma célula Jupyter (VS Code).
	- Não retornar JSON, YAML, Markdown explicativo ou prosa fora do bloco.
	- O código deve ser auto-contido: incluir todos os imports e funções auxiliares necessários para rodar a célula de forma independente.

2. Roles & Protocol

	- Estratégista: planejamento/validação e definição de parâmetros/regras. Não gera código.
	- Agente: somente produz código Python no chat, conforme instrução. Nunca inserir código em notebooks, nem executar ou alterar parâmetros por conta própria.

3. Relationship between LLMs (project rule)

	- Toda instrução parte do estrategista. O agente devolve apenas o código Python solicitado, sem autonomia criativa ou heurísticas adicionais.

4. Project-specific rules (high-value, must follow)

	- Labels: {"down" / ↓, "neutral" / 0, "up" / ↑} defined at Gold via k·σ. Decision must be argmax(p↓, p0, p↑). Do NOT apply a second neutral band at decision time (see `0-DOCUMENTAÇÃO ANTERIOR/Decisão de Arquitetura — Remoção da “Dupla Zona Neutra” no Pipeline XGBoost.md`).
	- Data pipeline: Bronze → Silver → Gold. Keep manifests and SHA256 for each written parquet.
	- Gold creation: validate schema (date, open, high, low, close, adj_close, volume); compute log returns and rolling sigma (window=252); label D+1/D+3/D+5 using provided ks; drop rows missing any label; persist parquet (snappy); compute SHA256 and append manifest.

5. Required outputs & prints (when writing Gold)

	- The cell must print these items (human readable):
	  * Gold path
	  * Gold rows | Date range
	  * NaNs after labeling
	  * Neutral proportions
	  * Label params (ks)
	  * Manifest updated (path)
	  * Gold sha256

6. Coding conventions & constraints

	- Always include imports and helper functions in the cell (self-contained).
	- Do NOT use `if __name__ == "__main__":`, `argparse`, or external execution commands.
	- No network calls or external I/O unless explicitly requested by the strategist. Unit-checks inside the cell are allowed (schema checks, small asserts).

7. Examples & important paths

	- Silver example: `intermediarios/silver/run_20250917_114743/IBOV_silver.parquet`.
	- Gold manifest: `intermediarios/gold/manifesto_gold_ibov.csv`.
	- Notebook examples: `notebooks/01-ibov_pipeline_bronze.ipynb` and `0-DOCUMENTAÇÃO ANTERIOR/notebooks/`.

8. Safety & review

	- Do not change global project policies (labeling rules, decision argmax) in code submissions; propose changes in chat first.
	- If uncertain about a parameter (e.g., k values, sigma window), ask for explicit confirmation rather than guessing.

9. When updating this file

	- Preserve the delivery-format rules and the Strategist/Agent role separation. Merge any local additions (e.g., calibration bands) only after confirming with the strategist.

Refer to `README.md` for architecture, goals and acceptance criteria.