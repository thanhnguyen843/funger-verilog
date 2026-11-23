#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
================================================================================
ULTRA-WIDE 140-COLUMN SHOWCASE ENGINE (KHÔNG GIAN MỞ & BẢN 140 CỘT TỰ DO)
Fear & Hunger: Terminal Labyrinth - Solo Explorer Architecture
================================================================================
Key Innovations of the 140-Column Architecture:
  1. Complete Freedom from Cramping:
     - 140 columns provides 40% more horizontal screen real estate than 100 cols.
     - 4 full heroes fit side-by-side on a single row with 100% native uncropped sprites!
  2. Three Selectable Wide Layout Paradigms:
     - Mode 1: [4 CỘT TRẢI NGANG SONG SONG] (4 Heroes side-by-side, 34 cols/card, 0% cropping)
     - Mode 2: [2x2 SIÊU RỘNG ULTRA QUAD] (68 cols/card: 29-col sprite + 35 cols full dossier)
     - Mode 3: [KHÔNG GIAN MỞ BORDERLESS] (Zero heavy boxes, floating figures on deep canvas)
  3. Majestic 140-Column Combat Arena:
     - Left Half (68 cols): Full Explorer Hero, anatomy status, limb health, and stats.
     - Right Half (68 cols): Full Adversary Monster, targetable limb health, intent telegraph.
     - Bottom (138 cols): Tactical Command Center with zero line wraps or trailing artifacts.
  4. 8-Slot Tactical Inventory (4x2 Grid):
     - 8 spacious item slots with colored pixel art icons and full lore inspection pane.
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
TOTAL_W = 140

# =============================================================================
# 1. HERO SELECTOR 140 COLS: MODE 1 - 4 CỘT TRẢI NGANG SONG SONG
# =============================================================================
def render_wide_hero_select_4col(sel_idx):
    """
    140 columns / 4 cards:
    Border: 5 chars (+ or |). Remaining: 135 cols.
    Card widths: 33, 34, 34, 34. Total = 135 + 5 = 140!
    Full 29-column sprite centered with generous breathing room!
    """
    page = sel_idx // 4
    start = page * 4
    p_heroes = [HEROES[start + i] if start + i < len(HEROES) else None for i in range(4)]
    active_h = HEROES[sel_idx]
    c_widths = [33, 34, 34, 34]

    lines = []
    lines.append("\033[1;30m+" + "=" * 138 + "+\033[0m")
    title = f"FEAR & HUNGER: HERO SELECTOR (140-COL ULTRA WIDE) - [CHẾ ĐỘ 1: 4 CỘT TRẢI NGANG]  (TRANG {page+1}/2)"
    tab_hint = "[TAB: ĐỔI MÀN HÌNH  |  M: ĐỔI KIỂU BỐ CỤC]"
    hdr = f" \033[1;37m{title:<94}\033[1;33m{tab_hint:>41} "
    lines.append(f"\033[1;30m|{fit_exact(hdr, 138)}\033[1;30m|\033[0m")

    # Divider line
    div_4 = "\033[1;30m+" + "+".join(["-" * w for w in c_widths]) + "+\033[0m"
    lines.append(div_4)

    # Hero Badges Row
    badge_cells = []
    for i, w in enumerate(c_widths):
        h = p_heroes[i]
        if h:
            real_idx = HEROES.index(h)
            is_cur = (real_idx == sel_idx)
            tag = f"[{h['id']}] {h['name']} ({h['role'].split()[0]})"
            txt = f"\033[1;32m ▶ {tag}\033[0m" if is_cur else f"\033[90m   {tag}\033[0m"
        else:
            txt = "   \033[90m-- TRỐNG --\033[0m"
        badge_cells.append(fit_exact(txt, w))
    lines.append(f"\033[1;30m|{'|'.join(badge_cells)}|\033[0m")
    lines.append(div_4)

    # 12 Sprite Rows (29 columns wide) - Zero cropping!
    for r in range(12):
        row_cells = []
        for i, w in enumerate(c_widths):
            h = p_heroes[i]
            if h:
                spr = HERO_TRI_STATES[h["name"]]["normal"]
                sp_line = spr[r] if r < len(spr) else " " * 29
                # 33 cols: 1 space + 29 cols + 3 spaces
                # 34 cols: 2 spaces + 29 cols + 3 spaces
                pad_left = 1 if w == 33 else 2
                pad_right = w - pad_left - 29
                cell_str = " " * pad_left + sp_line + " " * pad_right
            else:
                cell_str = " " * w
            row_cells.append(fit_exact(cell_str, w))
        lines.append(f"\033[1;30m|{'|'.join(row_cells)}|\033[0m")

    lines.append(div_4)

    # Stats Row 1: HP & ATK
    s1_cells = []
    for i, w in enumerate(c_widths):
        h = p_heroes[i]
        txt = f" \033[1;32mHP: {h['hp']:3d}/{h['max_hp']:3d}\033[0m  |  \033[1;31mATK: {h['atk']:2d} DMG\033[0m" if h else ""
        s1_cells.append(fit_exact(txt, w))
    lines.append(f"\033[1;30m|{'|'.join(s1_cells)}|\033[0m")

    # Stats Row 2: DEF & DODGE
    s2_cells = []
    for i, w in enumerate(c_widths):
        h = p_heroes[i]
        txt = f" \033[1;36mDEF: {h['def']:2d}\033[0m       |  \033[1;35mDOD: {int(h['dodge_rate']*100)}%\033[0m" if h else ""
        s2_cells.append(fit_exact(txt, w))
    lines.append(f"\033[1;30m|{'|'.join(s2_cells)}|\033[0m")

    # Stats Row 3: TRAIT
    s3_cells = []
    for i, w in enumerate(c_widths):
        h = p_heroes[i]
        txt = f" \033[1;33mTRAIT:\033[0m {h['trait'][:24]}" if h else ""
        s3_cells.append(fit_exact(txt, w))
    lines.append(f"\033[1;30m|{'|'.join(s3_cells)}|\033[0m")

    # Stats Row 4: SKILLS
    s4_cells = []
    for i, w in enumerate(c_widths):
        h = p_heroes[i]
        txt = f" \033[1;36mSKILL:\033[0m {h['skills'][0]['label'][:24]}" if h else ""
        s4_cells.append(fit_exact(txt, w))
    lines.append(f"\033[1;30m|{'|'.join(s4_cells)}|\033[0m")

    lines.append("\033[1;30m+" + "=" * 138 + "+\033[0m")

    # ACTIVE EXPLORER GRAND DOSSIER (Spanning 138 columns!)
    ah = active_h
    d1 = f" \033[1;33mĐANG CHỌN:\033[1;37m {ah['name']} [{ah['role']}]\033[0m  |  \033[1;32mHP: {ah['hp']}/{ah['max_hp']}\033[0m  |  \033[1;31mATK: {ah['atk']} DMG\033[0m  |  \033[1;36mDEF: {ah['def']}\033[0m  |  \033[1;35mNÉ TRÁNH: {int(ah['dodge_rate']*100)}%\033[0m  |  \033[1;33mKHÁNG VẬT LÝ: {ah['phys_resist_str']}\033[0m"
    lines.append(f"\033[1;30m|{fit_exact(d1, 138)}\033[1;30m|\033[0m")

    d2 = f" \033[1;37mĐẶC TÍNH  :\033[0;37m {ah['trait']:<32} \033[1;32mCƯỜNG HÓA: {ah['item_buff_str']:<32} \033[1;36mKỸ NĂNG: [1] {ah['skills'][0]['label']}  [2] {ah['skills'][1]['label']}\033[0m"
    lines.append(f"\033[1;30m|{fit_exact(d2, 138)}\033[1;30m|\033[0m")

    assess = " ".join(ah["assessment"][:3])
    d3 = f" \033[1;33mĐÁNH GIÁ  :\033[0;37m {assess[:126]}"
    lines.append(f"\033[1;30m|{fit_exact(d3, 138)}\033[1;30m|\033[0m")

    lines.append("\033[1;30m+" + "-" * 138 + "+\033[0m")
    ctrls = " \033[90m[ĐIỀU KHIỂN]:\033[0m \033[1;37m[A/D / Mũi tên Trái/Phải]\033[0m Chọn Hero  |  \033[1;37m[W/S]\033[0m Đổi Trang  |  \033[1;33m[1-8]\033[0m Nhảy số  |  \033[1;33m[M]\033[0m Đổi Bố cục 140  |  \033[1;32m[Enter]\033[0m Chọn  |  \033[1;31m[Q]\033[0m Thoát"
    lines.append(f"\033[1;30m|{fit_exact(ctrls, 138)}\033[1;30m|\033[0m")
    lines.append("\033[1;30m+" + "=" * 138 + "+\033[0m")

    return lines

