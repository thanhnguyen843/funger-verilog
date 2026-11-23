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

def atomic_blit(rows):
    """Blits entire screen atomically via cursor home to eliminate flicker 100%."""
    formatted_rows = [fit_100_cols(r) for r in rows]
    frame_str = "\033[H" + "\n".join(formatted_rows) + "\n\033[J"
    sys.stdout.write(frame_str)
    sys.stdout.flush()

# =============================================================================
# TITLE SCREEN & DIFFICULTY SELECTION
# =============================================================================
def render_title_screen():
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
    rows.append("   \033[1;32m[1] START EXPEDITION (EMBARK SOLO)\033[0m        \033[1;31m[0] ABANDON HOPE (QUIT)\033[0m")
    rows.append("")
    rows.append("\033[1;30m" + "=" * 100 + "\033[0m")
    rows.append("  [CONTROLS]: Press [1] or Enter to start  |  Press [0] or [Q] to quit")
    rows.append("\033[1;30m" + "=" * 100 + "\033[0m")
    atomic_blit(rows)

def run_title_screen():
    sys.stdout.write("\033[2J\033[H\033[?25l")
    sys.stdout.flush()

    while True:
        render_title_screen()
        if os.name == 'nt' and sys.stdin.isatty():
            ch = msvcrt.getch()
            while msvcrt.kbhit():
                msvcrt.getch()
            if ch in (b'1', b'\r', b'\n', b' '):
                return True
            elif ch in (b'0', b'q', b'Q', b'\x1b', b'\x03'):
                return False
        else:
            raw = sys.stdin.readline()
            if not raw:
                return False
            line = raw.strip().lower()
            if line in ('1', '', 'start', 'c'):
                return True
            elif line in ('0', 'q', 'quit'):
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
    rows.append("  [CONTROLS]: [W/S] or [Up/Down] Navigate  |  [Enter/1/2] Confirm Difficulty  |  [Q] Return")
    rows.append("\033[1;30m" + "=" * 100 + "\033[0m")
    atomic_blit(rows)

def run_difficulty_screen():
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
                return False # Normal
            elif ch == b'2':
                return True  # Hardcore
            elif ch in (b'\r', b'\n', b' '):
                return (cursor_idx == 1)
            elif ch in (b'q', b'Q', b'\x1b'):
                return None
        else:
            raw = sys.stdin.readline()
            if not raw:
                return False
            line = raw.strip().lower()
            if line in ('1', 'normal', ''):
                return False
            elif line in ('2', 'hard', 'hardcore'):
                return True
            elif line in ('q', 'quit'):
                return None

