@echo off
title LaserDAQ Setup

echo ======================================================
echo               LaserDAQ Setup Utility
echo ======================================================
echo.

:: --------------------------------------------------------
:: Check if Python is installed
:: --------------------------------------------------------

python --version >nul 2>&1

if errorlevel 1 (
    echo [ERROR] Python is not installed or not added to PATH.
    echo.
    echo Please install Python 3.11 or newer.
    pause
    exit /b
)

echo [OK] Python detected.
echo.

:: --------------------------------------------------------
:: Create Virtual Environment
:: --------------------------------------------------------

if exist venv (
    echo [INFO] Virtual Environment already exists.
) else (
    echo Creating Virtual Environment...
    python -m venv venv

    if errorlevel 1 (
        echo.
        echo [ERROR] Failed to create Virtual Environment.
        pause
        exit /b
    )
)

echo.

:: --------------------------------------------------------
:: Activate Environment
:: --------------------------------------------------------

call venv\Scripts\activate

echo Virtual Environment Activated.
echo.

:: --------------------------------------------------------
:: Upgrade pip
:: --------------------------------------------------------

echo Updating pip...

python -m pip install --upgrade pip

echo.

:: --------------------------------------------------------
:: Install Requirements
:: --------------------------------------------------------

echo Installing Dependencies...
echo.

pip install -r requirements.txt

if errorlevel 1 (
    echo.
    echo [ERROR] Failed to install dependencies.
    pause
    exit /b
)

echo.

:: --------------------------------------------------------
:: Finished
:: --------------------------------------------------------

echo ======================================================
echo           LaserDAQ Setup Completed Successfully
echo ======================================================
echo.
echo You can now start the software using:
echo.
echo     run.bat
echo.
pause