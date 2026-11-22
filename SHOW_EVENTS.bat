@echo off
setlocal enabledelayedexpansion
chcp 65001 >nul
reg add HKCU\Console /v VirtualTerminalLevel /t REG_DWORD /d 1 /f >nul 2>&1
cd /d "%~dp0funger_terminal"

cls
echo ====================================================================
echo   FEAR ^& HUNGER: TERMINAL LABYRINTH - COMPLETE EVENT ENCYCLOPEDIA
echo ====================================================================
echo [*] Dang khoi tao mo phong phan cung Verilog RTL cho 10 Su kien...
echo.

if not exist sim mkdir sim

where iverilog >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    echo [*] Bien dich Hardware Engine cho cac su kien va may trang thai FSM...
    iverilog -g2012 -I src -o sim/show_events.out tb/tb_show_events.v
    if %ERRORLEVEL% NEQ 0 (
        echo [ERROR] Loi bien dich Verilog!
        pause
        exit /b %ERRORLEVEL%
    )
    echo [OK] Bien dich thanh cong!
    echo.
) else (
    if not exist sim\show_events.out (
        echo [ERROR] Khong tim thay trinh bien dich iverilog trong PATH va file binary chua ton tai!
        echo Vui long cai dat Icarus Verilog de bien dich mo phong phan cung.
        pause
        exit /b 1
    )
)

echo [*] Dang render bieu do va logic 10 su kien sinh ton - tac chien Fear ^& Hunger...
echo.
vvp sim/show_events.out

echo.
echo ====================================================================
echo   Hoan tat xuat toan bo su kien Fear ^& Hunger: Terminal Labyrinth.
echo ====================================================================
pause
