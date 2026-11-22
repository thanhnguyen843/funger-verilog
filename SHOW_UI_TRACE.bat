@echo off
setlocal enabledelayedexpansion
chcp 65001 >nul
reg add HKCU\Console /v VirtualTerminalLevel /t REG_DWORD /d 1 /f >nul 2>&1
cd /d "%~dp0funger_terminal"

cls
echo ====================================================================
echo   FEAR ^& HUNGER - TRINH DIEN TU DONG CAC TRANG THAI GIAO DIEN MOI
echo ====================================================================
echo [*] Tu dong in ra chuoi menu 4 nut, dieu huong con tro va cac sub-menu...
echo.

python demo_interactive_ui.py --showcase

echo.
echo ====================================================================
echo   Hoan tat trinh dien tu dong UI.
echo ====================================================================
pause
