@echo off
setlocal EnableDelayedExpansion

set "D=%~dp0"
if "!D:~-1!"=="\" set "D=!D:~0,-1!"

if not exist "!D!\.venv\Scripts\python.exe" (
    echo [ERROR] Virtual environment not found. Run install.bat first.
    pause
    exit /b 1
)

echo [INFO] Starting JupyterLab...
echo [INFO] Press Ctrl+C to stop.
echo.

cd /d "!D!"

where uv >nul 2>&1
if !errorlevel! equ 0 (
    uv run jupyter lab
) else (
    "!D!\.venv\Scripts\python.exe" -m jupyter lab
)

pause
