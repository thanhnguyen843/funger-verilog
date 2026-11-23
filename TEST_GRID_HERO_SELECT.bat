@echo off
setlocal enabledelayedexpansion
chcp 65001 >nul
mode con: cols=100 lines=36
reg add HKCU\Console /v VirtualTerminalLevel /t REG_DWORD /d 1 /f >nul 2>&1
title Fear & Hunger: 2D Grid Explorer Selection (Experimental Parallel Prototype)
cd /d "%~dp0"

cls
python funger_terminal\demo_grid_hero_select.py
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo [ERROR] Failed to run demo_grid_hero_select.py!
)
pause
