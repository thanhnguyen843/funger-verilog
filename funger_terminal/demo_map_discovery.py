#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
================================================================================
FEAR & HUNGER: TERMINAL LABYRINTH - PERSISTENT FOG OF WAR & MAP DISCOVERY ENGINE
================================================================================
Feature Specification:
1. Complete darkness on start: Only starting sanctuary (2, 2) is visible.
2. Progressive Exploration: As the player moves, a circular torch radius (r=4)
   permanently illuminates surrounding tiles into a 720-bit discovery mask.
3. Persistent Illumination: Explored tiles stay permanently revealed. As the player
   explores corridors and rooms, the entire 36x20 labyrinth becomes fully visible.
4. Active Torch vs Explored Memory:
   - Uncharted cells: Pitch black darkness ("  ").
   - Explored memory: Softly illuminated stone & paths.
   - Active torchlight: Vibrant illumination with active player icon 'O'.
5. Interactive Controls: [W/A/S/D] or Arrows, [F] Full Reveal, [R] Reset, [Q] Quit.
================================================================================
"""

import sys
import os
import time

# Enable Windows ANSI Virtual Terminal Support & UTF-8
if os.name == 'nt':
    try:
        import ctypes
        kernel32 = ctypes.windll.kernel32
        hOut = kernel32.GetStdHandle(-11)
        mode = ctypes.c_ulong()
        if kernel32.GetConsoleMode(hOut, ctypes.byref(mode)):
            kernel32.SetConsoleMode(hOut, mode.value | 0x0004)
        kernel32.SetConsoleOutputCP(65001)
        kernel32.SetConsoleCP(65001)
    except Exception:
        pass
    import msvcrt

# Map Grid Dimensions (Matches map_rom.v 100%)
MAP_WIDTH = 36
MAP_HEIGHT = 20
TOTAL_TILES = MAP_WIDTH * MAP_HEIGHT # 720

TILE_WALL    = 0
TILE_PATH    = 1
TILE_MONSTER = 2
TILE_CHEST   = 3
TILE_GATE    = 4

def get_base_tile(x, y):
    """Replicates map_rom.v hardware logic exactly."""
    # 1. Gates embedded on rightmost wall (x = 35)
    if (x == MAP_WIDTH - 1 and y == 6) or (x == MAP_WIDTH - 1 and y == 14):
        return TILE_GATE
    # 2. Outer boundary walls
    if x <= 0 or x >= MAP_WIDTH - 1 or y <= 0 or y >= MAP_HEIGHT - 1:
        return TILE_WALL
    # 3. Gatekeeper monsters in front of gates (x = 34)
    if (x == MAP_WIDTH - 2 and y == 6) or (x == MAP_WIDTH - 2 and y == 14):
        return TILE_MONSTER
    # 4. Funnel walls around gatekeepers
    if x == MAP_WIDTH - 2 and y in (5, 7, 13, 15):
        return TILE_WALL
    # 5. Starting sanctuary around (2, 2)
    if 1 <= x <= 4 and 1 <= y <= 3:
        return TILE_PATH
    # 6. Treasure chests
    if (x, y) in [(8,2), (22,3), (6,11), (18,11), (28,10), (12,17), (26,17)]:
        return TILE_CHEST
    # 7. Dungeon roaming monsters
    if (x, y) in [(14,2), (10,6), (20,7), (28,4), (14,11), (24,11), (8,15), (20,15)]:
        return TILE_MONSTER
    # 8. Internal maze wall dividers
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
    # 9. Open pathway
    return TILE_PATH

# Game State
player_x = 2
player_y = 2
step_count = 0
key_count = 0
explored_mask = [[False for _ in range(MAP_WIDTH)] for _ in range(MAP_HEIGHT)]
cleared_tiles = set()
full_vision_cheat = False
recent_log = "Game started in safe sanctuary (2, 2). Uncharted corridors await."
milestones_reached = set()

def reveal_around(px, py, radius=4):
    """Reveals tiles around player in circular torch radius."""
    newly_revealed = 0
    r_sq = radius * radius
    for dy in range(-radius, radius + 1):
        for dx in range(-radius, radius + 1):
            if dx * dx + dy * dy <= r_sq:
                tx = px + dx
                ty = py + dy
                if 0 <= tx < MAP_WIDTH and 0 <= ty < MAP_HEIGHT:
                    if not explored_mask[ty][tx]:
                        explored_mask[ty][tx] = True
                        newly_revealed += 1
    return newly_revealed

def count_explored():
    return sum(row.count(True) for row in explored_mask)

def render_screen():
    global recent_log
    sys.stdout.write("\033[2J\033[H")

    exp_count = count_explored()
    pct = (exp_count * 100.0) / TOTAL_TILES

    # Milestone checks
    if pct >= 100.0 and 100 not in milestones_reached:
        milestones_reached.add(100)
        recent_log = "[ACHIEVEMENT]: 100% OF LABYRINTH FULLY ILLUMINATED & CHARTED!"
    elif pct >= 75.0 and 75 not in milestones_reached:
        milestones_reached.add(75)
        recent_log = "[MILESTONE]: 75% of catacombs illuminated! The exit draws near!"
    elif pct >= 50.0 and 50 not in milestones_reached:
        milestones_reached.add(50)
        recent_log = "[MILESTONE]: 50% of the labyrinth uncovered! Major sectors linked!"
    elif pct >= 25.0 and 25 not in milestones_reached:
        milestones_reached.add(25)
        recent_log = "[MILESTONE]: 25% of subterranean maze charted!"

    # Progress bar (20 chars)
    bar_fill = int(pct / 5.0)
    bar_str = "█" * bar_fill + "░" * (20 - bar_fill)

    print("\033[1;30m+====================================================================================================+\033[0m")
    print("\033[1;30m| \033[1;37m     FEAR & HUNGER: TERMINAL LABYRINTH - PERSISTENT FOG OF WAR & MAP DISCOVERY DEMO            \033[1;30m|\033[0m")
    print("\033[1;30m+====================================================================================================+\033[0m")
    print(f"  \033[1;33m[POSITION]:\033[0m X={player_x:2d}, Y={player_y:2d}   \033[1;36m[STEPS]:\033[0m {step_count:<4d}   \033[1;35m[RUNIC KEYS]:\033[0m {key_count}/3   \033[1;32m[MODE]:\033[0m {'ALL ILLUMINATED (CHEAT)' if full_vision_cheat else 'DYNAMIC FOG OF WAR'}")
    print(f"  \033[1;33m[DISCOVERY]:\033[0m [\033[1;32m{bar_str}\033[0m] \033[1;37m{pct:5.1f}%\033[0m ({exp_count:3d}/{TOTAL_TILES:3d} Tiles Illuminated)")
    print("\033[1;30m+----------------------------------------------------------------------------------------------------+\033[0m")

    # Render Map Area (36 columns x 2 characters = 72 columns width)
    # Total width with left & right borders: 14 spaces + 72 + 14 = 100 columns exact!
    border_left_pad = "              " # 14 spaces
    torch_sq = 16 # Radius 4 squared

    for y in range(MAP_HEIGHT):
        row_str = ""
        for x in range(MAP_WIDTH):
            dist_sq = (x - player_x) ** 2 + (y - player_y) ** 2
            is_active_torch = (dist_sq <= torch_sq)
            is_visited = explored_mask[y][x] or full_vision_cheat

            if x == player_x and y == player_y:
                # Active player icon
                row_str += "\033[1;33;40m O\033[0m"
            elif not is_visited:
                # Uncharted Pitch Black Darkness
                row_str += "  "
            else:
                # Discovered Tile
                tile = get_base_tile(x, y)
                if (x, y) in cleared_tiles and tile in (TILE_MONSTER, TILE_CHEST):
                    tile = TILE_PATH

                if is_active_torch:
                    # In direct torchlight: Full vibrant colors
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
                else:
                    # Explored Memory: Softly illuminated memory
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

        print(f"{border_left_pad}{row_str}")

    print("\033[1;30m+----------------------------------------------------------------------------------------------------+\033[0m")
    print(f"  \033[1;36m[LOG]:\033[0m \033[1;37m{recent_log:<90}\033[0m")
    print("\033[1;30m+====================================================================================================+\033[0m")
    print("  \033[90mLEGEND:\033[0m \033[42m  \033[0m Wall  |  \033[90m .\033[0m Path  |  \033[1;33m O\033[0m Player  |  \033[45;1;37m M\033[0m Foe  |  \033[48;2;139;69;19;1;37m C\033[0m Chest  |  \033[46;1;30m G\033[0m Exit Gate")
    print("  \033[90mCONTROLS:\033[0m \033[1;37m[W/A/S/D]\033[0m or \033[1;37m[Arrows]\033[0m Move  |  \033[1;33m[F]\033[0m Toggle Flashlight  |  \033[1;31m[R]\033[0m Reset Fog  |  \033[1;31m[Q]\033[0m Quit")
    print("\033[1;30m====================================================================================================\033[0m")
    sys.stdout.flush()

def handle_move(dx, dy):
    global player_x, player_y, step_count, key_count, recent_log
    nx = player_x + dx
    ny = player_y + dy

    # Check boundaries
    if nx < 0 or nx >= MAP_WIDTH or ny < 0 or ny >= MAP_HEIGHT:
        recent_log = "[!] Impassable abyss! You cannot step beyond the outer perimeter."
        return

    tile = get_base_tile(nx, ny)

    # Wall collision
    if tile == TILE_WALL:
        recent_log = f"[!] Solid bedrock wall at ({nx}, {ny}) blocks your passage."
        return

    # Interact with chest
    if tile == TILE_CHEST and (nx, ny) not in cleared_tiles:
        cleared_tiles.add((nx, ny))
        key_count = min(3, key_count + 1)
        recent_log = f"[CHEST]: Opened ancient chest at ({nx}, {ny})! Obtained Runic Key ({key_count}/3)!"
    # Interact with monster
    elif tile == TILE_MONSTER and (nx, ny) not in cleared_tiles:
        cleared_tiles.add((nx, ny))
        recent_log = f"[COMBAT]: Roaming horror engaged at ({nx}, {ny})! Target defeated and neutralized."
    # Reach gate
    elif tile == TILE_GATE:
        if key_count >= 3:
            recent_log = "[VICTORY]: Runic Gate unlocked with 3 keys! You have escaped the subterranean labyrinth!"
        else:
            recent_log = f"[GATE]: The massive exit gate is locked. Requires 3 Runic Keys (You have {key_count}/3)."

    # Execute movement
    player_x = nx
    player_y = ny
    step_count += 1
    new_tiles = reveal_around(player_x, player_y, radius=4)
    if new_tiles > 0 and not recent_log.startswith("["):
        recent_log = f"[*] Advanced into corridor. +{new_tiles} tiles permanently illuminated."

def main():
    global full_vision_cheat, recent_log, player_x, player_y, step_count, key_count, cleared_tiles, explored_mask, milestones_reached
    # Initial reveal around start (2, 2)
    reveal_around(player_x, player_y, radius=4)

    while True:
        render_screen()
        if os.name == 'nt':
            ch = msvcrt.getch()
            if ch in (b'\x00', b'\xe0'):
                ext = msvcrt.getch()
                if ext == b'H':   # Up
                    handle_move(0, -1)
                elif ext == b'P': # Down
                    handle_move(0, 1)
                elif ext == b'K': # Left
                    handle_move(-1, 0)
                elif ext == b'M': # Right
                    handle_move(1, 0)
            elif ch in (b'w', b'W'):
                handle_move(0, -1)
            elif ch in (b's', b'S'):
                handle_move(0, 1)
            elif ch in (b'a', b'A'):
                handle_move(-1, 0)
            elif ch in (b'd', b'D'):
                handle_move(1, 0)
            elif ch in (b'f', b'F'):
                full_vision_cheat = not full_vision_cheat
                recent_log = f"[CHEAT]: Flashlight mode {'ENABLED (100% visible)' if full_vision_cheat else 'DISABLED (Fog restored)'}."
            elif ch in (b'r', b'R'):
                # Reset fog
                explored_mask = [[False for _ in range(MAP_WIDTH)] for _ in range(MAP_HEIGHT)]
                player_x = 2
                player_y = 2
                step_count = 0
                key_count = 0
                cleared_tiles = set()
                milestones_reached = set()
                reveal_around(player_x, player_y, radius=4)
                recent_log = "[RESET]: Map exploration reset. Labyrinth re-shrouded in darkness."
            elif ch in (b'q', b'Q', b'\x1b'):
                print("\n[OK] Map Exploration Demo session terminated.")
                break
        else:
            line = sys.stdin.readline().strip().lower()
            if line == 'q':
                break
            elif line == 'w': handle_move(0, -1)
            elif line == 's': handle_move(0, 1)
            elif line == 'a': handle_move(-1, 0)
            elif line == 'd': handle_move(1, 0)

if __name__ == "__main__":
    main()
