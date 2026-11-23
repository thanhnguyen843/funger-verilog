@echo off
setlocal enabledelayedexpansion
chcp 65001 >nul
mode con: cols=104 lines=40 >nul 2>&1
reg add HKCU\Console /v VirtualTerminalLevel /t REG_DWORD /d 1 /f >nul 2>&1
cd /d "%~dp0funger_terminal"

cls
echo ====================================================================
echo   FEAR ^& HUNGER: TRI-STATE HARDWARE MONSTER RTL SHOWCASE
echo   (STATE 0: NORMAL  vs  STATE 1: INJURED  vs  STATE 2: DEAD)
echo ====================================================================
echo [*] Initializing Icarus Verilog hardware compiler...
echo.

if not exist sim mkdir sim

where iverilog >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    echo [*] Compiling monster_state_model.v and Verilog RTL testbench...
    iverilog -g2012 -I src -o sim/show_monster_states.out ^
        src/monster.v ^
        src/fantasy_creatures.v ^
        src/monster_state_model.v ^
        tb/tb_show_monster_states.v
    if %ERRORLEVEL% NEQ 0 (
        echo [ERROR] Verilog compilation failed!
        pause
        exit /b %ERRORLEVEL%
    )
    echo [OK] Hardware engine compiled successfully!
    echo.
) else (
    if not exist sim\show_monster_states.out (
        echo [ERROR] iverilog was not found in PATH and precompiled binary is missing!
        pause
        exit /b 1
    )
)

echo [*] Rendering side-by-side tri-state morphology for all 36 monsters...
echo.
vvp sim/show_monster_states.out

echo.
echo ====================================================================
echo   Tri-State Monster Hardware RTL Simulation Complete.
echo ====================================================================
pause