# =============================================================================
# 2. HERO SELECTOR 140 COLS: MODE 2 - 2x2 SIÊU RỘNG (ULTRA QUAD GRID)
# =============================================================================
def render_wide_hero_select_quad(sel_idx):
    """
    140 columns / 2 cards:
    Border: 3 chars. Remaining: 137 cols.
    Card widths: 68 and 69 columns!
    Each card holds full 29-col uncropped sprite on left + 35 columns of rich dossier on right!
    """
    page = sel_idx // 4
    start = page * 4
    q_heroes = [HEROES[start + i] if start + i < len(HEROES) else None for i in range(4)]
    active_h = HEROES[sel_idx]
    w_l, w_r = 68, 69

    lines = []
    lines.append("\033[1;30m+" + "=" * 138 + "+\033[0m")
    title = f"FEAR & HUNGER: HERO SELECTOR (140-COL ULTRA WIDE) - [CHẾ ĐỘ 2: 2x2 SIÊU RỘNG ULTRA]  (TRANG {page+1}/2)"
    tab_hint = "[TAB: ĐỔI MÀN HÌNH  |  M: ĐỔI KIỂU BỐ CỤC]"
    hdr = f" \033[1;37m{title:<94}\033[1;33m{tab_hint:>41} "
    lines.append(f"\033[1;30m|{fit_exact(hdr, 138)}\033[1;30m|\033[0m")

    div_2 = "\033[1;30m+" + "-" * w_l + "+" + "-" * w_r + "+\033[0m"
    lines.append(div_2)

    def make_badge(h, is_cur, w):
        if not h: return " " * w
        tag = f"[{h['id']}] {h['name']} ({h['role']})"
        return f"\033[1;32m▶ {tag}\033[0m" if is_cur else f"\033[90m  {tag}\033[0m"

    def get_rich_dossier(h):
        if not h: return [""] * 11
        return [
            f"\033[1;32mSINH MỆNH   : {h['hp']:3d} / {h['max_hp']:3d}\033[0m",
            f"\033[1;31mSỨC TẤN CÔNG: {h['atk']:2d} DMG\033[0m",
            f"\033[1;36mPHÒNG NGỰ   : {h['def']:2d}\033[0m",
            f"\033[1;35mNÉ TRÁNH    : {int(h['dodge_rate']*100)}% Evasion\033[0m",
            f"\033[1;37mKHÁNG VẬT LÝ: {h['phys_resist_str'][:18]}\033[0m",
            f"\033[1;33mĐẶC TÍNH    : {h['trait'][:18]}\033[0m",
            f"\033[1;32mCƯỜNG HÓA   : {h['item_buff_str'][:18]}\033[0m",
            f"\033[1;36mKỸ NĂNG 1   : {h['skills'][0]['label'][:18]}\033[0m",
            f"\033[1;36mKỸ NĂNG 2   : {h['skills'][1]['label'][:18]}\033[0m",
            f"\033[90mĐÁNH GIÁ    : {h['assessment'][0][:18]}...\033[0m",
            ""
        ]

    # Row 1: Heroes 0 & 1
    h_tl, h_tr = q_heroes[0], q_heroes[1]
    b_tl = fit_exact(" " + make_badge(h_tl, HEROES.index(h_tl) == sel_idx if h_tl else False, w_l - 1), w_l)
    b_tr = fit_exact(" " + make_badge(h_tr, HEROES.index(h_tr) == sel_idx if h_tr else False, w_r - 1), w_r)
    lines.append(f"\033[1;30m|{b_tl}\033[1;30m|{b_tr}\033[1;30m|\033[0m")
    lines.append(div_2)

    st_tl, st_tr = get_rich_dossier(h_tl), get_rich_dossier(h_tr)
    spr_tl = HERO_TRI_STATES[h_tl["name"]]["normal"] if h_tl else [" " * 29] * 12
    spr_tr = HERO_TRI_STATES[h_tr["name"]]["normal"] if h_tr else [" " * 29] * 12

    for r in range(11):
        sp_l = spr_tl[r] if r < len(spr_tl) else " " * 29
        st_l = st_tl[r] if r < len(st_tl) else ""
        c_l = fit_exact(f"  {sp_l}   {st_l}", w_l)

        sp_r = spr_tr[r] if r < len(spr_tr) else " " * 29
        st_r = st_tr[r] if r < len(st_tr) else ""
        c_r = fit_exact(f"  {sp_r}   {st_r}", w_r)
        lines.append(f"\033[1;30m|{c_l}\033[1;30m|{c_r}\033[1;30m|\033[0m")

    lines.append(div_2)

    # Row 2: Heroes 2 & 3
    h_bl, h_br = q_heroes[2], q_heroes[3]
    b_bl = fit_exact(" " + make_badge(h_bl, HEROES.index(h_bl) == sel_idx if h_bl else False, w_l - 1), w_l)
    b_br = fit_exact(" " + make_badge(h_br, HEROES.index(h_br) == sel_idx if h_br else False, w_r - 1), w_r)
    lines.append(f"\033[1;30m|{b_bl}\033[1;30m|{b_br}\033[1;30m|\033[0m")
    lines.append(div_2)

    st_bl, st_br = get_rich_dossier(h_bl), get_rich_dossier(h_br)
    spr_bl = HERO_TRI_STATES[h_bl["name"]]["normal"] if h_bl else [" " * 29] * 12
    spr_br = HERO_TRI_STATES[h_br["name"]]["normal"] if h_br else [" " * 29] * 12

    for r in range(11):
        sp_l = spr_bl[r] if r < len(spr_bl) else " " * 29
        st_l = st_bl[r] if r < len(st_bl) else ""
        c_l = fit_exact(f"  {sp_l}   {st_l}", w_l)

        sp_r = spr_br[r] if r < len(spr_br) else " " * 29
        st_r = st_br[r] if r < len(st_br) else ""
        c_r = fit_exact(f"  {sp_r}   {st_r}", w_r)
        lines.append(f"\033[1;30m|{c_l}\033[1;30m|{c_r}\033[1;30m|\033[0m")

    lines.append("\033[1;30m+" + "=" * 138 + "+\033[0m")
    ctrls = " \033[90m[ĐIỀU KHIỂN]:\033[0m \033[1;37m[W/A/S/D / Mũi tên]\033[0m Ô chọn  |  \033[1;33m[1-8]\033[0m Nhảy số  |  \033[1;33m[M]\033[0m Đổi Bố cục 140  |  \033[1;32m[Enter]\033[0m Chọn  |  \033[1;31m[Q]\033[0m Thoát"
    lines.append(f"\033[1;30m|{fit_exact(ctrls, 138)}\033[1;30m|\033[0m")
    lines.append("\033[1;30m+" + "=" * 138 + "+\033[0m")
    return lines

