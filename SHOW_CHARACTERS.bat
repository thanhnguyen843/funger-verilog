@echo off
setlocal enabledelayedexpansion
chcp 65001 >nul
reg add HKCU\Console /v VirtualTerminalLevel /t REG_DWORD /d 1 /f >nul 2>&1
cd /d "%~dp0funger_terminal"

cls
echo ====================================================================
echo   FEAR ^& HUNGER: TERMINAL LABYRINTH - PLAYABLE HERO ROSTER (RTL)
echo ====================================================================
echo [*] Initializing Verilog RTL hardware engine...
echo.

if not exist sim mkdir sim

where iverilog >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    echo [*] Compiling hardware engine for 8 expedition heroes...
    iverilog -g2012 -I src -o sim/show_characters.out ^
        src/character_rom.v ^
        src/funger_cahara_rom.v ^
        src/funger_darce_rom.v ^
        src/funger_enki_rom.v ^
        src/funger_ragnvaldr_rom.v ^
        src/funger_legarde_rom.v ^
        src/funger_moonless_rom.v ^
        src/funger_thegirl_rom.v ^
        src/funger_nashrah_rom.v ^
        src/monster.v ^
        src/fantasy_creatures.v ^
        src/sprite_router.v ^
        tb/tb_show_characters.v
    if %ERRORLEVEL% NEQ 0 (
        echo [ERROR] Verilog compilation failed!
        pause
        exit /b %ERRORLEVEL%
    )
    echo [OK] Compilation successful!
    echo.
) else (
    if not exist sim\show_characters.out (
        echo [ERROR] iverilog compiler was not found in PATH and binary is missing!
        pause
        exit /b 1
    )
)

where python >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    echo [*] Launching Interactive Hero Explorer with Live Models...
    python demo_interactive_ui.py --guide
) else (
    echo [*] Rendering TrueColor pixel art sprites and tactical attributes...
    echo.
    vvp sim/show_characters.out
    pause
)
