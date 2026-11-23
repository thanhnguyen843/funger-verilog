@echo off
setlocal enabledelayedexpansion
chcp 65001 >nul
mode con: cols=104 lines=54 >nul 2>&1
reg add HKCU\Console /v VirtualTerminalLevel /t REG_DWORD /d 1 /f >nul 2>&1
cd /d "%~dp0funger_terminal"

cls
echo ====================================================================
echo   FEAR ^& HUNGER: EXPEDITION DRAFT GUIDE ^& SQUAD FORMATION
echo ====================================================================
echo [*] Controls: [1/2/3] Choose Preset  ^|  [C] Custom 4-Hero Draft  ^|  [Enter] Deploy
echo [*] Features: 8 Explorers, Asymmetrical Metabolism, Softlock-Proof Verification
echo.

where python >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Python was not found in system PATH!
    pause
    exit /b 1
)

python demo_interactive_ui.py --draft

echo.
echo ====================================================================
echo   Draft Guide and Combat session completed.
echo ====================================================================
pause
