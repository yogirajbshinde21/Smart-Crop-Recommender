@echo off
echo ========================================
echo Smart Farmer System - Frontend Setup
echo ========================================
echo.

cd frontend

echo Step 1: Installing Node.js dependencies...
call npm install
if %errorlevel% neq 0 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)

echo.
echo ========================================
echo Frontend setup complete!
echo ========================================
echo.
echo To start the frontend server, run:
echo   cd frontend
echo   npm run dev
echo.
pause
