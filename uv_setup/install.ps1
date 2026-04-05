# =============================================================================
# ML Environment Installer for Windows 11 (PowerShell)
# Uses: uv (https://github.com/astral-sh/uv)
# =============================================================================
#Requires -Version 5.1
$ErrorActionPreference = "Continue"

$ScriptDir  = Split-Path -Parent $MyInvocation.MyCommand.Path
$VenvDir    = Join-Path $ScriptDir ".venv"
$PythonVer  = "3.12"

function Write-Info  { param($msg) Write-Host "[INFO]  $msg" -ForegroundColor Green  }
function Write-Warn  { param($msg) Write-Host "[WARN]  $msg" -ForegroundColor Yellow }
function Write-Err   { param($msg) Write-Host "[ERROR] $msg" -ForegroundColor Red; exit 1 }

Write-Host "=============================================" -ForegroundColor Cyan
Write-Host "  Python ML Environment Setup (uv)"          -ForegroundColor Cyan
Write-Host "=============================================" -ForegroundColor Cyan
Write-Host ""

# ── 1. uv のインストール確認 / インストール ──────────────────────────────────
if (Get-Command uv -ErrorAction SilentlyContinue) {
    Write-Info "uv is already installed: $(uv --version)"
} else {
    Write-Info "Installing uv..."
    powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"

    # PATH を現在のセッションに反映
    $env:PATH = "$env:USERPROFILE\.local\bin;$env:USERPROFILE\.cargo\bin;$env:PATH"

    if (-not (Get-Command uv -ErrorAction SilentlyContinue)) {
        Write-Err "uv not found after installation. Please restart PowerShell and re-run this script."
    }
    Write-Info "uv installed: $(uv --version)"
}

# ── 2. 仮想環境の作成 ────────────────────────────────────────────────────────
Set-Location $ScriptDir

if (Test-Path $VenvDir) {
    Write-Warn "Virtual environment already exists at $VenvDir"
    $answer = Read-Host "Recreate? [y/N]"
    if ($answer -match '^[Yy]$') {
        Remove-Item -Recurse -Force $VenvDir
        Write-Info "Removed existing virtual environment."
    } else {
        Write-Info "Keeping existing environment. Updating packages..."
    }
}

if (-not (Test-Path $VenvDir)) {
    Write-Info "Creating virtual environment with Python $PythonVer..."
    uv venv --python $PythonVer $VenvDir
    if ($LASTEXITCODE -ne 0) { Write-Err "Failed to create virtual environment." }
}

$pythonExe = Join-Path $VenvDir "Scripts\python.exe"

# ── 3. パッケージのインストール ──────────────────────────────────────────────
Write-Info "Installing packages (this may take 10-30 minutes)..."
Write-Info "PyTorch is large (~2GB). Please wait..."
Write-Host ""

uv pip install --python $pythonExe `
    "jupyterlab>=4.0" "ipywidgets>=8.0" "ipykernel>=6.0" `
    "numpy>=1.26" "pandas>=2.0" "polars>=0.20" `
    "scikit-learn>=1.4" "xgboost>=2.0" "lightgbm>=4.0" `
    "torch>=2.2" "torchvision>=0.17" `
    "matplotlib>=3.8" "seaborn>=0.13" "plotly>=5.18" `
    "tqdm>=4.66" "joblib>=1.3" "scipy>=1.12" `
    "japanize-matplotlib>=1.1"

if ($LASTEXITCODE -ne 0) { Write-Err "Package installation failed." }

# ── 4. インストール確認 ──────────────────────────────────────────────────────
$jupyterExe = Join-Path $VenvDir "Scripts\jupyter.exe"
if (-not (Test-Path $jupyterExe)) {
    Write-Err "jupyter.exe not found after installation. Please re-run this script."
}

# ── 5. Jupyter カーネル登録 ──────────────────────────────────────────────────
Write-Info "Registering Jupyter kernel..."
& $pythonExe -m ipykernel install --user --name ml-env --display-name "Python (ML)"
if ($LASTEXITCODE -ne 0) { Write-Warn "Kernel registration failed (non-critical)." }

# ── 6. 完了メッセージ ────────────────────────────────────────────────────────
Write-Host ""
Write-Host "=============================================" -ForegroundColor Cyan
Write-Info "Installation complete!"
Write-Host "=============================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "  Start JupyterLab:"
Write-Host "    .\uv_setup\start_jupyter.bat"
Write-Host ""
Write-Host "  Or manually:"
Write-Host "    .\uv_setup\.venv\Scripts\activate"
Write-Host "    jupyter lab"
Write-Host ""
