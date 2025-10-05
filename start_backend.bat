@echo off
echo ========================================
echo Smart Farmer System - Starting Backend
echo ========================================
echo.

cd backend

if not exist venv (
    echo ERROR: Virtual environment not found!
    echo Please run setup_backend.bat first
    pause
    exit /b 1
)

echo Activating virtual environment...
call venv\Scripts\activate.bat

echo Starting Flask server...
python app.py
