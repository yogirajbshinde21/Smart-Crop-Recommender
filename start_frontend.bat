@echo off
echo ========================================
echo Smart Farmer System - Starting Frontend
echo ========================================
echo.

cd frontend

if not exist node_modules (
    echo ERROR: Node modules not found!
    echo Please run setup_frontend.bat first
    pause
    exit /b 1
)

echo Starting Vite development server...
call npm run dev