# =============================================================================
# 3. HERO SELECTOR 140 COLS: MODE 3 - KHÔNG GIAN MỞ (DARK BORDERLESS)
# =============================================================================
def render_wide_hero_select_borderless(sel_idx):
    """
    Borderless / Dark Minimalist:
    No heavy ASCII box borders! Just clean subtle lines, dark atmosphere,
    floating hero sprites with natural glowing cursors.
    """
    page = sel_idx // 4
    start = page * 4
    p_heroes = [HEROES[start + i] if start + i < len(HEROES) else None for i in range(4)]
    active_h = HEROES[sel_idx]
    c_widths = [35, 35, 35, 35]

    lines = []
    lines.append(fit_exact(" \033[1;37mFEAR & HUNGER: SOLO SURVIVOR EXPEDITION\033[0m  \033[90m—\033[0m  \033[1;33m[KHÔNG GIAN MỞ BORDERLESS]\033[0m", 140))
    lines.append(fit_exact("\033[90m" + "─" * 140 + "\033[0m", 140))

    # Badges row
    b_cells = []
    for i, w in enumerate(c_widths):
        h = p_heroes[i]
        if h:
            real_idx = HEROES.index(h)
            is_cur = (real_idx == sel_idx)
            tag = f"[{h['id']}] {h['name'].upper()} ({h['role'].split()[0]})"
            txt = f"\033[1;32m◆ {tag}\033[0m" if is_cur else f"\033[90m  {tag}\033[0m"
        else:
            txt = "  \033[90m---\033[0m"
        b_cells.append(fit_exact(txt, w))
    lines.append("".join(b_cells))
    lines.append(fit_exact("\033[90m" + "· " * 70 + "\033[0m", 140))

    # 12 Sprite Rows
    for r in range(12):
        row_cells = []
        for i, w in enumerate(c_widths):
            h = p_heroes[i]
            if h:
                spr = HERO_TRI_STATES[h["name"]]["normal"]
                sp_line = spr[r] if r < len(spr) else " " * 29
                cell_str = "   " + sp_line + "   "
            else:
                cell_str = " " * w
            row_cells.append(fit_exact(cell_str, w))
        lines.append("".join(row_cells))

    lines.append(fit_exact("\033[90m" + "─" * 140 + "\033[0m", 140))

    # Stats rows
    s1_cells = []
    for i, w in enumerate(c_widths):
        h = p_heroes[i]
        txt = f"  \033[1;32mHP {h['hp']:3d}/{h['max_hp']:3d}\033[0m   \033[1;31mATK {h['atk']:2d}\033[0m" if h else ""
        s1_cells.append(fit_exact(txt, w))
    lines.append("".join(s1_cells))

    s2_cells = []
    for i, w in enumerate(c_widths):
        h = p_heroes[i]
        txt = f"  \033[1;36mDEF {h['def']:2d}\033[0m       \033[1;35mDOD {int(h['dodge_rate']*100)}%\033[0m" if h else ""
        s2_cells.append(fit_exact(txt, w))
    lines.append("".join(s2_cells))

    s3_cells = []
    for i, w in enumerate(c_widths):
        h = p_heroes[i]
        txt = f"  \033[1;33m{h['trait'][:28]}\033[0m" if h else ""
        s3_cells.append(fit_exact(txt, w))
    lines.append("".join(s3_cells))

    lines.append(fit_exact("\033[90m" + "─" * 140 + "\033[0m", 140))

    # Active Explorer Info
    ah = active_h
    d1 = f" \033[1;33mKHẢO SÁT:\033[1;37m {ah['name']} [{ah['role']}]\033[0m  |  \033[1;32mBUFF: {ah['item_buff_str']}\033[0m  |  \033[1;36mKỸ NĂNG: {ah['skills'][0]['label']} & {ah['skills'][1]['label']}\033[0m"
    lines.append(fit_exact(d1, 140))

    assess = " ".join(ah["assessment"][:3])
    d2 = f" \033[90mĐÁNH GIÁ: {assess[:128]}\033[0m"
    lines.append(fit_exact(d2, 140))

    lines.append(fit_exact("\033[90m" + "─" * 140 + "\033[0m", 140))
    ctrls = " \033[90m[A/D] Chọn  |  [W/S] Trang  |  [M] Bố Cục  |  [TAB] Đổi Màn Hình  |  [Enter] Xác Nhận  |  [Q] Thoát\033[0m"
    lines.append(fit_exact(ctrls, 140))
    return lines

