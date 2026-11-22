#!/usr/bin/env python3
"""
===============================================================================
 AUDIT SCRIPT 1: HARDWARE SYNTHESIZABILITY & LINTING AUDIT
 Corresponds to: GIAI ĐOẠN 1 (Hardware Synthesizability & Compiler Checks)
 - Checks for non-synthesizable division ('/') or modulo ('%') operators in RTL.
 - Strips string literals so formatting '%0d' or 'A / B' in strings are ignored.
 - Checks for forbidden hierarchical references in RTL ('module.signal').
 - Runs iverilog with strict warning flags (-Wall -g2012) across ALL modules.
===============================================================================
"""

import os
import re
import glob
import subprocess
import sys

def strip_strings_and_comments(line):
    # Remove single-line comments
    line = re.sub(r'//.*$', '', line)
    # Remove string literals
    line = re.sub(r'"([^"\\]|\\.)*"', '""', line)
    return line.strip()

def check_rtl_synthesizability(filepath):
    errors = []
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        lines = f.readlines()

    in_comment_block = False
    for idx, raw_line in enumerate(lines, 1):
        clean = raw_line.strip()
        if '/*' in clean:
            in_comment_block = True
        if '*/' in clean:
            in_comment_block = False
            continue
        if in_comment_block or clean.startswith('//'):
            continue

        code_part = strip_strings_and_comments(clean)
        if not code_part:
            continue

        # Ignore timescale and display/system tasks
        if code_part.startswith('`timescale') or '$display' in code_part or '$write' in code_part:
            continue

        # 1. Check for hardware division: exclude timescale and power-of-2 divisors
        div_matches = re.finditer(r'/\s*([a-zA-Z0-9_\'\$]+)', code_part)
        for m in div_matches:
            divisor = m.group(1)
            # Power of 2 is synthesizable (can be synthesized as shift)
            if not re.match(r"^(1|2|4|8|16|32|64|128|256|8'd1|8'd2|8'd4|8'd8|8'd16|8'd32)$", divisor):
                errors.append(f"Line {idx}: Forbidden hardware division by '{divisor}' -> {code_part}")

        # 2. Check for hardware modulo
        mod_matches = re.finditer(r'%\s*([a-zA-Z0-9_\'\$]+)', code_part)
        for m in mod_matches:
            mod_val = m.group(1)
            errors.append(f"Line {idx}: Forbidden hardware modulo by '{mod_val}' -> {code_part}")

        # 3. Check for hierarchical cross-module references in synthesizable RTL
        hier_matches = re.finditer(r'\b(u_\w+)\.(\w+)', code_part)
        for m in hier_matches:
            probe = m.group(0)
            errors.append(f"Line {idx}: Forbidden hierarchical probe '{probe}' -> {code_part}")

    return errors

def run_iverilog_strict_lint():
    print("[*] Running strict compiler linting (iverilog -Wall -g2012)...")
    src_files = glob.glob("funger_terminal/src/*.v")
    cmd = [
        "iverilog", "-Wall", "-g2012", "-I", "funger_terminal/src",
        "-o", "funger_terminal/sim/lint_check.out",
        "funger_terminal/tb/tb_play.v"
    ] + src_files

    res = subprocess.run(cmd, capture_output=True, text=True)
    lint_warnings = []
    if res.stderr:
        for l in res.stderr.strip().split('\n'):
            line_str = l.strip()
            if line_str and "timescale for" not in line_str and "The inherited timescale" not in line_str:
                lint_warnings.append(line_str)
    return res.returncode, lint_warnings

def main():
    print("=" * 70)
    print(" [STAGE 1] STATIC HARDWARE SYNTHESIZABILITY & LINTING AUDIT")
    print("=" * 70)

    # Core Synthesizable Hardware RTL modules
    core_rtl_files = [
        "funger_terminal/src/damage_alu.v",
        "funger_terminal/src/rng_unit.v",
        "funger_terminal/src/collision_unit.v",
        "funger_terminal/src/inventory_ram.v",
        "funger_terminal/src/map_rom.v",
        "funger_terminal/src/monster_rom.v",
        "funger_terminal/src/character_rom.v",
        "funger_terminal/src/battle_top.v",
        "funger_terminal/src/battle_fsm.v",
        "funger_terminal/src/tactical_stance_unit.v",
        "funger_terminal/src/sanity_meter_unit.v"
    ]

    total_errors = 0
    print(f"[*] Auditing {len(core_rtl_files)} Core Synthesizable RTL Modules...")
    for sf in core_rtl_files:
        rel_path = os.path.relpath(sf)
        errs = check_rtl_synthesizability(sf)
        if errs:
            print(f"  [FAIL] {rel_path}: {len(errs)} non-synthesizable violations found!")
            for e in errs:
                print(f"         - {e}")
            total_errors += len(errs)
        else:
            print(f"  [PASS] {rel_path}: Clean synthesizable RTL (0 $div, 0 $mod, 0 probes)")

    ret, compiler_warns = run_iverilog_strict_lint()
    if ret != 0:
        print("  [FAIL] Compiler reported compilation errors!")
        for w in compiler_warns:
            print(f"         {w}")
        total_errors += 1
    elif compiler_warns:
        serious = [w for w in compiler_warns if "warning:" in w and ("Padding" in w or "expects" in w or "undefined" in w)]
        if serious:
            print(f"  [FAIL] Compiler reported {len(serious)} serious port/width warnings!")
            for w in serious:
                print(f"         - {w}")
            total_errors += len(serious)
        else:
            print(f"  [PASS] Compiler completed cleanly (0 serious port/width warnings).")
    else:
        print("  [PASS] Compiler completed with 0 errors and 0 warnings.")

    print("-" * 70)
    if total_errors == 0:
        print(">>> GIAI ĐOẠN 1 KẾT QUẢ: 100% ĐẠT CHUẨN TỔNG HỢP PHẦN CỨNG (SYNTHESIZABLE RTL) <<<")
        return 0
    else:
        print(f">>> GIAI ĐOẠN 1 KẾT QUẢ: PHÁT HIỆN {total_errors} VI PHẠM CẦN KHẮC PHỤC! <<<")
        return 1

if __name__ == "__main__":
    sys.exit(main())
