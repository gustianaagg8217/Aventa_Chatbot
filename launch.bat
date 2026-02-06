@echo off
REM Project Robot Launcher
REM Pastikan Python 3.7+ sudah terinstall

echo.
echo ====================================================
echo   PROJECT ROBOT - CHATBOT OFFLINE YANG BISA DIAJARKAN
echo ====================================================
echo.
echo Pilih mode:
echo 1. CLI Mode (Terminal)
echo 2. GUI Mode (Grafis)
echo.

set /p choice="Masukkan pilihan (1 atau 2): "

if "%choice%"=="1" (
    echo Membuka CLI mode...
    python robot_core.py
) else if "%choice%"=="2" (
    echo Membuka GUI mode...
    python robot_gui.py
) else (
    echo Pilihan tidak valid!
    pause
)
