@echo off
title VisualGS Console

REM ---------------------------------------
REM Bootstrap environment
REM ---------------------------------------

python --version >nul 2>&1
if errorlevel 1 (
    echo Python not found.
    echo Please install Python 3.10 or newer.
    pause
    exit /b
)

if not exist .venv (
    echo Creating virtual environment...
    python -m venv .venv
)

call .venv\Scripts\activate

pip install --upgrade pip >nul
pip install -e . >nul

cls

REM ---------------------------------------
REM Welcome Screen (ASCII-safe)
REM ---------------------------------------
type banner.txt
echo.
echo  Environment ready.
echo.
echo  Commands:
echo    visualgs run
echo    visualgs replay dataset.csv --speed 2
echo    visualgs --help
echo.
echo  Press Ctrl+C to exit.
echo.

REM ---------------------------------------
REM Hand control to user
REM ---------------------------------------
cmd /k
