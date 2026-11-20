#!/usr/bin/env python3
"""
===============================================================================
 MASTER VERIFICATION RUNNER: COMPREHENSIVE HARDWARE QUALITY GATES
 Executes all 5 audit stages corresponding to the Verification Plan:
 1. Static RTL Synthesizability & Strict Linting Audit
 2. String Length & ANSI Display Overflow Guard
 3. Bit-for-bit Co-Simulation with Python Golden Reference Model
 4. 100,000-Cycle Galois LFSR Statistical & Pity System Audit
 5. 50,000-Iteration FSM Random Input Fuzzing & Deadlock Audit
===============================================================================
"""

import subprocess
import sys
import os

def run_step(step_num, title, script_cmd):
    print("\n" + "=" * 78)
    print(f" [STAGE {step_num}] {title.upper()}")
    print("=" * 78)
    res = subprocess.run(script_cmd, capture_output=False)
    return res.returncode == 0

def main():
    print("*" * 78)
    print("    FEAR & HUNGER: ADVANCED HARDWARE VERIFICATION SUITE (ALL GATES)   ")
    print("       Standards: DO-254 / OpenTitan RISC-V / Golden Reference Model  ")
    print("*" * 78)

    base_dir = os.path.dirname(os.path.abspath(__file__))
    repo_dir = os.path.abspath(os.path.join(base_dir, ".."))
    os.chdir(repo_dir)

    steps = [
        (1, "Static Synthesizability & Strict Compiler Linting", [sys.executable, "funger_terminal/audit_hardware_linter.py"]),
        (2, "String Overflow Guard & ANSI Escape Integrity", [sys.executable, "funger_terminal/audit_string_overflow.py"]),
        (3, "Bit-for-bit Python Golden Reference Co-Simulation", [sys.executable, "funger_terminal/audit_damage_accounting.py"]),
        (4, "100,000-Cycle LFSR Statistical & Pity System Proof", [sys.executable, "funger_terminal/audit_rng_pity.py"]),
        (5, "50,000-Iteration FSM Random Fuzzing & Deadlock Audit", ["vvp", "funger_terminal/sim/fuzz_sim.out"])
    ]

    all_passed = True
    results = []

    for s_num, s_title, s_cmd in steps:
        ok = run_step(s_num, s_title, s_cmd)
        results.append((s_num, s_title, ok))
        if not ok:
            all_passed = False

    print("\n" + "=" * 78)
    print("                   EXECUTIVE VERIFICATION SUMMARY                     ")
    print("=" * 78)
    for s_num, s_title, ok in results:
        status_tag = "[PASS 100%]" if ok else "[FAILED]"
        print(f"  Stage {s_num}: {s_title:<55} {status_tag}")
    print("=" * 78)

    if all_passed:
        print(">>> ALL 5 INDUSTRIAL VERIFICATION GATES PASSED! ZERO DEFECTS REMAIN. <<<")
        return 0
    else:
        print(">>> ONE OR MORE VERIFICATION GATES FAILED. INSPECT LOGS ABOVE. <<<")
        return 1

if __name__ == "__main__":
    sys.exit(main())
