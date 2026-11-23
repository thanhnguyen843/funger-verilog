#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
================================================================================
HERO SEVERED LIMB SHOWCASE & MORPHOLOGY VIEWER (INTERACTIVE TERMINAL UI)
Fear & Hunger: Terminal Labyrinth - Solo Explorer Architecture
================================================================================
Controls:
  - [W/S] or [Up/Down]   : Switch Active Hero (8 Characters)
  - [A/D] or [Left/Right]: Switch Mutilation State (Intact / Severed Arms / Crippled Legs)
  - [Q] or [Esc]         : Exit Viewer
================================================================================
"""

import sys
import os
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from hero_severed_limbs_catalog import HERO_SEVERED_MODELS, C_AMBER, C_RESET
import demo_interactive_ui as dui

if os.name == 'nt':
    import msvcrt

def run_hero_mutilation_showcase():
    hero_keys = ["D'ARCE", "CAHARA", "RAGNVALDR", "LE'GARDE", "ENKI", "THE GIRL", "MOONLESS", "NAS'HRAH"]
    hero_idx = 0
    variant_idx = 0

    dui.clear_screen()

    while True:
        h_name = hero_keys[hero_idx]
        hero_variants = HERO_SEVERED_MODELS[h_name]
        var_keys = list(hero_variants.keys())
        variant_idx = variant_idx % len(var_keys)
        cur_var_key = var_keys[variant_idx]

        sprite_rows = hero_variants[cur_var_key]

        rows = []
        rows.append("\033[1;30m+" + "=" * 98 + "+\033[0m")
        title_str = "FEAR & HUNGER: HERO SEVERED LIMB MORPHOLOGY SHOWCASE"
        rows.append(f"\033[1;30m| \033[1;33m{dui.fit_ansi(title_str, 96)}\033[1;30m |\033[0m")
        rows.append("\033[1;30m+----------------------------------------------------------------------------------------------------+\033[0m")

        hero_banner = f"  HERO: \033[1;32m{h_name:<14}\033[0m | MUTILATION: \033[1;31m{cur_var_key.upper().replace('_', ' '):<28}\033[0m | AMBER SOCKET: \033[38;2;255;170;40m#FFAA28\033[0m"
        rows.append(f"\033[1;30m|{dui.fit_ansi(hero_banner, 98)}\033[1;30m|\033[0m")
        rows.append("\033[1;30m+ - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -+\033[0m")

        # 12 rows of side-by-side rendering:
        # Left: Intact Hero Model (42 cols) | Mid divider: 4 cols | Right: Severed/Mutilated Model (52 cols)
        intact_rows = hero_variants.get("intact", [" " * 29] * 12)

        # Header for the two columns
        col_hdr = "       \033[1;37m[INTACT MODEL]\033[0m                   |      \033[1;33m[MUTILATED / AMBER STUMP MODEL]\033[0m"
        rows.append(f"\033[1;30m|\033[0m{dui.fit_ansi(col_hdr, 98)}\033[1;30m|\033[0m")
        rows.append("\033[1;30m+------------------------------------------------+---------------------------------------------------+\033[0m")

        for r in range(12):
            sp_left = intact_rows[r] if r < len(intact_rows) else " " * 29
            sp_right = sprite_rows[r] if r < len(sprite_rows) else " " * 29

            left_box = dui.fit_ansi("      " + sp_left, 48)
            right_box = dui.fit_ansi("      " + sp_right, 49)
            rows.append(f"\033[1;30m|{left_box}\033[1;30m|{right_box}\033[1;30m|\033[0m")

        rows.append("\033[1;30m+====================================================================================================+\033[0m")

        # Assessment / Lore box
        if h_name == "NAS'HRAH":
            lore = "\033[1;36mNAS'HRAH LORE:\033[0m Floating severed head possesses no arms/legs. Trauma shatters skull with amber fissures."
        elif h_name == "MOONLESS":
            lore = "\033[1;36mMOONLESS LORE:\033[0m Quadruped dire wolf amputations affect front forelegs and rear hindquarters."
        else:
            lore = f"\033[1;36m{h_name} LORE:\033[0m Wielding arm severing disables main weapons; crippled legs reduce combat mobility."

        rows.append(f"\033[1;30m|{dui.fit_ansi('  ' + lore, 98)}\033[1;30m|\033[0m")
        rows.append("\033[1;30m+----------------------------------------------------------------------------------------------------+\033[0m")
        rows.append("  \033[90m[CONTROLS]:\033[0m \033[1;37m[W/S]\033[0m Switch Hero  |  \033[1;37m[A/D]\033[0m Switch Mutilation State  |  \033[1;31m[Q/Esc]\033[0m Return to Menu")
        rows.append("\033[1;30m" + "=" * 100 + "\033[0m")

        dui.atomic_blit(rows)

        if not (os.name == 'nt' and sys.stdin.isatty()):
            # Non-interactive / headless test mode: render first frame and exit
            break

        ch = msvcrt.getch()
        if ch in (b'\x00', b'\xe0'):
            ch = msvcrt.getch()
            if ch == b'H':  # Up
                hero_idx = (hero_idx - 1) % len(hero_keys)
                variant_idx = 0
            elif ch == b'P':  # Down
                hero_idx = (hero_idx + 1) % len(hero_keys)
                variant_idx = 0
            elif ch == b'K':  # Left
                variant_idx = (variant_idx - 1) % len(var_keys)
            elif ch == b'M':  # Right
                variant_idx = (variant_idx + 1) % len(var_keys)
        elif ch in (b'w', b'W'):
            hero_idx = (hero_idx - 1) % len(hero_keys)
            variant_idx = 0
        elif ch in (b's', b'S'):
            hero_idx = (hero_idx + 1) % len(hero_keys)
            variant_idx = 0
        elif ch in (b'a', b'A'):
            variant_idx = (variant_idx - 1) % len(var_keys)
        elif ch in (b'd', b'D'):
            variant_idx = (variant_idx + 1) % len(var_keys)
        elif ch in (b'q', b'Q', b'\x1b'):
            break

    dui.clear_screen()
    return 0

if __name__ == "__main__":
    run_hero_mutilation_showcase()
