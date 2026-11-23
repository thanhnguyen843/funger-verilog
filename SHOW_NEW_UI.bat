@echo off
setlocal enabledelayedexpansion
chcp 65001 >nul
mode con: cols=104 lines=54 >nul 2>&1
reg add HKCU\Console /v VirtualTerminalLevel /t REG_DWORD /d 1 /f >nul 2>&1
cd /d "%~dp0funger_terminal"

cls
echo ====================================================================
echo   FEAR ^& HUNGER: TACTICAL COMBAT ARENA - INTERACTIVE TERMINAL HUD
echo ====================================================================
echo [*] Controls: [W/S] Navigate  ^|  [Enter] Confirm  ^|  [B/Esc] Back
echo [*] Features: Diagonal Arena, Balanced Hero Roster, Postural Dismemberment
echo.

where python >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Python was not found in system PATH!
    pause
    exit /b 1
)

python demo_interactive_ui.py

echo.
echo ====================================================================
echo   Combat Arena interactive session terminated.
echo ====================================================================
pause
