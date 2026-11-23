#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
================================================================================
FEAR & HUNGER: 36-MONSTER TRI-STATE MORPHOLOGY SHOWCASE & VIEWER
Hardware Inspection: NORMAL (Trắng nguyên vẹn) vs INJURED (Hổ phách) vs DEAD (Tro xám)
================================================================================
Displays the 3 distinct anatomical states for all 36 Labyrinth Monsters:
  1. MODEL THƯỜNG       : Phosphor White (#FFFFFF), tư thế đứng nguyên vẹn.
  2. MODEL CHẤN THƯƠNG  : Technical Amber (#FFAA28), gãy vũ khí, khớp rách hổ phách, khụy gối.
  3. MODEL TỬ VONG      : Deactivated Ash Gray (#6E7378), đầu lìa hoặc gục ngã hoàn toàn.
================================================================================
"""

import sys
import os
import re
import json
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from monsters_catalog import ALL_MONSTERS_CATALOG
import demo_interactive_ui as dui

ANSI_RE = re.compile(r'\x1b\[[0-9;]*[a-zA-Z]')

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

# Tải cơ sở dữ liệu sprite quái vật từ all_monster_sprites.json
SPRITES_JSON_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "all_monster_sprites.json")
with open(SPRITES_JSON_PATH, "r", encoding="utf-8") as f:
    ALL_MONSTER_SPRITES = json.load(f)

ARCHETYPE_DESCS = {
    "ARMORED":  "HỆ GIÁP NẶNG: -50% sát thương nhận. Đòn đánh có thể làm gãy vũ khí đối phương.",
    "SPECTRAL": "HỆ BÓNG MA: Miễn nhiễm sát thương vật lý nhẹ. Tấn công trừ trực tiếp Mind.",
    "TERROR":   "HỆ KINH HOÀNG: Phát tán Dread Aura gây hoảng loạn (-25 Mind/lượt).",
    "NORMAL":   "HỆ DÃ THÚ: Đòn cắn xé vật lý tàn bạo, có tỷ lệ gây chảy máu (-4 HP/lượt)."
}

def build_monster_card_rows(mid):
    """Tạo card 3 cột chuẩn xác 100 ký tự cho quái vật mid (1..36)."""
    s_mid = str(mid)
    m_sprite = ALL_MONSTER_SPRITES.get(s_mid, {})
    m_info = ALL_MONSTERS_CATALOG.get(mid, {
        "id": mid,
        "name": m_sprite.get("name", f"FOE #{mid}"),
        "archetype": "NORMAL",
        "hp": 100,
        "atk": 20,
        "def": 12
    })

    name = m_info.get("name", m_sprite.get("name", f"MONSTER #{mid}"))
    archetype = m_info.get("archetype", "NORMAL")
    hp = m_info.get("hp", 100)
    atk = m_info.get("atk", 20)
    defense = m_info.get("def", 12)
    is_boss = m_info.get("is_boss", False)
    is_mimic = m_info.get("is_mimic", False)

    norm_rows = m_sprite.get("normal", [])
    inj_rows = m_sprite.get("injured", [])
    dead_rows = m_sprite.get("dead", [])

    lines = []
    # Viền trên cùng (Border Top)
    lines.append("\033[1;30m+" + "=" * 98 + "+\033[0m")

    # Banner Tiêu đề quái vật
    tag_archetype = f"[{archetype}]"
    if is_boss:
        badge = "\033[1;31m★ TRÙM MÊ CUNG (BOSS)\033[0m"
    elif is_mimic:
        badge = "\033[1;33m⚠ RƯƠNG QUỶ (MIMIC)\033[0m"
    else:
        badge = f"\033[1;36m{tag_archetype}\033[0m"

    title_left = f" [FOE {mid:2d}/36] \033[1;37m{name:<22}\033[0m {badge}"
    stats_right = f"\033[1;32mHP: {hp:3d}\033[0m | \033[1;31mATK: {atk:2d}\033[0m | \033[1;34mDEF: {defense:2d}\033[0m"
    vl_left = vis_len(title_left)
    vl_right = vis_len(stats_right)
    gap = max(1, 96 - vl_left - vl_right)
    banner_content = title_left + (" " * gap) + stats_right
    lines.append(f"\033[1;30m| \033[0m{fit_exact(banner_content, 96)}\033[1;30m |\033[0m")

    # Đường phân cách 3 cột
    div_mid = "\033[1;30m+" + "-" * 32 + "+" + "-" * 32 + "+" + "-" * 32 + "+\033[0m"
    lines.append(div_mid)

    # Tiêu đề 3 trạng thái
    hdr1 = "\033[1;32m  [1] THƯỜNG (PHOSPHOR TRẮNG)   \033[0m"
    hdr2 = "\033[1;33m  [2] CHẤN THƯƠNG (HỔ PHÁCH)    \033[0m"
    hdr3 = "\033[1;31m  [3] TỬ VONG (TRO XÁM)         \033[0m"
    lines.append(f"\033[1;30m|{fit_exact(hdr1, 32)}\033[1;30m|{fit_exact(hdr2, 32)}\033[1;30m|{fit_exact(hdr3, 32)}\033[1;30m|\033[0m")
    lines.append(div_mid)

    # 11 dòng sprite của quái vật
    num_rows = max(len(norm_rows), len(inj_rows), len(dead_rows), 11)
    for r in range(num_rows):
        r_norm = norm_rows[r] if r < len(norm_rows) else " " * 24
        r_inj  = inj_rows[r] if r < len(inj_rows) else " " * 24
        r_dead = dead_rows[r] if r < len(dead_rows) else " " * 24

        c1 = fit_exact("    " + r_norm, 32)
        c2 = fit_exact("    " + r_inj, 32)
        c3 = fit_exact("    " + r_dead, 32)
        lines.append(f"\033[1;30m|{c1}\033[1;30m|{c2}\033[1;30m|{c3}\033[1;30m|\033[0m")

    # Dòng phụ chú thích 3 trạng thái
    lines.append(div_mid)
    s1 = fit_exact(" Nguyên vẹn, sẵn sàng ra đòn", 32)
    s2 = fit_exact(" Gãy vũ khí / Khớp hổ phách", 32)
    s3 = fit_exact(" Gục ngã / Đầu lìa / Tiêu diệt", 32)
    lines.append(f"\033[1;30m|\033[0;37m{s1}\033[1;30m|\033[0;33m{s2}\033[1;30m|\033[0;31m{s3}\033[1;30m|\033[0m")

    # Dòng ghi chú cơ chế giải phẫu
    lines.append(div_mid)
    lore_text = ARCHETYPE_DESCS.get(archetype, "Đòn tấn công hầm ngục tiêu chuẩn.")
    mech_str = f" \033[1;36mCƠ CHẾ GIẢI PHẪU:\033[0;37m {lore_text}"
    lines.append(f"\033[1;30m|{fit_exact(mech_str, 98)}\033[1;30m|\033[0m")

    # Viền đáy
    lines.append("\033[1;30m+" + "=" * 98 + "+\033[0m")
    return lines

def print_all_monsters():
    """In toàn bộ 36 quái vật tuần tự ra terminal để người dùng cuộn xem."""
    print("\033[1;30m+" + "=" * 98 + "+\033[0m")
    banner = "FEAR & HUNGER: TOÀN BỘ 36 MODEL QUÁI VẬT 3 TRẠNG THÁI (NORMAL / INJURED / DEAD)"
    print(f"\033[1;30m| \033[1;33m{fit_exact(banner, 96)}\033[1;30m |\033[0m")
    rule = "QUY TẮC: [THƯỜNG] Trắng nguyên vẹn | [CHẤN THƯƠNG] Khớp hổ phách #FFAA28 | [TỬ VONG] Tro xám #6E7378"
    print(f"\033[1;30m| \033[0;36m{fit_exact(rule, 96)}\033[1;30m |\033[0m")
    print("\033[1;30m+" + "=" * 98 + "+\033[0m\n")

    for mid in range(1, 37):
        card = build_monster_card_rows(mid)
        for line in card:
            print(line)
        print()  # Khoảng cách giữa các quái vật

def run_interactive_viewer(start_id=1):
    """Trình duyệt tương tác phóng to từng quái vật (chuẩn 100 cột, không trôi dòng)."""
    if os.name == 'nt':
        import msvcrt

    cur_id = max(1, min(36, start_id))
    dui.clear_screen()

    while True:
        card = build_monster_card_rows(cur_id)
        frame = []

        # Header bar
        hdr_top = "\033[1;30m+" + "=" * 98 + "+\033[0m"
        mode_str = f"XEM CHI TIẾT MODEL QUÁI VẬT {cur_id:2d}/36 - TRI-STATE ANATOMICAL VIEWER"
        frame.append(hdr_top)
        frame.append(f"\033[1;30m| \033[1;33m{fit_exact(mode_str, 96)}\033[1;30m |\033[0m")

        frame.extend(card)

        # Footer controls
        frame.append("\033[1;30m+" + "-" * 98 + "+\033[0m")
        ctrls = " [W/S / Mũi tên] Chuyển Quái  |  [A] In Toàn Bộ 36 Quái  |  [1..36] Nhập Số Quái  |  [Q/Esc] Thoát"
        frame.append(f"\033[1;30m|{fit_exact(ctrls, 98)}\033[1;30m|\033[0m")
        frame.append("\033[1;30m+" + "=" * 98 + "+\033[0m")

        dui.atomic_blit(frame)

        if not (os.name == 'nt' and sys.stdin.isatty()):
            break

        ch = msvcrt.getch()
        while msvcrt.kbhit():
            msvcrt.getch()

        if ch in (b'\x00', b'\xe0'):
            ext = msvcrt.getch()
            if ext in (b'H', b'K'):    # Up or Left
                cur_id = 36 if cur_id <= 1 else (cur_id - 1)
            elif ext in (b'P', b'M'):  # Down or Right
                cur_id = 1 if cur_id >= 36 else (cur_id + 1)
        elif ch in (b'w', b'W'):
            cur_id = 36 if cur_id <= 1 else (cur_id - 1)
        elif ch in (b's', b'S'):
            cur_id = 1 if cur_id >= 36 else (cur_id + 1)
        elif ch in (b'a', b'A'):
            dui.clear_screen()
            print_all_monsters()
            print("Nhấn phím bất kỳ để quay lại chế độ xem chi tiết...")
            msvcrt.getch()
            dui.clear_screen()
        elif ch in (b'q', b'Q', b'\x1b'):
            break

def main():
    if "--interactive" in sys.argv or "-i" in sys.argv:
        run_interactive_viewer(1)
        return

    # In toàn bộ 36 quái vật
    print_all_monsters()

    # Nếu chạy tương tác từ console, hiển thị tùy chọn điều hướng nhanh
    if os.name == 'nt' and sys.stdin.isatty():
        print("\033[1;37m[ĐIỀU HƯỚNG NHANH]:\033[0m")
        print("  - Nhập \033[1;33m[1-36]\033[0m để xem phóng to chi tiết quái vật đó")
        print("  - Nhập \033[1;32m[V]\033[0m để vào chế độ duyệt tương tác bằng phím [W/S]")
        print("  - Nhấn \033[1;31m[Enter]\033[0m hoặc \033[1;31m[Q]\033[0m để thoát")
        try:
            choice = input("\nLựa chọn của bạn: ").strip().lower()
            if choice == 'v':
                run_interactive_viewer(1)
            elif choice.isdigit() and 1 <= int(choice) <= 36:
                run_interactive_viewer(int(choice))
        except (KeyboardInterrupt, EOFError):
            pass

if __name__ == "__main__":
    main()
