#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
================================================================================
EXPANDED HIGH-FIDELITY HERO SELECTOR: 3 SELECTABLE LAYOUT ENGINES
Fear & Hunger: Terminal Labyrinth - Solo Explorer Architecture
================================================================================
Includes 3 distinct layout paradigms switchable in real-time with [TAB]:
  1. Mode 1: [MA TRẬN 4 Ô TO RỘNG 2x2]
     - 4 heroes per screen in spacious 48/49-column cards (2 pages).
     - Full 100% native uncropped models (29 columns wide, 10-12 rows tall).
     - Clean side-by-side combat stats & traits. Zero distortion!
  2. Mode 2: [BẢN DỌC TRUYỀN THỐNG 1 Ô LỚN]
     - Left pane: 30-column vertical roster list with glowing cursor.
     - Right pane: 67-column grand hero stage with full model, stats & lore.
  3. Mode 3: [BẢN DÀN HÀNG 3 CỘT KHỔ LỚN (PANORAMA)]
     - 3 wide 32-column cards across 100 columns (3 pages).
     - Full 29-column uncropped sprites with dedicated multi-line stats rows.
     - Zero text cramming or truncated lines.
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

HEROES = dui.ALL_HEROES

# -----------------------------------------------------------------------------
# LAYOUT 1: MA TRẬN 4 Ô LỚN (2x2 Quad Grid, 48 cols per card, Big Uncropped Models)
# -----------------------------------------------------------------------------
def render_quad_grid(sel_idx):
    page = sel_idx // 4
    start = page * 4
    quad_heroes = [HEROES[start + i] if start + i < len(HEROES) else None for i in range(4)]
    active_h = HEROES[sel_idx]

    w_left, w_right = 48, 49
    lines = []
    lines.append("\033[1;30m+" + "=" * 98 + "+\033[0m")
    title = f"FEAR & HUNGER: HERO SELECTOR - [BẢN 1: MA TRẬN 4 Ô TO RỘNG 2x2]  (TRANG {page+1}/2)"
    tab_hint = "[TAB: ĐỔI 3 GIAO DIỆN]"
    hdr = f" \033[1;37m{title:<74}\033[1;33m{tab_hint:>21} "
    lines.append(f"\033[1;30m|{fit_exact(hdr, 98)}\033[1;30m|\033[0m")

    div_2 = "\033[1;30m+" + "-" * w_left + "+" + "-" * w_right + "+\033[0m"
    lines.append(div_2)

    def make_badge(h, is_cur, w):
        if not h: return " " * w
        tag = f"[{h['id']}] {h['name']} ({h['role']})"
        return f"\033[1;32m▶ {tag}\033[0m" if is_cur else f"\033[90m  {tag}\033[0m"

    h_tl, h_tr = quad_heroes[0], quad_heroes[1]
    b_tl = fit_exact(" " + make_badge(h_tl, HEROES.index(h_tl) == sel_idx if h_tl else False, w_left - 1), w_left)
    b_tr = fit_exact(" " + make_badge(h_tr, HEROES.index(h_tr) == sel_idx if h_tr else False, w_right - 1), w_right)
    lines.append(f"\033[1;30m|{b_tl}\033[1;30m|{b_tr}\033[1;30m|\033[0m")
    lines.append(div_2)

    def get_side_stats(h):
        if not h: return [""] * 10
        return [
            f"\033[1;32mHP : {h['hp']:3d}/{h['max_hp']:3d}\033[0m",
            f"\033[1;31mATK: {h['atk']:2d}\033[0m",
            f"\033[1;36mDEF: {h['def']:2d}\033[0m",
            f"\033[1;35mDOD: {int(h['dodge_rate']*100)}%\033[0m",
            "",
            f"\033[1;33mĐẶC TÍNH:\033[0m",
            f"\033[0;37m{h['trait'][:16]}\033[0m",
            "",
            f"\033[1;36mKỸ NĂNG:\033[0m",
            f"\033[0;37m{h['skills'][0]['label'][:16]}\033[0m"
        ]

    st_tl, st_tr = get_side_stats(h_tl), get_side_stats(h_tr)
    spr_tl = HERO_TRI_STATES[h_tl["name"]]["normal"] if h_tl else [" " * 29] * 12
    spr_tr = HERO_TRI_STATES[h_tr["name"]]["normal"] if h_tr else [" " * 29] * 12

    for r in range(10):
        sp_l = spr_tl[r+1] if r+1 < len(spr_tl) else " " * 29
        st_l = st_tl[r] if r < len(st_tl) else ""
        c_l = fit_exact(" " + sp_l + " " + st_l, w_left)

        sp_r = spr_tr[r+1] if r+1 < len(spr_tr) else " " * 29
        st_r = st_tr[r] if r < len(st_tr) else ""
        c_r = fit_exact(" " + sp_r + " " + st_r, w_right)
        lines.append(f"\033[1;30m|{c_l}\033[1;30m|{c_r}\033[1;30m|\033[0m")

    lines.append(div_2)

    h_bl, h_br = quad_heroes[2], quad_heroes[3]
    b_bl = fit_exact(" " + make_badge(h_bl, HEROES.index(h_bl) == sel_idx if h_bl else False, w_left - 1), w_left)
    b_br = fit_exact(" " + make_badge(h_br, HEROES.index(h_br) == sel_idx if h_br else False, w_right - 1), w_right)
    lines.append(f"\033[1;30m|{b_bl}\033[1;30m|{b_br}\033[1;30m|\033[0m")
    lines.append(div_2)

    st_bl, st_br = get_side_stats(h_bl), get_side_stats(h_br)
    spr_bl = HERO_TRI_STATES[h_bl["name"]]["normal"] if h_bl else [" " * 29] * 12
    spr_br = HERO_TRI_STATES[h_br["name"]]["normal"] if h_br else [" " * 29] * 12

    for r in range(10):
        sp_l = spr_bl[r+1] if r+1 < len(spr_bl) else " " * 29
        st_l = st_bl[r] if r < len(st_bl) else ""
        c_l = fit_exact(" " + sp_l + " " + st_l, w_left)

        sp_r = spr_br[r+1] if r+1 < len(spr_br) else " " * 29
        st_r = st_br[r] if r < len(st_br) else ""
        c_r = fit_exact(" " + sp_r + " " + st_r, w_right)
        lines.append(f"\033[1;30m|{c_l}\033[1;30m|{c_r}\033[1;30m|\033[0m")

    div_wide = "\033[1;30m+" + "=" * 98 + "+\033[0m"
    lines.append(div_wide)

    d1 = f" \033[1;33mCHỌN:\033[1;37m {active_h['name']} [{active_h['role']}]\033[0m | \033[1;32mBUFF: {active_h['item_buff_str'][:26]}\033[0m | \033[1;36mSKILL: {active_h['skills'][0]['label']}\033[0m"
    lines.append(f"\033[1;30m|{fit_exact(d1, 98)}\033[1;30m|\033[0m")

    assess = " ".join(active_h["assessment"][:2])
    d2 = f" \033[1;33mĐÁNH GIÁ:\033[0;37m {assess[:86]}"
    lines.append(f"\033[1;30m|{fit_exact(d2, 98)}\033[1;30m|\033[0m")

    lines.append("\033[1;30m+" + "-" * 98 + "+\033[0m")
    ctrls = " \033[90m[ĐIỀU KHIỂN]:\033[0m \033[1;37m[W/A/S/D / Mũi tên]\033[0m Ô chọn  |  \033[1;33m[1-8]\033[0m Nhảy số  |  \033[1;33m[TAB]\033[0m Đổi Giao diện  |  \033[1;32m[Enter]\033[0m Chọn  |  \033[1;31m[Q]\033[0m Thoát"
    lines.append(f"\033[1;30m|{fit_exact(ctrls, 98)}\033[1;30m|\033[0m")
    lines.append(div_wide)
    return lines

