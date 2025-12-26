@echo off
title VisualGS Console

REM -------------------------------
REM Banner
REM -------------------------------
echo.
echo ======================================
echo      VisualGS - Ground Station
echo ======================================
echo.

REM -------------------------------
REM Check Python
REM -------------------------------
python --version >nul 2>&1
if errorlevel 1 (
    echo Python not found.
    echo Please install Python 3.10 or newer.
    pause
    exit /b
)

REM -------------------------------
REM Create venv if missing
REM -------------------------------
if not exist .venv (
    echo Creating virtual environment...
    python -m venv .venv

    call .venv\Scripts\activate

    echo Installing dependencies...
    python -m pip install --upgrade pip
    pip install -e .
) else (
    call .venv\Scripts\activate
)

REM -------------------------------
REM Ready state
REM -------------------------------
echo.
echo Environment ready.
echo Type:
echo   visualgs run
echo   visualgs replay dataset.csv --speed 2
echo   visualgs --help
echo.

REM Drop user into active shell
cmd /k
