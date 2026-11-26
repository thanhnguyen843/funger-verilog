@echo off
setlocal enabledelayedexpansion
chcp 65001 >nul
mode con: cols=100 lines=46
reg add HKCU\Console /v VirtualTerminalLevel /t REG_DWORD /d 1 /f >nul 2>&1
cd /d "%~dp0funger_terminal"

cls
echo ====================================================================
echo   FEAR ^& HUNGER: TERMINAL LABYRINTH - PURE VERILOG RTL EDITION
echo ====================================================================
echo.

if not exist sim mkdir sim

where iverilog >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    where vvp >nul 2>&1
    if %ERRORLEVEL% EQU 0 (
        if exist sim\funger_play.out (
            echo [NOTE] iverilog not in PATH; running pre-compiled RTL binary...
            echo.
            powershell -NoProfile -ExecutionPolicy Bypass -Command "$s=[IO.File]::ReadAllText('%~f0'); $p=[regex]::Split($s,'(?m)^__PS_HOST_BEGIN__\r?$'); Invoke-Expression $p[1]"
            pause
            exit /b %ERRORLEVEL%
        )
    )
    echo [ERROR] Icarus Verilog ^(iverilog / vvp^) was not found in PATH!
    echo Please install Icarus Verilog to compile and simulate the Verilog RTL.
    pause
    exit /b 1
)

echo [*] Compiling Verilog RTL modules and interactive testbench...
iverilog -Wall -g2012 -I src -o sim/funger_play.out ^
    src/damage_alu.v ^
    src/rng_unit.v ^
    src/character_rom.v ^
    src/monster_rom.v ^
    src/map_rom.v ^
    src/collision_unit.v ^
    src/inventory_ram.v ^
    src/chest_sprite_rom.v ^
    src/key_sprite_rom.v ^
    src/sprite_rom.v ^
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
    src/monster_state_model.v ^
    src/tactical_stance_unit.v ^
    src/sanity_meter_unit.v ^
    src/sprite_router.v ^
    src/terminal_ui.v ^
    tb/tb_play.v
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo [ERROR] Verilog RTL compilation failed! See diagnostics above.
    pause
    exit /b 1
)

echo [OK] Hardware RTL compiled with 0 errors and 0 warnings!
echo [*] Launching pure Verilog RTL simulation ^(vvp sim/funger_play.out^)...
echo.
powershell -NoProfile -ExecutionPolicy Bypass -Command "$s=[IO.File]::ReadAllText('%~f0'); $p=[regex]::Split($s,'(?m)^__PS_HOST_BEGIN__\r?$'); Invoke-Expression $p[1]"
set "RC=%ERRORLEVEL%"

pause
exit /b %RC%

__PS_HOST_BEGIN__
$ErrorActionPreference = 'Stop'
if ([Console]::IsInputRedirected) {
    & vvp sim/funger_play.out
    exit $LASTEXITCODE
}

function Convert-KeyToCmd {
    param([System.ConsoleKeyInfo]$KeyInfo)
    if ([int]$KeyInfo.KeyChar -eq 3) { return $null }
    if ($KeyInfo.Key -eq [ConsoleKey]::UpArrow)    { return "w" }
    if ($KeyInfo.Key -eq [ConsoleKey]::DownArrow)  { return "s" }
    if ($KeyInfo.Key -eq [ConsoleKey]::LeftArrow)  { return "a" }
    if ($KeyInfo.Key -eq [ConsoleKey]::RightArrow) { return "d" }
    if ($KeyInfo.Key -eq [ConsoleKey]::Enter -or $KeyInfo.Key -eq [ConsoleKey]::Spacebar) { return "e" }
    if ($KeyInfo.Key -eq [ConsoleKey]::Escape -or $KeyInfo.Key -eq [ConsoleKey]::Backspace) { return "x" }
    if ([int]$KeyInfo.KeyChar -ge 33 -and [int]$KeyInfo.KeyChar -le 126) { return [string]$KeyInfo.KeyChar }
    return $null
}

function Test-FrameComplete {
    param([System.IO.MemoryStream]$Ms)
    $len = [int]$Ms.Length
    if ($len -lt 3) { return $false }
    $raw = $Ms.GetBuffer()
    $end = $len
    while ($end -gt 0 -and ($len - $end) -lt 2 -and ($raw[$end - 1] -eq 0x0A -or $raw[$end - 1] -eq 0x0D)) {
        $end--
    }
    if ($end -ge 3 -and $raw[$end - 3] -eq 0x1B -and $raw[$end - 2] -eq 0x5B -and $raw[$end - 1] -eq 0x4A) {
        return $true
    }
    if ($end -ge 6 -and $raw[$end - 6] -eq 0x1B -and $raw[$end - 5] -eq 0x5B -and $raw[$end - 4] -eq 0x3F -and $raw[$end - 3] -eq 0x32 -and $raw[$end - 2] -eq 0x35 -and $raw[$end - 1] -eq 0x68) {
        return $true
    }
    return $false
}