# =============================================================================
# INTERACTIVE MAP EXPLORATION WITH FOG OF WAR & ENCOUNTERS
# =============================================================================
def run_master_game():
    # 1. Title Screen
    if not run_title_screen():
        sys.stdout.write("\033[?25h\n[OK] Expedition abandoned before entering the darkness.\n")
        return

    # 2. Difficulty Select
    is_hardcore = run_difficulty_screen()
    if is_hardcore is None:
        sys.stdout.write("\033[?25h\n[OK] Expedition aborted.\n")
        return

    # 3. Solo Explorer Selection (W/S vertical live model selector)
    selected_hero, sel_idx = combat_engine.run_solo_select_interactive()
    if selected_hero is None:
        sys.stdout.write("\033[?25h\n[OK] Expedition cancelled.\n")
        return

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

    def count_explored():
        return sum(row.count(True) for row in explored_mask)

    # Initial reveal around start (2, 2)
    reveal_around(player_x, player_y, radius=4)

    def render_map_view(pouch_open=False, pouch_cur=0):
        rows = []
        exp_count = count_explored()
        pct = (exp_count * 100.0) / TOTAL_TILES

        # Progress bar (20 chars)
        bar_fill = int(pct / 5.0)
        bar_str = "█" * bar_fill + "░" * (20 - bar_fill)

        diff_tag = "\033[1;31m[TERROR & STARVATION]\033[0m" if is_hardcore else "\033[1;32m[FEAR & HUNGER]\033[0m"
        h_info = f"{solo_hero['name']} [{solo_hero['role']}] - HP:{solo_hero['hp']:3d}/{solo_hero['max_hp']:3d}"

        rows.append("\033[1;30m+====================================================================================================+\033[0m")
        rows.append(f"\033[1;30m| \033[1;37m     FEAR & HUNGER: TERMINAL LABYRINTH - SOLO EXPLORER EXPEDITION  {diff_tag:<32}\033[1;30m |\033[0m")
        rows.append("\033[1;30m+====================================================================================================+\033[0m")
        rows.append(f"  \033[1;33m[POSITION]:\033[0m X={player_x:2d}, Y={player_y:2d}   \033[1;36m[KEYS]:\033[0m {key_count}/3   \033[1;32m[EXPLORER]:\033[0m \033[1;37m{h_info:<27}\033[0m  \033[1;35m[TRAIT]:\033[0m \033[1;33m{solo_hero['trait'][:20]}\033[0m")
        rows.append(f"  \033[1;33m[DISCOVERY]:\033[0m [\033[1;32m{bar_str}\033[0m] \033[1;37m{pct:5.1f}%\033[0m ({exp_count:3d}/{TOTAL_TILES:3d}) | \033[1;36mSTEPS:\033[0m {step_count:<4d} | \033[1;31mFOES SLAIN:\033[0m {monsters_defeated}")
        rows.append("\033[1;30m+----------------------------------------------------------------------------------------------------+\033[0m")

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
            p_items = [
                f"[1] Poppy Flower x{inventory['poppy']} (+50 HP)",
                f"[2] Marijuana Herb x{inventory['weed']} (+120 HP)",
                f"[3] Moldy Bread x{inventory['bread']} (-40 Hunger)",
                f"[4] Vintage Ale x{inventory['ale']} (+35 Mind)",
                f"[C] Close Pouch"
            ]
            p_str = "  |  ".join(p_items)
            rows.append(f"  \033[1;35m[SURVIVAL POUCH]:\033[0m \033[1;37m{fit_ansi(p_str, 80)}\033[0m")
        else:
            rows.append(f"  \033[1;36m[LOG]:\033[0m \033[1;37m{fit_ansi(recent_log, 88)}\033[0m")

        rows.append("\033[1;30m+====================================================================================================+\033[0m")
        rows.append("  \033[90mLEGEND:\033[0m \033[42m  \033[0m Wall  \033[90m .\033[0m Path  \033[1;33m O\033[0m Hero  \033[41;1;37m #\033[0m Rock  \033[45;1;37m §\033[0m Seal  \033[43;1;30m =\033[0m Crevice  \033[48;2;139;69;19;1;37m C\033[0m Chest  \033[46;1;30m G\033[0m Gate")
        rows.append("  \033[90mCONTROLS:\033[0m \033[1;37m[W/A/S/D]\033[0m Move  |  \033[1;35m[I]\033[0m Pouch / Items  |  \033[1;32m[H]\033[0m Quick Heal  |  \033[1;31m[Q]\033[0m Quit")
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
                inventory["poppy"] += 1
                inventory["bread"] += 1
                recent_log = f"[CHEST]: Looted supplies at ({nx}, {ny}) (+1 Poppy Flower, +1 Moldy Bread)!"

        # Roaming Monster Encounter -> Launch Turn-based Combat Arena!
        elif base_tile == TILE_MONSTER and (nx, ny) not in cleared_tiles:
            m_data = MONSTER_ENCOUNTERS.get((nx, ny), {
                "id": 8, "name": "SHADOW SWORDSMAN", "archetype": "ARMORED",
                "hp": 95, "atk": 24, "def": 99, "drops_key": False
            })

            # Enter real Pokémon-style combat arena
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
    while True:
        render_map_view(pouch_open=in_pouch)

        if os.name == 'nt' and sys.stdin.isatty():
            ch = msvcrt.getch()
            while msvcrt.kbhit():
                msvcrt.getch()

            if in_pouch:
                if ch == b'1':
                    if inventory["poppy"] > 0:
                        inventory["poppy"] -= 1
                        heal = 65 if solo_hero["name"] == "CAHARA" else (30 if is_hardcore else 50)
                        solo_hero["hp"] = min(solo_hero["max_hp"], solo_hero["hp"] + heal)
                        recent_log = f"[POUCH]: Applied Poppy Flower (+{heal} HP). Current HP: {solo_hero['hp']}/{solo_hero['max_hp']}"
                    else:
                        recent_log = "[POUCH]: Out of Poppy Flowers!"
                    in_pouch = False
                elif ch == b'2':
                    if inventory["weed"] > 0:
                        inventory["weed"] -= 1
                        heal = 75 if is_hardcore else 120
                        solo_hero["hp"] = min(solo_hero["max_hp"], solo_hero["hp"] + heal)
                        recent_log = f"[POUCH]: Smoked Marijuana Herb (+{heal} HP). Current HP: {solo_hero['hp']}/{solo_hero['max_hp']}"
                    else:
                        recent_log = "[POUCH]: Out of Marijuana Herbs!"
                    in_pouch = False
                elif ch == b'3':
                    if inventory["bread"] > 0:
                        inventory["bread"] -= 1
                        solo_hero["hunger"] = max(0, solo_hero.get("hunger", 0) - 40)
                        recent_log = f"[POUCH]: Ate Moldy Bread. Hunger relieved (-40 Hunger)."
                    else:
                        recent_log = "[POUCH]: Out of Bread!"
                    in_pouch = False
                elif ch == b'4':
                    if inventory["ale"] > 0:
                        inventory["ale"] -= 1
                        solo_hero["mind"] = min(solo_hero["max_mind"], solo_hero.get("mind", 100) + 35)
                        recent_log = f"[POUCH]: Drank Vintage Ale (+35 Mind). Terror cleansed!"
                    else:
                        recent_log = "[POUCH]: Out of Ale!"
                    in_pouch = False
                elif ch in (b'c', b'C', b'i', b'I', b'\x1b'):
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
                sys.stdout.write("\033[?25h\n[OK] Labyrinth Expedition suspended.\n")
                break

            if res in ("VICTORY", "GAME_OVER", "QUIT"):
                break
        else:
            raw = sys.stdin.readline()
            if not raw:
                break
            line = raw.strip().lower()
            if line == 'w':
                res = handle_map_move(0, -1)
            elif line == 's':
                res = handle_map_move(0, 1)
            elif line == 'a':
                res = handle_map_move(-1, 0)
            elif line == 'd':
                res = handle_map_move(1, 0)
            elif line in ('i', 'pouch'):
                in_pouch = not in_pouch
            elif line == 'q':
                break
            if res in ("VICTORY", "GAME_OVER", "QUIT"):
                break