# =============================================================================
# 4. COMBAT ARENA 140 COLS: MAJESTIC SYMMETRICAL DUAL ARENA
# =============================================================================
def render_wide_combat_arena(sel_hero_idx, foe_id="13", action_idx=0):
    """
    140-Column Symmetrical Combat Arena:
    Left Half (68 cols): Explorer Hero (Sprite + Limb Integrity + Stats)
    Right Half (68 cols): Foe / Horror (Targetable Anatomy + Sprite + Telegraph)
    Bottom (138 cols): Tactical Command Center
    """
    hero = HEROES[sel_hero_idx]
    foe_data = dui.ALL_MONSTER_SPRITES.get(foe_id, dui.ALL_MONSTER_SPRITES["13"])
    foe_name = foe_data["name"]
    foe_spr = foe_data["normal"]

    w_half = 68
    lines = []
    lines.append("\033[1;30m+" + "=" * 138 + "+\033[0m")
    title = f"FEAR & HUNGER: SOLO SURVIVOR COMBAT ARENA (140-COL BATTLEFIELD)"
    hint = "[TAB: ĐỔI MÀN HÌNH  |  Q: RÚT CHẠY]"
    hdr = f" \033[1;31m⚔  \033[1;37m{title:<92}\033[1;33m{hint:>40} "
    lines.append(f"\033[1;30m|{fit_exact(hdr, 138)}\033[1;30m|\033[0m")

    div_mid = "\033[1;30m+" + "-" * w_half + "+" + "-" * (137 - w_half) + "+\033[0m"
    lines.append(div_mid)

    # Header Row: Explorer vs Foe
    h_left = f" \033[1;32m[EXPLORER HERO]:\033[1;37m {hero['name']} [{hero['role']}]\033[0m"
    h_right = f" \033[1;31m[ADVERSARY FOE]:\033[1;37m #{foe_id} {foe_name.upper()} [TERROR CLASS]\033[0m"
    lines.append(f"\033[1;30m|{fit_exact(h_left, w_half)}\033[1;30m|{fit_exact(h_right, 137 - w_half)}\033[1;30m|\033[0m")
    lines.append(div_mid)

    # 12 Combat Stage Rows
    h_spr = HERO_TRI_STATES[hero["name"]]["normal"]

    left_stats = [
        f"\033[1;32mHP   :\033[0m \033[1;32m[████████████████] {hero['hp']}/{hero['max_hp']}\033[0m",
        f"\033[1;36mMIND :\033[0m \033[1;36m[██████████░░░░░░] 70/100 (Bình Tĩnh)\033[0m",
        f"\033[1;33mHUNGR:\033[0m \033[1;33m[████████████░░░░] 75/100 (No Nê)\033[0m",
        f"\033[1;35mTOXIC:\033[0m \033[0;37m[░░░░░░░░░░░░░░░░]  0% [AN TOÀN]\033[0m",
        "",
        f"\033[1;33m[TỨ CHI & CHẤN THƯƠNG]:\033[0m",
        f"  \033[1;32m● Tay Phải: Nguyên Vẹn\033[0m (Vũ khí sẵn sàng)",
        f"  \033[1;32m● Tay Trái: Nguyên Vẹn\033[0m (Khiên phòng thủ)",
        f"  \033[1;32m● Chân Trái: Lành Lặn\033[0m  (Né tránh 100%)",
        f"  \033[1;32m● Chân Phải: Lành Lặn\033[0m (Chạy trốn 100%)",
        f"\033[1;33mĐẶC TÍNH: {hero['trait'][:24]}\033[0m",
        ""
    ]

    right_stats = [
        f"\033[1;31mSINH MỆNH QUÁI:\033[0m \033[1;31m[████████████████] 90/90 (100%)\033[0m",
        f"\033[1;33mÝ ĐỒ HÀNH ĐỘNG :\033[1;37m Rình rập vồ đứt cánh tay!\033[0m",
        "",
        f"\033[1;33m[MỤC TIÊU CƠ THỂ ĐỐI THỦ]:\033[0m",
        f"  \033[1;31m[1] ĐẦU (HEAD)   :\033[0m 25 HP (Tỉ lệ trúng 60% - Chí mạng)",
        f"  \033[1;37m[2] THÂN (TORSO) :\033[0m 50 HP (Tỉ lệ trúng 95% - Vững chãi)",
        f"  \033[1;33m[3] VUỐT PHẢI    :\033[0m 20 HP (Chặt đứt để tước vũ khí)",
        f"  \033[1;33m[4] VUỐT TRÁI    :\033[0m 20 HP (Chặt đứt để giảm 50% DMG)",
        f"  \033[1;36m[5] CHÂN SAU     :\033[0m 25 HP (Đánh què để triệt hạ né)",
        "",
        f"\033[1;35mTRẠNG THÁI: Tứ chi hung hãn, chưa chịu thương tổn!\033[0m",
        ""
    ]

    for r in range(12):
        sp_l = h_spr[r] if r < len(h_spr) else " " * 29
        st_l = left_stats[r] if r < len(left_stats) else ""
        c_l = fit_exact(f" {sp_l}  {st_l}", w_half)

        # Right side: stats on left, monster sprite on right
        sp_r = foe_spr[r] if r < len(foe_spr) else " " * 14
        st_r = right_stats[r] if r < len(right_stats) else ""
        c_r = fit_exact(f" {st_r:<38}  {sp_r}", 137 - w_half)

        lines.append(f"\033[1;30m|{c_l}\033[1;30m|{c_r}\033[1;30m|\033[0m")

    lines.append("\033[1;30m+" + "=" * 138 + "+\033[0m")

    # Combat Log Line
    c_log = f" \033[1;33m[NHẬT KÝ CHIẾN TRƯỜNG]:\033[1;37m {hero['name']} rút vũ khí đối mặt {foe_name}! Mùi tanh tưởi của tử khí tràn ngập hành lang hầm ngục!\033[0m"
    lines.append(f"\033[1;30m|{fit_exact(c_log, 138)}\033[1;30m|\033[0m")

    lines.append("\033[1;30m+" + "-" * 138 + "+\033[0m")

    # 5 Tactical Action Buttons (Spaced wide across 138 columns!)
    actions = [
        "[1] TẤN CÔNG ĐIỂM YẾU",
        "[2] PHÒNG THỦ (-70% DMG)",
        "[3] KỸ NĂNG ĐẶC BIỆT",
        "[4] TÚI ĐỒ (TOTEM/HERB)",
        "[5] RÚT CHẠY (50%)"
    ]
    act_row = "   "
    for i, a in enumerate(actions):
        if i == action_idx:
            act_row += f"\033[1;42;30m ▶ {a} \033[0m   "
        else:
            act_row += f"\033[1;37m {a} \033[0m   "
    lines.append(f"\033[1;30m|{fit_exact(act_row, 138)}\033[1;30m|\033[0m")

    lines.append("\033[1;30m+" + "-" * 138 + "+\033[0m")
    ctrls = " \033[90m[ĐIỀU KHIỂN]:\033[0m \033[1;37m[A/D / 1-5]\033[0m Chọn Hành Động  |  \033[1;32m[Enter/Space]\033[0m Thi Hành  |  \033[1;33m[TAB]\033[0m Đổi Màn Hình  |  \033[1;31m[Q]\033[0m Thoát"
    lines.append(f"\033[1;30m|{fit_exact(ctrls, 138)}\033[1;30m|\033[0m")
    lines.append("\033[1;30m+" + "=" * 138 + "+\033[0m")
    return lines