[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
[Console]::TreatControlCAsInput = $true
$psi = New-Object System.Diagnostics.ProcessStartInfo
$psi.FileName = "vvp"
$psi.Arguments = "sim/funger_play.out"
$psi.WorkingDirectory = (Get-Location).Path
$psi.UseShellExecute = $false
$psi.RedirectStandardInput = $true
$psi.RedirectStandardOutput = $true
$psi.RedirectStandardError = $false

$proc = [System.Diagnostics.Process]::Start($psi)
$stdout = [Console]::OpenStandardOutput()
$buf = New-Object byte[] 8192
$frameMs = New-Object System.IO.MemoryStream
$ar = $proc.StandardOutput.BaseStream.BeginRead($buf, 0, $buf.Length, $null, $null)
$eof = $false
$queuedKey = $null
$sw = [System.Diagnostics.Stopwatch]::StartNew()

try {
    [Console]::CursorVisible = $false
    while ($true) {
        while ($ar.IsCompleted) {
            $n = $proc.StandardOutput.BaseStream.EndRead($ar)
            if ($n -le 0) { $eof = $true; break }
            $frameMs.Write($buf, 0, $n)
            $ar = $proc.StandardOutput.BaseStream.BeginRead($buf, 0, $buf.Length, $null, $null)
        }
        if ($frameMs.Length -gt 0 -and -not $eof -and -not $proc.HasExited) {
            $burstStart = $sw.ElapsedMilliseconds
            while (-not $eof -and -not $proc.HasExited) {
                while ($ar.IsCompleted) {
                    $n = $proc.StandardOutput.BaseStream.EndRead($ar)
                    if ($n -le 0) { $eof = $true; break }
                    $frameMs.Write($buf, 0, $n)
                    $ar = $proc.StandardOutput.BaseStream.BeginRead($buf, 0, $buf.Length, $null, $null)
                }
                if ($eof -or $proc.HasExited) { break }
                if (Test-FrameComplete $frameMs) {
                    if ($ar.AsyncWaitHandle.WaitOne(4)) {
                        continue
                    }
                    break
                }
                $elapsed = $sw.ElapsedMilliseconds - $burstStart
                if ($elapsed -ge 180) { break }
                $waitMs = [Math]::Min(16, [int](180 - $elapsed))
                if (-not $ar.AsyncWaitHandle.WaitOne($waitMs)) {
                    if (($sw.ElapsedMilliseconds - $burstStart) -ge 180) { break }
                }
            }
        }
        if ($frameMs.Length -gt 0) {
            $arr = $frameMs.ToArray()
            $stdout.Write($arr, 0, $arr.Length)
            $stdout.Flush()
            $frameMs.SetLength(0)
        }
        if ($eof -or $proc.HasExited) { break }

        if ($queuedKey -ne $null -or [Console]::KeyAvailable) {
            if ($queuedKey -ne $null) {
                $k = $queuedKey
                $queuedKey = $null
            } else {
                $k = [Console]::ReadKey($true)
            }
            if ([int]$k.KeyChar -eq 3) {
                $rst = [byte[]](0x1B, 0x5B, 0x30, 0x6D, 0x1B, 0x5B, 0x3F, 0x32, 0x35, 0x68)
                $stdout.Write($rst, 0, $rst.Length)
                $stdout.Flush()
                break
            }
            $cmd = Convert-KeyToCmd $k
            if ($cmd -ne $null) {
                while ([Console]::KeyAvailable) {
                    $next = [Console]::ReadKey($true)
                    if ([int]$next.KeyChar -eq 3) {
                        $queuedKey = $next
                        break
                    }
                    $nextCmd = Convert-KeyToCmd $next
                    if ($nextCmd -eq $null) {
                        continue
                    }
                    if (($next.Key -eq $k.Key) -or ($nextCmd -eq $cmd)) {
                        continue
                    }
                    $queuedKey = $next
                    break
                }
                try {
                    $proc.StandardInput.WriteLine($cmd)
                    $proc.StandardInput.Flush()
                } catch {
                    break
                }
            }
        } else {
            $null = $ar.AsyncWaitHandle.WaitOne(10)
        }
    }
} finally {
    [Console]::CursorVisible = $true
    if (-not $proc.HasExited) {
        try { $proc.Kill() } catch {}
    }
    $proc.WaitForExit()
}
exit $proc.ExitCode