# =============================================================================
# END-GAME SCREENS: VICTORY & GAME OVER
# =============================================================================
def show_victory_screen(hero, steps, slain, chests, is_hardcore):
    rows = []
    rows.append(make_border_line("=", border_color="\033[1;33m"))
    rows.append("\033[1;33m|   ___      ___ ___  ________  _________  ________  ________      ___    ___                       |\033[0m")
    rows.append("\033[1;33m|  |\\  \\    /  /|\\  \\|\\   ____\\|\\___   ___\\\\   __  \\|\\   __  \\    |\\  \\  /  /|                      |\033[0m")
    rows.append("\033[1;33m|  \\ \\  \\  /  / | \\  \\ \\  \\___|\\|___ \\  \\_\\ \\  \\|\\  \\ \\  \\|\\  \\   \\ \\  \\/  / /                      |\033[0m")
    rows.append("\033[1;33m|   \\ \\  \\/  / / \\ \\  \\ \\  \\        \\ \\  \\ \\ \\  \\\\\\  \\ \\   _  _\\   \\ \\    / /                       |\033[0m")
    rows.append("\033[1;33m|    \\ \\    / /   \\ \\  \\ \\  \\____    \\ \\  \\ \\ \\  \\\\\\  \\ \\  \\\\  \\|   \\/  /  /                        |\033[0m")
    rows.append("\033[1;33m|     \\ \\__/ /     \\ \\__\\ \\_______\\   \\ \\__\\ \\ \\_______\\ \\__\\\\ _\\   __/  / /                         |\033[0m")
    rows.append("\033[1;33m|      \\|__|/       \\|__|\\|_______|    \\|__|  \\|_______|\\|__|\\|__| |\\___/ /                          |\033[0m")
    rows.append("\033[1;33m|                                                                  \\|___|/                           |\033[0m")
    rows.append(make_centered_box_row("\033[1;32m[ E S C A P E   A C H I E V E D   -   V I C T O R Y ]\033[0m", border_color="\033[1;33m"))
    rows.append(make_border_line("=", border_color="\033[1;33m"))
    rows.append(make_left_box_row("\033[1;32mALL 3 RUNIC KEYS INSERTED! THE MASSIVE RUNIC GATES GRIND OPEN AS GOLDEN SUNLIGHT FLOODS THE DARK!\033[0m", border_color="\033[1;33m"))
    rows.append(make_left_box_row(f"\033[1;37m{hero['name']} [{hero['role']}] has triumphed over subterranean dread and escaped alive!\033[0m", border_color="\033[1;33m"))
    rows.append(make_border_line("-", border_color="\033[1;33m"))
    mode_str = "TERROR & STARVATION (Hardcore Survivor)" if is_hardcore else "FEAR & HUNGER (Standard Survivor)"
    rows.append(f"  \033[1;33mEXPEDITION STATS:\033[0m")
    rows.append(f"    - Difficulty Conquered : \033[1;32m{mode_str}\033[0m")
    rows.append(f"    - Hero Standing        : \033[1;37m{hero['name']} ({hero['hp']}/{hero['max_hp']} HP, Mind: {hero['mind']}/100)\033[0m")
    rows.append(f"    - Total Steps Taken    : \033[1;36m{steps} steps\033[0m")
    rows.append(f"    - Foes Neutralized     : \033[1;31m{slain} monsters vanquished\033[0m")
    rows.append(f"    - Ancient Chests Looted: \033[1;33m{chests} vaults cleared\033[0m")
    rows.append("")
    rows.append("\033[1;30m" + "=" * 100 + "\033[0m")
    rows.append("  [CONTROLS]: Press [Enter] or [Q] to return to surface")
    rows.append("\033[1;30m" + "=" * 100 + "\033[0m")
    atomic_blit(rows)
    if os.name == 'nt' and sys.stdin.isatty():
        msvcrt.getch()
    else:
        sys.stdin.readline()

