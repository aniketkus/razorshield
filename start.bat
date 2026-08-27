@echo off
echo.
echo  ====================================================
echo   RazorShield -- AI Risk Manager Startup Script
echo  ====================================================
echo.

echo [1/4] Installing Python dependencies...
cd backend
pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: pip install failed. Make sure Python 3.11+ is installed.
    pause
    exit /b 1
)

echo.
echo [2/4] Training ML models (this takes ~2-3 minutes)...
python data/train_models.py
if errorlevel 1 (
    echo ERROR: Model training failed.
    pause
    exit /b 1
)

echo.
echo [3/4] Starting FastAPI backend on port 8000...
start "RazorShield Backend" cmd /k "uvicorn main:app --reload --port 8000"

echo.
echo [4/4] Installing frontend and starting dev server...
cd ..\frontend
call npm install
start "RazorShield Frontend" cmd /k "npm run dev"

echo.
echo  ====================================================
echo   RazorShield is running!
echo   Dashboard:  http://localhost:5173
echo   API Docs:   http://localhost:8000/docs
echo   Metrics:    http://localhost:8000/metrics
echo  ====================================================
echo.
pause
