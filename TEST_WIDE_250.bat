@echo off
setlocal enabledelayedexpansion
chcp 65001 >nul
mode con: cols=250 lines=38
reg add HKCU\Console /v VirtualTerminalLevel /t REG_DWORD /d 1 /f >nul 2>&1
title Fear & Hunger: Panoptic 250-Column Grand Architecture Showcase
cd /d "%~dp0"

cls
python funger_terminal\demo_wide_250.py
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo [ERROR] Failed to run demo_wide_250.py!
)
pause
