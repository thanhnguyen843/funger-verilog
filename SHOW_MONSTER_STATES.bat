@echo off
setlocal enabledelayedexpansion
chcp 65001 >nul
reg add HKCU\Console /v VirtualTerminalLevel /t REG_DWORD /d 1 /f >nul 2>&1
cd /d "%~dp0funger_terminal"

cls
echo ====================================================================
echo   FEAR ^& HUNGER: TRI-STATE HARDWARE MONSTER MODEL SHOWCASE
echo   (STATE 0: NORMAL  vs  STATE 1: INJURED  vs  STATE 2: DEAD)
echo ====================================================================
echo [*] Khoi dong trinh bien dich phan cung Icarus Verilog...
echo.

if not exist sim mkdir sim

where iverilog >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    echo [*] Bien dich Module monster_state_model.v va Testbench Verilog RTL...
    iverilog -g2012 -I src -o sim/show_monster_states.out ^
        src/monster.v ^
        src/fantasy_creatures.v ^
        src/monster_state_model.v ^
        tb/tb_show_monster_states.v
    if %ERRORLEVEL% NEQ 0 (
        echo [ERROR] Loi bien dich Verilog!
        pause
        exit /b %ERRORLEVEL%
    )
    echo [OK] Bien dich phan cung thanh cong!
    echo.
) else (
    if not exist sim\show_monster_states.out (
        echo [ERROR] Khong tim thay iverilog trong PATH va file binary chua ton tai!
        pause
        exit /b 1
    )
)

echo [*] Dang render 3 trang thai dong thoi (Normal - Injured - Dead) cho 36 quai vat...
echo.
vvp sim/show_monster_states.out

echo.
echo ====================================================================
echo   Hoan tat trinh dien 3 trang thai quai vat Fear ^& Hunger Hardware RTL.
echo ====================================================================
pause
