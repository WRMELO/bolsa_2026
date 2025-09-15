# Ambiente virtual para análise financeira

Este repositório contém arquivos para criar um ambiente Python local focado em ciência de dados, visualização e dados financeiros.

Passos rápidos:
# Ambiente virtual para análise financeira

Este repositório contém arquivos para criar um ambiente Python local focado em ciência de dados, visualização e dados financeiros.

Quick setup

1. Create a virtualenv (example name `.venv`):

   python -m venv .venv

2. Activate and install core requirements:

   source .venv/bin/activate
   python -m pip install --upgrade pip
   pip install -r requirements-core.txt

3. To install the finance stack as well:

   pip install -r requirements-finance.txt

4. Or install everything:

   pip install -r requirements-full.txt

Note: `pyarrow` is pinned and may already be installed as a wheel; building from source requires system deps (cmake, liblz4-dev, libzstd-dev, etc.) — consider using conda if you need to build from source.
