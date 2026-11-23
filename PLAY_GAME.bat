@echo off
setlocal enabledelayedexpansion
chcp 65001 >nul
mode con: cols=100 lines=36
reg add HKCU\Console /v VirtualTerminalLevel /t REG_DWORD /d 1 /f >nul 2>&1
cd /d "%~dp0funger_terminal"

cls
echo ====================================================================
echo   FEAR ^& HUNGER: TERMINAL LABYRINTH - SOLO EXPLORER EDITION
echo ====================================================================
echo.

if not exist sim mkdir sim

where iverilog >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    echo [*] Verifying Verilog RTL hardware engine...
    iverilog -I src -o sim/funger_play.out ^
        src/damage_alu.v ^
        src/rng_unit.v ^
        src/character_rom.v ^
        src/monster_rom.v ^
        src/map_rom.v ^
        src/collision_unit.v ^
        src/inventory_ram.v ^
        src/chest_sprite_rom.v ^
        src/key_sprite_rom.v ^
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
        src/tactical_stance_unit.v ^
        src/sanity_meter_unit.v ^
        src/sprite_router.v ^
        src/terminal_ui.v ^
        tb/tb_play.v
    if %ERRORLEVEL% NEQ 0 (
        echo [ERROR] Verilog compilation failed!
        pause
        exit /b %ERRORLEVEL%
    )
    echo [OK] Hardware RTL verified successfully!
    echo.
) else (
    if not exist sim\funger_play.out (
        echo [ERROR] iverilog compiler was not found in PATH and precompiled binary is missing!
        pause
        exit /b 1
    )
)

where python >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    python master_game.py
) else (
    vvp sim/funger_play.out
)

pause
