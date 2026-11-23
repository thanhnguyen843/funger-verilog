@echo off
setlocal enabledelayedexpansion
chcp 65001 >nul
mode con: cols=104 lines=36 >nul 2>&1
reg add HKCU\Console /v VirtualTerminalLevel /t REG_DWORD /d 1 /f >nul 2>&1
cd /d "%~dp0funger_terminal"

cls
echo ====================================================================
echo   FEAR ^& HUNGER: INTERACTIVE TRI-STATE MONSTER VIEWER
echo ====================================================================
echo [*] Controls: [1] Normal  ^|  [2] Injured  ^|  [3] Dead  ^|  [A/D] Change Foe
echo.

where python >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Python was not found in system PATH!
    pause
    exit /b 1
)

python demo_monster_states.py

echo.
echo ====================================================================
echo   Tri-state interactive inspection session terminated.
echo ====================================================================
pause
