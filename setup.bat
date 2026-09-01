@echo off
REM FastAPI CRUD Application Setup Script for Windows

echo.
echo ========================================
echo FastAPI CRUD Setup
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% NEQ 0 (
    echo ERROR: Python is not installed or not in PATH
    echo.
    echo Please install Python 3.8+ from https://www.python.org/
    echo Make sure to check "Add Python to PATH" during installation
    pause
    exit /b 1
)

echo Python is installed. Creating virtual environment...

REM Create virtual environment
if not exist "venv" (
    py -3.12 -m venv venv
    echo Virtual environment created
) else (
    echo Virtual environment already exists
)

REM Activate virtual environment
call venv\Scripts\activate.bat

echo.
echo Installing dependencies...
pip install -r requirements.txt

echo.
echo ========================================
echo Setup Complete!
echo ========================================
echo.
echo To run the application:
echo   1. Activate venv: venv\Scripts\activate.bat
echo   2. Run: uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
echo   3. Open browser: http://localhost:8000/docs
echo.
pause
