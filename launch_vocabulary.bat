@echo off
REM Launch script untuk Online Vocabulary Chatbot
REM dengan auto-setup dan instalasi dependencies

setlocal enabledelayedexpansion

cls
echo.
echo ================================================================
echo    PROJECT ROBOT - ONLINE VOCABULARY SYSTEM
echo ================================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH
    echo Please install Python 3.7+ from https://www.python.org
    pause
    exit /b 1
)

REM Show Python version
echo [INFO] Python version:
python --version
echo.

REM Check if setup is needed
if not exist "data\vocabulary_cache\cache_metadata.json" (
    echo [SETUP] First time setup detected...
    echo.
    python setup_vocabulary.py
    if errorlevel 1 (
        echo Setup failed!
        pause
        exit /b 1
    )
    echo.
)

REM Choose between online and offline mode
echo ================================================================
echo    SELECT MODE
echo ================================================================
echo.
echo 1. Online Vocabulary (Recommended) - Fetch from online + local cache
echo 2. Original Robot (Offline) - Local patterns only
echo 3. Exit
echo.
set /p choice="Enter choice (1-3): "

if "%choice%"=="1" (
    echo.
    echo [RUN] Starting chatbot dengan online vocabulary...
    echo.
    python robot_with_vocabulary.py
) else if "%choice%"=="2" (
    echo.
    echo [RUN] Starting original chatbot...
    echo.
    python robot_core.py
) else (
    echo Exiting...
)

pause
