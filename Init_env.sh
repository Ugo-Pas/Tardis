#!/usr/bin/env bash

# This script must be sourced so the virtualenv activation affects current shell.
if [ "${BASH_SOURCE[0]}" = "$0" ]; then
    echo "Run this with: source ./Init_env.sh"
    exit 1
fi

VENV_DIR="env"
KERNEL_NAME="tardis-env"
KERNEL_DISPLAY_NAME="Python (tardis-env)"

if [ ! -d "$VENV_DIR" ]; then
    python3 -m venv "$VENV_DIR" || {
        echo "Failed to create virtual environment at $VENV_DIR"
        return 1
    }
fi

source "./$VENV_DIR/bin/activate" || {
    echo "Failed to activate virtual environment at ./$VENV_DIR/bin/activate"
    return 1
}

python -m pip install --upgrade pip
python -m pip install -r requirements.txt

# Jupyter kernel setup for this venv
python -m pip install ipykernel
python -m ipykernel install --user --name="$KERNEL_NAME" --display-name="$KERNEL_DISPLAY_NAME"

echo "Environment ready. In VS Code, select kernel: $KERNEL_DISPLAY_NAME"