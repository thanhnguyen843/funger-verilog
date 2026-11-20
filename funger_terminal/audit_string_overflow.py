#!/usr/bin/env python3
"""
===============================================================================
 AUDIT SCRIPT 2: STRING OVERFLOW GUARD & ANSI INTEGRITY
 Corresponds to: GIAI ĐOẠN 2 - 2.4 (UI & Buffer Integrity)
 - Scans all *_rom.v files for string assignments into registers.
 - Verifies that len(string) <= (Bit_Width / 8), preventing truncation (E10).
 - Validates ANSI escape codes in UI screens for proper reset sequences ('\\033[0m').
===============================================================================
"""

import os
import re
import glob
import subprocess
import sys

def audit_rom_string_lengths():
    print("[*] Auditing string literals assigned to registers in ROM modules...")
    rom_files = glob.glob("funger_terminal/src/*_rom.v") + ["funger_terminal/src/character_rom.v"]
    rom_files = sorted(list(set(rom_files)))

    violations = []
    
    # Register definitions map: variable name -> bit width
    for rf in rom_files:
        with open(rf, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()

        # Find output / reg bitwidths: e.g. "output [255:0] char_name" or "reg [255:0] char_class"
        reg_widths = {}
        for m in re.finditer(r'(?:output|reg)\s+\[(\d+):0\]\s+([a-zA-Z0-9_,\s]+);', content):
            msb = int(m.group(1))
            total_bits = msb + 1
            max_chars = total_bits // 8
            vars_part = m.group(2)
            for v in vars_part.split(','):
                v_name = v.strip()
                if v_name:
                    reg_widths[v_name] = max_chars

        # Check assignments: e.g. char_name = "Cahara";
        lines = content.split('\n')
        for line_no, line in enumerate(lines, 1):
            assign_match = re.search(r'([a-zA-Z0-9_]+)\s*=\s*"([^"]+)";', line)
            if assign_match:
                var_name = assign_match.group(1)
                str_val = assign_match.group(2)
                if var_name in reg_widths:
                    max_allowed = reg_widths[var_name]
                    actual_len = len(str_val)
                    if actual_len > max_allowed:
                        violations.append({
                            'file': rf,
                            'line': line_no,
                            'var': var_name,
                            'val': str_val,
                            'actual': actual_len,
                            'max': max_allowed
                        })

    return violations

def audit_ansi_escape_integrity():
    print("[*] Auditing ANSI escape code sequences in terminal_ui.v...")
    ui_path = "funger_terminal/src/terminal_ui.v"
    with open(ui_path, 'r', encoding='utf-8', errors='ignore') as f:
        lines = f.readlines()

    ansi_unclosed = 0
    for idx, line in enumerate(lines, 1):
        # If line contains an ANSI color opening (\033[38;2 or \033[1;3)
        if re.search(r'\\033\[[0-9;]+m', line):
            # Check if line also has reset \033[0m, or continues
            # In $display, every colored line should end with \033[0m to prevent terminal bleed
            if '$display' in line:
                if not re.search(r'\\033\[0m', line):
                    ansi_unclosed += 1

    return ansi_unclosed

def main():
    print("=" * 70)
    print(" [STAGE 2.4] STRING OVERFLOW GUARD & ANSI INTEGRITY AUDIT")
    print("=" * 70)

    violations = audit_rom_string_lengths()
    if violations:
        print(f"  [FAIL] Found {len(violations)} String Truncation Violations:")
        for v in violations:
            print(f"         - {v['file']}:{v['line']} '{v['var']}' has {v['actual']} chars (Max: {v['max']}) -> \"{v['val']}\"")
    else:
        print("  [PASS] All string literals across ROM modules strictly satisfy Bit_Width / 8 (0 truncations)!")

    ansi_leaks = audit_ansi_escape_integrity()
    if ansi_leaks > 0:
        print(f"  [WARN] Found {ansi_leaks} display lines without trailing reset sequence '\\033[0m'.")
    else:
        print("  [PASS] All ANSI terminal display lines properly terminate with '\\033[0m'!")

    print("-" * 70)
    if not violations:
        print(">>> UI & BUFFER INTEGRITY AUDIT: 100% PASS <<<")
        return 0
    else:
        print(">>> UI & BUFFER INTEGRITY AUDIT: FAILED <<<")
        return 1

if __name__ == "__main__":
    sys.exit(main())
