#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
================================================================================
CALCULATED 4-HERO ROW SELECTION ARCHITECTURE (ĐÚNG CHUẨN TÍNH TOÁN 4 NHÂN VẬT/HÀNG)
Fear & Hunger: Terminal Labyrinth - Solo Explorer Architecture
================================================================================
BẢNG TÍNH TOÁN KÍCH THƯỚC Ô (FORMULA SPECIFICATION):
  1. Chiều rộng Mô hình Sprite (Model):
     - Rộng tối đa của tất cả 8 Hero: 29 ký tự.
     - Đệm an toàn (Padding): 1 ký tự trái + 1 ký tự phải = 2 ký tự.
     => Chiều rộng tối thiểu cho Model = 29 + 2 = 31 ký tự.

  2. Chiều rộng Thông tin phụ (HP, ATK, DEF, DODGE, TRAIT, SKILL):
     - Dòng 1 (HP & ATK): ' HP: 120/120 | ATK: 32 DMG' = 25 ký tự (<= 31).
     - Dòng 2 (DEF & DODGE): ' DEF: 18     | DOD: 25%' = 23 ký tự (<= 31).
     - Dòng 3 (TRAIT): ' TRAIT: Deep Pockets' = 21 ký tự (<= 31).
     - Dòng 4 (SKILL): ' SKILL: TWIN DAGGERS' = 20 ký tự (<= 31).
     => Toàn bộ thông số phụ nằm gọn 100% trong 31 ký tự mà không bị cắt chữ.

  3. Công thức nhân 4 nhân vật trên một hàng:
     - 4 ô nội dung: 31 x 4 = 124 ký tự.
     - 5 ký tự đường viền ngăn ('|' trái, 3 '|' giữa, '|' phải) = 5 ký tự.
     => TỔNG CHIỀU RỘNG CHÍNH XÁC = 124 + 5 = 129 CỘT!

  4. Chiều cao an toàn:
     - 28 dòng (<= 35 dòng) => Tuyệt đối không bao giờ cuộn trang (Zero Scroll).
     - Hàng 1 (Trang 1): 4 nhân vật đầu (Cahara, D'Arce, Enki, Ragnvaldr).
     - Hàng 2 (Trang 2): 4 nhân vật sau (Le'Garde, Moonless, The Girl, Nas'hrah).
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
CARD_WIDTHS = [31, 31, 31, 31]
TOTAL_WIDTH = sum(CARD_WIDTHS) + 5  # 124 + 5 = 129 CỘT

def render_4hero_row_screen(sel_idx):
    """
    Kết xuất màn hình chọn Hero chuẩn toán học 129 cột:
    4 nhân vật trên 1 hàng, 31 ký tự/ô, 0% cắt xén, 0% tràn dòng.
    """
    page = sel_idx // 4
    start = page * 4
    p_heroes = [HEROES[start + i] for i in range(4)]
    active_h = HEROES[sel_idx]

    lines = []
    # Viền trên cùng (129 cột)
    lines.append("\033[1;30m+" + "=" * (TOTAL_WIDTH - 2) + "+\033[0m")
    
    # Tiêu đề chính & thanh trạng thái trang
    t_str = f"FEAR & HUNGER: SOLO SURVIVOR EXPEDITION - CHỌN EXPLORER (TRANG {page+1}/2)"
    sub_t = "[W/S: LẬT TRANG 1-4/5-8  |  A/D: ĐỔI HERO  |  1-8: NHẢY SỐ]"
    hdr = f" \033[1;37m{t_str:<76}\033[1;33m{sub_t:>48} "
    lines.append(f"\033[1;30m|{fit_exact(hdr, TOTAL_WIDTH - 2)}\033[1;30m|\033[0m")

    # Đường phân cách 4 ô: +-------------------------------+...
    div_4 = "\033[1;30m+" + "+".join(["-" * w for w in CARD_WIDTHS]) + "+\033[0m"
    lines.append(div_4)

    # Dòng Nhãn / Tên nhân vật của 4 ô
    b_cells = []
    for i, w in enumerate(CARD_WIDTHS):
        h = p_heroes[i]
        real_idx = HEROES.index(h)
        is_cur = (real_idx == sel_idx)
        tag = f"[{h['id']}] {h['name']} ({h['role'].split()[0]})"
        txt = f"\033[1;32m▶ {tag}\033[0m" if is_cur else f"\033[90m  {tag}\033[0m"
        b_cells.append(fit_exact(txt, w))
    lines.append(f"\033[1;30m|{'|'.join(b_cells)}|\033[0m")
    lines.append(div_4)

    # 12 Dòng Mô hình Pixel của 4 nhân vật (Model rộng đúng 29 ký tự)
    # 31 ký tự = 1 khoảng trắng trái + 29 ký tự sprite + 1 khoảng trắng phải
    for r in range(12):
        r_cells = []
        for i, w in enumerate(CARD_WIDTHS):
            h = p_heroes[i]
            spr = HERO_TRI_STATES[h["name"]]["normal"]
            sp_line = spr[r] if r < len(spr) else " " * 29
            cell_str = " " + sp_line + " "
            r_cells.append(fit_exact(cell_str, w))
        lines.append(f"\033[1;30m|{'|'.join(r_cells)}|\033[0m")

    lines.append(div_4)

    # Dòng Thông số 1: HP & ATK
    s1_cells = []
    for i, w in enumerate(CARD_WIDTHS):
        h = p_heroes[i]
        txt = f" \033[1;32mHP: {h['hp']:3d}/{h['max_hp']:3d}\033[0m | \033[1;31mATK: {h['atk']:2d} DMG\033[0m"
        s1_cells.append(fit_exact(txt, w))
    lines.append(f"\033[1;30m|{'|'.join(s1_cells)}|\033[0m")

    # Dòng Thông số 2: DEF & DODGE
    s2_cells = []
    for i, w in enumerate(CARD_WIDTHS):
        h = p_heroes[i]
        txt = f" \033[1;36mDEF: {h['def']:2d}\033[0m     | \033[1;35mDOD: {int(h['dodge_rate']*100):2d}%\033[0m"
        s2_cells.append(fit_exact(txt, w))
    lines.append(f"\033[1;30m|{'|'.join(s2_cells)}|\033[0m")

    # Dòng Thông số 3: TRAIT (Đặc tính)
    s3_cells = []
    for i, w in enumerate(CARD_WIDTHS):
        h = p_heroes[i]
        txt = f" \033[1;33mTRAIT:\033[0m {h['trait'][:w-9]}"
        s3_cells.append(fit_exact(txt, w))
    lines.append(f"\033[1;30m|{'|'.join(s3_cells)}|\033[0m")

    # Dòng Thông số 4: SKILL (Kỹ năng)
    s4_cells = []
    for i, w in enumerate(CARD_WIDTHS):
        h = p_heroes[i]
        txt = f" \033[1;36mSKILL:\033[0m {h['skills'][0]['label'][:w-9]}"
        s4_cells.append(fit_exact(txt, w))
    lines.append(f"\033[1;30m|{'|'.join(s4_cells)}|\033[0m")

    lines.append("\033[1;30m+" + "=" * (TOTAL_WIDTH - 2) + "+\033[0m")

    # KHUNG HỒ SƠ CHI TIẾT NHÂN VẬT ĐANG CHỌN (Độ rộng 127 ký tự trong)
    ah = active_h
    d1 = f" \033[1;33mĐANG CHỌN:\033[1;37m {ah['name']} [{ah['role']}]\033[0m  |  \033[1;32mHP: {ah['hp']}/{ah['max_hp']}\033[0m  |  \033[1;31mATK: {ah['atk']} DMG\033[0m  |  \033[1;36mDEF: {ah['def']}\033[0m  |  \033[1;35mNÉ TRÁNH: {int(ah['dodge_rate']*100)}%\033[0m  |  \033[1;33mKHÁNG VẬT LÝ: {ah['phys_resist_str']}\033[0m"
    lines.append(f"\033[1;30m|{fit_exact(d1, TOTAL_WIDTH - 2)}\033[1;30m|\033[0m")

    d2 = f" \033[1;37mĐẶC TÍNH :\033[0m {ah['trait']:<30}  \033[1;32mCƯỜNG HÓA: {ah['item_buff_str']:<26}\033[0m  \033[1;36mKỸ NĂNG: [1] {ah['skills'][0]['label']}  [2] {ah['skills'][1]['label']}\033[0m"
    lines.append(f"\033[1;30m|{fit_exact(d2, TOTAL_WIDTH - 2)}\033[1;30m|\033[0m")

    assess = " ".join(ah["assessment"][:2])
    d3 = f" \033[1;33mĐÁNH GIÁ :\033[0;37m {assess[:114]}"
    lines.append(f"\033[1;30m|{fit_exact(d3, TOTAL_WIDTH - 2)}\033[1;30m|\033[0m")

    # Dòng Điều Khiển
    lines.append("\033[1;30m+" + "-" * (TOTAL_WIDTH - 2) + "+\033[0m")
    ctrls = " \033[90m[ĐIỀU KHIỂN]:\033[0m \033[1;37m[A/D / Mũi tên Trái/Phải]\033[0m Chọn Hero  |  \033[1;37m[W/S / Lên/Xuống]\033[0m Lật Trang (1-4 / 5-8)  |  \033[1;33m[1-8]\033[0m Nhảy số  |  \033[1;32m[Enter]\033[0m Chọn  |  \033[1;31m[Q]\033[0m Thoát"
    lines.append(f"\033[1;30m|{fit_exact(ctrls, TOTAL_WIDTH - 2)}\033[1;30m|\033[0m")
    lines.append("\033[1;30m+" + "=" * (TOTAL_WIDTH - 2) + "+\033[0m")

    return lines

def run_calculated_hero_select():
    sel_idx = 0
    num_heroes = len(HEROES)

    dui.clear_screen()
    print("\033[?25l", end="", flush=True)

    try:
        while True:
            frame = render_4hero_row_screen(sel_idx)
            dui.atomic_blit(frame)

            if not (os.name == 'nt' and sys.stdin.isatty()):
                return HEROES[sel_idx], sel_idx

            ch = msvcrt.getch()
            while msvcrt.kbhit():
                msvcrt.getch()

            # Phím Mũi tên
            if ch in (b'\x00', b'\xe0'):
                ext = msvcrt.getch()
                if ext == b'K':  # Trái
                    sel_idx = (sel_idx - 1) % num_heroes
                elif ext == b'M':  # Phải
                    sel_idx = (sel_idx + 1) % num_heroes
                elif ext == b'H':  # Lên -> lật trang
                    sel_idx = (sel_idx - 4) % num_heroes
                elif ext == b'P':  # Xuống -> lật trang
                    sel_idx = (sel_idx + 4) % num_heroes

            # Nhảy số trực tiếp 1-8
            elif ch in (b'1', b'2', b'3', b'4', b'5', b'6', b'7', b'8'):
                val = int(ch.decode('ascii')) - 1
                if val < num_heroes:
                    sel_idx = val

            # WASD
            elif ch in (b'a', b'A'):
                sel_idx = (sel_idx - 1) % num_heroes
            elif ch in (b'd', b'D'):
                sel_idx = (sel_idx + 1) % num_heroes
            elif ch in (b'w', b'W'):
                sel_idx = (sel_idx - 4) % num_heroes
            elif ch in (b's', b'S'):
                sel_idx = (sel_idx + 4) % num_heroes

            # Xác nhận chọn
            elif ch in (b'\r', b'\n', b' '):
                return HEROES[sel_idx], sel_idx

            # Thoát
            elif ch in (b'q', b'Q', b'\x1b'):
                return None, None

    finally:
        print("\033[?25h", end="", flush=True)

def main():
    hero, idx = run_calculated_hero_select()
    if hero is None:
        dui.clear_screen()
        print("\033[1;31m[THOÁT]: Bạn đã hủy chọn nhân vật.\033[0m")
        return

    dui.clear_screen()
    print("\033[1;30m+" + "=" * (TOTAL_WIDTH - 2) + "+\033[0m")
    title = f" [XÁC NHẬN CHỌN EXPLORER]: {hero['name']} [{hero['role']}]"
    print(f"\033[1;30m| \033[1;32m{fit_exact(title, TOTAL_WIDTH - 4)}\033[1;30m |\033[0m")
    print("\033[1;30m+" + "=" * (TOTAL_WIDTH - 2) + "+\033[0m")
    print(f"\n  Bạn đã chọn: \033[1;33m{hero['name']}\033[0m ({hero['role']})")
    print(f"  HP: {hero['hp']}/{hero['max_hp']}  |  ATK: {hero['atk']}  |  DEF: {hero['def']}  |  TRAIT: {hero['trait']}")
    print(f"  Đặc tính: {hero['item_buff_str']}")
    print(f"  Kỹ năng : [1] {hero['skills'][0]['label']}  |  [2] {hero['skills'][1]['label']}")
    print("\n\033[1;30m+" + "-" * (TOTAL_WIDTH - 2) + "+\033[0m")
    print("  \033[1;37m[1]\033[0m Khởi động chơi game thám hiểm Labyrinth ngay với Hero này")
    print("  \033[1;37m[2]\033[0m Thử nghiệm lại bộ chọn nhân vật (4 Nhân Vật / Hàng)")
    print("  \033[1;37m[Q]\033[0m Thoát ra ngoài")
    print("\033[1;30m+" + "=" * (TOTAL_WIDTH - 2) + "+\033[0m")

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
