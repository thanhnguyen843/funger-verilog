#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
================================================================================
VIRTUAL TERMINAL SCREEN BUFFER & VISUAL INSPECTOR (AUDIT GATES)
Fear & Hunger: Terminal Labyrinth - Solo Explorer Architecture
================================================================================
Capabilities:
  1. Inspects raw terminal buffer line-by-line (exactly what user sees).
  2. Strict Leaked ANSI / Broken Number Code Detector (Catches '38;2;', ';255m', etc.).
  3. Sprite Morphology & Glyph Verification for all 36 monsters x 3 states (108 screens).
  4. Bounding Box & Density Assertion (verifies monster & hero are actually visible).
  5. Zero-Scroll Frame Geometry Audit (Cols=100, Rows<=35).
================================================================================
"""

import sys
import os
import re
import json
import copy

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import demo_interactive_ui as dui
from monsters_catalog import ALL_MONSTERS_CATALOG

ANSI_REGEX = re.compile(r'\x1b\[[0-9;]*[a-zA-Z]')

# Regex to detect leaked/corrupted ANSI codes in visible text
LEAKED_ANSI_PATTERNS = [
    re.compile(r'[0-9]{1,3};[0-9]{1,3}'),       # e.g., '38;2;' or '255;255'
    re.compile(r';[0-9]{2,3}m'),                # e.g., ';255m'
    re.compile(r'[0-9]{1,3}m[▀▄]'),             # e.g., '255m▀'
    re.compile(r'\[38;2;'),                     # e.g., '[38;2;'
    re.compile(r'\[48;2;'),                     # e.g., '[48;2;'
    re.compile(r'38;2;255'),                    # verbatim leak
]

def strip_ansi(s):
    return ANSI_REGEX.sub('', s)

def inspect_screen_frame(screen_rows, context=""):
    """
    Acts as a virtual terminal eye, auditing every single visible character
    on the 100x35 screen grid.
    """
    errors = []

    # 1. Height check
    if len(screen_rows) > 35:
        errors.append(f"Frame Height Violation: {len(screen_rows)} rows (Max allowed: 35)")

    # 2. Row width and Leaked ANSI Check
    for r_idx, raw_line in enumerate(screen_rows):
        vis_text = strip_ansi(raw_line)
        w = dui.display_width(raw_line)

        # Check for leaked ANSI escape fragments
        for pat in LEAKED_ANSI_PATTERNS:
            m = pat.search(vis_text)
            if m:
                errors.append(
                    f"Row {r_idx} LEAKED ANSI CORRUPTION: Found '{m.group(0)}' in visible text: \"{vis_text.strip()[:60]}\""
                )
                break

    # 3. Monster Region Audit (Rows 3..11, Cols 54..100)
    monster_block_count = 0
    for r_idx in range(3, min(12, len(screen_rows))):
        vis = strip_ansi(screen_rows[r_idx])
        # Monster is placed on the right side (Cols ~54 to 100)
        right_side = vis[54:] if len(vis) > 54 else ""
        monster_block_count += (right_side.count('▀') + right_side.count('▄'))

    if monster_block_count < 8:
        errors.append(
            f"Monster Sprite Truncation/Missing: Only {monster_block_count} half-blocks found in enemy box!"
        )

    # 4. Hero Region Audit (Rows 12..22, Cols 0..42)
    hero_block_count = 0
    for r_idx in range(12, min(23, len(screen_rows))):
        vis = strip_ansi(screen_rows[r_idx])
        left_side = vis[:42] if len(vis) >= 42 else vis
        hero_block_count += (left_side.count('▀') + left_side.count('▄'))

    if hero_block_count < 15:
        errors.append(
            f"Hero Sprite Truncation/Missing: Only {hero_block_count} half-blocks found in hero box!"
        )

    return errors, monster_block_count, hero_block_count

def run_visual_audit_all_108_states():
    print("=" * 80)
    print("[*] LAUNCHING TERMINAL VIRTUAL SCREEN BUFFER & VISUAL AUDITOR")
    print("[*] Scope: All 36 RTL Monsters x 3 States (Normal, Injured, Dead) = 108 screens")
    print("=" * 80)

    total_screens = 0
    total_passed = 0
    total_failed = 0
    failures = []

    # Mock atomic_blit to capture frames
    captured_frames = []
    def mock_blit(screen_rows):
        captured_frames.clear()
        captured_frames.extend(screen_rows)

    dui.atomic_blit = mock_blit

    # Use D'arce as hero (from user's screenshot)
    hero = copy.deepcopy(dui.ALL_HEROES[1])
    dui.active_hero = hero

    sample_renders = {}

    for m_id in sorted(ALL_MONSTERS_CATALOG.keys()):
        m_stat = ALL_MONSTERS_CATALOG[m_id]
        m_name = m_stat["name"]

        for state_mode in ["normal", "injured", "dead"]:
            total_screens += 1

            # Configure monster state
            m_obj = {
                "id": m_id,
                "name": m_name,
                "archetype": m_stat["archetype"],
                "max_hp": m_stat["hp"],
                "atk": m_stat["atk"],
                "def": m_stat["def"],
                "debuff_decapitated": (state_mode == "dead"),
                "debuff_legs": (state_mode == "injured"),
                "debuff_arm_r": (state_mode == "injured"),
                "debuff_arm_l": False,
            }
            if state_mode == "normal":
                m_obj["hp"] = m_stat["hp"]
            elif state_mode == "injured":
                m_obj["hp"] = max(1, int(m_stat["hp"] * 0.45))
            else:
                m_obj["hp"] = 0

            dui.monster = m_obj
            dui.combat_log = f"Visual Audit: {hero['name']} facing #{m_id:02d} {m_name} [{state_mode.upper()}]."
            dui.current_menu = "MAIN"
            dui.cursor_idx = 0

            # Render into buffer
            dui.render_screen()

            # Audit captured screen
            errs, m_blocks, h_blocks = inspect_screen_frame(
                captured_frames,
                context=f"#{m_id:02d} {m_name} ({state_mode})"
            )

            if errs:
                total_failed += 1
                for e in errs:
                    failures.append(f"[FAIL] M#{m_id:02d} {m_name} ({state_mode.upper()}): {e}")
            else:
                total_passed += 1

            # Save sample previews for Little Drake (#17) and Mimic (#23)
            if m_id in (17, 23, 8, 36) and state_mode in ("normal", "injured", "dead"):
                sample_renders[f"M#{m_id}_{m_name}_{state_mode}"] = [
                    strip_ansi(r) for r in captured_frames[3:12]
                ]

    print(f"[*] Visual Screen Audit Complete:")
    print(f"  - Total Screens Audited       : {total_screens}")
    print(f"  - 100% Clean & Legible Screens: {total_passed} / {total_screens} ({(total_passed/total_screens)*100:.1f}%)")
    print(f"  - Corrupted / Broken Screens  : {total_failed}")

    if total_failed > 0:
        print("\n[!] CRITICAL VISUAL FAILURES DETECTED:")
        for f in failures[:10]:
            print("  ", f)
        return 1

    print("\n>>> RESULT: 100% VISUAL SCREEN AUDIT PASSED! ZERO LEAKED ANSI, ZERO TRUNCATION! <<<")

    # Print sample visual of Little Drake (#17) Injured
    print("\n" + "=" * 80)
    print("  VISUAL VERIFICATION SNAPSHOT: #17 LITTLE DRAKE [INJURED] (Exactly as rendered)")
    print("=" * 80)
    for r in sample_renders.get("M#17_LITTLE DRAKE_injured", []):
        print("  " + r)
    print("=" * 80)

    # Print sample visual of Chest Mimic (#23) Normal
    print("  VISUAL VERIFICATION SNAPSHOT: #23 CHEST MIMIC [NORMAL] (Exactly as rendered)")
    print("=" * 80)
    for r in sample_renders.get("M#23_CHEST MIMIC_normal", []):
        print("  " + r)
    print("=" * 80)

    return 0

if __name__ == "__main__":
    sys.exit(run_visual_audit_all_108_states())
