@echo off
:: =============================================================================
:: ML Environment Installer for Windows 11 (Command Prompt)
:: Launches PowerShell installer
:: =============================================================================
echo =============================================
echo   Python ML Environment Setup (uv)
echo =============================================
echo.
echo Launching PowerShell installer...
echo.

PowerShell -NoProfile -ExecutionPolicy Bypass -File "%~dp0install.ps1"

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo [ERROR] Installation failed. Check the output above.
    pause
    exit /b 1
)
pause
