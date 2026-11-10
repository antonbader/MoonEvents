@echo off
chcp 65001 >nul
title auto-py-to-exe starten

cd /d "%~dp0"

echo ============================================================
echo   Starte auto-py-to-exe mit geladener MoonEvents-Konfiguration
echo ============================================================
echo.

auto-py-to-exe --config "%~dp0auto_py_to_exe_config.json"
if %ERRORLEVEL% NEQ 0 (
    echo [HINWEIS] auto-py-to-exe konnte nicht direkt aufgerufen werden, versuche via Python...
    python -m auto_py_to_exe --config "%~dp0auto_py_to_exe_config.json"
)

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo [FEHLER] auto-py-to-exe konnte nicht gestartet werden.
    echo Installieren Sie es bei Bedarf mit: pip install auto-py-to-exe
    pause
)