def show_game_over_screen(hero, killer):
    rows = []
    rows.append(make_border_line("=", border_color="\033[1;31m"))
    rows.append("\033[1;31m|   ________  ________  _____ ______   _______           ________  ___      ___ _______   ________   |\033[0m")
    rows.append("\033[1;31m|  |\\   ____\\|\\   __  \\|\\   _ \\  _   \\|\\  ___ \\         |\\   __  \\|\\  \\    /  /|\\  ___ \\ |\\   __  \\  |\033[0m")
    rows.append("\033[1;31m|  \\ \\  \\___|\\ \\  \\|\\  \\ \\  \\\\\\__\\ \\  \\ \\   __/|        \\ \\  \\|\\  \\ \\  \\  /  / | \\   __/|\\ \\  \\|\\  \\ |\033[0m")
    rows.append("\033[1;31m|   \\ \\  \\  __\\ \\   __  \\ \\  \\\\|__| \\  \\ \\  \\_|/__       \\ \\  \\\\\\  \\ \\  \\/  / / \\ \\  \\_|/_\\ \\   _  _\\|\033[0m")
    rows.append("\033[1;31m|    \\ \\  \\|\\  \\ \\  \\ \\  \\ \\  \\    \\ \\  \\ \\  \\_|\\ \\       \\ \\  \\\\\\  \\ \\    / /   \\ \\  \\_|\\ \\ \\  \\\\  \\||\033[0m")
    rows.append("\033[1;31m|     \\ \\_______\\ \\__\\ \\__\\ \\__\\    \\ \\__\\ \\_______\\       \\ \\_______\\ \\__/ /     \\ \\_______\\ \\__\\\\ _\\|\033[0m")
    rows.append("\033[1;31m|      \\|_______|\\|__|\\|__|\\|__|     \\|__|\\|_______|        \\|_______|\\|__|/       \\|_______|\\|__|\\|__|\033[0m")
    rows.append(make_border_line("=", border_color="\033[1;31m"))
    rows.append(make_left_box_row(f"\033[1;37m{hero['name']} HAS FALLEN TO {killer.upper()} IN THE DARK PERIMETER OF THE LABYRINTH.\033[0m", border_color="\033[1;31m"))
    rows.append(make_left_box_row("\033[90mYour flesh decays into subterranean ash... The forgotten gods claim another soul.\033[0m", border_color="\033[1;31m"))
    rows.append(make_border_line("=", border_color="\033[1;31m"))
    rows.append("")
    rows.append("\033[1;30m" + "=" * 100 + "\033[0m")
    rows.append("  [CONTROLS]: Press [Enter] or [Q] to exit")
    rows.append("\033[1;30m" + "=" * 100 + "\033[0m")
    atomic_blit(rows)
    if os.name == 'nt' and sys.stdin.isatty():
        msvcrt.getch()
    else:
        sys.stdin.readline()

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
