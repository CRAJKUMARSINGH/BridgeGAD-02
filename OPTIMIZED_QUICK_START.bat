@echo off
title Bridge CAD - Optimized Quick Start
color 0A

echo ========================================
echo    BRIDGE CAD - OPTIMIZED LAUNCHER
echo ========================================
echo.
echo Starting optimized Bridge application...
echo Performance mode: FAST
echo.

REM Kill any existing Python processes to free memory
echo Cleaning up existing processes...
taskkill /f /im python.exe >nul 2>&1
taskkill /f /im streamlit.exe >nul 2>&1

echo ✅ Memory cleaned

REM Start only the most efficient app (Flask - fastest)
echo.
echo 🚀 Starting BridgeGAD-02 (Flask) - Optimized Mode
echo.
echo Features available:
echo - Fast DXF generation
echo - Professional CAD output
echo - Minimal resource usage
echo - Instant preview
echo.

REM Set performance optimizations
set PYTHONDONTWRITEBYTECODE=1
set PYTHONOPTIMIZE=1

REM Start the Flask app with optimization
echo Opening http://localhost:5000 in 3 seconds...
timeout /t 3 >nul
start http://localhost:5000

python main.py

echo.
echo Application stopped. Press any key to exit...
pause >nul