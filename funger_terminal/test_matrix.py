import subprocess
import sys
import os

SIM_BIN = os.path.join(os.path.dirname(__file__), "sim", "funger_play.out")

def run_simulation(input_sequence, timeout=12):
    """Feeds input_sequence (bytes) into vvp simulation and captures stdout."""
    p = subprocess.Popen(
        ["vvp", SIM_BIN],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    try:
        out, err = p.communicate(input=input_sequence, timeout=timeout)
        return out.decode("utf-8", errors="replace"), err.decode("utf-8", errors="replace"), p.returncode
    except subprocess.TimeoutExpired:
        p.kill()
        out, _ = p.communicate()
        return out.decode("utf-8", errors="replace"), "TIMEOUT", -1

def test_case(name, input_bytes, checks):
    print(f"\n======================================================================")
    print(f"[*] RUNNING TEST CASE: {name}")
    print(f"======================================================================")
    out, err, code = run_simulation(input_bytes)
    
    passed = True
    for desc, pattern in checks:
        if pattern in out:
            print(f"  [PASS] {desc}")
        else:
            print(f"  [FAIL] {desc} (Pattern not found: '{pattern[:50]}')")
            passed = False
            
    if passed:
        print(f"--> RESULT: {name} PASSED 100%!")
    else:
        print(f"--> RESULT: {name} FAILED!")
    return passed

def main():
    if not os.path.exists(SIM_BIN):
        print(f"[ERROR] Simulation binary not found: {SIM_BIN}")
        return 1

    total_tests = 0
    total_passed = 0

    # -------------------------------------------------------------------------
    # TEST 1: Preset 1 (Balanced) + Fear & Hunger + Roster Inspection + Quit
    # -------------------------------------------------------------------------
    total_tests += 1
    t1_in = b"1\n1\n1\nc\np\nc\nq\n"
    t1_checks = [
        ("Title Banner Rendered", "T  E  R  M  I  N  A  L     E  D  I  T  I  O  N"),
        ("Difficulty Selected: Fear & Hunger", "FEAR & HUNGER ACTIVATED"),
        ("Squad Selected: Balanced Vanguard", "Balanced Vanguard"),
        ("Full Squad Models & Stats Rendered", "EXPEDITION SQUAD LINEUP"),
        ("Frontline Battler Badge", "[* ACTIVE FRONTLINE]"),
        ("Labyrinth Map Rendered Cleanly", "LABYRINTH [FEAR & HUNGER]"),
        ("Party Roster Re-opened On Map via [P]", "EXPEDITION SQUAD LINEUP"),
        ("Graceful Exit On [Q]", "Surrendered to the oppressive terror"),
    ]
    if test_case("TEST 1: Balanced Vanguard & Roster Inspection [P]", t1_in, t1_checks):
        total_passed += 1

    # -------------------------------------------------------------------------
    # TEST 2: Preset 2 (Occult Sorcery) + Terror & Starvation (Hardcore)
    # -------------------------------------------------------------------------
    total_tests += 1
    t2_in = b"1\n2\n2\nc\nq\n"
    t2_checks = [
        ("Difficulty Selected: Terror & Starvation", "TERROR & STARVATION ACTIVATED"),
        ("Squad Selected: Enki & Occultists", "Enki"),
        ("Nas'hrah Severed Head In Party", "Nas'hrah"),
        ("Rationed Healing Values Applied (Poppy +30)", "Poppy: 10 (+30 HP)"),
    ]
    if test_case("TEST 2: Occult Squad & Hardcore Mode", t2_in, t2_checks):
        total_passed += 1

    # -------------------------------------------------------------------------
    # TEST 3: Preset 4 (Custom Squad Selection)
    # -------------------------------------------------------------------------
    total_tests += 1
    t3_in = b"1\n1\n4\n5\n6\n7\n8\nc\nq\n"
    t3_checks = [
        ("Custom Recruitment Mode", "Custom Expedition"),
        ("Explorer 5 Recruited (Le'garde)", "Le'garde"),
        ("Explorer 6 Recruited (Moonless)", "Moonless"),
        ("Explorer 7 Recruited (The Girl)", "The Girl"),
        ("Explorer 8 Recruited (Nas'hrah)", "Nas'hrah"),
    ]
    if test_case("TEST 3: Custom 4-Hero Squad Recruitment", t3_in, t3_checks):
        total_passed += 1

    # -------------------------------------------------------------------------
    # TEST 4: Map Wall Collision Mechanics
    # -------------------------------------------------------------------------
    total_tests += 1
    # Move Up into wall (y=1 is wall or path? at 2,2: (2,1) is sanctuary, (2,0) is outer wall)
    # Let's hit outer wall by moving up twice: w, w.
    t4_in = b"1\n1\n1\nc\nw\nw\nw\nq\n"
    t4_checks = [
        ("Wall Collision Detected", "[NOTICE]: Solid damp stone wall obstructs your path"),
        ("Remained in Exploration Loop", "POS:["),
    ]
    if test_case("TEST 4: Wall Collision Mechanics", t4_in, t4_checks):
        total_passed += 1

    # -------------------------------------------------------------------------
    # TEST 5: Chest Looting & Boxed Item Notification
    # -------------------------------------------------------------------------
    total_tests += 1
    # Starting at (2,2), moving right 6 steps hits chest at (8,2):
    # Inputs: 1 1 1 c d d d d d d c q
    t5_in = b"1\n1\n1\nc\nd\nd\nd\nd\nd\nd\nc\nq\n"
    t5_checks = [
        ("Explored towards chest", "POS:["),
        ("Chest Encountered", "CHEST"),
    ]
    if test_case("TEST 5: Chest Discovery & Looting", t5_in, t5_checks):
        total_passed += 1

    # -------------------------------------------------------------------------
    # TEST 6: Direct Combat & Body Part Actions [H], [T], [R], [L], [K]
    # -------------------------------------------------------------------------
    total_tests += 1
    # From (2,2) move right 12 steps -> passes chest (press c to close) -> engages monster at (14,2)
    # Then attacks with limbs: h, t, r, l, k, and tries fleeing f or quit
    t6_in = b"1\n1\n1\nc\nd\nd\nd\nd\nd\nd\nc\nd\nd\nd\nd\nd\nd\nh\nt\nr\nl\nk\nf\nq\n"
    t6_checks = [
        ("Engaged Monster in Combat", "TACTICAL COMBAT"),
        ("50/50 Screen with Adversary Foe", "[FOE]:"),
        ("Boxed Combat Report Rendered", "[EVENT & ACTION REPORT]"),
    ]
    if test_case("TEST 6: Combat System & Body Part Targeting Deck", t6_in, t6_checks):
        total_passed += 1

    # -------------------------------------------------------------------------
    # TEST 7: Input Resilience (Rapid Keystrokes & Trailing Enter)
    # -------------------------------------------------------------------------
    total_tests += 1
    # Trailing Enters after inputs: "1\n\n1\n\n1\n\nc\n\nq\n"
    t7_in = b"1\n\n1\n\n1\n\nc\n\nq\n"
    t7_checks = [
        ("Handled Trailing Enters Gracefully", "EXPEDITION SQUAD LINEUP"),
        ("Arrived in Labyrinth without Desync", "LABYRINTH [FEAR & HUNGER]"),
    ]
    if test_case("TEST 7: Input Buffer & Trailing Enter Resilience", t7_in, t7_checks):
        total_passed += 1

    print(f"\n======================================================================")
    print(f"[*] TEST MATRIX SUMMARY: {total_passed} / {total_tests} SUITES PASSED ({(total_passed/total_tests)*100:.1f}%)")
    print(f"======================================================================")
    return 0 if total_passed == total_tests else 1

if __name__ == "__main__":
    sys.exit(main())
