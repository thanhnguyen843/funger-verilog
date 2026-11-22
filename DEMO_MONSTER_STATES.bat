@echo off
setlocal enabledelayedexpansion
chcp 65001 >nul
reg add HKCU\Console /v VirtualTerminalLevel /t REG_DWORD /d 1 /f >nul 2>&1
cd /d "%~dp0funger_terminal"

cls
echo ====================================================================
echo   FEAR ^& HUNGER: INTERACTIVE TRI-STATE MONSTER VIEWER
echo   Dieu khien phim: [1] Normal  |  [2] Injured  |  [3] Dead  |  [A/D] Doi Quai
echo ====================================================================
echo.

where python >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Khong tim thay Python trong he thong!
    pause
    exit /b 1
)

python demo_monster_states.py

echo.
echo ====================================================================
echo   Hoan tat phien kiem tra tuong tac mo hinh quai vat 3 trang thai.
echo ====================================================================
pause