# =============================================================================
# 5. INVENTORY 140 COLS: 8-SLOT TACTICAL GRID (4x2 WITH PIXEL ART ICONS)
# =============================================================================
def render_wide_inventory(sel_slot=0):
    """
    140-Column Tactical Inventory (4x2 = 8 slots):
    Each slot is 34 columns wide, featuring 4x4 pixel art icons, quantity counters,
    and a large lore / trauma curing pane at the bottom!
    """
    items = [
        {
            "name": "TOTEM OF FLESH",
            "type": "CỔ THẦN (ARTIFACT)",
            "qty": 1,
            "cure": "Gãy xương, Đứt chi, Xuất huyết",
            "lore": "Bảo vật Hổ Phách Sylvian vô giá. Tái sinh toàn bộ tứ chi bị đứt và hàn gắn da thịt!",
            "icon": ["  ▄▄▄▀(O)▀▄▄▄  ", " ██ ▀█▀█▀ █▄   ", " ▀▄▄ ▀█▀ ▄▄▀   ", "   ▀▀▀█▀▀▀     "]
        },
        {
            "name": "POPPY FLOWER",
            "type": "THẢO DƯỢC Y TẾ",
            "qty": 3,
            "cure": "Hồi phục 50 HP & Cầm máu",
            "lore": "Loài hoa đỏ thẫm sinh trưởng từ máu. Cầm máu tức thì cho các vết chém sâu.",
            "icon": ["    ▄▄█▄▄      ", "   ██(O)██     ", "    ▀▀█▀▀      ", "      █        "]
        },
        {
            "name": "MARIJUANA HERB",
            "type": "DƯỢC LIỆU XOA DỊU",
            "qty": 2,
            "cure": "Hồi phục 120 HP & Giảm đau",
            "lore": "Thảo mộc xanh làm dịu hệ thần kinh, triệt tiêu cơn đau đớn khi gãy xương.",
            "icon": ["    \033[32m ▄ █ ▄     \033[0m", "   \033[32m▀█████▀    \033[0m", "    \033[32m▀███▀     \033[0m", "     \033[32m █       \033[0m"]
        },
        {
            "name": "MOLDY BREAD",
            "type": "LƯƠNG THỰC SINH TỒN",
            "qty": 4,
            "cure": "Giảm 40 Cơn Đói Khát",
            "lore": "Ổ bánh mì ẩm mốc trong hầm tối. Vị đắng chát nhưng cứu sống kẻ đói lả.",
            "icon": ["   \033[33m ▄▄████▄▄   \033[0m", "   \033[33m███░░████   \033[0m", "   \033[33m▀███████▀   \033[0m", "               "]
        },
        {
            "name": "VINTAGE ALE",
            "type": "RƯỢU THANH TẨY",
            "qty": 2,
            "cure": "Hồi phục 35 Điểm Mind",
            "lore": "Men rượu nồng giúp tâm trí đứng vững trước nỗi kinh hoàng của hầm ngục tối.",
            "icon": ["     \033[36m ▄█▄      \033[0m", "     \033[36m█████     \033[0m", "     \033[36m█████     \033[0m", "     \033[36m ▀▀▀      \033[0m"]
        },
        {
            "name": "WOOD SPLINT",
            "type": "DỤNG CỤ Y TẾ",
            "qty": 1,
            "cure": "Cố định xương gãy",
            "lore": "Nẹp gỗ thô sơ giúp ổn định xương tay chân, phục hồi khả năng cầm nắm vũ khí.",
            "icon": ["     \033[33m █  █     \033[0m", "     \033[33m █══█     \033[0m", "     \033[33m █══█     \033[0m", "     \033[33m █  █     \033[0m"]
        },
        {
            "name": "LUCKY COIN",
            "type": "CỔ TIỀN RÙA RÙI",
            "qty": 2,
            "cure": "Tung 2 đồng xu cứu nguy",
            "lore": "Đồng xu cổ trao cơ hội lật ngược số phận khi đối đầu các đòn tất sát tử thần.",
            "icon": ["    \033[33m ▄████▄    \033[0m", "    \033[33m██($)██    \033[0m", "    \033[33m ▀████▀    \033[0m", "               "]
        },
        {
            "name": "RUNIC KEY",
            "type": "CHÌA KHÓA CỔ NGỮ",
            "qty": 2,
            "cure": "Cần 3 Chìa mở Cổng Đông",
            "lore": "Chìa khóa khắc cổ tự Hexen. Đủ 3 chiếc sẽ giải phong ấn Cổng Thoát Hiểm Đông.",
            "icon": ["     \033[36m ▄▀█      \033[0m", "     \033[36m █▀█      \033[0m", "     \033[36m █ █      \033[0m", "     \033[36m ▀ ▀      \033[0m"]
        }
    ]

    lines = []
    lines.append("\033[1;30m+" + "=" * 138 + "+\033[0m")
    title = f"FEAR & HUNGER: TÚI ĐỒ Ô LƯỚI CHIẾN THUẬT (140-COL 8-SLOT GRID)"
    hint = "[W/A/S/D / 1-8: CHỌN Ô  |  TAB: ĐỔI MÀN HÌNH]"
    hdr = f" \033[1;35m🎒 \033[1;37m{title:<94}\033[1;33m{hint:>39} "
    lines.append(f"\033[1;30m|{fit_exact(hdr, 138)}\033[1;30m|\033[0m")

    c_widths = [33, 34, 34, 34]
    div_4 = "\033[1;30m+" + "+".join(["-" * w for w in c_widths]) + "+\033[0m"
    lines.append(div_4)

    # Function to render a 4-slot row
    def render_slot_row(row_items, start_idx):
        row_lines = []
        # Badges
        b_cells = []
        for c, it in enumerate(row_items):
            w = c_widths[c]
            idx = start_idx + c
            is_cur = (idx == sel_slot)
            tag = f"[{idx+1}] {it['name']} (x{it['qty']})"
            txt = f"\033[1;32m▶ {tag}\033[0m" if is_cur else f"\033[90m  {tag}\033[0m"
            b_cells.append(fit_exact(txt, w))
        row_lines.append(f"\033[1;30m|{'|'.join(b_cells)}|\033[0m")
        row_lines.append(div_4)

        # 4 Icon Rows
        for r in range(4):
            i_cells = []
            for c, it in enumerate(row_items):
                w = c_widths[c]
                ic = it["icon"][r] if r < len(it["icon"]) else " " * 15
                # Center icon in cell
                pad = (w - 15) // 2
                cell_str = " " * pad + ic + " " * (w - pad - 15)
                i_cells.append(fit_exact(cell_str, w))
            row_lines.append(f"\033[1;30m|{'|'.join(i_cells)}|\033[0m")

        # Summary line
        s_cells = []
        for c, it in enumerate(row_items):
            w = c_widths[c]
            txt = f" \033[1;33m{it['cure'][:w-3]}\033[0m"
            s_cells.append(fit_exact(txt, w))
        row_lines.append(f"\033[1;30m|{'|'.join(s_cells)}|\033[0m")
        return row_lines

    # Row 1: slots 0..3
    lines.extend(render_slot_row(items[0:4], 0))
    lines.append(div_4)
    # Row 2: slots 4..7
    lines.extend(render_slot_row(items[4:8], 4))
    lines.append("\033[1;30m+" + "=" * 138 + "+\033[0m")

    # Lore & Detailed Inspection Pane (Selected Item)
    cur_it = items[sel_slot]
    it_name = cur_it["name"]
    it_type = cur_it["type"]
    it_qty = cur_it["qty"]
    it_cure = cur_it["cure"]
    it_lore = cur_it["lore"]

    d_info = f" \033[1;33m[GIÁM ĐỊNH CHI TIẾT]:\033[1;37m {it_name}  |  \033[1;32mLOẠI: {it_type}\033[0m  |  \033[1;36mSỐ LƯỢNG: {it_qty}\033[0m"
    lines.append(f"\033[1;30m|{fit_exact(d_info, 138)}\033[1;30m|\033[0m")
    d_cure = f" \033[1;32mCHỮA TRỊ :\033[0;37m {it_cure}"
    lines.append(f"\033[1;30m|{fit_exact(d_cure, 138)}\033[1;30m|\033[0m")
    d_lore = f" \033[1;33mCỐT TRUYỆN:\033[0;37m {it_lore}"
    lines.append(f"\033[1;30m|{fit_exact(d_lore, 138)}\033[1;30m|\033[0m")

    lines.append("\033[1;30m+" + "-" * 138 + "+\033[0m")
    ctrls = " \033[90m[ĐIỀU KHIỂN]:\033[0m \033[1;37m[W/A/S/D / 1-8]\033[0m Chọn Ô  |  \033[1;32m[Enter/Space]\033[0m Sử Dụng Vật Phẩm  |  \033[1;33m[TAB]\033[0m Đổi Màn Hình  |  \033[1;31m[Q]\033[0m Thoát"
    lines.append(f"\033[1;30m|{fit_exact(ctrls, 138)}\033[1;30m|\033[0m")
    lines.append("\033[1;30m+" + "=" * 138 + "+\033[0m")
    return lines

