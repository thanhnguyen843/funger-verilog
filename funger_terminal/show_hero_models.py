#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
================================================================================
HERO TRI-STATE MORPHOLOGY SHOWCASE & VIEWER
Fear & Hunger: Terminal Labyrinth - Solo Explorer Architecture
================================================================================
Displays the 3 distinct anatomical states for all 8 Heroes side-by-side:
  1. MODEL THƯỜNG       : Intact upright silhouette, vibrant truecolor palette.
  2. MODEL CHẤN THƯƠNG  : Severed limbs, glowing Technical Amber (#FFAA28) joint stumps.
  3. MODEL TỬ VONG      : Collapsed horizontal corpse in Deactivated Ash Gray (#6E7378).
================================================================================
"""

import sys
import os
import re
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from hero_tri_state_catalog import HERO_TRI_STATES, HERO_ORDER
import demo_interactive_ui as dui

ANSI_RE = re.compile(r'\x1b\[[0-9;]*m')

def vis_len(s):
    return len(ANSI_RE.sub('', s))

def fit_exact(s, width):
    cur = vis_len(s)
    if cur > width:
        # Strip trailing chars cleanly
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

def build_hero_card_rows(name, dead_variant="fallen"):
    """Generates an array of strings representing a 100-col boxed card for one hero."""
    data = HERO_TRI_STATES[name]
    role = data["role"]
    norm_rows = data["normal"]
    inj_rows = data["injured"]
    dead_rows = data["dead"] if dead_variant == "fallen" else data["dead_standing"]

    lines = []
    # Outer top border
    lines.append("\033[1;30m+" + "=" * 98 + "+\033[0m")

    # Hero Title Banner
    h_idx = HERO_ORDER.index(name) + 1
    title_str = f" [HERO {h_idx}/8] {name}  \033[1;30m[{role.upper()}]\033[1;37m"
    status_tag = "ANATOMICAL TRI-STATE CATALOG "
    inner_title = f"{title_str:<50}{status_tag:>46}"
    lines.append(f"\033[1;30m| \033[1;37m{fit_exact(inner_title, 96)}\033[1;30m |\033[0m")

    # Column Dividers
    div_mid = "\033[1;30m+" + "-" * 32 + "+" + "-" * 32 + "+" + "-" * 32 + "+\033[0m"
    lines.append(div_mid)

    # 3 Column Headers
    hdr1 = "\033[1;32m  [1] THƯỜNG (VIBRANT INTACT)   \033[0m"
    hdr2 = "\033[1;33m  [2] CHẤN THƯƠNG (HỔ PHÁCH)    \033[0m"
    dead_label = "TỬ VONG (GỤC NGÃ)" if dead_variant == "fallen" else "TỬ VONG (TRO XÁM)"
    hdr3 = f"\033[1;31m  [3] {dead_label:<24}\033[0m"
    lines.append(f"\033[1;30m|{fit_exact(hdr1, 32)}\033[1;30m|{fit_exact(hdr2, 32)}\033[1;30m|{fit_exact(hdr3, 32)}\033[1;30m|\033[0m")
    lines.append(div_mid)

    # 12 Sprite Rows
    for r in range(12):
        r_norm = norm_rows[r] if r < len(norm_rows) else " " * 29
        r_inj  = inj_rows[r] if r < len(inj_rows) else " " * 29
        r_dead = dead_rows[r] if r < len(dead_rows) else " " * 29

        c1 = fit_exact(" " + r_norm + "  ", 32)
        c2 = fit_exact(" " + r_inj + "  ", 32)
        c3 = fit_exact(" " + r_dead + "  ", 32)
        lines.append(f"\033[1;30m|{c1}\033[1;30m|{c2}\033[1;30m|{c3}\033[1;30m|\033[0m")

    # State Sub-Captions
    lines.append(div_mid)
    s1 = fit_exact(" " + data["desc_normal"], 32)
    s2 = fit_exact(" " + data["desc_injured"], 32)
    s3 = fit_exact(" " + data["desc_dead"], 32)
    lines.append(f"\033[1;30m|\033[0;37m{s1}\033[1;30m|\033[0;33m{s2}\033[1;30m|\033[0;31m{s3}\033[1;30m|\033[0m")

    # Lore Footnote
    lines.append(div_mid)
    lore_str = f" \033[1;36mGHI CHÚ GIẢI PHẪU:\033[0;37m {data['lore']}"
    lines.append(f"\033[1;30m|{fit_exact(lore_str, 98)}\033[1;30m|\033[0m")

    # Outer bottom border
    lines.append("\033[1;30m+" + "=" * 98 + "+\033[0m")
    return lines

def print_all_heroes():
    """Prints all 8 heroes sequentially to stdout."""
    # Top Showcase Header
    print("\033[1;30m+" + "=" * 98 + "+\033[0m")
    banner = "FEAR & HUNGER: DANH MỤC 3 MODEL NHÂN VẬT (THƯỜNG / CHẤN THƯƠNG / TỬ VONG)"
    print(f"\033[1;30m| \033[1;33m{fit_exact(banner, 96)}\033[1;30m |\033[0m")
    rule = "QUY TẮC: [THƯỜNG] Sung sức | [CHẤN THƯƠNG] Khớp hổ phách #FFAA28 | [TỬ VONG] Gục ngã tro xám #6E7378"
    print(f"\033[1;30m| \033[0;36m{fit_exact(rule, 96)}\033[1;30m |\033[0m")
    print("\033[1;30m+" + "=" * 98 + "+\033[0m\n")

    for idx, name in enumerate(HERO_ORDER):
        card = build_hero_card_rows(name, dead_variant="fallen")
        for line in card:
            print(line)
        print() # Spacer between heroes

def run_interactive_viewer(start_idx=0):
    """Runs full-screen single hero viewer (strictly <= 35 rows, 100 cols)."""
    if os.name == 'nt':
        import msvcrt

    hero_idx = start_idx
    dead_mode = "fallen" # "fallen" or "standing"

    dui.clear_screen()

    while True:
        name = HERO_ORDER[hero_idx]
        card = build_hero_card_rows(name, dead_variant=dead_mode)

        # Header bar (2 rows)
        frame = []
        hdr_top = "\033[1;30m+" + "=" * 98 + "+\033[0m"
        mode_str = f"XEM CHI TIẾT MODEL HERO {hero_idx + 1}/8 | DẠNG TỬ VONG: {dead_mode.upper()}"
        frame.append(hdr_top)
        frame.append(f"\033[1;30m| \033[1;33m{fit_exact(mode_str, 96)}\033[1;30m |\033[0m")

        # Add the card lines (skipping outer borders if needed, or including them)
        # Card has 19 lines. Total so far: 2 + 19 = 21 lines.
        frame.extend(card)

        # Controls footer (3 lines)
        frame.append("\033[1;30m+" + "-" * 98 + "+\033[0m")
        ctrls = " [W/S] Đổi Hero  |  [M] Đổi Dạng Tử Vong (Gục Sàn / Tro Xám)  |  [A] In Toàn Bộ 8 Hero  |  [Q] Thoát"
        frame.append(f"\033[1;30m|{fit_exact(ctrls, 98)}\033[1;30m|\033[0m")
        frame.append("\033[1;30m+" + "=" * 98 + "+\033[0m")

        dui.atomic_blit(frame)

        if not (os.name == 'nt' and sys.stdin.isatty()):
            # Headless / batch mode
            break

        ch = msvcrt.getch()
        if ch in (b'\x00', b'\xe0'):
            ch = msvcrt.getch()
            if ch == b'H': # Up
                hero_idx = (hero_idx - 1) % len(HERO_ORDER)
            elif ch == b'P': # Down
                hero_idx = (hero_idx + 1) % len(HERO_ORDER)
        elif ch in (b'w', b'W'):
            hero_idx = (hero_idx - 1) % len(HERO_ORDER)
        elif ch in (b's', b'S'):
            hero_idx = (hero_idx + 1) % len(HERO_ORDER)
        elif ch in (b'm', b'M'):
            dead_mode = "standing" if dead_mode == "fallen" else "fallen"
        elif ch in (b'a', b'A'):
            dui.clear_screen()
            print_all_heroes()
            print("Nhấn phím bất kỳ để quay lại chế độ xem chi tiết...")
            msvcrt.getch()
            dui.clear_screen()
        elif ch in (b'q', b'Q', b'\x1b', b'\r'):
            break

def main():
    # If run with --interactive or -i
    if "--interactive" in sys.argv or "-i" in sys.argv:
        run_interactive_viewer()
        return

    # Default mode: High-Speed Print All Heroes
    print_all_heroes()

    # If running interactively from console, offer quick inspect or exit
    if os.name == 'nt' and sys.stdin.isatty():
        print("\033[1;37m[ĐIỀU HƯỚNG NHANH]:\033[0m")
        print("  - Nhập \033[1;33m[1-8]\033[0m để xem chi tiết phóng to từng nhân vật")
        print("  - Nhấn \033[1;32m[Enter]\033[0m hoặc \033[1;31m[Q]\033[0m để thoát")
        try:
            choice = input("\nLựa chọn của bạn: ").strip()
            if choice.isdigit() and 1 <= int(choice) <= 8:
                run_interactive_viewer(int(choice) - 1)
        except (KeyboardInterrupt, EOFError):
            pass

if __name__ == "__main__":
    main()
