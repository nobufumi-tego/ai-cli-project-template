# JupyterLab 起動スクリプト (Windows PowerShell)
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path

if (-not (Test-Path (Join-Path $ScriptDir ".venv"))) {
    Write-Host "[ERROR] Virtual environment not found. Run install.bat first." -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host "[INFO] Starting JupyterLab..." -ForegroundColor Green
Write-Host "[INFO] Press Ctrl+C to stop." -ForegroundColor Green
Write-Host ""

Set-Location $ScriptDir
uv run jupyter lab