# =============================================================================
# MAIN INTERACTIVE ENGINE & SHOWCASE LOOP
# =============================================================================
def run_wide_engine():
    screen_idx = 0  # 0: Hero Select, 1: Combat Arena, 2: Inventory
    hero_layout_mode = 0  # 0: 4-Col, 1: 2x2 Ultra Quad, 2: Borderless
    sel_hero_idx = 0
    sel_combat_act = 0
    sel_inv_slot = 0

    dui.clear_screen()
    print("\033[?25l", end="", flush=True)

    try:
        while True:
            # Render current screen
            if screen_idx == 0:
                if hero_layout_mode == 0:
                    frame = render_wide_hero_select_4col(sel_hero_idx)
                elif hero_layout_mode == 1:
                    frame = render_wide_hero_select_quad(sel_hero_idx)
                else:
                    frame = render_wide_hero_select_borderless(sel_hero_idx)
            elif screen_idx == 1:
                frame = render_wide_combat_arena(sel_hero_idx, "13", sel_combat_act)
            else:
                frame = render_wide_inventory(sel_inv_slot)

            dui.atomic_blit(frame)

            if not (os.name == 'nt' and sys.stdin.isatty()):
                # Non-interactive fallback
                break

            ch = msvcrt.getch()
            while msvcrt.kbhit():
                msvcrt.getch()

            # Handle Arrows
            if ch in (b'\x00', b'\xe0'):
                ext = msvcrt.getch()
                if screen_idx == 0:
                    if ext in (b'K',): # Left
                        sel_hero_idx = (sel_hero_idx - 1) % len(HEROES)
                    elif ext in (b'M',): # Right
                        sel_hero_idx = (sel_hero_idx + 1) % len(HEROES)
                    elif ext in (b'H',): # Up
                        sel_hero_idx = (sel_hero_idx - 4) % len(HEROES)
                    elif ext in (b'P',): # Down
                        sel_hero_idx = (sel_hero_idx + 4) % len(HEROES)
                elif screen_idx == 1:
                    if ext in (b'K', b'H'):
                        sel_combat_act = (sel_combat_act - 1) % 5
                    elif ext in (b'M', b'P'):
                        sel_combat_act = (sel_combat_act + 1) % 5
                else: # Inventory
                    r = sel_inv_slot // 4
                    c = sel_inv_slot % 4
                    if ext == b'H': r = (r - 1) % 2
                    elif ext == b'P': r = (r + 1) % 2
                    elif ext == b'K': c = (c - 1) % 4
                    elif ext == b'M': c = (c + 1) % 4
                    sel_inv_slot = r * 4 + c

            # Handle TAB -> Switch Screen
            elif ch in (b'\t',):
                screen_idx = (screen_idx + 1) % 3

            # Handle M -> Switch Hero Layout Mode
            elif ch in (b'm', b'M'):
                if screen_idx == 0:
                    hero_layout_mode = (hero_layout_mode + 1) % 3

            # Number jumps
            elif ch in (b'1', b'2', b'3', b'4', b'5', b'6', b'7', b'8'):
                val = int(ch.decode('ascii')) - 1
                if screen_idx == 0 and val < len(HEROES):
                    sel_hero_idx = val
                elif screen_idx == 1 and val < 5:
                    sel_combat_act = val
                elif screen_idx == 2 and val < 8:
                    sel_inv_slot = val

            # WASD Controls
            elif ch in (b'a', b'A'):
                if screen_idx == 0: sel_hero_idx = (sel_hero_idx - 1) % len(HEROES)
                elif screen_idx == 1: sel_combat_act = (sel_combat_act - 1) % 5
                else: sel_inv_slot = (sel_inv_slot - 1) % 8
            elif ch in (b'd', b'D'):
                if screen_idx == 0: sel_hero_idx = (sel_hero_idx + 1) % len(HEROES)
                elif screen_idx == 1: sel_combat_act = (sel_combat_act + 1) % 5
                else: sel_inv_slot = (sel_inv_slot + 1) % 8
            elif ch in (b'w', b'W'):
                if screen_idx == 0: sel_hero_idx = (sel_hero_idx - 4) % len(HEROES)
                elif screen_idx == 2: sel_inv_slot = (sel_inv_slot - 4) % 8
            elif ch in (b's', b'S'):
                if screen_idx == 0: sel_hero_idx = (sel_hero_idx + 4) % len(HEROES)
                elif screen_idx == 2: sel_inv_slot = (sel_inv_slot + 4) % 8

            # Confirm
            elif ch in (b'\r', b'\n', b' '):
                pass

            # Quit
            elif ch in (b'q', b'Q', b'\x1b'):
                break

    finally:
        print("\033[?25h", end="", flush=True)

