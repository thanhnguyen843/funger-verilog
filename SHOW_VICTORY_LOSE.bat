@echo off
setlocal enabledelayedexpansion
chcp 65001 >nul
reg add HKCU\Console /v VirtualTerminalLevel /t REG_DWORD /d 1 /f >nul 2>&1
cd /d "%~dp0funger_terminal"

cls
echo ====================================================================
echo   FEAR ^& HUNGER: TERMINAL LABYRINTH - VICTORY ^& DEFEAT SCREENS
echo ====================================================================
echo [*] Initializing Verilog RTL hardware engine for end screens...
echo.

if not exist sim mkdir sim

where iverilog >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    echo [*] Compiling hardware engine for Victory and Game Over screens...
    iverilog -g2012 -I src -o sim/show_victory_lose.out tb/tb_show_victory_lose.v
    if %ERRORLEVEL% NEQ 0 (
        echo [ERROR] Verilog compilation failed!
        pause
        exit /b %ERRORLEVEL%
    )
    echo [OK] Compilation successful!
    echo.
) else (
    if not exist sim\show_victory_lose.out (
        echo [ERROR] iverilog compiler was not found in PATH and binary is missing!
        pause
        exit /b 1
    )
)

echo [*] Rendering ASCII Victory banner, Gothic Game Over, and 5 demise scenarios...
echo.
vvp sim/show_victory_lose.out

echo.
echo ====================================================================
echo   End-screen simulation complete.
echo ====================================================================
pause
