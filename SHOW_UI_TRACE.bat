@echo off
setlocal enabledelayedexpansion
chcp 65001 >nul
reg add HKCU\Console /v VirtualTerminalLevel /t REG_DWORD /d 1 /f >nul 2>&1
cd /d "%~dp0funger_terminal"

cls
echo ====================================================================
echo   FEAR ^& HUNGER: COMBAT ARENA - AUTOMATED STATE TRACE SHOWCASE
echo ====================================================================
echo [*] Executing 6-step combat cycle: Limb damage, Debuff, Decapitate...
echo.

python demo_interactive_ui.py --showcase

echo.
echo ====================================================================
echo   Showcase Execution Finished.
echo ====================================================================
pause
