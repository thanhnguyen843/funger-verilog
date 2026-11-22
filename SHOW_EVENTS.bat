@echo off
setlocal enabledelayedexpansion
chcp 65001 >nul
reg add HKCU\Console /v VirtualTerminalLevel /t REG_DWORD /d 1 /f >nul 2>&1
cd /d "%~dp0funger_terminal"

cls
echo ====================================================================
echo   FEAR ^& HUNGER: TERMINAL LABYRINTH - EVENT ENCYCLOPEDIA (RTL)
echo ====================================================================
echo [*] Initializing Verilog RTL hardware engine for 10 survival events...
echo.

if not exist sim mkdir sim

where iverilog >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    echo [*] Compiling hardware event logic and FSM testbench...
    iverilog -g2012 -I src -o sim/show_events.out tb/tb_show_events.v
    if %ERRORLEVEL% NEQ 0 (
        echo [ERROR] Verilog compilation failed!
        pause
        exit /b %ERRORLEVEL%
    )
    echo [OK] Compilation successful!
    echo.
) else (
    if not exist sim\show_events.out (
        echo [ERROR] iverilog compiler was not found in PATH and binary is missing!
        pause
        exit /b 1
    )
)

echo [*] Simulating logic for 10 survival-tactical labyrinth events...
echo.
vvp sim/show_events.out

echo.
echo ====================================================================
echo   Event simulation complete for Fear ^& Hunger: Terminal Labyrinth.
echo ====================================================================
pause
