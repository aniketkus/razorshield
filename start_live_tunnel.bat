@echo off
title RazorShield - Live Demo Launcher with Cloudflare Tunnel
echo ====================================================
echo   RazorShield -- Launching Local Servers + Live Tunnel
echo ====================================================
echo.

echo [1/3] Starting FastAPI backend on port 8000...
cd /d "%~dp0backend"
start "RazorShield Backend (Port 8000)" cmd /k "python -m uvicorn main:app --reload --port 8000"

echo [2/3] Starting Vite frontend on port 5173...
cd /d "%~dp0frontend"
start "RazorShield Frontend (Port 5173)" cmd /k "npm run dev"

echo [3/3] Waiting 4 seconds for servers to initialize...
timeout /t 4 /nobreak >nul

echo Starting Cloudflare Tunnel...
cd /d "%~dp0"
echo.
echo =========================================================================
echo   IMPORTANT: Keep this window OPEN to keep your Live Demo link active!
echo   Look below for your https://*.trycloudflare.com URL.
echo   Copy that URL to test in your browser or share with evaluators.
echo =========================================================================
echo.
cloudflared.exe tunnel --url http://localhost:5173
pause
