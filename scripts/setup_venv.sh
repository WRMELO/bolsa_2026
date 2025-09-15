#!/usr/bin/env bash
set -euo pipefail

# Usage: ./scripts/setup_venv.sh [venv_name] [--finance]
VENV_NAME=${1:-.venv}
ARG2=${2:-}
PYTHON=${3:-python3}

FINANCE_FLAG=false
if [ "${ARG2}" = "--finance" ] || [ "${ARG2}" = "finance" ]; then
  FINANCE_FLAG=true
fi

echo "Creating virtual environment at $VENV_NAME using $PYTHON"
$PYTHON -m venv "$VENV_NAME"
source "$VENV_NAME/bin/activate"

echo "Upgrading pip and installing wheel"
pip install --upgrade pip wheel

if [ -f requirements-core.txt ]; then
  echo "Installing core requirements from requirements-core.txt"
  pip install -r requirements-core.txt
else
  echo "requirements-core.txt not found in $(pwd)"
  exit 1
fi

if [ "$FINANCE_FLAG" = "true" ]; then
  if [ -f requirements-finance.txt ]; then
    echo "Installing optional finance requirements from requirements-finance.txt"
    pip install -r requirements-finance.txt
  else
    echo "requirements-finance.txt not found in $(pwd)"
  fi
fi

echo "Installing ipykernel and registering kernel"
python -m ipykernel install --user --name="$(basename $VENV_NAME)" --display-name="Python (project: $(basename $(pwd)))"

echo "Done. To activate: source $VENV_NAME/bin/activate"
