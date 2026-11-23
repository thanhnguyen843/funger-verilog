#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
================================================================================
FEAR & HUNGER: TRI-STATE POSTURAL MORPHOLOGY & TECHNICAL AMBER VIEWER
Hardware Inspection: NORMAL (2'b00 - White) vs INJURED (2'b01 - Amber) vs DEAD (2'b10 - Ash)
================================================================================
"""

import sys
import os
import time
import re

# Windows VT & UTF-8 setup
if os.name == 'nt':
    try:
        import ctypes
        k32 = ctypes.windll.kernel32
        hOut = k32.GetStdHandle(-11)
        mode = ctypes.c_ulong()
        if k32.GetConsoleMode(hOut, ctypes.byref(mode)):
            k32.SetConsoleMode(hOut, mode.value | 0x0004)
        k32.SetConsoleOutputCP(65001)
        k32.SetConsoleCP(65001)
    except Exception:
        pass
    import msvcrt

MONSTER_NAMES = [
    "Mage Ghost", "Classic Ghost", "Maw Slime", "Brachio Titan", "Antler Totem",
    "Kraken Octopus", "Beholder Eye", "Shadow Swordsman", "Giant Snail", "Grave Spider",
    "Dungeon Ant", "Battle Llama", "Shadow Hound", "Forest Stag", "Cave Gnome",
    "Mini Knight", "Little Drake", "Shadow Slug", "Dark Construct", "Abyssal Overlord",
    "Wyvern", "Gargoyle", "Chest Mimic", "Hydra Serpent", "Imp Demon",
    "Spectral Beast", "Ancient Treant", "Abyss Beholder", "Dungeon Basilisk", "Chimera Horror",
    "Cave Manticore", "Cathedral Gargoyle", "Troll Berserker", "Crypt Vampire", "Lich Necromancer",
    "Dark Dragon"
]

current_mid = 8   # Default: Shadow Swordsman
current_state = 0 # 0: NORMAL, 1: INJURED, 2: DEAD

def get_sprite_lines(mid, state):
    """
    Renders pure postural morphology:
      - State 0: Phosphor White (#FFFFFF), standing tall, weapon armed
      - State 1: Technical Amber (#FFAA28), body crouched 4 rows down, weapon arm disarmed
      - State 2: Deactivated Ash Gray (#6E7378), head removed, collapsed silhouette
    """
    if mid == 8: # Shadow Swordsman
        if state == 0: # Normal (Phosphor White)
            return [
                "      \033[1;37m▄▀▀▀▄▄▀▀▀▄\033[0m             ",
                "     \033[1;37m▀▀ ▄ ▀▀ ▄ ▀\033[0m             ",
                "     \033[1;37m▀▀▄▄▄▀▀▄▄▄▀\033[0m             ",
                "      \033[1;37m▄▀▀▀▄▄▀▀▀▄\033[0m  \033[1;37m▄▀\033[0m(SWORD)  ",
                "      \033[1;37m▀ ▀▀▀▀▀▀ ▀\033[0m  \033[1;37m▀▀▀\033[0m        ",
                "      \033[1;37m▀  ▀▄ ▀▄ ▀\033[0m             ",
                "      \033[1;37m▀▀  ▀  ▀ ▀\033[0m             ",
                "                             ",
                "                             ",
                "                             ",
                "                             ",
                "                             "
            ]
        elif state == 1: # Injured (Phosphor White body with Technical Amber fracture joints)
            return [
                "                             ",
                "                             ",
                "                             ",
                "                             ",
                "      \033[1;37m▄▀▀▀▄▄▀▀▀▄\033[0m             ",
                "     \033[1;37m▀▀ ▄ ▀▀ ▄ ▀\033[0m             ",
                "     \033[1;37m▀▀▄▄▄▀▀▄▄▄▀\033[0m             ",
                "      \033[1;37m▄▀▀▀▄▄▀▀\033[0m\033[1;33m▄▀\033[0m  (DISARMED) ",
                "   \033[1;37m▄▀▀▀▀▀▀▀▀▀▀\033[0m\033[1;33m▀▀▀▄\033[0m (CROUCHED)",
                "   \033[1;37m▀▀▀▀\033[0m   \033[1;33m▀▀\033[0m  \033[1;37m▀▀▀▀\033[0m           ",
                "                             ",
                "                             "
            ]
        else: # Dead (Ash Gray - Headless collapsed entity)
            return [
                "                             ",
                "                             ",
                "                             ",
                "                             ",
                "                             ",
                "                             ",
                "                             ",
                "      \033[90m▄▀▀▀▄▄▀▀▀▄\033[0m             ",
                "   \033[90m▄▀▀▀▀▀▀▀▀▀▀▀▀▀▄\033[0m           ",
                "   \033[90m▀▀▀▀   ▀▀  ▀▀▀▀\033[0m(COLLAPSED)",
                "   \033[90m░░░░░░░░░░░░░░░\033[0m           ",
                "                             "
            ]
    elif mid == 18: # Shadow Slug (17x12 Low-Profile Gastropod)
        if state == 0: # Normal
            return [
                "  \033[1;37m▀▀   ▀▀\033[0m                    ",
                "   \033[1;37m▄▀▀▀▄\033[0m                     ",
                "   \033[1;37m▀ ▀ ▀▄▀▀▀▀▄▄\033[0m              ",
                "    \033[1;37m▀▀▀▀▀▀▀▀▀▀▀▀▀▄▄\033[0m          ",
                "    \033[1;37m▀ ▀   ▀  ▀\033[0m               ",
                "   \033[1;37m▄▀ ▀▄ ▄▀ ▄▀\033[0m               ",
                "                             ",
                "    \033[90m[SLUG CREEPING POSTURE]\033[0m  ",
                "                             ",
                "                             ",
                "                             ",
                "                             "
            ]
        elif state == 1: # Injured (Severed Right Antenna with Amber Socket)
            return [
                "  \033[1;37m▀▀\033[0m                         ",
                "   \033[1;37m▄▀▀\033[0m \033[1;33m▄\033[0m  (ANTENNA SEVERED)  ",
                "   \033[1;37m▀ ▀ ▀▄▀▀▀▀▄▄\033[0m              ",
                "    \033[1;37m▀▀▀▀▀▀▀▀▀▀▀▀▀▄▄\033[0m          ",
                "    \033[1;37m▀ ▀   ▀  ▀\033[0m               ",
                "   \033[1;33m▄▀\033[0m \033[1;37m▀▄ ▄▀ ▄▀\033[0m (LEG FRACTURE)",
                "                             ",
                "  \033[1;33m[SHELL WOUNDED & SLOWED]\033[0m   ",
                "                             ",
                "                             ",
                "                             ",
                "                             "
            ]
        else: # Dead (Crushed Head, Inert Shell in Ash Gray)
            return [
                "                             ",
                "                             ",
                "   \033[90m▀ ▀ ▀▄▀▀▀▀▄▄\033[0m              ",
                "    \033[90m▀▀▀▀▀▀▀▀▀▀▀▀▀▄▄\033[0m          ",
                "    \033[90m▀ ▀   ▀  ▀\033[0m               ",
                "   \033[90m▄▀ ▀▄ ▄▀ ▄▀\033[0m (DEFLATED)    ",
                "                             ",
                "   \033[90m[INERT SHELL NEUTRALIZED]\033[0m ",
                "                             ",
                "                             ",
                "                             ",
                "                             "
            ]
    elif mid == 19: # Dark Construct (23x12 Mechanical Automaton)
        if state == 0: # Normal
            return [
                "  \033[1;37m▄▀▀▄ ▄▀▀▄\033[0m                  ",
                "  \033[1;37m▀▄▄▀ ▀▄▄▀\033[0m                  ",
                "    \033[1;37m▀    ▀\033[0m                   ",
                "    \033[1;37m▀▀   ▀▀  ▄▄▄▄▄\033[0m           ",
                "     \033[1;37m▄▀▄▄▀▀▀▀ ▀▀ ▀▀▀▀▄▄\033[0m      ",
                "     \033[1;37m▀▀▄▀▄▀▄▄▀▄▄▀▄▄▀▄▀▄▀▀\033[0m    ",
                "                             ",
                "    \033[90m[TWIN-CORE POWER CHASSIS]\033[0m",
                "                             ",
                "                             ",
                "                             ",
                "                             "
            ]
        elif state == 1: # Injured (Right Core Blasted Off, Amber Energy Leak)
            return [
                "  \033[1;37m▄▀▀▄\033[0m                       ",
                "  \033[1;37m▀▄▄▀\033[0m     (CORE CRACKED)    ",
                "    \033[1;37m▀\033[0m    \033[1;33m▄\033[0m  (AMBER LEAK)     ",
                "    \033[1;37m▀▀   ▀▀  ▄▄▄▄▄\033[0m           ",
                "     \033[1;37m▄▀▄▄▀▀▀▀ ▀▀\033[0m \033[1;33m▀▀▀▀▄▄\033[0m      ",
                "     \033[1;37m▀▀▄▀▄▀▄▄▀▄▄▀▄▄▀▄▀▄▀▀\033[0m    ",
                "                             ",
                "    \033[1;33m[CHASSIS OVERHEATING]\033[0m    ",
                "                             ",
                "                             ",
                "                             ",
                "                             "
            ]
        else: # Dead (Cores Extinguished, Deactivated Chassis in Ash Gray)
            return [
                "                             ",
                "                             ",
                "                             ",
                "    \033[90m▀▀   ▀▀  ▄▄▄▄▄\033[0m           ",
                "     \033[90m▄▀▄▄▀▀▀▀ ▀▀ ▀▀▀▀▄▄\033[0m      ",
                "     \033[90m▀▀▄▀▄▀▄▄▀▄▄▀▄▄▀▄▀▄▀▀\033[0m    ",
                "                             ",
                "    \033[90m[CONSTRUCT DEACTIVATED]\033[0m  ",
                "                             ",
                "                             ",
                "                             ",
                "                             "
            ]
    else:
        # Generic Postural Transformation
        if state == 0: # Normal
            return [
                "       \033[1;37m▄▀▀▀▀▀▀▀▄\033[0m             ",
                "      \033[1;37m▀▀ ▄  ▄ ▀▀\033[0m             ",
                "      \033[1;37m▀▀▀▀▀▀▀▀▀▀\033[0m             ",
                "       \033[1;37m▄▀▀▀▀▀▄\033[0m   \033[1;37m▄▀\033[0m(WEAPON)  ",
                "      \033[1;37m▀▀▀▀▀▀▀▀ ▄▀▀\033[0m           ",
                "      \033[1;37m▀▀▀▀▀▀▀▀▀▀▀▀\033[0m           ",
                "      \033[1;37m▀▀ ▀▀▀▀ ▀▀\033[0m             ",
                "      \033[1;37m▀▀  ▀▀  ▀▀\033[0m             ",
                "      \033[1;37m▀   ▀▀   ▀\033[0m             ",
                "                             ",
                "    \033[90m[UPRIGHT STANCE]\033[0m         ",
                "                             "
            ]
        elif state == 1: # Injured (White body, Amber fracture joints, Shifted down 4 rows)
            return [
                "                             ",
                "                             ",
                "                             ",
                "                             ",
                "       \033[1;37m▄▀▀▀▀▀▀▀▄\033[0m             ",
                "      \033[1;37m▀▀ ▄  ▄ ▀▀\033[0m             ",
                "      \033[1;37m▀▀▀▀▀▀▀▀▀▀\033[0m             ",
                "       \033[1;37m▄▀▀▀▀\033[0m\033[1;33m▀▄\033[0m  (DISARMED)   ",
                "      \033[1;37m▀▀▀▀▀▀▀▀\033[0m               ",
                "    \033[1;37m▄▀▀▀▀▀▀▀\033[0m\033[1;33m▀▀▀▄\033[0m (CROUCHED)  ",
                "   \033[1;37m▀▀▀▀▀▀\033[0m\033[1;33m▀▀\033[0m\033[1;37m▀▀▀▀▀▀\033[0m            ",
                "                             "
            ]
        else: # Dead (Ash Gray, Head removed, collapsed)
            return [
                "                             ",
                "                             ",
                "                             ",
                "                             ",
                "                             ",
                "                             ",
                "                             ",
                "       \033[90m▄▀▀▀▀▀▄\033[0m  (HEADLESS)   ",
                "      \033[90m▀▀▀▀▀▀▀▀\033[0m               ",
                "   \033[90m▄▀▀▀▀▀▀▀▀▀▀▀▄\033[0m(NEUTRALIZED)",
                "   \033[90m░░░░░░░░░░░░░░\033[0m            ",
                "                             "
            ]

def strip_ansi(s):
    return re.sub(r'\x1b\[[0-9;]*[a-zA-Z]', '', s)

def visible_len(s):
    return len(strip_ansi(s))

def fit_100_cols(s):
    vlen = visible_len(s)
    if vlen < 100:
        return s + " " * (100 - vlen)
    elif vlen > 100:
        return s
    return s

def render_interactive():
    name = MONSTER_NAMES[current_mid - 1]
    lines = get_sprite_lines(current_mid, current_state)

    state_labels = [
        "NORMAL (2'b00) - Phosphor White",
        "INJURED (2'b01) - White + Amber Joints",
        "DEAD (2'b10) - Deactivated Ash"
    ]
    state_colors = ["\033[1;37m", "\033[1;33m", "\033[90m"]
    state_reg = f"2'b0{current_state}" if current_state < 2 else "2'b10"

    rows = []
    rows.append("\033[1;30m+" + "=" * 98 + "+\033[0m")
    rows.append("\033[1;30m|  \033[1;37mFEAR & HUNGER: TRI-STATE POSTURAL MORPHOLOGY & TECHNICAL AMBER INSPECTOR (RTL ARCHITECTURE)     \033[1;30m|\033[0m")
    rows.append("\033[1;30m+" + "=" * 98 + "+\033[0m")
    rows.append("")

    st_badge = f"{state_colors[current_state]}[{state_labels[current_state]}]\033[0m"
    card_rows = [
        f"\033[1;30m+--------------------------------------------------+\033[0m",
        f"|  \033[1;33mFOE #{current_mid:02d}: {name:<26}\033[0m        |",
        f"|  Status   : {st_badge:<38} |",
        f"|  Hardware : \033[1;36mstate_reg = {state_reg}\033[0m (Module: monster_state) |",
        f"|  Color LUT: \033[1;37m{state_colors[current_state]}Phosphor Spectrum Mode\033[0m              |",
        f"|                                                  |",
        f"|  \033[1;37mPOSTURAL MORPHOLOGY & DISMEMBERMENT:\033[0m            |",
    ]

    if current_mid == 18:
        if current_state == 0:
            card_rows += [
                "|  * Antennae  : \033[1;37mDUAL INTACT (Sensory Radar)\033[0m       |",
                "|  * Shell Body: \033[1;37mHARDENED (Low Crawling Stance)\033[0m    |",
                "|  * Mandibles : \033[1;37mARMED (Venomous Creeping Bite)\033[0m    |",
                "|  * Aesthetics: \033[1;37mPure Phosphor White (#FFFFFF)\033[0m     |",
                "|                                                  |",
                "|  \033[90m(Press [2] to sever sensory antennae)\033[0m           |",
            ]
        elif current_state == 1:
            card_rows += [
                "|  * Antennae  : \033[1;33mRIGHT SEVERED (Sensory Blinded)\033[0m   |",
                "|  * Socket    : \033[1;33mCAUTERIZED (Amber Fracture Joint)\033[0m |",
                "|  * Shell/Legs: \033[1;33mFRACTURED (Disoriented Crawl)\033[0m     |",
                "|  * Aesthetics: \033[1;37mWhite Body\033[0m + \033[1;33mAmber Socket & Joints\033[0m|",
                "|                                                  |",
                "|  \033[1;33m[MECHANIC]: Blinded; accuracy & speed halved!\033[0m   |",
            ]
        else:
            card_rows += [
                "|  * Head/Sensors: \033[90mCRUSHED & NEUTRALIZED\033[0m           |",
                "|  * Carcass     : \033[90mCOLLAPSED (Inert Shell Residue)\033[0m |",
                "|  * Integrity   : \033[90m0 / MAX HP (NEUTRALIZED)\033[0m        |",
                "|  * Aesthetics  : \033[90mDeactivated Ash Gray (#6E7378)\033[0m |",
                "|                                                  |",
                "|  \033[1;32m[VICTORY]: Subterranean slug neutralized!\033[0m        |",
            ]
    elif current_mid == 19:
        if current_state == 0:
            card_rows += [
                "|  * Power Core: \033[1;37mTWIN CHARGED (Full Output)\033[0m        |",
                "|  * Chassis   : \033[1;37mARMORED (Heavy Tracked Automaton)\033[0m |",
                "|  * Cannon Arm: \033[1;37mCALIBRATED (Dark Pulse Laser)\033[0m     |",
                "|  * Aesthetics: \033[1;37mPure Phosphor White (#FFFFFF)\033[0m     |",
                "|                                                  |",
                "|  \033[90m(Press [2] to blast right power core)\033[0m           |",
            ]
        elif current_state == 1:
            card_rows += [
                "|  * Power Core: \033[1;33mRIGHT CORE BLASTED OFF (50% PWR)\033[0m  |",
                "|  * Core Root : \033[1;33mAMBER DISCHARGE (Energy Sparking)\033[0m |",
                "|  * Chassis   : \033[1;33mREAR CRACK (Leaking Arc Fissures)\033[0m |",
                "|  * Aesthetics: \033[1;37mWhite Body\033[0m + \033[1;33mAmber Discharge Joint\033[0m|",
                "|                                                  |",
                "|  \033[1;33m[MECHANIC]: Overheating! Laser cannon offline\033[0m    |",
            ]
        else:
            card_rows += [
                "|  * Power Cores : \033[90mEXTINGUISHED (0 V Energy Output)\033[0m|",
                "|  * Automaton   : \033[90mDEACTIVATED (Inert Chassis)\033[0m     |",
                "|  * Integrity   : \033[90m0 / MAX HP (NEUTRALIZED)\033[0m        |",
                "|  * Aesthetics  : \033[90mDeactivated Ash Gray (#6E7378)\033[0m |",
                "|                                                  |",
                "|  \033[1;32m[VICTORY]: Dark Construct powered down!\033[0m         |",
            ]
    elif current_state == 0:
        card_rows += [
            "|  * Weapon Arm: \033[1;37mWIELDING (Full Attack Power)\033[0m      |",
            "|  * Lower Body: \033[1;37mUPRIGHT (Standing Stance)\033[0m         |",
            "|  * Head/Neck : \033[1;37mINTACT (100% Armor Guard)\033[0m         |",
            "|  * Aesthetics: \033[1;37mPure Phosphor White (#FFFFFF)\033[0m     |",
            "|                                                  |",
            "|  \033[90m(Press [2] to inflict Postural Limb Damage)\033[0m     |",
        ]
    elif current_state == 1:
        card_rows += [
            "|  * Weapon Arm: \033[1;33mSEVERED (Disarmed - Column Off)\033[0m   |",
            "|  * Lower Body: \033[1;33mBROKEN (Crouched - Row Shift -4)\033[0m  |",
            "|  * Mobility  : \033[1;33mCRAWLING (100% Flee Success)\033[0m      |",
            "|  * Aesthetics: \033[1;37mWhite Body\033[0m + \033[1;33mAmber Fracture Joints\033[0m  |",
            "|                                                  |",
            "|  \033[1;33m[MECHANIC]: Foe cannot chase; weapon lost!\033[0m      |",
        ]
    else:
        card_rows += [
            "|  * Head/Neck : \033[90mDECAPITATED (Rows 0-5 Masked Off)\033[0m |",
            "|  * Posture   : \033[90mCOLLAPSED (Floor Silhouette)\033[0m      |",
            "|  * Integrity : \033[90m0 / MAX HP (NEUTRALIZED)\033[0m          |",
            "|  * Aesthetics: \033[90mDeactivated Ash Gray (#6E7378)\033[0m   |",
            "|                                                  |",
            "|  \033[1;32m[VICTORY]: Target neutralized cleanly!\033[0m          |",
        ]
    card_rows.append(f"\033[1;30m+--------------------------------------------------+\033[0m")

    # Combine Side-by-Side (Card 52 cols + Gap 4 + Sprite 42 cols)
    for idx in range(14):
        c_line = card_rows[idx] if idx < len(card_rows) else " " * 52
        s_line = lines[idx] if idx < len(lines) else " " * 29
        row_str = f"  {c_line}    {s_line}"
        rows.append(fit_100_cols(row_str))

    rows.append("")
    rows.append("\033[1;30m" + "=" * 100 + "\033[0m")
    rows.append(fit_100_cols("  \033[90m[STATE]:\033[0m \033[1;37m[1]\033[0m Normal (White)  |  \033[1;33m[2]\033[0m Injured (Amber)  |  \033[90m[3]\033[0m Dead (Ash)  |  \033[1;37m[Space]\033[0m Cycle"))
    rows.append(fit_100_cols("  \033[90m[SELECT FOE]:\033[0m \033[1;37m[A / Left]\033[0m Prev Foe  |  \033[1;37m[D / Right]\033[0m Next Foe   |  \033[1;31m[Q]\033[0m Quit Viewer"))
    rows.append("\033[1;30m" + "=" * 100 + "\033[0m")

    # Atomic in-place write: Cursor Home + Overwrite Rows + Clear Tail
    formatted_rows = [fit_100_cols(r) for r in rows]
    frame_text = "\033[H" + "\n".join(formatted_rows) + "\n\033[J"
    sys.stdout.write(frame_text)
    sys.stdout.flush()

def main():
    global current_mid, current_state

    # Initial screen setup & cursor suppression
    sys.stdout.write("\033[2J\033[H\033[?25l")
    sys.stdout.flush()

    try:
        while True:
            render_interactive()
            if os.name == 'nt' and sys.stdin.isatty():
                ch = msvcrt.getch()
                if ch in (b'\x00', b'\xe0'):
                    ext = msvcrt.getch()
                    if ext in (b'K', b'H'): # Left or Up Arrow
                        current_mid = 36 if current_mid == 1 else current_mid - 1
                    elif ext in (b'M', b'P'): # Right or Down Arrow
                        current_mid = 1 if current_mid == 36 else current_mid + 1
                    while msvcrt.kbhit():
                        msvcrt.getch()
                elif ch in (b'a', b'A', b'w', b'W'):
                    current_mid = 36 if current_mid == 1 else current_mid - 1
                    while msvcrt.kbhit():
                        msvcrt.getch()
                elif ch in (b'd', b'D', b's', b'S'):
                    current_mid = 1 if current_mid == 36 else current_mid + 1
                    while msvcrt.kbhit():
                        msvcrt.getch()
                elif ch == b'1':
                    current_state = 0
                elif ch == b'2':
                    current_state = 1
                elif ch == b'3':
                    current_state = 2
                elif ch in (b' ', b'\r', b'\n'):
                    current_state = (current_state + 1) % 3
                elif ch in (b'q', b'Q', b'\x1b'):
                    break
            else:
                raw = sys.stdin.readline()
                if not raw:
                    break
                line = raw.strip().lower()
                if line == 'q':
                    break
                elif line in ('1', '2', '3'):
                    current_state = int(line) - 1
                elif line in ('a', 'w', 'prev'):
                    current_mid = 36 if current_mid == 1 else current_mid - 1
                elif line in ('d', 's', 'next'):
                    current_mid = 1 if current_mid == 36 else current_mid + 1
                elif line in (' ', 'cycle'):
                    current_state = (current_state + 1) % 3
    finally:
        # Restore cursor on exit
        sys.stdout.write("\033[?25h\n")
        sys.stdout.flush()
        print("[OK] Tri-State Monster Inspector session terminated cleanly.")

if __name__ == "__main__":
    main()
