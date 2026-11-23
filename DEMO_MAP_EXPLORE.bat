@echo off
setlocal enabledelayedexpansion
chcp 65001 >nul
reg add HKCU\Console /v VirtualTerminalLevel /t REG_DWORD /d 1 /f >nul 2>&1
cd /d "%~dp0funger_terminal"

cls
echo ====================================================================
echo   FEAR ^& HUNGER: LABYRINTH - PERSISTENT FOG OF WAR ^& MAP EXPLORATION
echo ====================================================================
echo [*] Controls: [W/A/S/D] or [Arrows] Move  ^|  [F] Toggle Vision  ^|  [R] Reset
echo [*] Mechanics: Dynamic Torchlight permanently illuminates explored tiles.
echo [*] Objective: Venture into the darkness to map out the entire labyrinth!
echo.

where python >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Python was not found in system PATH!
    pause
    exit /b 1
)

python demo_map_discovery.py

echo.
echo ====================================================================
echo   Map exploration session terminated.
echo ====================================================================
pause