def print_samples():
    """Outputs all 140-column sample screens for terminal verification."""
    print("\n" + "=" * 140)
    print(" SAMPLE 1: HERO SELECTOR 140 COLS - CHẾ ĐỘ 1: 4 CỘT TRẢI NGANG SONG SONG")
    print("=" * 140)
    f1 = render_wide_hero_select_4col(0)
    for l in f1: print(l)

    print("\n" + "=" * 140)
    print(" SAMPLE 2: HERO SELECTOR 140 COLS - CHẾ ĐỘ 2: 2x2 SIÊU RỘNG (ULTRA QUAD)")
    print("=" * 140)
    f2 = render_wide_hero_select_quad(0)
    for l in f2: print(l)

    print("\n" + "=" * 140)
    print(" SAMPLE 3: HERO SELECTOR 140 COLS - CHẾ ĐỘ 3: KHÔNG GIAN MỞ BORDERLESS")
    print("=" * 140)
    f3 = render_wide_hero_select_borderless(0)
    for l in f3: print(l)

    print("\n" + "=" * 140)
    print(" SAMPLE 4: COMBAT ARENA 140 COLS - ĐẤU TRƯỜNG ĐỐI XỨNG HERO VS QUÁI")
    print("=" * 140)
    f4 = render_wide_combat_arena(3, "13", 0)
    for l in f4: print(l)

    print("\n" + "=" * 140)
    print(" SAMPLE 5: INVENTORY 140 COLS - TÚI ĐỒ 8 Ô CHIẾN THUẬT (4x2)")
    print("=" * 140)
    f5 = render_wide_inventory(0)
    for l in f5: print(l)

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--print-samples":
        print_samples()
    else:
        run_wide_engine()
