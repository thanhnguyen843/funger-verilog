#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
================================================================================
FEAR & HUNGER: TERMINAL LABYRINTH - SOLO EXPLORER MASTER GAME ENGINE
Unified Hardware-Accurate Adventure:
  1. Title Screen & Expedition Difficulty Selection
  2. Vertical Solo Explorer Selector with Real-time 24-bit ANSI Sprite Preview
  3. Persistent Fog of War Labyrinth Exploration (36x20) with Dynamic Torchlight
  4. Universal Map Obstacle Resolution (Barricades, Seals, Crawlspaces, Chests)
  5. Seamless Transition into Pokémon-style Limb-Targeting Combat Arena
  6. Real-time Inventory Pouch & Quick Healing
  7. Grand Runic Gate Escape Victory & Gothic Game Over Demise
  8. Double-Buffered Atomic Blit Engine (Zero Screen Flicker & Zero Drift)
================================================================================
"""

import sys
import os
import time
import copy
import random
import re

# Enable Windows Virtual Terminal Processing & UTF-8
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

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import demo_interactive_ui as combat_engine
from monsters_catalog import ALL_MONSTERS_CATALOG, REGULAR_MONSTER_IDS, BOSS_MONSTER_IDS, MIMIC_ID

# =============================================================================
# CONSTANTS & MAP DEFINITIONS (36 x 20)
# =============================================================================
MAP_WIDTH = 36
MAP_HEIGHT = 20
TOTAL_TILES = MAP_WIDTH * MAP_HEIGHT

TILE_WALL = 0
TILE_PATH = 1
TILE_CHEST = 2
TILE_MONSTER = 3
TILE_GATE = 4
TILE_BARRICADE = 5
TILE_SEAL = 6
TILE_CRAWLSPACE = 7

# Map Layout Generator (Bit-exact match with hardware map_rom.v)
def get_base_tile(x, y):
    if (x == MAP_WIDTH - 1 and y == 6) or (x == MAP_WIDTH - 1 and y == 14):
        return TILE_GATE
    if x <= 0 or x >= MAP_WIDTH - 1 or y <= 0 or y >= MAP_HEIGHT - 1:
        return TILE_WALL
    if (x == MAP_WIDTH - 2 and y == 6) or (x == MAP_WIDTH - 2 and y == 14):
        return TILE_MONSTER
    if x == MAP_WIDTH - 2 and (y in (5, 7, 13, 15)):
        return TILE_WALL
    if 1 <= x <= 4 and 1 <= y <= 3:
        return TILE_PATH

    # Vault Chests
    if (x, y) in [(8, 2), (22, 3), (6, 11), (18, 11), (28, 10), (12, 17), (26, 17)]:
        return TILE_CHEST

    # Roaming Monsters
    if (x, y) in [(14, 2), (10, 6), (20, 7), (28, 4), (14, 11), (24, 11), (8, 15), (20, 15)]:
        return TILE_MONSTER

    # Specialty Obstacles
    if (x, y) in [(6, 7), (20, 11)]:
        return TILE_BARRICADE
    if (x, y) in [(16, 3), (24, 15)]:
        return TILE_SEAL
    if (x, y) in [(10, 2), (28, 16)]:
        return TILE_CRAWLSPACE

    # Internal Labyrinth Walls
    if ((x == 6 and 4 <= y <= 9) or
        (x == 12 and 3 <= y <= 8) or
        (x == 16 and 1 <= y <= 5) or
        (x == 16 and 8 <= y <= 13) or
        (x == 22 and 5 <= y <= 9) or
        (x == 26 and 2 <= y <= 7) or
        (x == 30 and 1 <= y <= 4) or
        (x == 30 and 8 <= y <= 12) or
        (y == 4 and 7 <= x <= 10) or
        (y == 9 and 1 <= x <= 4) or
        (y == 13 and 7 <= x <= 14) or
        (y == 13 and 18 <= x <= 22) or
        (y == 15 and 10 <= x <= 16) or
        (x == 4 and 14 <= y <= 17) or
        (x == 10 and 16 <= y <= 18) or
        (x == 22 and 14 <= y <= 17) or
        (x == 30 and 16 <= y <= 18)):
        return TILE_WALL
    return TILE_PATH

# Specific Monster Encounters across Map Coordinates
MONSTER_ENCOUNTERS = {
    (14, 2):  {"id": 8,  "name": "SHADOW SWORDSMAN", "archetype": "ARMORED",     "hp": 95,  "atk": 24, "def": 99, "drops_key": False},
    (10, 6):  {"id": 1,  "name": "MAGE GHOST",       "archetype": "SPECTRAL",    "hp": 80,  "atk": 22, "def": 12, "drops_key": False},
    (20, 7):  {"id": 3,  "name": "MAW SLIME",        "archetype": "NORMAL",      "hp": 85,  "atk": 20, "def": 14, "drops_key": False},
    (28, 4):  {"id": 7,  "name": "BEHOLDER EYE",     "archetype": "TERROR",      "hp": 90,  "atk": 25, "def": 18, "drops_key": False},
    (14, 11): {"id": 9,  "name": "GIANT SNAIL",      "archetype": "ARMORED",     "hp": 110, "atk": 18, "def": 99, "drops_key": False},
    (24, 11): {"id": 10, "name": "GRAVE SPIDER",     "archetype": "AMBUSHER",    "hp": 100, "atk": 28, "def": 16, "drops_key": False},
    (8, 15):  {"id": 13, "name": "SHADOW HOUND",     "archetype": "NORMAL",      "hp": 90,  "atk": 24, "def": 16, "drops_key": False},
    (20, 15): {"id": 19, "name": "DARK CONSTRUCT",   "archetype": "ARMORED",     "hp": 120, "atk": 30, "def": 99, "drops_key": False},
    (34, 6):  {"id": 20, "name": "ABYSSAL OVERLORD", "archetype": "ARMORED",     "hp": 150, "atk": 36, "def": 99, "drops_key": True},
    (34, 14): {"id": 36, "name": "DARK DRAGON",       "archetype": "ARMORED",     "hp": 180, "atk": 40, "def": 99, "drops_key": True},
}

# ANSI Helpers for strict 100-column alignment
ANSI_REGEX = re.compile(r'\x1b\[[0-9;]*[a-zA-Z]')
def strip_ansi(s):
    return ANSI_REGEX.sub('', s)

def visible_len(s):
    return len(strip_ansi(s))

def fit_ansi(s, max_len):
    return combat_engine.fit_ansi(s, max_len)

def fit_100_cols(s):
    vlen = visible_len(s)
    if vlen < 100:
        return s + " " * (100 - vlen)
    elif vlen > 100:
        return fit_ansi(s, 100)
    return s

def make_centered_box_row(text, width=100, border_color=""):
    raw_len = visible_len(text)
    total_space = (width - 2) - raw_len
    if total_space < 0:
        text = fit_ansi(text, width - 4)
        raw_len = visible_len(text)
        total_space = (width - 2) - raw_len
    left_space = total_space // 2
    right_space = total_space - left_space
    return f"{border_color}|" + (" " * left_space) + text + (" " * right_space) + f"|\033[0m"

def make_left_box_row(text, width=100, border_color="", pad_left=2):
    raw_len = visible_len(text)
    max_len = width - 2 - pad_left
    if raw_len > max_len:
        text = fit_ansi(text, max_len)
        raw_len = visible_len(text)
    right_space = width - 2 - pad_left - raw_len
    return f"{border_color}|" + (" " * pad_left) + text + (" " * right_space) + f"|\033[0m"

def make_border_line(char="=", width=100, border_color=""):
    return f"{border_color}+" + (char * (width - 2)) + f"+\033[0m"

def clear_screen():
    if os.name == 'nt':
        os.system('cls')
    sys.stdout.write("\033[2J\033[3J\033[H\033[?25l")
    sys.stdout.flush()

def atomic_blit(rows):
    """Blits entire screen atomically via cursor home to eliminate flicker 100%."""
    formatted_rows = [fit_100_cols(r) for r in rows]
    frame_str = "\033[H" + "\n".join(formatted_rows) + "\033[J"
    sys.stdout.write(frame_str)
    sys.stdout.flush()

# =============================================================================
# TITLE SCREEN & DIFFICULTY SELECTION
# =============================================================================
def render_title_screen(cursor_idx=0):
    rows = []
    rows.append(make_border_line("=", border_color="\033[1;31m"))
    rows.append(make_left_box_row("", border_color="\033[1;31m", pad_left=0))
    rows.append("\033[1;31m|          ________  ___  ___      ________       ________      _______       ________             |\033[0m")
    rows.append("\033[1;31m|         |\\  _____\\|\\  \\|\\  \\    |\\   ___  \\    |\\   ____\\    |\\  ___ \\     |\\   __  \\            |\033[0m")
    rows.append("\033[1;31m|         \\ \\  \\__/ \\ \\  \\\\\\  \\   \\ \\  \\\\ \\  \\   \\ \\  \\___|    \\ \\   __/|    \\ \\  \\|\\  \\           |\033[0m")
    rows.append("\033[1;31m|          \\ \\   __\\ \\ \\  \\\\\\  \\   \\ \\  \\\\ \\  \\   \\ \\  \\  ___   \\ \\  \\_|/__   \\ \\   _  _\\          |\033[0m")
    rows.append("\033[1;31m|           \\ \\  \\_|  \\ \\  \\\\\\  \\   \\ \\  \\\\ \\  \\   \\ \\  \\|\\  \\   \\ \\  \\_|\\ \\   \\ \\  \\\\  \\|         |\033[0m")
    rows.append("\033[1;31m|            \\ \\__\\    \\ \\_______\\   \\ \\__\\\\ \\__\\   \\ \\_______\\   \\ \\_______\\   \\ \\__\\\\ _\\         |\033[0m")
    rows.append("\033[1;31m|             \\|__|     \\|_______|    \\|__| \\|__|    \\|_______|    \\|_______|    \\|__|\\|__|        |\033[0m")
    rows.append(make_centered_box_row("\033[1;33m[   T  E  R  M  I  N  A  L     E  D  I  T  I  O  N   ]\033[0m", border_color="\033[1;31m"))
    rows.append(make_left_box_row("", border_color="\033[1;31m", pad_left=0))
    rows.append(make_border_line("=", border_color="\033[1;31m"))
    rows.append(make_left_box_row("\033[1;33m[OBJECTIVE]: Collect 3 Dungeon Keys to open the Cyan Exit Gate 'G' on the eastern perimeter!\033[0m", border_color="\033[1;31m"))
    rows.append(make_left_box_row("\033[1;36m[CHESTS]   : Open chests 'C' for survival herbs or disarm lethal needle traps!\033[0m", border_color="\033[1;31m"))
    rows.append(make_left_box_row("\033[1;35m[COMBAT]   : Confront roaming beasts 'M' in turn-based Pokémon-style limb combat!\033[0m", border_color="\033[1;31m"))
    rows.append(make_border_line("=", border_color="\033[1;31m"))
    rows.append("")

    p1 = "▶" if cursor_idx == 0 else " "
    c1 = "\033[1;32m" if cursor_idx == 0 else "\033[90m"
    p2 = "▶" if cursor_idx == 1 else " "
    c2 = "\033[1;31m" if cursor_idx == 1 else "\033[90m"

    rows.append(f"   {c1}{p1} [1] START EXPEDITION (EMBARK SOLO)\033[0m")
    rows.append(f"   {c2}{p2} [2] ABANDON HOPE (QUIT)\033[0m")
    rows.append("")
    rows.append("\033[1;30m" + "=" * 100 + "\033[0m")
    rows.append("  [CONTROLS]: [W/S] or [Up/Down] Navigate  |  [Enter] Confirm Selection  |  [Q] Quit")
    rows.append("\033[1;30m" + "=" * 100 + "\033[0m")
    atomic_blit(rows)

def run_title_screen():
    clear_screen()
    cursor_idx = 0
    while True:
        render_title_screen(cursor_idx)
        if os.name == 'nt' and sys.stdin.isatty():
            ch = msvcrt.getch()
            while msvcrt.kbhit():
                msvcrt.getch()
            if ch in (b'\x00', b'\xe0'):
                ext = msvcrt.getch()
                if ext in (b'H', b'P'):
                    cursor_idx = 1 - cursor_idx
            elif ch in (b'w', b'W', b's', b'S'):
                cursor_idx = 1 - cursor_idx
            elif ch == b'1':
                cursor_idx = 0
            elif ch == b'2':
                cursor_idx = 1
            elif ch in (b'\r', b'\n', b' '):
                clear_screen()
                return (cursor_idx == 0)
            elif ch in (b'0', b'q', b'Q', b'\x1b', b'\x03'):
                clear_screen()
                return False
        else:
            raw = sys.stdin.readline()
            if not raw:
                clear_screen()
                return False
            line = raw.strip().lower()
            if line in ('w', 's', 'up', 'down'):
                cursor_idx = 1 - cursor_idx
            elif line == '1':
                cursor_idx = 0
            elif line == '2':
                cursor_idx = 1
            elif line in ('', 'enter', 'start', 'c'):
                clear_screen()
                return (cursor_idx == 0)
            elif line in ('0', 'q', 'quit'):
                clear_screen()
                return False

def render_difficulty_screen(cursor_idx):
    rows = []
    rows.append(make_border_line("=", border_color="\033[1;35m"))
    rows.append(make_centered_box_row("SELECT EXPEDITION DIFFICULTY - CHOOSE YOUR PATH INTO DARKNESS", border_color="\033[1;35m"))
    rows.append(make_border_line("=", border_color="\033[1;35m"))
    rows.append("")

    p1 = "▶" if cursor_idx == 0 else " "
    c1 = "\033[1;32m" if cursor_idx == 0 else "\033[90m"
    rows.append(f"  {c1}{p1} [1] FEAR & HUNGER (Normal Mode - Standard Survival)\033[0m")
    rows.append("      - Explorer Combat Stats  : \033[1;32mEmpowered Survival Training\033[0m (Fair combat odds)")
    rows.append("      - Poppy Flower Healing   : \033[1;32m+50 HP\033[0m per application")
    rows.append("      - Marijuana Herb Healing : \033[1;32m+120 HP\033[0m potent medicinal cure")
    rows.append("      - Recommended for tacticians seeking fair odds against subterranean horrors.")
    rows.append("")

    p2 = "▶" if cursor_idx == 1 else " "
    c2 = "\033[1;31m" if cursor_idx == 1 else "\033[90m"
    rows.append(f"  {c2}{p2} [2] TERROR & STARVATION (Hardcore Mode - Ruthless Reality)\033[0m")
    rows.append("      - Explorer Combat Stats  : \033[1;31mPure Baseline Vulnerability\033[0m (Beasts strike to maim)")
    rows.append("      - Poppy Flower Healing   : \033[1;31m+30 HP\033[0m degraded potency")
    rows.append("      - Marijuana Herb Healing : \033[1;31m+75 HP\033[0m scarce medicinal value")
    rows.append("      - Intended only for master explorers where every limb loss is permanent.")
    rows.append("")
    rows.append("\033[1;30m" + "=" * 100 + "\033[0m")
    rows.append("  [CONTROLS]: [W/S] or [Up/Down] Navigate  |  [Enter] Confirm Difficulty  |  [Q] Return")
    rows.append("\033[1;30m" + "=" * 100 + "\033[0m")
    atomic_blit(rows)

def run_difficulty_screen():
    clear_screen()
    cursor_idx = 0
    while True:
        render_difficulty_screen(cursor_idx)
        if os.name == 'nt' and sys.stdin.isatty():
            ch = msvcrt.getch()
            while msvcrt.kbhit():
                msvcrt.getch()
            if ch in (b'\x00', b'\xe0'):
                ext = msvcrt.getch()
                if ext in (b'H', b'P'):
                    cursor_idx = 1 - cursor_idx
            elif ch in (b'w', b'W', b's', b'S'):
                cursor_idx = 1 - cursor_idx
            elif ch == b'1':
                cursor_idx = 0
            elif ch == b'2':
                cursor_idx = 1
            elif ch in (b'\r', b'\n', b' '):
                clear_screen()
                return (cursor_idx == 1)
            elif ch in (b'q', b'Q', b'\x1b'):
                clear_screen()
                return None
        else:
            raw = sys.stdin.readline()
            if not raw:
                clear_screen()
                return False
            line = raw.strip().lower()
            if line in ('w', 's', 'up', 'down'):
                cursor_idx = 1 - cursor_idx
            elif line == '1':
                cursor_idx = 0
            elif line == '2':
                cursor_idx = 1
            elif line in ('', 'enter', 'normal', 'hard', 'hardcore'):
                clear_screen()
                return (cursor_idx == 1)
            elif line in ('q', 'quit'):
                clear_screen()
                return None

# =============================================================================
# ON-DEMAND EXPEDITION SURVIVOR GUIDE BOOK [G]
# =============================================================================
def run_guide_modal():
    clear_screen()
    rows = []
    # Box 1: Title Header Box
    rows.append(make_border_line("=", border_color="\033[1;36m"))
    rows.append(make_centered_box_row("\033[1;37mFEAR & HUNGER: EXPEDITION SURVIVOR GUIDE BOOK\033[0m", border_color="\033[1;36m"))
    rows.append(make_border_line("=", border_color="\033[1;36m"))
    rows.append("")

    # Box 2: Labyrinth Tiles & Hazards
    rows.append(make_border_line("-", border_color="\033[1;33m"))
    rows.append(make_left_box_row("\033[1;33m[LABYRINTH TILES & HAZARDS]\033[0m", border_color="\033[1;33m"))
    rows.append(make_left_box_row("  \033[1;33m O\033[0m Explorer   : Your current position in the pitch-black catacombs.", border_color="\033[1;33m"))
    rows.append(make_left_box_row("  \033[90m .\033[0m Pathway    : Stone dungeon corridor illuminated by your torchlight.", border_color="\033[1;33m"))
    rows.append(make_left_box_row("  \033[42m  \033[0m Wall       : Solid masonry bedrock. Impassable barrier.", border_color="\033[1;33m"))
    rows.append(make_left_box_row("  \033[45;1;37m M\033[0m Monster    : Roaming subterranean beast. Contact initiates combat arena.", border_color="\033[1;33m"))
    rows.append(make_left_box_row("  \033[48;2;139;69;19;1;37m C\033[0m Chest      : Ancient vault. Contains supplies or lethal needle traps.", border_color="\033[1;33m"))
    rows.append(make_left_box_row("  \033[41;1;37m #\033[0m Barricade  : Heavy rockfall debris. Smashed open upon forceful contact.", border_color="\033[1;33m"))
    rows.append(make_left_box_row("  \033[45;1;37m §\033[0m Seal       : Arcane Hexen ward. Occultists dispel it; others suffer burns.", border_color="\033[1;33m"))
    rows.append(make_left_box_row("  \033[43;1;30m =\033[0m Crevice    : Narrow rock crawlspace. Squeeze through carefully.", border_color="\033[1;33m"))
    rows.append(make_left_box_row("  \033[46;1;30m G\033[0m Exit Gate  : Eastern escape portal. REQUIRES 3 RUNIC KEYS TO UNLOCK!", border_color="\033[1;33m"))
    rows.append(make_border_line("-", border_color="\033[1;33m"))
    rows.append("")

    # Box 3: Survival Supplies & Medicine
    rows.append(make_border_line("-", border_color="\033[1;32m"))
    rows.append(make_left_box_row("\033[1;32m[SURVIVAL SUPPLIES & MEDICINE]\033[0m", border_color="\033[1;32m"))
    rows.append(make_left_box_row("  Poppy Flower   : +50 HP (+65 Cahara, +30 Hardcore). Staunches bleeding flesh.", border_color="\033[1;32m"))
    rows.append(make_left_box_row("  Marijuana Herb : +120 HP (+75 Hardcore). Potent medicinal smoke.", border_color="\033[1;32m"))
    rows.append(make_left_box_row("  Moldy Bread    : -40 Hunger. Relieves starvation to prevent HP deterioration.", border_color="\033[1;32m"))
    rows.append(make_left_box_row("  Vintage Ale    : +35 Mind. Quells creeping madness, terror, and panic.", border_color="\033[1;32m"))
    rows.append(make_border_line("-", border_color="\033[1;32m"))
    rows.append("")

    # Box 4: Controls & Navigation
    rows.append(make_border_line("-", border_color="\033[1;37m"))
    rows.append(make_left_box_row("\033[1;37m[EXPEDITION CONTROLS & NAVIGATION]\033[0m", border_color="\033[1;37m"))
    rows.append(make_left_box_row("  [W/A/S/D] or Arrows : Navigate catacombs (expands torchlight).", border_color="\033[1;37m"))
    rows.append(make_left_box_row("  [I] Pouch           : Open vertical survival pouch ([W/S] Navigate, [Enter] Use).", border_color="\033[1;37m"))
    rows.append(make_left_box_row("  [H] Quick Heal      : Heal immediately with best available herb from pouch.", border_color="\033[1;37m"))
    rows.append(make_left_box_row("  [Q] Surrender       : Surrender current expedition and quit back to surface.", border_color="\033[1;37m"))
    rows.append(make_border_line("-", border_color="\033[1;37m"))
    rows.append("")

    # Return Prompt
    rows.append("  \033[1;37m[GUIDE CONTROLS]: Press [G], [Enter], or [Esc] to close Guide and return to Map\033[0m")
    atomic_blit(rows)
    if os.name == 'nt' and sys.stdin.isatty():
        while True:
            ch = msvcrt.getch()
            while msvcrt.kbhit():
                msvcrt.getch()
            if ch in (b'g', b'G', b'\r', b'\n', b' ', b'\x1b', b'q', b'Q'):
                break
    else:
        sys.stdin.readline()
    clear_screen()

# =============================================================================
# INTERACTIVE MAP EXPLORATION WITH FOG OF WAR & ENCOUNTERS
# =============================================================================
def run_master_game():
    # 1. Title Screen
    if not run_title_screen():
        clear_screen()
        sys.stdout.write("\033[?25h\n[OK] Expedition abandoned before entering the darkness.\n")
        return

    # 2. Difficulty Select
    is_hardcore = run_difficulty_screen()
    if is_hardcore is None:
        clear_screen()
        sys.stdout.write("\033[?25h\n[OK] Expedition aborted.\n")
        return

    # 3. Solo Explorer Selection (W/S vertical live model selector)
    selected_hero, sel_idx = combat_engine.run_solo_select_interactive()
    if selected_hero is None:
        clear_screen()
        sys.stdout.write("\033[?25h\n[OK] Expedition cancelled.\n")
        return

    clear_screen()
    solo_hero = copy.deepcopy(selected_hero)
    solo_hero["is_guarding"] = False
    solo_hero["buff"] = ""
    solo_hero["debuffs"] = []

    # Inventory setup
    if solo_hero["name"] == "CAHARA":
        inventory = {"poppy": 5, "weed": 3, "bread": 6, "ale": 3}
    else:
        inventory = {"poppy": 3, "weed": 2, "bread": 4, "ale": 2}

    # Map State
    player_x = 2
    player_y = 2
    step_count = 0
    key_count = 0
    monsters_defeated = 0
    chests_opened = 0
    cleared_tiles = set()
    explored_mask = [[False for _ in range(MAP_WIDTH)] for _ in range(MAP_HEIGHT)]
    milestones_reached = set()
    recent_log = f"[*] {solo_hero['name']} [{solo_hero['role']}] steps into the pitch-black catacombs."

    # Dynamic unique monster assignment per run (100% NO DUPLICATES!)
    chosen_reg_ids = random.sample(REGULAR_MONSTER_IDS, 8)
    chosen_boss_ids = random.sample(BOSS_MONSTER_IDS, 2)
    reg_coords = [
        (14, 2), (10, 6), (20, 7), (28, 4),
        (14, 11), (24, 11), (8, 15), (20, 15)
    ]
    boss_coords = [(34, 6), (34, 14)]
    run_monsters = {}
    for coord, mid in zip(reg_coords, chosen_reg_ids):
        m_data = copy.deepcopy(ALL_MONSTERS_CATALOG[mid])
        m_data["drops_key"] = False
        run_monsters[coord] = m_data
    for coord, mid in zip(boss_coords, chosen_boss_ids):
        m_data = copy.deepcopy(ALL_MONSTERS_CATALOG[mid])
        m_data["drops_key"] = True
        run_monsters[coord] = m_data
    encountered_monsters_this_run = set()

    def reveal_around(px, py, radius=4):
        new_revealed = 0
        r_sq = radius * radius
        for dy in range(-radius, radius + 1):
            for dx in range(-radius, radius + 1):
                if (dx * dx + dy * dy) <= r_sq:
                    tx = px + dx
                    ty = py + dy
                    if 0 <= tx < MAP_WIDTH and 0 <= ty < MAP_HEIGHT:
                        if not explored_mask[ty][tx]:
                            explored_mask[ty][tx] = True
                            new_revealed += 1
        return new_revealed

    # Initial reveal around start (2, 2)
    reveal_around(player_x, player_y, radius=4)

    def render_map_view(pouch_open=False, pouch_cur=0):
        rows = []
        diff_tag = "\033[1;31m[TERROR & STARVATION]\033[0m" if is_hardcore else "\033[1;32m[FEAR & HUNGER]\033[0m"
        h_info = f"{solo_hero['name']} [{solo_hero['role']}] - HP:{solo_hero['hp']:3d}/{solo_hero['max_hp']:3d}"

        rows.append("\033[1;30m+" + "=" * 98 + "+\033[0m")
        title_inside = f"     FEAR & HUNGER: TERMINAL LABYRINTH - SOLO EXPLORER EXPEDITION          {diff_tag}"
        rows.append(f"\033[1;30m|\033[0m{combat_engine.fit_ansi(title_inside, 98)}\033[1;30m|\033[0m")
        rows.append("\033[1;30m+" + "-" * 98 + "+\033[0m")

        h_name_role = f"{solo_hero['name']} [{solo_hero['role']}]"
        h_hp_str = f"HP: {solo_hero['hp']:3d}/{solo_hero['max_hp']:3d}"
        h_mind_str = f"MIND: {solo_hero.get('mind', 100):3d}/{solo_hero.get('max_mind', 100):3d}"
        h_hunger_str = f"HUNGER: {solo_hero.get('hunger', 0):2d}/100"
        content_exp = f"  \033[1;32m[EXPLORER]\033[0m   \033[1;37m{h_name_role:<24}\033[0m |  \033[1;32m{h_hp_str:<14}\033[0m |  \033[1;36m{h_mind_str:<15}\033[0m |  \033[1;33m{h_hunger_str:<15}\033[0m"
        rows.append(f"\033[1;30m|\033[0m{combat_engine.fit_ansi(content_exp, 98)}\033[1;30m|\033[0m")

        rows.append("\033[1;30m+" + (" -" * 49) + "+\033[0m")

        pos_str = f"POS: ({player_x:2d},{player_y:2d})"
        keys_str = f"KEYS: {key_count}/3"
        slain_str = f"SLAIN: {monsters_defeated} FOES"
        steps_str = f"STEPS: {step_count:<4d}"
        trait_str = f"TRAIT: {solo_hero['trait']}"
        content_quest = f"  \033[1;33m[EXPEDITION]\033[0m \033[1;37m{pos_str:<13}\033[0m |  \033[1;36m{keys_str:<11}\033[0m |  \033[1;31m{slain_str:<13}\033[0m |  \033[1;37m{steps_str:<12}\033[0m |  \033[1;35m{trait_str[:24]}\033[0m"
        rows.append(f"\033[1;30m|\033[0m{combat_engine.fit_ansi(content_quest, 98)}\033[1;30m|\033[0m")

        rows.append("\033[1;30m+" + "-" * 98 + "+\033[0m")

        # 20 rows of map area (14 spaces pad + 72 cols map + 14 spaces pad = 100 cols)
        border_left_pad = "              "
        torch_sq = 16

        for y in range(MAP_HEIGHT):
            row_str = ""
            for x in range(MAP_WIDTH):
                dist_sq = (x - player_x) ** 2 + (y - player_y) ** 2
                is_active_torch = (dist_sq <= torch_sq)
                is_visited = explored_mask[y][x]

                if x == player_x and y == player_y:
                    row_str += "\033[1;33;40m O\033[0m"
                elif not is_visited:
                    row_str += "  "
                else:
                    tile = get_base_tile(x, y)
                    if (x, y) in cleared_tiles and tile in (TILE_MONSTER, TILE_CHEST, TILE_BARRICADE, TILE_SEAL):
                        tile = TILE_PATH

                    if is_active_torch:
                        if tile == TILE_WALL:
                            row_str += "\033[42m  \033[0m"
                        elif tile == TILE_PATH:
                            row_str += "\033[90m .\033[0m"
                        elif tile == TILE_MONSTER:
                            row_str += "\033[45;1;37m M\033[0m"
                        elif tile == TILE_CHEST:
                            row_str += "\033[48;2;139;69;19;1;37m C\033[0m"
                        elif tile == TILE_GATE:
                            row_str += "\033[46;1;30m G\033[0m"
                        elif tile == TILE_BARRICADE:
                            row_str += "\033[41;1;37m #\033[0m"
                        elif tile == TILE_SEAL:
                            row_str += "\033[45;1;37m §\033[0m"
                        elif tile == TILE_CRAWLSPACE:
                            row_str += "\033[43;1;30m =\033[0m"
                    else:
                        if tile == TILE_WALL:
                            row_str += "\033[48;2;20;75;30m  \033[0m"
                        elif tile == TILE_PATH:
                            row_str += "\033[38;2;75;75;75m .\033[0m"
                        elif tile == TILE_MONSTER:
                            row_str += "\033[48;2;80;25;80;1;37m M\033[0m"
                        elif tile == TILE_CHEST:
                            row_str += "\033[48;2;90;45;15;1;37m C\033[0m"
                        elif tile == TILE_GATE:
                            row_str += "\033[48;2;20;85;85;1;30m G\033[0m"
                        elif tile == TILE_BARRICADE:
                            row_str += "\033[48;2;100;20;20;1;37m #\033[0m"
                        elif tile == TILE_SEAL:
                            row_str += "\033[48;2;70;20;70;1;37m §\033[0m"
                        elif tile == TILE_CRAWLSPACE:
                            row_str += "\033[48;2;90;70;10;1;30m =\033[0m"

            rows.append(f"{border_left_pad}{row_str}")

        rows.append("\033[1;30m+----------------------------------------------------------------------------------------------------+\033[0m")

        if pouch_open:
            rows.append("  \033[1;33m[SURVIVAL POUCH - SELECT ITEM TO ADMINISTER]:\033[0m")
            pouch_options = [
                (f"Poppy Flower    x{inventory['poppy']:<2}  (+50 HP)    - Staunches bleeding & heals flesh", inventory['poppy'] > 0),
                (f"Marijuana Herb  x{inventory['weed']:<2}  (+120 HP)   - Potent ancient medicinal cure", inventory['weed'] > 0),
                (f"Moldy Bread     x{inventory['bread']:<2}  (-40 Hngr)  - Relieves gnawing starvation", inventory['bread'] > 0),
                (f"Vintage Ale     x{inventory['ale']:<2}  (+35 Mind)  - Restores shattered sanity", inventory['ale'] > 0),
                (f"Close Pouch     (Return to Map Exploration)", True)
            ]
            for p_idx, (p_text, p_avail) in enumerate(pouch_options):
                is_cur = (p_idx == pouch_cur)
                prefix = "▶" if is_cur else " "
                c_code = "\033[1;33m" if is_cur else ("\033[1;37m" if p_avail else "\033[90m")
                rows.append(f"  {c_code}{prefix} [{p_idx+1}] {p_text}\033[0m")
            rows.append("\033[1;30m+====================================================================================================+\033[0m")
            rows.append("  \033[1;37m[CONTROLS]: [W/S] Navigate  |  [Enter] Administer Item  |  [I/Esc] Close Pouch\033[0m")
        else:
            rows.append(f"  \033[1;33m[EXPEDITION LOG]:\033[0m \033[1;37m{fit_ansi(recent_log, 78)}\033[0m")
            rows.append("")
            rows.append("\033[1;30m+====================================================================================================+\033[0m")
            rows.append("  \033[1;37m[CONTROLS]: [W/A/S/D] Move  |  [I] Pouch  |  [H] Quick Heal  |  [G] Guide  |  [Q] Quit\033[0m")
            rows.append("\033[1;30m====================================================================================================\033[0m")
        atomic_blit(rows)

    def handle_map_move(dx, dy):
        nonlocal player_x, player_y, step_count, key_count, monsters_defeated, chests_opened, recent_log
        nx = player_x + dx
        ny = player_y + dy

        if nx < 0 or nx >= MAP_WIDTH or ny < 0 or ny >= MAP_HEIGHT:
            recent_log = "[COLLISION]: Chiseled dungeon bedrock blocks passage."
            return

        base_tile = get_base_tile(nx, ny)

        # Wall Collision
        if base_tile == TILE_WALL:
            recent_log = "[COLLISION]: Heavy stone wall blocks advancement."
            return

        # Barricade Obstacle
        if base_tile == TILE_BARRICADE and (nx, ny) not in cleared_tiles:
            cleared_tiles.add((nx, ny))
            recent_log = f"[{solo_hero['name']}]: Smashes through rock barricade with forceful blows! Passage cleared!"

        # Hexen Arcane Seal
        elif base_tile == TILE_SEAL and (nx, ny) not in cleared_tiles:
            cleared_tiles.add((nx, ny))
            if solo_hero["name"] in ("ENKI", "NAS'HRAH"):
                recent_log = f"[{solo_hero['name']}]: Chants counter-curse in eldritch tongue, dissolving the seal into ash!"
            else:
                solo_hero["hp"] = max(1, solo_hero["hp"] - 10)
                recent_log = f"[{solo_hero['name']}]: Arcane runes burn flesh (-10 HP) but shatter into ash! Passage open!"

        # Crawlspace
        elif base_tile == TILE_CRAWLSPACE:
            if solo_hero["name"] in ("THE GIRL", "MOONLESS"):
                recent_log = f"[{solo_hero['name']}]: Squeezes effortlessly through the narrow rock crevice!"
            else:
                recent_log = f"[{solo_hero['name']}]: Wedges carefully through the narrow rock crevice with effort!"

        # Vault Chest
        elif base_tile == TILE_CHEST and (nx, ny) not in cleared_tiles:
            cleared_tiles.add((nx, ny))
            chests_opened += 1
            if (nx, ny) in [(6, 11), (12, 17), (26, 17)]:
                if solo_hero["name"] in ("CAHARA", "LE'GARDE"):
                    key_count = min(3, key_count + 1)
                    recent_log = f"[{solo_hero['name']}]: Keen perception disarms spring needle safely! Obtained Runic Key ({key_count}/3)!"
                else:
                    solo_hero["hp"] = max(1, solo_hero["hp"] - 20)
                    key_count = min(3, key_count + 1)
                    recent_log = f"[TRAP TRIGGERED]: Spring needle grazed {solo_hero['name']} (-20 HP)! Retrieved Runic Key ({key_count}/3)!"
            else:
                # Regular supply chest: 25% chance of Chest Mimic encounter!
                is_mimic = (random.random() < 0.25) and (MIMIC_ID not in encountered_monsters_this_run)
                if is_mimic:
                    encountered_monsters_this_run.add(MIMIC_ID)
                    mimic_data = copy.deepcopy(ALL_MONSTERS_CATALOG[MIMIC_ID])
                    recent_log = f"[AMBUSH!]: The chest sprouts razor fangs! CHEST MIMIC springs forward!"
                    clear_screen()
                    outcome, updated_hero, updated_inv = combat_engine.run_solo_combat(
                        solo_hero,
                        monster_id=mimic_data["id"],
                        monster_name=mimic_data["name"],
                        monster_archetype=mimic_data["archetype"],
                        monster_hp=mimic_data["hp"],
                        monster_atk=mimic_data["atk"],
                        monster_def=mimic_data["def"],
                        inv=inventory
                    )
                    clear_screen()
                    solo_hero["hp"] = updated_hero["hp"]
                    solo_hero["mind"] = updated_hero.get("mind", solo_hero["mind"])
                    solo_hero["toxicity"] = updated_hero.get("toxicity", solo_hero["toxicity"])
                    inventory.update(updated_inv)
                    if outcome == "VICTORY":
                        monsters_defeated += 1
                        inventory["poppy"] += 2
                        inventory["ale"] += 1
                        recent_log = f"[MIMIC SLAIN!]: {solo_hero['name']} smashed the Mimic! Looted +2 White Poppy, +1 Vintage Ale!"
                    elif outcome == "FLEE":
                        recent_log = f"[TACTICAL RETREAT]: Slipped away from the Mimic's snapping fangs back to corridor!"
                        return
                    elif outcome == "DEFEAT":
                        show_game_over_screen(solo_hero, mimic_data["name"])
                        return "GAME_OVER"
                    elif outcome == "QUIT":
                        return "QUIT"
                else:
                    inventory["poppy"] += 1
                    inventory["bread"] += 1
                    recent_log = f"[CHEST]: Looted supplies at ({nx}, {ny}) (+1 Poppy Flower, +1 Moldy Bread)!"

        # Roaming Monster Encounter -> Launch Turn-based Combat Arena!
        elif base_tile == TILE_MONSTER and (nx, ny) not in cleared_tiles:
            m_data = run_monsters.get((nx, ny))
            if not m_data:
                m_data = copy.deepcopy(ALL_MONSTERS_CATALOG[8])
                m_data["drops_key"] = False

            encountered_monsters_this_run.add(m_data["id"])

            # Enter real Pokémon-style combat arena
            clear_screen()
            outcome, updated_hero, updated_inv = combat_engine.run_solo_combat(
                solo_hero,
                monster_id=m_data["id"],
                monster_name=m_data["name"],
                monster_archetype=m_data["archetype"],
                monster_hp=m_data["hp"],
                monster_atk=m_data["atk"],
                monster_def=m_data["def"],
                inv=inventory
            )
            clear_screen()

            # Sync updated state back
            solo_hero["hp"] = updated_hero["hp"]
            solo_hero["mind"] = updated_hero.get("mind", solo_hero["mind"])
            solo_hero["toxicity"] = updated_hero.get("toxicity", solo_hero["toxicity"])
            inventory.update(updated_inv)

            if outcome == "VICTORY":
                cleared_tiles.add((nx, ny))
                monsters_defeated += 1
                if m_data.get("drops_key") and key_count < 3:
                    key_count += 1
                    recent_log = f"[VICTORY]: Vanquished {m_data['name']}! Obtained Boss Runic Key ({key_count}/3)!"
                else:
                    recent_log = f"[VICTORY]: {solo_hero['name']} neutralized {m_data['name']}! Room secured."
            elif outcome == "FLEE":
                recent_log = f"[TACTICAL RETREAT]: Successfully disengaged from {m_data['name']} back into corridor."
                return # Do not move player onto monster tile
            elif outcome == "DEFEAT":
                show_game_over_screen(solo_hero, m_data["name"])
                return "GAME_OVER"
            elif outcome == "QUIT":
                return "QUIT"

        # Exit Gate
        elif base_tile == TILE_GATE:
            if key_count >= 3:
                show_victory_screen(solo_hero, step_count, monsters_defeated, chests_opened, is_hardcore)
                return "VICTORY"
            else:
                recent_log = f"[GATE]: The massive Runic Gate is locked! Requires 3 Runic Keys (You have {key_count}/3)."
                return

        # Advance movement
        player_x = nx
        player_y = ny
        step_count += 1
        new_tiles = reveal_around(player_x, player_y, radius=4)
        if new_tiles > 0 and not recent_log.startswith("["):
            recent_log = f"[*] Advanced into dark corridor. +{new_tiles} tiles permanently illuminated."

        # Hunger drain check
        if step_count % 35 == 0 and solo_hero["name"] != "NAS'HRAH":
            solo_hero["hunger"] = min(100, solo_hero.get("hunger", 0) + 15)
            if solo_hero["hunger"] >= 80:
                solo_hero["hp"] = max(1, solo_hero["hp"] - 10)
                recent_log = f"[STARVATION]: Severe stomach cramps drain -10 HP! Eat bread in pouch [I]."

    # Exploration Game Loop
    in_pouch = False
    pouch_cur = 0
    while True:
        render_map_view(pouch_open=in_pouch, pouch_cur=pouch_cur)

        if os.name == 'nt' and sys.stdin.isatty():
            ch = msvcrt.getch()
            while msvcrt.kbhit():
                msvcrt.getch()

            if in_pouch:
                if ch in (b'\x00', b'\xe0'):
                    ext = msvcrt.getch()
                    if ext == b'H':    # Up Arrow
                        pouch_cur = (pouch_cur - 1) % 5
                    elif ext == b'P':  # Down Arrow
                        pouch_cur = (pouch_cur + 1) % 5
                elif ch in (b'w', b'W'):
                    pouch_cur = (pouch_cur - 1) % 5
                elif ch in (b's', b'S'):
                    pouch_cur = (pouch_cur + 1) % 5
                elif ch in (b'1', b'2', b'3', b'4', b'5'):
                    pouch_cur = int(ch.decode('ascii')) - 1
                elif ch in (b'\r', b'\n', b' '):
                    if pouch_cur == 0:
                        if inventory["poppy"] > 0:
                            inventory["poppy"] -= 1
                            heal = 65 if solo_hero["name"] == "CAHARA" else (30 if is_hardcore else 50)
                            solo_hero["hp"] = min(solo_hero["max_hp"], solo_hero["hp"] + heal)
                            recent_log = f"[POUCH]: Applied Poppy Flower (+{heal} HP). Current HP: {solo_hero['hp']}/{solo_hero['max_hp']}"
                            in_pouch = False
                        else:
                            recent_log = "[POUCH]: You have no Poppy Flowers remaining!"
                    elif pouch_cur == 1:
                        if inventory["weed"] > 0:
                            inventory["weed"] -= 1
                            heal = 75 if is_hardcore else 120
                            solo_hero["hp"] = min(solo_hero["max_hp"], solo_hero["hp"] + heal)
                            recent_log = f"[POUCH]: Smoked Marijuana Herb (+{heal} HP). Current HP: {solo_hero['hp']}/{solo_hero['max_hp']}"
                            in_pouch = False
                        else:
                            recent_log = "[POUCH]: You have no Marijuana Herbs remaining!"
                    elif pouch_cur == 2:
                        if inventory["bread"] > 0:
                            inventory["bread"] -= 1
                            solo_hero["hunger"] = max(0, solo_hero.get("hunger", 0) - 40)
                            recent_log = f"[POUCH]: Ate Moldy Bread. Hunger relieved (-40 Hunger)."
                            in_pouch = False
                        else:
                            recent_log = "[POUCH]: You have no Bread remaining!"
                    elif pouch_cur == 3:
                        if inventory["ale"] > 0:
                            inventory["ale"] -= 1
                            solo_hero["mind"] = min(solo_hero.get("max_mind", 100), solo_hero.get("mind", 100) + 35)
                            recent_log = f"[POUCH]: Drank Vintage Ale (+35 Mind). Terror cleansed!"
                            in_pouch = False
                        else:
                            recent_log = "[POUCH]: You have no Vintage Ale remaining!"
                    elif pouch_cur == 4:
                        in_pouch = False
                elif ch in (b'c', b'C', b'i', b'I', b'\x1b', b'b', b'B'):
                    in_pouch = False
                continue

            if ch in (b'\x00', b'\xe0'):
                ext = msvcrt.getch()
                if ext == b'H':   # Up Arrow
                    res = handle_map_move(0, -1)
                elif ext == b'P': # Down Arrow
                    res = handle_map_move(0, 1)
                elif ext == b'K': # Left Arrow
                    res = handle_map_move(-1, 0)
                elif ext == b'M': # Right Arrow
                    res = handle_map_move(1, 0)
            elif ch in (b'w', b'W'):
                res = handle_map_move(0, -1)
            elif ch in (b's', b'S'):
                res = handle_map_move(0, 1)
            elif ch in (b'a', b'A'):
                res = handle_map_move(-1, 0)
            elif ch in (b'd', b'D'):
                res = handle_map_move(1, 0)
            elif ch in (b'i', b'I'):
                in_pouch = True
                pouch_cur = 0
                continue
            elif ch in (b'g', b'G'):
                run_guide_modal()
                continue
            elif ch in (b'h', b'H'):
                # Quick heal
                if inventory["poppy"] > 0:
                    inventory["poppy"] -= 1
                    heal = 65 if solo_hero["name"] == "CAHARA" else (30 if is_hardcore else 50)
                    solo_hero["hp"] = min(solo_hero["max_hp"], solo_hero["hp"] + heal)
                    recent_log = f"[QUICK HEAL]: Consumed Poppy Flower (+{heal} HP). HP: {solo_hero['hp']}/{solo_hero['max_hp']}"
                elif inventory["weed"] > 0:
                    inventory["weed"] -= 1
                    heal = 75 if is_hardcore else 120
                    solo_hero["hp"] = min(solo_hero["max_hp"], solo_hero["hp"] + heal)
                    recent_log = f"[QUICK HEAL]: Consumed Marijuana Herb (+{heal} HP). HP: {solo_hero['hp']}/{solo_hero['max_hp']}"
                else:
                    recent_log = "[QUICK HEAL]: No medicinal herbs in pouch!"
                continue
            elif ch in (b'q', b'Q', b'\x03'):
                clear_screen()
                sys.stdout.write("\033[?25h\n[OK] Labyrinth Expedition suspended.\n")
                break

            if res in ("VICTORY", "GAME_OVER", "QUIT"):
                break
        else:
            raw = sys.stdin.readline()
            if not raw:
                break
            line = raw.strip().lower()
            res = None
            if in_pouch:
                if line in ('w', 'up'):
                    pouch_cur = (pouch_cur - 1) % 5
                elif line in ('s', 'down'):
                    pouch_cur = (pouch_cur + 1) % 5
                elif line in ('1', '2', '3', '4', '5'):
                    pouch_cur = int(line) - 1
                elif line in ('', 'enter', 'use'):
                    if pouch_cur == 0 and inventory["poppy"] > 0:
                        inventory["poppy"] -= 1
                        heal = 65 if solo_hero["name"] == "CAHARA" else (30 if is_hardcore else 50)
                        solo_hero["hp"] = min(solo_hero["max_hp"], solo_hero["hp"] + heal)
                        in_pouch = False
                    elif pouch_cur == 1 and inventory["weed"] > 0:
                        inventory["weed"] -= 1
                        heal = 75 if is_hardcore else 120
                        solo_hero["hp"] = min(solo_hero["max_hp"], solo_hero["hp"] + heal)
                        in_pouch = False
                    elif pouch_cur == 2 and inventory["bread"] > 0:
                        inventory["bread"] -= 1
                        solo_hero["hunger"] = max(0, solo_hero.get("hunger", 0) - 40)
                        in_pouch = False
                    elif pouch_cur == 3 and inventory["ale"] > 0:
                        inventory["ale"] -= 1
                        solo_hero["mind"] = min(solo_hero.get("max_mind", 100), solo_hero.get("mind", 100) + 35)
                        in_pouch = False
                    elif pouch_cur == 4:
                        in_pouch = False
                elif line in ('i', 'c', 'close', 'esc'):
                    in_pouch = False
                continue

            if line == 'w':
                res = handle_map_move(0, -1)
            elif line == 's':
                res = handle_map_move(0, 1)
            elif line == 'a':
                res = handle_map_move(-1, 0)
            elif line == 'd':
                res = handle_map_move(1, 0)
            elif line in ('i', 'pouch'):
                in_pouch = True
                pouch_cur = 0
                continue
            elif line in ('g', 'guide'):
                run_guide_modal()
                continue
            elif line in ('h', 'heal'):
                if inventory["poppy"] > 0:
                    inventory["poppy"] -= 1
                    heal = 65 if solo_hero["name"] == "CAHARA" else (30 if is_hardcore else 50)
                    solo_hero["hp"] = min(solo_hero["max_hp"], solo_hero["hp"] + heal)
                elif inventory["weed"] > 0:
                    inventory["weed"] -= 1
                    heal = 75 if is_hardcore else 120
                    solo_hero["hp"] = min(solo_hero["max_hp"], solo_hero["hp"] + heal)
                continue
            elif line == 'q':
                break
            if res in ("VICTORY", "GAME_OVER", "QUIT"):
                break

# =============================================================================
# END-GAME SCREENS: VICTORY & GAME OVER
# =============================================================================
def show_victory_screen(hero, steps, slain, chests, is_hardcore):
    clear_screen()
    rows = []
    raw_banner = [
        r" ___      ___ ___  ________  _________  ________  ________      ___    ___",
        r"|\  \    /  /|\  \|\   ____\|\___   ___\\   __  \|\   __  \    |\  \  /  /|",
        r"\ \  \  /  / | \  \ \  \___|\|___ \  \_\ \  \|\  \ \  \|\  \   \ \  \/  / /",
        r" \ \  \/  / / \ \  \ \  \        \ \  \ \ \  \\\  \ \   _  _\   \ \    / /",
        r"  \ \    / /   \ \  \ \  \____    \ \  \ \ \  \\\  \ \  \\  \|   \/  /  /",
        r"   \ \__/ /     \ \__\ \_______\   \ \__\ \ \_______\ \__\\ _\   __/  / /",
        r"    \|__|/       \|__|\|_______|    \|__|  \|_______|\|__|\|__| |\___/ /",
        r"                                                                \|___|/"
    ]
    max_b_len = max(len(l) for l in raw_banner)

    # Box 1: Victory Banner
    rows.append(make_border_line("=", border_color="\033[1;33m"))
    for b_line in raw_banner:
        rows.append(make_centered_box_row("\033[1;33m" + b_line.ljust(max_b_len) + "\033[0m", border_color="\033[1;33m"))
    rows.append(make_centered_box_row("\033[1;32m[ E S C A P E   A C H I E V E D   -   V I C T O R Y ]\033[0m", border_color="\033[1;33m"))
    rows.append(make_border_line("=", border_color="\033[1;33m"))
    rows.append("")

    # Box 2: Proclamation Box
    rows.append(make_border_line("-", border_color="\033[1;32m"))
    rows.append(make_centered_box_row("\033[1;32mALL 3 RUNIC KEYS INSERTED! THE RUNIC GATES GRIND OPEN AS GOLDEN SUNLIGHT FLOODS THE DARK!\033[0m", border_color="\033[1;32m"))
    rows.append(make_centered_box_row(f"\033[1;37m{hero['name']} [{hero['role']}] has triumphed over subterranean dread and escaped alive!\033[0m", border_color="\033[1;32m"))
    rows.append(make_border_line("-", border_color="\033[1;32m"))
    rows.append("")

    # Box 3: Expedition Performance Log
    mode_str = "TERROR & STARVATION (Hardcore Survivor)" if is_hardcore else "FEAR & HUNGER (Standard Survivor)"
    rows.append(make_border_line("-", border_color="\033[1;36m"))
    rows.append(make_left_box_row("\033[1;36m[EXPEDITION PERFORMANCE LOG]:\033[0m", border_color="\033[1;36m"))
    rows.append(make_left_box_row(f"  - Difficulty Conquered : \033[1;32m{mode_str}\033[0m", border_color="\033[1;36m"))
    rows.append(make_left_box_row(f"  - Hero Standing        : \033[1;37m{hero['name']} ({hero['hp']}/{hero['max_hp']} HP, Mind: {hero['mind']}/100)\033[0m", border_color="\033[1;36m"))
    rows.append(make_left_box_row(f"  - Total Steps Taken    : \033[1;33m{steps} steps\033[0m", border_color="\033[1;36m"))
    rows.append(make_left_box_row(f"  - Foes Neutralized     : \033[1;31m{slain} monsters vanquished\033[0m", border_color="\033[1;36m"))
    rows.append(make_left_box_row(f"  - Ancient Vaults Looted: \033[1;33m{chests} vaults cleared\033[0m", border_color="\033[1;36m"))
    rows.append(make_border_line("-", border_color="\033[1;36m"))
    rows.append("")

    # Box 4: Controls
    rows.append("\033[1;30m" + "=" * 100 + "\033[0m")
    rows.append("  \033[1;37m[CONTROLS]: Press [Enter] or [Q] to return to surface\033[0m")
    rows.append("\033[1;30m" + "=" * 100 + "\033[0m")
    atomic_blit(rows)
    if os.name == 'nt' and sys.stdin.isatty():
        msvcrt.getch()
    else:
        sys.stdin.readline()
    clear_screen()

def show_game_over_screen(hero, killer):
    clear_screen()
    rows = []
    raw_banner = [
        r"  ____    _    __  __ _____    _____     _______ ____  ",
        r" / ___|  / \  |  \/  | ____|  / _ \ \   / / ____|  _ \ ",
        r"| |  _  / _ \ | |\/| |  _|   | | | \ \ / /|  _| | |_) |",
        r"| |_| |/ ___ \| |  | | |___  | |_| |\ V / | |___|  _ < ",
        r" \____/_/   \_\_|  |_|_____|  \___/  \_/  |_____|_| \_\\"
    ]
    max_b_len = max(len(l) for l in raw_banner)

    # Box 1: Game Over Banner
    rows.append(make_border_line("=", border_color="\033[1;31m"))
    for b_line in raw_banner:
        rows.append(make_centered_box_row("\033[1;31m" + b_line.ljust(max_b_len) + "\033[0m", border_color="\033[1;31m"))
    rows.append(make_centered_box_row("\033[1;31m[ S U R V I V O R   D E M I S E   -   Y O U   D I E D ]\033[0m", border_color="\033[1;31m"))
    rows.append(make_border_line("=", border_color="\033[1;31m"))
    rows.append("")

    # Box 2: Demise Proclamation Box
    rows.append(make_border_line("-", border_color="\033[1;31m"))
    rows.append(make_centered_box_row(f"\033[1;37m{hero['name']} HAS FALLEN TO {killer.upper()} IN THE DARK PERIMETER.\033[0m", border_color="\033[1;31m"))
    rows.append(make_centered_box_row("\033[90mYour flesh decays into subterranean ash... The forgotten gods claim another soul.\033[0m", border_color="\033[1;31m"))
    rows.append(make_border_line("-", border_color="\033[1;31m"))
    rows.append("")

    # Box 3: Controls
    rows.append("\033[1;30m" + "=" * 100 + "\033[0m")
    rows.append("  \033[1;37m[CONTROLS]: Press [Enter] or [Q] to exit\033[0m")
    rows.append("\033[1;30m" + "=" * 100 + "\033[0m")
    atomic_blit(rows)
    if os.name == 'nt' and sys.stdin.isatty():
        msvcrt.getch()
    else:
        sys.stdin.readline()
    clear_screen()

# =============================================================================
# MAIN ENTRY POINT
# =============================================================================
def main():
    try:
        run_master_game()
    finally:
        sys.stdout.write("\033[?25h\n")
        sys.stdout.flush()

if __name__ == "__main__":
    main()
