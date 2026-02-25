@echo off
title CanteenPay - Launcher
echo ==========================================
echo Starting CanteenPay (Backend + Frontend)
echo ==========================================

:: Start Backend in a new window
echo [1/2] Launching Backend Server (FastAPI)...
start "CanteenPay - Backend" cmd /k "cd backend && uvicorn app.main:app --reload --host 127.0.0.1 --port 8000"

:: Wait a moment for backend to initialize
timeout /t 3 /nobreak > nul

:: Start Frontend in a new window
echo [2/2] Launching Frontend (Vite)...
start "CanteenPay - Frontend" cmd /k "cd frontend && npm run dev"

echo.
echo ==========================================
echo Project successfully launched!
echo Backend:  http://127.0.0.1:8000
echo Frontend: http://localhost:3000
echo ==========================================
echo.
echo Leave this window open or close it. The project windows are separate.
pause
