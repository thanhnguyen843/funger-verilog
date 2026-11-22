@echo off
setlocal enabledelayedexpansion
chcp 65001 >nul
reg add HKCU\Console /v VirtualTerminalLevel /t REG_DWORD /d 1 /f >nul 2>&1
cd /d "%~dp0funger_terminal"

cls
echo ====================================================================
echo   FEAR ^& HUNGER: COMBAT ARENA - INTERACTIVE TERMINAL UI DEMO
echo ====================================================================
echo [*] Launching W/S cursor navigation combat interface...
echo.

where python >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Python not found in system PATH!
    pause
    exit /b 1
)

python demo_interactive_ui.py

echo.
echo ====================================================================
echo   Combat Arena UI Demo Session Terminated.
echo ====================================================================
pause