# -----------------------------------------------------------------------------
# LAYOUT 2: BẢN DỌC TRUYỀN THỐNG 1 Ô DUY NHẤT (Vertical List + Big Hero Stage)
# -----------------------------------------------------------------------------
def render_vertical_split(sel_idx):
    active_h = HEROES[sel_idx]
    spr = HERO_TRI_STATES[active_h["name"]]["normal"]

    lines = []
    lines.append("\033[1;30m+" + "=" * 98 + "+\033[0m")
    title = f"FEAR & HUNGER: HERO SELECTOR - [BẢN 2: DỌC TRUYỀN THỐNG 1 Ô LỚN]"
    tab_hint = "[TAB: ĐỔI 3 GIAO DIỆN]"
    hdr = f" \033[1;37m{title:<74}\033[1;33m{tab_hint:>21} "
    lines.append(f"\033[1;30m|{fit_exact(hdr, 98)}\033[1;30m|\033[0m")

    div_split = "\033[1;30m+" + "-" * 30 + "+" + "-" * 67 + "+\033[0m"
    lines.append(div_split)

    # Left: 18 rows of vertical hero list + controls
    left_rows = [
        "\033[1;33m DANH SÁCH HERO [W/S]:\033[0m",
        ""
    ]
    for idx, h in enumerate(HEROES):
        is_cur = (idx == sel_idx)
        tag = f"[{h['id']}] {h['name']:<10} ({h['role'].split()[0]})"
        if is_cur:
            left_rows.append(f"\033[1;32m ▶ {tag}\033[0m")
        else:
            left_rows.append(f"\033[90m   {tag}\033[0m")
    left_rows.extend([
        "",
        "\033[1;33m [ĐIỀU KHIỂN]:\033[0m",
        "\033[1;37m [W/S]\033[0m   : Đổi Hero",
        "\033[1;33m [1-8]\033[0m   : Nhảy số Hero",
        "\033[1;33m [TAB]\033[0m   : Đổi Giao diện",
        "\033[1;32m [Enter]\033[0m : Chọn Hero",
        "\033[1;31m [Q]\033[0m     : Thoát",
        ""
    ])

    # Right: 12 rows of sprite (29 cols) + stats (34 cols) = 63 cols
    right_rows = []
    right_stats = [
        f"\033[1;33mTÊN    :\033[1;37m {active_h['name']}\033[0m",
        f"\033[1;33mVAI TRÒ:\033[1;37m {active_h['role']}\033[0m",
        f"\033[1;32mSINH MỆNH : {active_h['hp']:3d} / {active_h['max_hp']:3d}\033[0m",
        f"\033[1;31mSỨC TẤN CÔNG : {active_h['atk']:2d} DMG\033[0m",
        f"\033[1;36mPHÒNG NGỰ   : {active_h['def']:2d}\033[0m",
        f"\033[1;35mNÉ TRÁNH    : {int(active_h['dodge_rate']*100)}% Evasion\033[0m",
        f"\033[1;37mKHÁNG VẬT LÝ: {active_h['phys_resist_str'][:18]}\033[0m",
        f"\033[1;37mKHÁNG PHÉP  : {active_h['magic_resist_str'][:18]}\033[0m",
        f"\033[1;33mĐẶC TÍNH    : {active_h['trait'][:18]}\033[0m",
        f"\033[1;32mCƯỜNG HÓA   : {active_h['item_buff_str'][:18]}\033[0m",
        f"\033[1;36mKỸ NĂNG 1   : {active_h['skills'][0]['label'][:18]}\033[0m",
        f"\033[1;36mKỸ NĂNG 2   : {active_h['skills'][1]['label'][:18]}\033[0m"
    ]

    for r in range(12):
        sp = spr[r] if r < len(spr) else " " * 29
        st = right_stats[r] if r < len(right_stats) else ""
        right_rows.append(f"  {sp}  {fit_exact(st, 32)}")

    right_rows.append("\033[1;30m" + "-" * 67 + "\033[0m")
    right_rows.append(" \033[1;33m[ĐÁNH GIÁ KHẢ NĂNG SINH TỒN SOLO]:\033[0m")
    for a in active_h["assessment"][:3]:
        right_rows.append(f"  \033[0;37m{a[:63]}\033[0m")

    max_sub = max(len(left_rows), len(right_rows))
    for i in range(max_sub):
        l_txt = left_rows[i] if i < len(left_rows) else ""
        r_txt = right_rows[i] if i < len(right_rows) else ""
        lines.append(f"\033[1;30m|{fit_exact(l_txt, 30)}\033[1;30m|{fit_exact(r_txt, 67)}\033[1;30m|\033[0m")

    div_wide = "\033[1;30m+" + "=" * 98 + "+\033[0m"
    lines.append(div_wide)
    return lines

