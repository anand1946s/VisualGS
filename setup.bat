@echo off
echo ======================================
echo VisualGS - First Time Setup
echo ======================================

REM Check python
python --version >nul 2>&1
if errorlevel 1 (
    echo Python not found. Please install Python 3.10+
    pause
    exit /b
)

REM Create venv if not exists
if not exist .venv (
    echo Creating virtual environment...
    python -m venv .venv
)

REM Activate venv
call .venv\Scripts\activate

REM Upgrade pip
python -m pip install --upgrade pip

REM Install project
pip install -e .

echo.
echo ======================================
echo Setup complete.
echo Next time, just run:
echo     run.bat
echo ======================================
pause
