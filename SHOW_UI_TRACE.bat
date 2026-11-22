@echo off
setlocal enabledelayedexpansion
chcp 65001 >nul
reg add HKCU\Console /v VirtualTerminalLevel /t REG_DWORD /d 1 /f >nul 2>&1
cd /d "%~dp0funger_terminal"

cls
echo ====================================================================
echo   FEAR ^& HUNGER: TACTICAL COMBAT ARENA - 6-STEP STATE SHOWCASE
echo ====================================================================
echo [*] Executing combat trace: Limb severance, Amber crouch, Decapitate finish...
echo.

where python >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Python was not found in system PATH!
    pause
    exit /b 1
)

python demo_interactive_ui.py --showcase

echo.
echo ====================================================================
echo   Showcase execution finished successfully.
echo ====================================================================
pause