# -----------------------------------------------------------------------------
# LAYOUT 3: BẢN DÀN HÀNG 3 CỘT KHỔ LỚN (3-Column Panorama, Spacious Stats)
# -----------------------------------------------------------------------------
def render_panorama_3col(sel_idx):
    page = sel_idx // 3
    start = page * 3
    page_heroes = [HEROES[start + i] if start + i < len(HEROES) else None for i in range(3)]
    active_h = HEROES[sel_idx]

    lines = []
    lines.append("\033[1;30m+" + "=" * 98 + "+\033[0m")
    title = f"FEAR & HUNGER: HERO SELECTOR - [BẢN 3: DÀN HÀNG 3 CỘT KHỔ LỚN]  (TRANG {page+1}/3)"
    tab_hint = "[TAB: ĐỔI 3 GIAO DIỆN]"
    hdr = f" \033[1;37m{title:<74}\033[1;33m{tab_hint:>21} "
    lines.append(f"\033[1;30m|{fit_exact(hdr, 98)}\033[1;30m|\033[0m")

    div_3 = "\033[1;30m+" + "-" * 32 + "+" + "-" * 32 + "+" + "-" * 32 + "+\033[0m"
    lines.append(div_3)

    # Badges row
    h_tags = []
    for c in range(3):
        h = page_heroes[c]
        if h:
            h_real = HEROES.index(h)
            is_cur = (h_real == sel_idx)
            tag = f"[{h['id']}] {h['name']} ({h['role'].split()[0]})"
            txt = f"\033[1;32m▶ {tag:<28}\033[0m" if is_cur else f"\033[90m  {tag:<28}\033[0m"
        else:
            txt = "  \033[90m-- TRỐNG --\033[0m"
        h_tags.append(fit_exact(txt, 32))
    lines.append(f"\033[1;30m|{h_tags[0]}|{h_tags[1]}|{h_tags[2]}|\033[0m")
    lines.append(div_3)

    # 12 full uncropped sprite rows
    for r in range(12):
        cells = []
        for c in range(3):
            h = page_heroes[c]
            if h:
                spr = HERO_TRI_STATES[h["name"]]["normal"]
                r_txt = " " + spr[r] + "  " if r < len(spr) else " " * 32
            else:
                r_txt = " " * 32
            cells.append(fit_exact(r_txt, 32))
        lines.append(f"\033[1;30m|{cells[0]}|{cells[1]}|{cells[2]}|\033[0m")

    lines.append(div_3)

    # Row 1: HP & ATK
    s1_cells = []
    for c in range(3):
        h = page_heroes[c]
        txt = f" \033[1;32mHP: {h['hp']:3d}/{h['max_hp']:3d}\033[0m  |  \033[1;31mATK: {h['atk']:2d} DMG\033[0m" if h else ""
        s1_cells.append(fit_exact(txt, 32))
    lines.append(f"\033[1;30m|{s1_cells[0]}|{s1_cells[1]}|{s1_cells[2]}|\033[0m")

    # Row 2: DEF & DODGE
    s2_cells = []
    for c in range(3):
        h = page_heroes[c]
        txt = f" \033[1;36mDEF: {h['def']:2d}\033[0m       |  \033[1;35mDODGE: {int(h['dodge_rate']*100)}%\033[0m" if h else ""
        s2_cells.append(fit_exact(txt, 32))
    lines.append(f"\033[1;30m|{s2_cells[0]}|{s2_cells[1]}|{s2_cells[2]}|\033[0m")

    # Row 3: TRAIT
    s3_cells = []
    for c in range(3):
        h = page_heroes[c]
        txt = f" \033[1;33mTRAIT:\033[0m {h['trait'][:22]}" if h else ""
        s3_cells.append(fit_exact(txt, 32))
    lines.append(f"\033[1;30m|{s3_cells[0]}|{s3_cells[1]}|{s3_cells[2]}|\033[0m")

    div_wide = "\033[1;30m+" + "=" * 98 + "+\033[0m"
    lines.append(div_wide)

    # Active hero summary
    d1 = f" \033[1;33mEXPLORER:\033[1;37m {active_h['name']} [{active_h['role']}]\033[0m  |  \033[1;36mSKILL:\033[0m {active_h['skills'][0]['label']} & {active_h['skills'][1]['label']}"
    lines.append(f"\033[1;30m|{fit_exact(d1, 98)}\033[1;30m|\033[0m")

    assess = " ".join(active_h["assessment"][:2])
    d2 = f" \033[1;33mĐÁNH GIÁ:\033[0;37m {assess[:86]}"
    lines.append(f"\033[1;30m|{fit_exact(d2, 98)}\033[1;30m|\033[0m")

    lines.append("\033[1;30m+" + "-" * 98 + "+\033[0m")
    ctrls = f" \033[90m[ĐIỀU KHIỂN]:\033[0m \033[1;37m[A/D / Mũi tên Trái/Phải]\033[0m Đổi Hero  |  \033[1;33m[1-8]\033[0m Nhảy số  |  \033[1;33m[TAB]\033[0m Đổi Giao diện  |  \033[1;32m[Enter]\033[0m Chọn  |  \033[1;31m[Q]\033[0m Thoát"
    lines.append(f"\033[1;30m|{fit_exact(ctrls, 98)}\033[1;30m|\033[0m")
    lines.append(div_wide)
    return lines

