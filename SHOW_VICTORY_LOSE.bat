@echo off
setlocal enabledelayedexpansion
chcp 65001 >nul
reg add HKCU\Console /v VirtualTerminalLevel /t REG_DWORD /d 1 /f >nul 2>&1
cd /d "%~dp0funger_terminal"

cls
echo ====================================================================
echo   FEAR ^& HUNGER: TERMINAL LABYRINTH - VICTORY ^& DEFEAT SCREENS
echo ====================================================================
echo [*] Dang khoi tao mo phong phan cung Verilog RTL cho Victory ^& Lose...
echo.

if not exist sim mkdir sim

where iverilog >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    echo [*] Bien dich Hardware Engine cho man hinh Chien thang va Game Over...
    iverilog -g2012 -I src -o sim/show_victory_lose.out tb/tb_show_victory_lose.v
    if %ERRORLEVEL% NEQ 0 (
        echo [ERROR] Loi bien dich Verilog!
        pause
        exit /b %ERRORLEVEL%
    )
    echo [OK] Bien dich thanh cong!
    echo.
) else (
    if not exist sim\show_victory_lose.out (
        echo [ERROR] Khong tim thay trinh bien dich iverilog trong PATH va file binary chua ton tai!
        echo Vui long cai dat Icarus Verilog de bien dich mo phong phan cung.
        pause
        exit /b 1
    )
)

echo [*] Dang render Banner ASCII Victory, Gothic Game Over va 5 kich ban tu nan...
echo.
vvp sim/show_victory_lose.out

echo.
echo ====================================================================
echo   Hoan tat xuat toan bo thong bao Victory ^& Lose Fear ^& Hunger.
echo ====================================================================
pause
