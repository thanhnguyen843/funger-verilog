@echo off
setlocal enabledelayedexpansion
chcp 65001 >nul
mode con: cols=100 lines=36
reg add HKCU\Console /v VirtualTerminalLevel /t REG_DWORD /d 1 /f >nul 2>&1
title Fear ^& Hunger: Hero Tri-State Models Showcase (Normal, Injured, Dead)
cd /d "%~dp0"

cls
python funger_terminal\show_hero_models.py
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo [ERROR] Failed to run show_hero_models.py!
)
pause
