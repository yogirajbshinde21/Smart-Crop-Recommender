@echo off
echo ========================================
echo Smart Farmer System - Backend Setup
echo ========================================
echo.

cd backend

echo Step 1: Creating virtual environment...
python -m venv venv
if %errorlevel% neq 0 (
    echo ERROR: Failed to create virtual environment
    pause
    exit /b 1
)

echo Step 2: Activating virtual environment...
call venv\Scripts\activate.bat

echo Step 3: Installing dependencies...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)

echo Step 4: Training ML models (this may take 5-10 minutes)...
python train_models.py
if %errorlevel% neq 0 (
    echo ERROR: Failed to train models
    pause
    exit /b 1
)

echo.
echo ========================================
echo Backend setup complete!
echo ========================================
echo.
echo To start the backend server, run:
echo   cd backend
echo   venv\Scripts\activate
echo   python app.py
echo.
pause
