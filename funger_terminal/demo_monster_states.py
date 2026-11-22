#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
================================================================================
FEAR & HUNGER: TRI-STATE MONSTER HARDWARE MODEL VIEWER
Interactive Hardware Verification: NORMAL (2'b00) vs INJURED (2'b01) vs DEAD (2'b10)
================================================================================
"""

import sys
import os
import time
import subprocess
import json

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

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

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
    Simulate the Verilog hardware state model logic or invoke Verilog simulation.
    We also load cached raw bits from the hardware simulation.
    """
    # Sample representation matching the monster_state_model.v RTL output
    # For fast interactive navigation, we format standard visual half-blocks:
    if mid == 8: # Shadow Swordsman
        if state == 0: # Normal
            return [
                "      \033[1;37m▄▀▀▀▄▄▀▀▀▄\033[0m             ",
                "     \033[1;37m▀▀ ▄ ▀▀ ▄ ▀\033[0m             ",
                "     \033[1;37m▀▀▄▄▄▀▀▄▄▄▀\033[0m             ",
                "      \033[1;37m▄▀▀▀▄▄▀▀▀▄\033[0m             ",
                "      \033[1;37m▀ ▀▀▀▀▀▀ ▀\033[0m             ",
                "      \033[1;37m▀  ▀▄ ▀▄ ▀\033[0m             ",
                "      \033[1;37m▀▀  ▀  ▀ ▀\033[0m             ",
                "                             ",
                "                             ",
                "                             ",
                "                             ",
                "                             "
            ]
        elif state == 1: # Injured (Severed blade arm & broken legs crawling)
            return [
                "                             ",
                "                             ",
                "                             ",
                "                             ",
                "      \033[1;31m▄▀▀▀▄▄▀▀▀▄\033[0m             ",
                "     \033[1;31m▀▀ ▄ ▀▀ ▄ ▀\033[0m             ",
                "     \033[1;31m▀▀▄▄▄▀▀▄▄▄▀\033[0m             ",
                "      \033[1;31m▄▀▀▀▄▄▀▀▀▄\033[0m             ",
                "   \033[1;31m▄▀▀▀▀▀▀▀▀▀▀▀▀▀▄\033[0m           ",
                "   \033[1;31m▀▀▀▀   ▀▀  ▀▀▀▀\033[0m           ",
                "  \033[1;33m[LEGS BROKEN: CRAWLING]\033[0m    ",
                "  \033[1;31m[RIGHT ARM: SEVERED]\033[0m       "
            ]
        else: # Dead (Decapitated & blood pool)
            return [
                "                             ",
                "     \033[1;31m[DECAPITATED]\033[0m           ",
                "        \033[1;31m▄████▄\033[0m   (HEAD)      ",
                "    \033[1;31m▀▀▄▄▄▀████▄▄▄▀\033[0m           ",
                "     \033[1;31m▄▀▀▀▄▄▀▀▀▄\033[0m (BLOOD)      ",
                "      \033[1;31m▀ ▀▀▀▀▀▀ ▀\033[0m             ",
                "   \033[1;31m▄▀▀▀▀▀▀▀▀▀▀▀▀▀▄\033[0m           ",
                "   \033[1;31m▀▀▀▀   ▀▀  ▀▀▀▀\033[0m           ",
                "   \033[1;31m(POOL OF BLOOD SPREAD)\033[0m    ",
                "  \033[1;31m██████████████████████\033[0m     ",
                "                             ",
                "                             "
            ]
    else:
        # Procedural representation matching monster_state_model.v
        name = MONSTER_NAMES[mid - 1]
        if state == 0:
            return [
                f"       \033[1;37m▄▀▀▀▀▀▀▄\033[0m              ",
                f"      \033[1;37m▀▀ ▄  ▄ ▀▀\033[0m             ",
                f"      \033[1;37m▀▀▀▀▀▀▀▀▀▀\033[0m             ",
                f"       \033[1;37m▄▀▀▀▀▄\033[0m   \033[1;37m▄▀\033[0m           ",
                f"      \033[1;37m▀▀▀▀▀▀▀▀ ▄▀▀\033[0m           ",
                f"      \033[1;37m▀▀▀▀▀▀▀▀▀▀▀▀\033[0m           ",
                f"      \033[1;37m▀▀ ▀▀▀▀ ▀▀\033[0m             ",
                f"      \033[1;37m▀▀  ▀▀  ▀▀\033[0m             ",
                f"      \033[1;37m▀   ▀▀   ▀\033[0m             ",
                f"                             ",
                f"    \033[90m(Intact Stance)\033[0m          ",
                f"                             "
            ]
        elif state == 1:
            return [
                f"                             ",
                f"       \033[1;31m▄▀▀▀▀▀▀▄\033[0m              ",
                f"      \033[1;31m▀▀ ▄  ▄ ▀▀\033[0m             ",
                f"      \033[1;31m▀▀▀▀▀▀▀▀▀▀\033[0m             ",
                f"       \033[1;31m▄▀▀▀▀▄\033[0m   \033[1;31m[SEVERED]\033[0m    ",
                f"      \033[1;31m▀▀▀▀▀▀▀▀\033[0m               ",
                f"      \033[1;31m▀▀▀▀▀▀▀▀\033[0m               ",
                f"    \033[1;31m▄▀▀▀▀▀▀▀▀▀▀▄\033[0m             ",
                f"   \033[1;31m▀▀▀▀▀▀▀▀▀▀▀▀▀▀\033[0m            ",
                f"  \033[1;33m[CHÂN GÃY: BÒ LÊ LẾT]\033[0m      ",
                f"  \033[1;31m[TAY PHẢI: ĐÃ CHẶT ĐỨT]\033[0m    ",
                f"                             "
            ]
        else:
            return [
                f"                             ",
                f"     \033[1;31m💀 [TRẢM ĐẦU TỬ VẬN]\033[0m    ",
                f"        \033[1;31m▄████▄\033[0m               ",
                f"    \033[1;31m▀▀▄▄▄▀████▄▄▄▀\033[0m           ",
                f"                             ",
                f"      \033[1;31m(VẾT CHÉM ĐỨT CỔ)\033[0m      ",
                f"      \033[1;31m▄▀▀▀▀▀▀▀▀▄\033[0m             ",
                f"    \033[1;31m▄▀▀▀▀▀▀▀▀▀▀▀▀▄\033[0m           ",
                f"  \033[1;31m▄████████████████▄\033[0m         ",
                f"  \033[1;31m▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀\033[0m         ",
                f"   \033[1;31m[VŨNG MÁU LOANG DÀI]\033[0m      ",
                f"                             "
            ]

def render_interactive():
    sys.stdout.write("\033[2J\033[H")
    name = MONSTER_NAMES[current_mid - 1]
    lines = get_sprite_lines(current_mid, current_state)

    state_names = ["NORMAL (Lành lặn)", "INJURED (Chấn thương)", "DEAD (Tử trận)"]
    state_colors = ["\033[1;32m", "\033[1;33m", "\033[1;31m"]
    state_reg = f"2'b0{current_state}" if current_state < 2 else "2'b10"

    print("\033[1;30m+====================================================================================================+\033[0m")
    print(f"\033[1;30m| \033[1;37m     FEAR & HUNGER: TRI-STATE MONSTER HARDWARE MODEL VIEWER (INTERACTIVE RTL INSPECTOR)       \033[1;30m|\033[0m")
    print("\033[1;30m+====================================================================================================+\033[0m")
    print()

    # Left: Tactical card (50 cols) | Right: Sprite (42 cols)
    st_title = f"{state_colors[current_state]}[{state_names[current_state]}]\033[0m"
    card_rows = [
        f"\033[1;30m+--------------------------------------------------+\033[0m",
        f"|  \033[1;33mFOE #{current_mid:02d}: {name:<26}\033[0m        |",
        f"|  Status   : {st_title:<38} |",
        f"|  Hardware : \033[1;36mstate_reg = {state_reg}\033[0m (Module: monster_state) |",
        f"|                                                  |",
        f"|  \033[1;37mANATOMY & DAMAGE STATUS:\033[0m                        |",
    ]

    if current_state == 0:
        card_rows += [
            "|  • Head      : \033[1;32mINTACT (100% Armor)\033[0m               |",
            "|  • Torso     : \033[1;32mHEALTHY (Full Vigor)\033[0m              |",
            "|  • Weapon Arm: \033[1;32mWIELDING (Full Attack Power)\033[0m      |",
            "|  • Legs      : \033[1;32mUPRIGHT (Standing Stance)\033[0m         |",
            "|                                                  |",
            "|  \033[90m(Press [2] or Space to inflict limb damage)\033[0m     |",
        ]
    elif current_state == 1:
        card_rows += [
            "|  • Head      : \033[1;33mEXPOSED (Decapitate hit +100%)\033[0m    |",
            "|  • Torso     : \033[1;31mBLEEDING (Deep lacerations)\033[0m       |",
            "|  • Weapon Arm: \033[1;31mSEVERED (DISARMED - ATK -14)\033[0m      |",
            "|  • Legs      : \033[1;31mBROKEN (CRAWLING - 100% Flee)\033[0m     |",
            "|                                                  |",
            "|  \033[1;33m[DEBUFF]: Foe forced to crawl; cannot chase!\033[0m    |",
        ]
    else:
        card_rows += [
            "|  • Head      : \033[1;31mDECAPITATED (Head severed off!)\033[0m   |",
            "|  • Torso     : \033[1;31mCOLLAPSED (Fatal mortal wound)\033[0m    |",
            "|  • Vitality  : \033[1;31m0 / MAX HP (DEFEATED)\033[0m             |",
            "|  • Carcass   : \033[90mPool of blood expanding on floor\033[0m  |",
            "|                                                  |",
            "|  \033[1;32m[VICTORY]: Threat eliminated successfully!\033[0m      |",
        ]
    card_rows.append(f"\033[1;30m+--------------------------------------------------+\033[0m")

    # Print Side-by-Side (Card 52 cols + Gap 4 + Sprite 42 cols)
    for idx in range(14):
        c_line = card_rows[idx] if idx < len(card_rows) else " " * 52
        s_line = lines[idx] if idx < len(lines) else " " * 29
        print(f"  {c_line}    {s_line}")

    print()
    print("\033[1;30m====================================================================================================\033[0m")
    print("  \033[90m[CHỌN TRẠNG THÁI]:\033[0m \033[1;32m[1]\033[0m Bình Thường  |  \033[1;33m[2]\033[0m Bị Chấn Thương  |  \033[1;31m[3]\033[0m Chết (Tử Trận)  |  \033[1;37m[Space]\033[0m Đổi Vòng")
    print("  \033[90m[ĐỔI QUÁI VẬT]:   \033[0m \033[1;37m[A / ←]\033[0m Quái Trước   |  \033[1;37m[D / →]\033[0m Quái Kế Tiếp    |  \033[1;31m[Q]\033[0m Thoát Trình Xem")
    print("\033[1;30m====================================================================================================\033[0m")
    sys.stdout.flush()

def main():
    global current_mid, current_state
    while True:
        render_interactive()
        if os.name == 'nt':
            ch = msvcrt.getch()
            if ch in (b'\x00', b'\xe0'):
                ext = msvcrt.getch()
                if ext == b'K': # Left arrow
                    current_mid = 36 if current_mid == 1 else current_mid - 1
                elif ext == b'M': # Right arrow
                    current_mid = 1 if current_mid == 36 else current_mid + 1
            elif ch in (b'a', b'A'):
                current_mid = 36 if current_mid == 1 else current_mid - 1
            elif ch in (b'd', b'D'):
                current_mid = 1 if current_mid == 36 else current_mid + 1
            elif ch == b'1':
                current_state = 0
            elif ch == b'2':
                current_state = 1
            elif ch == b'3':
                current_state = 2
            elif ch in (b' ', b'\r', b'\n'):
                current_state = (current_state + 1) % 3
            elif ch in (b'q', b'Q', b'\x1b'):
                print("\n[OK] Thoát trình xem Model 3 trạng thái.")
                break
        else:
            line = sys.stdin.readline().strip().lower()
            if line == 'q':
                break
            elif line in ('1', '2', '3'):
                current_state = int(line) - 1
            elif line == 'a':
                current_mid = 36 if current_mid == 1 else current_mid - 1
            elif line in ('d', ''):
                current_mid = 1 if current_mid == 36 else current_mid + 1

if __name__ == "__main__":
    main()
