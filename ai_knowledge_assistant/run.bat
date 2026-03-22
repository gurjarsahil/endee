@echo off
echo ========================================
echo AI Knowledge Assistant
echo ========================================
echo.
echo Starting application...
echo Your API key will be loaded automatically from .env file
echo.

REM Check if virtual environment exists
if exist venv (
    echo Activating virtual environment...
    call venv\Scripts\activate.bat
) else (
    echo WARNING: Virtual environment not found!
    echo Please run quick_start.bat first
    pause
    exit /b 1
)

REM Check if .env file exists
if not exist .env (
    echo WARNING: .env file not found!
    echo Your API key should be in the .env file
    echo.
)

echo.
echo Opening browser at http://localhost:8501
echo Press Ctrl+C to stop the server
echo.

streamlit run app.py
