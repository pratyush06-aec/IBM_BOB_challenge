@echo off
echo ========================================
echo GraphMind AI - Backend Startup Script
echo ========================================
echo.

cd backend

echo [1/3] Checking Python version...
python --version
echo.

echo [2/3] Checking if dependencies are installed...
python -c "try: from ibm_watsonx_ai.foundation_models import Model; print('✅ IBM watsonx.ai SDK installed')" 2>nul || (
    echo ❌ IBM watsonx.ai SDK not found
    echo Installing dependencies... This may take 2-3 minutes
    pip install -r requirements.txt
)
echo.

echo [3/3] Starting FastAPI server...
echo Server will be available at: http://localhost:8000
echo API Documentation: http://localhost:8000/docs
echo.
echo Press CTRL+C to stop the server
echo.

python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

@REM Made with Bob
