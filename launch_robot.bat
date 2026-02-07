@echo off
REM Launcher for Project Robot (Windows CMD)
REM Usage: double-click or run from PowerShell/CMD

cd /d "%~dp0"
echo Starting Project Robot (with vocabulary + Wikipedia)...
python robot_with_vocabulary.py
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo The program exited with code %ERRORLEVEL%.
)
pause
