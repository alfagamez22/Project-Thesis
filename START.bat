@echo off
:: Thesis Prototype - Quick Start Script
:: Optimized startup for Windows

echo ============================================================
echo Thesis Prototype - Human Activity Recognition System
echo ============================================================
echo.

:: Check if conda environment exists
call conda env list | findstr /C:"env" >nul
if errorlevel 1 (
    echo [ERROR] Conda environment 'env' not found!
    echo.
    echo Please create the environment first:
    echo   conda create -n env python=3.10
    echo   conda activate env
    echo   pip install -r requirements.txt
    echo.
    pause
    exit /b 1
)

:: Activate environment
echo [1/3] Activating conda environment...
call conda activate env
if errorlevel 1 (
    echo [ERROR] Failed to activate environment
    pause
    exit /b 1
)

:: Check GPU
echo.
echo [2/3] Checking GPU availability...
python -c "import torch; print(f'GPU Available: {torch.cuda.is_available()}'); print(f'GPU Name: {torch.cuda.get_device_name(0) if torch.cuda.is_available() else \"N/A\"}')" 2>nul
if errorlevel 1 (
    echo [WARNING] PyTorch not installed or GPU check failed
)

:: Start server
echo.
echo [3/3] Starting server...
echo ============================================================
echo.
python start_server.py

pause
