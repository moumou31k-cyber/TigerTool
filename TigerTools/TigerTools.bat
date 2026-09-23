@echo off
title Tiger Tools
color 04
cls

echo.
echo  ============================================================
echo   TIGER TOOLS - Multi-Tool Suite
echo  ============================================================
echo.

:: Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo  [-] Python not found. Please install Python 3.x
    echo      https://www.python.org/downloads/
    echo.
    pause
    exit /b 1
)

echo  [~] Python found.
echo  [~] Launching TigerTools...
echo.

python TigerTools.py
pause
