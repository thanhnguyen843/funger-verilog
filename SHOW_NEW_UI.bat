@echo off
setlocal enabledelayedexpansion
chcp 65001 >nul
reg add HKCU\Console /v VirtualTerminalLevel /t REG_DWORD /d 1 /f >nul 2>&1
cd /d "%~dp0funger_terminal"

cls
echo ====================================================================
echo   FEAR ^& HUNGER: TERMINAL LABYRINTH - DEMO GIAO DIEN CHIEN DAU MOI
echo ====================================================================
echo [*] Khoi dong giao dien dieu huong 4 nut con tro W/S 2 tang...
echo.

where python >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Khong tim thay Python trong PATH de chay trinh demo tuong tac!
    pause
    exit /b 1
)

python demo_interactive_ui.py

echo.
echo ====================================================================
echo   Hoan tat phien trai nghiem Demo UI Fear ^& Hunger.
echo ====================================================================
pause
