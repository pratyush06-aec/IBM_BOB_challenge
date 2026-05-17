@echo off
echo ========================================
echo GraphMind AI - Frontend Startup Script
echo ========================================
echo.

cd frontend

echo [1/3] Checking Node.js version...
node --version
echo.

echo [2/3] Checking if dependencies are installed...
if not exist "node_modules" (
    echo ❌ Dependencies not found
    echo Installing dependencies... This may take 2-3 minutes
    call npm install
) else (
    echo ✅ Dependencies already installed
)
echo.

echo [3/3] Starting Next.js development server...
echo Frontend will be available at: http://localhost:3000
echo.
echo Press CTRL+C to stop the server
echo.

call npm run dev

@REM Made with Bob
