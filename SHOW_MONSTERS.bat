@echo off
setlocal enabledelayedexpansion
chcp 65001 >nul
reg add HKCU\Console /v VirtualTerminalLevel /t REG_DWORD /d 1 /f >nul 2>&1
cd /d "%~dp0funger_terminal"

cls
echo ====================================================================
echo   FEAR ^& HUNGER: TERMINAL LABYRINTH - MONSTER ENCYCLOPEDIA (RTL)
echo ====================================================================
echo [*] Initializing Verilog RTL hardware engine for 36 monsters...
echo.

if not exist sim mkdir sim

where iverilog >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    echo [*] Compiling hardware engine for 36 beasts and mythological entities...
    iverilog -g2012 -I src -o sim/show_monsters.out ^
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
        src/monster_rom.v ^
        tb/tb_show_monsters.v
    if %ERRORLEVEL% NEQ 0 (
        echo [ERROR] Verilog compilation failed!
        pause
        exit /b %ERRORLEVEL%
    )
    echo [OK] Compilation successful!
    echo.
) else (
    if not exist sim\show_monsters.out (
        echo [ERROR] iverilog compiler was not found in PATH and binary is missing!
        pause
        exit /b 1
    )
)

where python >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    echo [*] Launching Interactive Monster Encyclopedia & Morphology Inspector...
    python demo_monster_states.py
) else (
    echo [*] Rendering 36 monster sprites and tactical specifications...
    echo.
    vvp sim/show_monsters.out
    pause
)
