@echo off
chcp 65001 >nul
title MoonEvents - Exe erstellen

echo ============================================================
echo           MoonEvents - Exe-Erstellung (PyInstaller)
echo ============================================================
echo.

cd /d "%~dp0"

:: Python pruefen
python --version >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo [FEHLER] Python wurde nicht gefunden!
    echo Bitte stellen Sie sicher, dass Python installiert und im PATH registriert ist.
    echo.
    pause
    exit /b 1
)

echo [1/3] Pruefe Abhaengigkeiten...
python -m pip install -r requirements.txt pyinstaller >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo [HINWEIS] Weiter mit vorhandenen Paketen...
)

echo [2/3] Erstelle ausfuehrbare Datei (MoonEvents.exe)...
pyinstaller --noconfirm --onefile --windowed --icon "icon.ico" --name "MoonEvents" --add-data "moon_map.jpg;." --add-data "info.conf;." --add-data "icon.ico;." --clean main.py

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo [FEHLER] Die Erstellung der Exe-Datei ist fehlgeschlagen!
    echo.
    pause
    exit /b %ERRORLEVEL%
)

echo.
echo [3/3] Erfolgreich abgeschlossen!
echo.
echo Die Exe-Datei wurde erstellt unter:
echo   %~dp0dist\MoonEvents.exe
echo ============================================================
echo.
pause
