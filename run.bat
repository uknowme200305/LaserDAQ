@echo off
title LaserDAQ

echo ============================================
echo          Starting LaserDAQ
echo ============================================
echo.

:: Check if virtual environment exists

if not exist venv (
    echo.
    echo [ERROR] Virtual Environment not found.
    echo.
    echo Please run:
    echo.
    echo     setup.bat
    echo.
    pause
    exit /b
)

:: Activate Virtual Environment

call venv\Scripts\activate

:: Start LaserDAQ

python laserdaq.py

pause