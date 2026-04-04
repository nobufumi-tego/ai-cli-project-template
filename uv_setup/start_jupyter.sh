#!/usr/bin/env bash
# JupyterLab 起動スクリプト (macOS / Linux)
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# uv を PATH に追加（bashスクリプトでは .bashrc/.zshrc が読まれないため）
export PATH="$HOME/.local/bin:$HOME/.cargo/bin:$PATH"

if ! command -v uv &>/dev/null; then
    echo "[ERROR] uv command not found. Please install uv first." >&2
    echo "  curl -LsSf https://astral.sh/uv/install.sh | sh" >&2
    exit 1
fi

if [ ! -d "$SCRIPT_DIR/.venv" ]; then
    echo "[ERROR] Virtual environment not found. Run install.sh first." >&2
    exit 1
fi

echo "[INFO] Starting JupyterLab..."
echo "[INFO] Press Ctrl+C to stop."
echo ""

cd "$SCRIPT_DIR"
exec uv run jupyter lab
