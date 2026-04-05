#!/usr/bin/env bash
# =============================================================================
# ML Environment Installer for macOS / Linux
# Uses: uv (https://github.com/astral-sh/uv)
# =============================================================================
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_DIR="$SCRIPT_DIR/.venv"

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

info()    { echo -e "${GREEN}[INFO]${NC}  $*"; }
warn()    { echo -e "${YELLOW}[WARN]${NC}  $*"; }
error()   { echo -e "${RED}[ERROR]${NC} $*" >&2; exit 1; }

echo "============================================="
echo "  Python ML Environment Setup (uv)"
echo "============================================="
echo ""

# ── 1. uv のインストール確認 / インストール ──────────────────────────────────
if command -v uv &>/dev/null; then
    info "uv is already installed: $(uv --version)"
else
    info "Installing uv..."
    curl -LsSf https://astral.sh/uv/install.sh | sh

    # PATH に追加（カレントシェルへの即時反映）
    export PATH="$HOME/.cargo/bin:$HOME/.local/bin:$PATH"

    if ! command -v uv &>/dev/null; then
        error "uv installation failed. Please install manually: https://docs.astral.sh/uv/getting-started/installation/"
    fi
    info "uv installed successfully: $(uv --version)"
fi

# ── 2. システムライブラリのインストール ──────────────────────────────────────
# LightGBM / XGBoost が必要とする OpenMP ライブラリを確認・インストール

if [[ "$(uname)" == "Linux" ]]; then
    info "Checking system libraries for Linux..."

    if ! ldconfig -p 2>/dev/null | grep -q "libgomp.so.1"; then
        warn "libgomp.so.1 not found. Installing..."

        if command -v apt-get &>/dev/null; then
            sudo apt-get update -qq
            sudo apt-get install -y -qq libgomp1
        elif command -v dnf &>/dev/null; then
            sudo dnf install -y libgomp
        elif command -v yum &>/dev/null; then
            sudo yum install -y libgomp
        elif command -v pacman &>/dev/null; then
            sudo pacman -S --noconfirm gcc-libs
        else
            warn "Could not auto-install libgomp. If LightGBM fails, run:"
            warn "  sudo apt-get install libgomp1   # Ubuntu/Debian"
            warn "  sudo dnf install libgomp        # Fedora/RHEL"
        fi
    else
        info "libgomp.so.1 found."
    fi

elif [[ "$(uname)" == "Darwin" ]]; then
    info "Checking system libraries for macOS..."

    # LightGBM は libomp (LLVM OpenMP) を必要とする
    if ! brew list libomp &>/dev/null 2>&1; then
        if command -v brew &>/dev/null; then
            warn "libomp not found. Installing via Homebrew..."
            brew install libomp
        else
            warn "Homebrew not found. If LightGBM fails, install Homebrew then run:"
            warn "  brew install libomp"
        fi
    else
        info "libomp found."
    fi
fi

# ── 3. Python バージョン確認 ─────────────────────────────────────────────────
PYTHON_VERSION="3.12"
info "Using Python $PYTHON_VERSION"

# ── 4. 仮想環境の作成 ────────────────────────────────────────────────────────
if [ -d "$VENV_DIR" ]; then
    warn "Virtual environment already exists at $VENV_DIR"
    read -rp "Recreate? [y/N]: " answer
    if [[ "$answer" =~ ^[Yy]$ ]]; then
        rm -rf "$VENV_DIR"
        info "Removed existing virtual environment."
    else
        info "Keeping existing environment. Running sync..."
    fi
fi

cd "$SCRIPT_DIR"

if [ ! -d "$VENV_DIR" ]; then
    info "Creating virtual environment with Python $PYTHON_VERSION..."
    uv venv --python "$PYTHON_VERSION" "$VENV_DIR"
fi

# ── 5. パッケージのインストール ──────────────────────────────────────────────
info "Installing packages (this may take 10-30 minutes)..."
info "PyTorch is large (~2GB). Please wait..."
echo ""

uv pip install --python "$VENV_DIR/bin/python" \
    "jupyterlab>=4.0" "ipywidgets>=8.0" "ipykernel>=6.0" \
    "numpy>=1.26" "pandas>=2.0" "polars>=0.20" \
    "scikit-learn>=1.4" "xgboost>=2.0" "lightgbm>=4.0" \
    "torch>=2.2" "torchvision>=0.17" \
    "matplotlib>=3.8" "seaborn>=0.13" "plotly>=5.18" \
    "tqdm>=4.66" "joblib>=1.3" "scipy>=1.12" \
    "japanize-matplotlib>=1.1"

# インストール確認
if [ ! -f "$VENV_DIR/bin/jupyter" ]; then
    error "jupyter not found after installation. Please re-run this script."
fi

# ── 6. 起動スクリプトに実行権限を付与 ───────────────────────────────────────
chmod +x "$SCRIPT_DIR/start_jupyter.sh"

# ── 7. Jupyterカーネル登録 ───────────────────────────────────────────────────
info "Registering Jupyter kernel..."
"$VENV_DIR/bin/python" -m ipykernel install --user --name ml-env --display-name "Python (ML)"

# ── 8. 完了メッセージ ────────────────────────────────────────────────────────
echo ""
echo "============================================="
info "Installation complete!"
echo "============================================="
echo ""
echo "  Start JupyterLab:"
echo "    ./uv_setup/start_jupyter.sh"
echo ""
echo "  Or manually:"
echo "    source uv_setup/.venv/bin/activate"
echo "    jupyter lab"
echo ""
