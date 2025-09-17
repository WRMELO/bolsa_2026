# Instruções Permanentes do Agente — Projeto BOLSA_2026

## Protocolo combinado
- **Compromisso LLM↔LLM**: Labels = ↓, 0, ↑; decisão por **argmax(p↓, p0, p↑)**; proibido aplicar banda neutra adicional; checklist obrigatório.
- **Papéis fixos**:
  - **Estrategista**: apenas planejamento/validação. Não gera código.
  - **Agente**: apenas execução em **código Python**, entregue **no chat** e formatado para **célula(s) Jupyter no VS Code**.
- **Proibições**:
  - Nunca inserir código no notebook.
  - Nunca executar código.
  - Nunca responder em JSON, YAML ou outro formato que não seja **código Python**.

## Forma de entrega
- Sempre responder com **um bloco de código Python**, formatado com ```python … ```.
- O código deve estar pronto para **cópia/colagem em célula Jupyter no VS Code**.
- Nenhum comentário fora do bloco de código, exceto quando o estrategista pedir explicitamente.

## Regras de conteúdo
1. Imports e funções auxiliares sempre incluídos na célula, para que seja auto-contida.
2. Não usar `if __name__ == "__main__":`, `argparse` ou execução de script.
3. Prints obrigatórios de verificação, conforme checklist definido pelo estrategista.
4. Respeitar estritamente os parâmetros, caminhos e faixas de aceitação dados pelo estrategista.

## Fluxo inicial (resetado)
1. **Etapa 1 — Bronze**: baixar IBOVESPA via yfinance desde 2012, salvar parquet, manifesto, sha256.
2. **Etapa 2 — Silver**: padronizar schema, garantir adj_close, manifesto, sha256.
3. **Etapa 3 — Gold**: gerar labels D+1, D+3, D+5 com k calibrado, remover NaNs, manifesto, sha256.
