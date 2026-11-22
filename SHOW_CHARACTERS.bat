@echo off
setlocal enabledelayedexpansion
chcp 65001 >nul
reg add HKCU\Console /v VirtualTerminalLevel /t REG_DWORD /d 1 /f >nul 2>&1
cd /d "%~dp0funger_terminal"

cls
echo ====================================================================
echo   FEAR ^& HUNGER: TERMINAL LABYRINTH - PLAYABLE CHARACTER ENCYCLOPEDIA
echo ====================================================================
echo [*] Dang khoi tao mo phong phan cung Verilog RTL...
echo.

if not exist sim mkdir sim

where iverilog >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    echo [*] Bien dich Hardware Engine cho 8 nhan vat tham hiem...
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
        echo [ERROR] Loi bien dich Verilog!
        pause
        exit /b %ERRORLEVEL%
    )
    echo [OK] Bien dich thanh cong!
    echo.
) else (
    if not exist sim\show_characters.out (
        echo [ERROR] Khong tim thay trinh bien dich iverilog trong PATH va file binary chua ton tai!
        echo Vui long cai dat Icarus Verilog de bien dich mo phong phan cung.
        pause
        exit /b 1
    )
)

echo [*] Dang render sprite pixel art TrueColor va chi so chien thuat...
echo.
vvp sim/show_characters.out

echo.
echo ====================================================================
echo   Hoan tat xuat thong tin 8 nhan vat tham hiem Fear ^& Hunger.
echo ====================================================================
pause
