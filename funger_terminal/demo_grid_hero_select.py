#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
================================================================================
EXPANDED HIGH-FIDELITY HERO SELECTOR (FULL RESOLUTION 3-COLUMN PANORAMA & GRID)
Fear & Hunger: Terminal Labyrinth - Solo Explorer Architecture
================================================================================
Key Innovations:
  1. Wide 3-Column Panorama Mode (Default):
     - Displays 3 large, spacious cards across the 100-column screen (32 cols each).
     - Models are 100% UNCROPPED at native resolution: ALL 29 columns wide, ALL 12 rows tall!
     - Zero distortion, zero missing limbs or cut-off weapons.
     - Selector buttons, HP/ATK/DEF/DODGE stats, and Traits directly underneath each model.
     - Smooth carousel / page pagination across all 8 heroes ([A/D] or [Left/Right]).
     - Direct jump keys [1-8].
  2. 4x2 Grid Matrix Mode (Toggle via [TAB]):
     - Displays all 8 heroes at once for users who want simultaneous overview.
  3. Live Explorer Dossier & Solo Survival Assessment at bottom.
================================================================================
"""

import sys
import os
import re
import copy
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import demo_interactive_ui as dui
from hero_tri_state_catalog import HERO_TRI_STATES

if os.name == 'nt':
    import msvcrt

ANSI_RE = re.compile(r'\x1b\[[0-9;]*m')

def vis_len(s):
    return len(ANSI_RE.sub('', s))

def fit_exact(s, width):
    cur = vis_len(s)
    if cur > width:
        clean = ""
        idx = 0
        w = 0
        while idx < len(s) and w < width:
            if s[idx] == '\x1b':
                m = ANSI_RE.match(s[idx:])
                if m:
                    clean += m.group(0)
                    idx += len(m.group(0))
                    continue
            clean += s[idx]
            w += 1
            idx += 1
        return clean + "\033[0m" + " " * (width - w)
    return s + " " * (width - cur)

def render_wide_3card_screen(sel_idx):
    """Renders 3-Column Spacious Panorama Screen with 100% full-resolution uncropped models (28 rows, 100 cols)."""
    heroes = dui.ALL_HEROES
    active_h = heroes[sel_idx]

    page_idx = sel_idx // 3
    start_hero = page_idx * 3
    page_heroes = [heroes[start_hero + i] if start_hero + i < len(heroes) else None for i in range(3)]

    lines = []
    lines.append("\033[1;30m+" + "=" * 98 + "+\033[0m")
    t_str = "FEAR & HUNGER: SOLO SURVIVOR EXPEDITION - WIDE EXPLORER SELECTOR"
    sub_t = f"[TRANG {page_idx+1}/3  |  TAB: ĐỔI MA TRẬN 4x2]"
    hdr_line = f" \033[1;37m{t_str:<62}\033[1;33m{sub_t:>33} "
    lines.append(f"\033[1;30m|{fit_exact(hdr_line, 98)}\033[1;30m|\033[0m")

    # 3 Column Divider: 32 + 32 + 32 = 96 + 4 borders = 100
    div_3 = "\033[1;30m+" + "-" * 32 + "+" + "-" * 32 + "+" + "-" * 32 + "+\033[0m"
    lines.append(div_3)

    # 3 Selection Badges directly at top of card
    h_tags = []
    for c in range(3):
        h = page_heroes[c]
        if h:
            h_real_idx = heroes.index(h)
            is_cur = (h_real_idx == sel_idx)
            tag = f"[{h['id']}] {h['name']} ({h['role'].split()[0]})"
            txt = f"\033[1;32m▶ {tag:<28}\033[0m" if is_cur else f"\033[90m  {tag:<28}\033[0m"
        else:
            txt = "  \033[90m-- Ô TRỐNG --\033[0m"
        h_tags.append(fit_exact(txt, 32))
    lines.append(f"\033[1;30m|{h_tags[0]}|{h_tags[1]}|{h_tags[2]}|\033[0m")
    lines.append(div_3)

    # 12 SPRITE ROWS - 100% NATIVE UNCROPPED RESOLUTION (29 columns wide, all 12 rows!)
    for r in range(12):
        cells = []
        for c in range(3):
            h = page_heroes[c]
            if h:
                spr = HERO_TRI_STATES[h["name"]]["normal"]
                sp_row = spr[r] if r < len(spr) else " " * 29
                # 1 space padding + 29 chars uncropped sprite + 2 spaces padding = 32 columns
                row_fmt = " " + sp_row + "  "
            else:
                row_fmt = " " * 32
            cells.append(fit_exact(row_fmt, 32))
        lines.append(f"\033[1;30m|{cells[0]}|{cells[1]}|{cells[2]}|\033[0m")

    lines.append(div_3)

    # Combat Stats Under Each Model
    stat_cells = []
    for c in range(3):
        h = page_heroes[c]
        if h:
            s_str = f" \033[1;32mHP:{h['hp']:3d}\033[0m | \033[1;31mATK:{h['atk']:2d}\033[0m | \033[1;36mDEF:{h['def']:2d}\033[0m | \033[1;35mDOD:{int(h['dodge_rate']*100)}%\033[0m"
        else:
            s_str = ""
        stat_cells.append(fit_exact(s_str, 32))
    lines.append(f"\033[1;30m|{stat_cells[0]}|{stat_cells[1]}|{stat_cells[2]}|\033[0m")

    # Traits Under Each Model
    trait_cells = []
    for c in range(3):
        h = page_heroes[c]
        if h:
            t_str = f" \033[1;33mTRAIT:\033[0m {h['trait'][:24]}"
        else:
            t_str = ""
        trait_cells.append(fit_exact(t_str, 32))
    lines.append(f"\033[1;30m|{trait_cells[0]}|{trait_cells[1]}|{trait_cells[2]}|\033[0m")

    div_wide = "\033[1;30m+" + "=" * 98 + "+\033[0m"
    lines.append(div_wide)

    # LIVE EXPLORER DOSSIER & EVALUATION (5 rows)
    s_h = active_h
    d1 = f" \033[1;33mEXPLORER:\033[1;37m {s_h['name']:<12} \033[1;30m[{s_h['role']}]\033[0m  |  \033[1;32mHP: {s_h['hp']:3d}/{s_h['max_hp']:3d}\033[0m  |  \033[1;31mATK: {s_h['atk']:2d}\033[0m  |  \033[1;36mDEF: {s_h['def']:2d}\033[0m  |  \033[1;35mDODGE: {int(s_h['dodge_rate']*100)}%\033[0m"
    lines.append(f"\033[1;30m|{fit_exact(d1, 98)}\033[1;30m|\033[0m")

    d2 = f" \033[1;37mTRAIT   :\033[0m {s_h['trait']:<26}  |  \033[1;32mBUFF: {s_h['item_buff_str']:<22}\033[0m  |  \033[1;36mRESIST: {s_h['phys_resist_str'][:18]}\033[0m"
    lines.append(f"\033[1;30m|{fit_exact(d2, 98)}\033[1;30m|\033[0m")

    d3 = f" \033[1;36mSKILLS  :\033[0m \033[1;37m[1] {s_h['skills'][0]['label']:<26}\033[0m  \033[1;37m[2] {s_h['skills'][1]['label']:<26}\033[0m"
    lines.append(f"\033[1;30m|{fit_exact(d3, 98)}\033[1;30m|\033[0m")

    assess = " ".join(s_h["assessment"][:2])
    d4 = f" \033[1;33mASSESS  :\033[0;37m {assess[:88]}"
    lines.append(f"\033[1;30m|{fit_exact(d4, 98)}\033[1;30m|\033[0m")

    # Controls footer (3 rows)
    lines.append("\033[1;30m+" + "-" * 98 + "+\033[0m")
    p_info = f"Trang {page_idx+1}/3"
    ctrls = f" \033[90m[ĐIỀU KHIỂN]:\033[0m \033[1;37m[A/D / Mũi tên Trái/Phải]\033[0m Đổi Hero ({p_info})  |  \033[1;33m[1-8]\033[0m Nhảy số  |  \033[1;32m[Enter]\033[0m Chọn  |  \033[1;31m[Q]\033[0m Thoát"
    lines.append(f"\033[1;30m|{fit_exact(ctrls, 98)}\033[1;30m|\033[0m")
    lines.append(div_wide)
    return lines

def parse_line(line, target_width=29):
    cells = []
    fg, bg = None, None
    i = 0
    while i < len(line):
        if line[i] == '\x1b':
            m = re.match(r'\x1b\[([0-9;]*)m', line[i:])
            if m:
                code = m.group(1)
                i += len(m.group(0))
                if code in ('0', ''):
                    fg, bg = None, None
                elif code.startswith('38;2;'):
                    fg = code
                elif code.startswith('48;2;'):
                    bg = code
                elif code == '39':
                    fg = None
                elif code == '49':
                    bg = None
                continue
        cells.append((line[i], fg, bg))
        i += 1
    while len(cells) < target_width:
        cells.append((' ', None, None))
    return cells[:target_width]

def serialize_line(cells):
    res = []
    last_fg, last_bg = None, None
    for ch, fg, bg in cells:
        if fg != last_fg or bg != last_bg:
            code = ''
            if fg is None and bg is None:
                code = '\x1b[0m'
            else:
                if fg != last_fg:
                    code += f'\x1b[{fg}m' if fg else '\x1b[39m'
                if bg != last_bg:
                    code += f'\x1b[{bg}m' if bg else '\x1b[49m'
            res.append(code)
            last_fg, last_bg = fg, bg
        res.append(ch)
    res.append('\x1b[0m')
    return ''.join(res)

def crop_center_sprite(sprite_rows, target_w=23, row_start=1, row_end=10):
    out = []
    for r_idx in range(row_start, row_end):
        if r_idx < len(sprite_rows):
            cells = parse_line(sprite_rows[r_idx])
            non_empty = [i for i, c in enumerate(cells) if c[0] not in (' ', '\t')]
            if non_empty:
                min_i, max_i = min(non_empty), max(non_empty)
                content_w = max_i - min_i + 1
                if content_w <= target_w:
                    pad_left = max(0, (target_w - content_w) // 2)
                    c_cells = [(' ', None, None)] * pad_left + cells[min_i:max_i+1]
                    while len(c_cells) < target_w:
                        c_cells.append((' ', None, None))
                    out.append(serialize_line(c_cells[:target_w]))
                    continue
            out.append(serialize_line(cells[:target_w]))
        else:
            out.append(" " * target_w)
    return out

def render_grid_4x2_screen(sel_idx):
    """Renders 4x2 Grid Screen overview (32 rows, 100 cols)."""
    heroes = dui.ALL_HEROES
    active_h = heroes[sel_idx]
    widths = [23, 24, 24, 24]
    
    lines = []
    lines.append("\033[1;30m+" + "=" * 98 + "+\033[0m")
    t_str = "FEAR & HUNGER: SOLO SURVIVOR EXPEDITION - 2D GRID SELECTOR"
    sub_t = "[DÀN HÀNG 4x2 | TAB: ĐỔI DÀN HÀNG 3-3]"
    hdr_line = f" \033[1;37m{t_str:<62}\033[1;33m{sub_t:>33} "
    lines.append(f"\033[1;30m|{fit_exact(hdr_line, 98)}\033[1;30m|\033[0m")

    div_grid = "\033[1;30m+" + "-" * 23 + "+" + "-" * 24 + "+" + "-" * 24 + "+" + "-" * 24 + "+\033[0m"
    lines.append(div_grid)

    r1_sprites = [crop_center_sprite(HERO_TRI_STATES[heroes[i]["name"]]["normal"], widths[i], 1, 10) for i in range(4)]
    for r in range(9):
        cells = [fit_exact(r1_sprites[c][r], widths[c]) for c in range(4)]
        lines.append(f"\033[1;30m|{cells[0]}|{cells[1]}|{cells[2]}|{cells[3]}|\033[0m")

    b_cells = []
    for c in range(4):
        is_cur = (c == sel_idx)
        h = heroes[c]
        tag = f"[{h['id']}] {h['name']}"
        txt = f"\033[1;32m▶ {tag:<19}\033[0m" if is_cur else f"\033[90m  {tag:<19}\033[0m"
        b_cells.append(fit_exact(txt, widths[c]))
    lines.append(f"\033[1;30m|{b_cells[0]}|{b_cells[1]}|{b_cells[2]}|{b_cells[3]}|\033[0m")
    lines.append(div_grid)

    r2_sprites = [crop_center_sprite(HERO_TRI_STATES[heroes[4+i]["name"]]["normal"], widths[i], 1, 10) for i in range(4)]
    for r in range(9):
        cells = [fit_exact(r2_sprites[c][r], widths[c]) for c in range(4)]
        lines.append(f"\033[1;30m|{cells[0]}|{cells[1]}|{cells[2]}|{cells[3]}|\033[0m")

    b2_cells = []
    for c in range(4):
        is_cur = (4 + c == sel_idx)
        h = heroes[4 + c]
        tag = f"[{h['id']}] {h['name']}"
        txt = f"\033[1;32m▶ {tag:<19}\033[0m" if is_cur else f"\033[90m  {tag:<19}\033[0m"
        b2_cells.append(fit_exact(txt, widths[c]))
    lines.append(f"\033[1;30m|{b2_cells[0]}|{b2_cells[1]}|{b2_cells[2]}|{b2_cells[3]}|\033[0m")

    div_wide = "\033[1;30m+" + "=" * 98 + "+\033[0m"
    lines.append(div_wide)

    s_h = active_h
    d_row1 = f" \033[1;33mEXPLORER:\033[1;37m {s_h['name']:<12} \033[1;30m[{s_h['role']}]\033[0m  |  \033[1;32mHP: {s_h['hp']:3d}/{s_h['max_hp']:3d}\033[0m  |  \033[1;31mATK: {s_h['atk']:2d}\033[0m  |  \033[1;36mDEF: {s_h['def']:2d}\033[0m  |  \033[1;35mDODGE: {int(s_h['dodge_rate']*100)}%\033[0m"
    lines.append(f"\033[1;30m|{fit_exact(d_row1, 98)}\033[1;30m|\033[0m")

    d_row2 = f" \033[1;37mTRAIT  :\033[0m {s_h['trait']:<26}  |  \033[1;32mBUFF: {s_h['item_buff_str']:<22}\033[0m  |  \033[1;36mRESIST: {s_h['phys_resist_str'][:16]}\033[0m"
    lines.append(f"\033[1;30m|{fit_exact(d_row2, 98)}\033[1;30m|\033[0m")

    d_row3 = f" \033[1;36mSKILLS :\033[0m \033[1;37m[1] {s_h['skills'][0]['label']:<24}\033[0m  \033[1;37m[2] {s_h['skills'][1]['label']:<24}\033[0m"
    lines.append(f"\033[1;30m|{fit_exact(d_row3, 98)}\033[1;30m|\033[0m")

    assess_text = " ".join(s_h["assessment"][:2])
    d_row4 = f" \033[1;33mASSESS :\033[0;37m {assess_text[:88]}"
    lines.append(f"\033[1;30m|{fit_exact(d_row4, 98)}\033[1;30m|\033[0m")

    lines.append("\033[1;30m+" + "-" * 98 + "+\033[0m")
    ctrls = " \033[90m[ĐIỀU KHIỂN]:\033[0m \033[1;37m[W/A/S/D / Mũi tên]\033[0m Ô chọn  |  \033[1;33m[TAB]\033[0m Đổi Dàn 3 Cột  |  \033[1;32m[Enter]\033[0m Bắt đầu  |  \033[1;31m[Q]\033[0m Thoát"
    lines.append(f"\033[1;30m|{fit_exact(ctrls, 98)}\033[1;30m|\033[0m")
    lines.append(div_wide)
    return lines

def run_grid_select_interactive(initial_sel=0):
    dui.clear_screen()
    sel_idx = initial_sel
    mode = "wide_3card" # Default to WIDE 3-CARD PANORAMA to ensure 100% full uncropped sprites
    num_heroes = len(dui.ALL_HEROES)

    while True:
        if mode == "wide_3card":
            frame = render_wide_3card_screen(sel_idx)
        else:
            frame = render_grid_4x2_screen(sel_idx)

        dui.atomic_blit(frame)

        if not (os.name == 'nt' and sys.stdin.isatty()):
            return dui.ALL_HEROES[sel_idx], sel_idx

        ch = msvcrt.getch()
        while msvcrt.kbhit():
            msvcrt.getch()

        if ch in (b'\x00', b'\xe0'):
            ext = msvcrt.getch()
            if mode == "wide_3card":
                if ext in (b'K', b'H'): # Left or Up
                    sel_idx = (sel_idx - 1) % num_heroes
                elif ext in (b'M', b'P'): # Right or Down
                    sel_idx = (sel_idx + 1) % num_heroes
            else:
                cur_r = sel_idx // 4
                cur_c = sel_idx % 4
                if ext == b'H': cur_r = (cur_r - 1) % 2
                elif ext == b'P': cur_r = (cur_r + 1) % 2
                elif ext == b'K': cur_c = (cur_c - 1) % 4
                elif ext == b'M': cur_c = (cur_c + 1) % 4
                sel_idx = cur_r * 4 + cur_c

        elif ch in (b'\t',):
            mode = "grid" if mode == "wide_3card" else "wide_3card"

        elif mode == "wide_3card":
            if ch in (b'a', b'A', b'w', b'W'):
                sel_idx = (sel_idx - 1) % num_heroes
            elif ch in (b'd', b'D', b's', b'S'):
                sel_idx = (sel_idx + 1) % num_heroes
            elif ch in (b'1', b'2', b'3', b'4', b'5', b'6', b'7', b'8'):
                sel_idx = int(ch.decode('ascii')) - 1
            elif ch in (b'\r', b'\n', b' '):
                return dui.ALL_HEROES[sel_idx], sel_idx
            elif ch in (b'q', b'Q', b'\x1b'):
                return None, None

        else: # grid
            cur_r = sel_idx // 4
            cur_c = sel_idx % 4
            if ch in (b'w', b'W'):
                cur_r = (cur_r - 1) % 2
                sel_idx = cur_r * 4 + cur_c
            elif ch in (b's', b'S'):
                cur_r = (cur_r + 1) % 2
                sel_idx = cur_r * 4 + cur_c
            elif ch in (b'a', b'A'):
                cur_c = (cur_c - 1) % 4
                sel_idx = cur_r * 4 + cur_c
            elif ch in (b'd', b'D'):
                cur_c = (cur_c + 1) % 4
                sel_idx = cur_r * 4 + cur_c
            elif ch in (b'1', b'2', b'3', b'4', b'5', b'6', b'7', b'8'):
                sel_idx = int(ch.decode('ascii')) - 1
            elif ch in (b'\r', b'\n', b' '):
                return dui.ALL_HEROES[sel_idx], sel_idx
            elif ch in (b'q', b'Q', b'\x1b'):
                return None, None

def main():
    hero, idx = run_grid_select_interactive()
    if hero is None:
        dui.clear_screen()
        print("\033[1;31m[THOÁT]: Bạn đã hủy chọn nhân vật.\033[0m")
        return

    dui.clear_screen()
    print("\033[1;30m+" + "=" * 98 + "+\033[0m")
    title = f" [XÁC NHẬN CHỌN EXPLORER]: {hero['name']} [{hero['role']}]"
    print(f"\033[1;30m| \033[1;32m{fit_exact(title, 96)}\033[1;30m |\033[0m")
    print("\033[1;30m+" + "=" * 98 + "+\033[0m")
    print(f"\n  Bạn đã chọn: \033[1;33m{hero['name']}\033[0m ({hero['role']})")
    print(f"  HP: {hero['hp']}/{hero['max_hp']}  |  ATK: {hero['atk']}  |  DEF: {hero['def']}  |  TRAIT: {hero['trait']}")
    print(f"  Đặc tính: {hero['item_buff_str']}")
    print(f"  Kỹ năng : [1] {hero['skills'][0]['label']}  |  [2] {hero['skills'][1]['label']}")
    print("\n\033[1;30m+" + "-" * 98 + "+\033[0m")
    print("  \033[1;37m[1]\033[0m Khởi động chơi game thám hiểm Labyrinth ngay với Hero này")
    print("  \033[1;37m[2]\033[0m Thử nghiệm lại bộ chọn nhân vật (Grid / Panorama)")
    print("  \033[1;37m[Q]\033[0m Thoát ra ngoài")
    print("\033[1;30m+" + "=" * 98 + "+\033[0m")

    if os.name == 'nt' and sys.stdin.isatty():
        choice = input("\nLựa chọn của bạn [1/2/Q]: ").strip().lower()
        if choice == '1':
            dui.clear_screen()
            os.system(f"python funger_terminal/master_game.py")
        elif choice == '2':
            main()
        else:
            print("[OK] Đã thoát bộ chọn nhân vật.")

if __name__ == "__main__":
    main()
