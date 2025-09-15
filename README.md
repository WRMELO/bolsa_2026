# Ambiente virtual para análise financeira

Este repositório contém arquivos para criar um ambiente Python local focado em ciência de dados, visualização e dados financeiros.

Passos rápidos:

1. Crie o venv e instale dependências core (recomendado):

   ./scripts/setup_venv.sh .venv

2. (Opcional) Instale dependências financeiras separadamente — útil quando bibliotecas como `yfinance` exigem compilações nativas:

   ./scripts/setup_venv.sh .venv --finance

2. Ative o ambiente:

   source .venv/bin/activate

3. Abra o projeto no VS Code. O workspace recomenda usar `.venv` como interpretador.

4. Abra `notebooks/01-setup.ipynb` para um teste inicial.

Observações:
- O script registra um kernel Jupyter com o nome do venv.
- Se preferir conda, adapte o script.