LAYOUT_MODES = ["quad_grid", "vertical_split", "panorama_3col"]

def run_grid_select_interactive():
    sel_idx = 0
    mode_idx = 0  # 0: quad_grid (Bản 1), 1: vertical_split (Bản 2), 2: panorama_3col (Bản 3)
    num_heroes = len(HEROES)

    dui.clear_screen()
    print("\033[?25l", end="", flush=True)

    try:
        while True:
            cur_mode = LAYOUT_MODES[mode_idx]
            if cur_mode == "quad_grid":
                frame = render_quad_grid(sel_idx)
            elif cur_mode == "vertical_split":
                frame = render_vertical_split(sel_idx)
            else:
                frame = render_panorama_3col(sel_idx)

            dui.atomic_blit(frame)

            if not (os.name == 'nt' and sys.stdin.isatty()):
                return HEROES[sel_idx], sel_idx

            ch = msvcrt.getch()
            while msvcrt.kbhit():
                msvcrt.getch()

            # Handle Arrows
            if ch in (b'\x00', b'\xe0'):
                ext = msvcrt.getch()
                if cur_mode == "quad_grid":
                    page = sel_idx // 4
                    local_idx = sel_idx % 4
                    r = local_idx // 2
                    c = local_idx % 2
                    if ext == b'H': # Up
                        r = (r - 1) % 2
                    elif ext == b'P': # Down
                        r = (r + 1) % 2
                    elif ext == b'K': # Left
                        if c == 0:
                            page = (page - 1) % 2
                            c = 1
                        else:
                            c = 0
                    elif ext == b'M': # Right
                        if c == 1:
                            page = (page + 1) % 2
                            c = 0
                        else:
                            c = 1
                    sel_idx = min(page * 4 + r * 2 + c, num_heroes - 1)
                elif cur_mode == "vertical_split":
                    if ext == b'H': # Up
                        sel_idx = (sel_idx - 1) % num_heroes
                    elif ext == b'P': # Down
                        sel_idx = (sel_idx + 1) % num_heroes
                else: # panorama_3col
                    if ext in (b'K', b'H'): # Left or Up
                        sel_idx = (sel_idx - 1) % num_heroes
                    elif ext in (b'M', b'P'): # Right or Down
                        sel_idx = (sel_idx + 1) % num_heroes

            # Handle TAB -> Cycle 3 layouts
            elif ch in (b'\t',):
                mode_idx = (mode_idx + 1) % len(LAYOUT_MODES)

            # Direct Jump 1-8 for heroes
            elif ch in (b'1', b'2', b'3', b'4', b'5', b'6', b'7', b'8'):
                val = int(ch.decode('ascii')) - 1
                if val < num_heroes:
                    sel_idx = val

            # WASD controls
            elif ch in (b'w', b'W'):
                if cur_mode == "quad_grid":
                    page = sel_idx // 4
                    local_idx = sel_idx % 4
                    r = (local_idx // 2 - 1) % 2
                    c = local_idx % 2
                    sel_idx = min(page * 4 + r * 2 + c, num_heroes - 1)
                else:
                    sel_idx = (sel_idx - 1) % num_heroes
            elif ch in (b's', b'S'):
                if cur_mode == "quad_grid":
                    page = sel_idx // 4
                    local_idx = sel_idx % 4
                    r = (local_idx // 2 + 1) % 2
                    c = local_idx % 2
                    sel_idx = min(page * 4 + r * 2 + c, num_heroes - 1)
                else:
                    sel_idx = (sel_idx + 1) % num_heroes
            elif ch in (b'a', b'A'):
                if cur_mode == "quad_grid":
                    page = sel_idx // 4
                    local_idx = sel_idx % 4
                    r = local_idx // 2
                    c = local_idx % 2
                    if c == 0:
                        page = (page - 1) % 2
                        c = 1
                    else:
                        c = 0
                    sel_idx = min(page * 4 + r * 2 + c, num_heroes - 1)
                else:
                    sel_idx = (sel_idx - 1) % num_heroes
            elif ch in (b'd', b'D'):
                if cur_mode == "quad_grid":
                    page = sel_idx // 4
                    local_idx = sel_idx % 4
                    r = local_idx // 2
                    c = local_idx % 2
                    if c == 1:
                        page = (page + 1) % 2
                        c = 0
                    else:
                        c = 1
                    sel_idx = min(page * 4 + r * 2 + c, num_heroes - 1)
                else:
                    sel_idx = (sel_idx + 1) % num_heroes

            # Confirm Selection
            elif ch in (b'\r', b'\n', b' '):
                return HEROES[sel_idx], sel_idx

            # Quit / Cancel
            elif ch in (b'q', b'Q', b'\x1b'):
                return None, None

    finally:
        print("\033[?25h", end="", flush=True)

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
    print("  \033[1;37m[2]\033[0m Thử nghiệm lại bộ chọn nhân vật (3 Giao diện: 2x2 / Dọc / Panorama)")
    print("  \033[1;37m[Q]\033[0m Thoát ra ngoài")
    print("\033[1;30m+" + "=" * 98 + "+\033[0m")

    if os.name == 'nt' and sys.stdin.isatty():
        choice = input("\nLựa chọn của bạn [1/2/Q]: ").strip().lower()
        if choice == '1':
            dui.clear_screen()
            os.system("python funger_terminal/master_game.py")
        elif choice == '2':
            main()
        else:
            print("[OK] Đã thoát bộ chọn nhân vật.")

if __name__ == "__main__":
    main()
