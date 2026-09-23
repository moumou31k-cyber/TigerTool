@echo off
title Tiger Tools - Setup
color 04
cls

echo.
echo  ============================================================
echo   TIGER TOOLS - Setup
echo  ============================================================
echo.

:: Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo  [-] Python not found!
    echo  [~] Download: https://www.python.org/downloads/
    echo  [!] Make sure to check "Add Python to PATH" during install.
    echo.
    pause
    exit /b 1
)

echo  [+] Python found.
echo  [~] Running setup...
echo.

python Setup.py

pause
