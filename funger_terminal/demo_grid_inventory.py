#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
================================================================================
CANONICAL SURVIVAL POUCH & ITEM STASH (TỦ ĐỒ CHUẨN 100 CỘT ĐỒNG NHẤT VỚI CHỌN HERO)
Fear & Hunger: Terminal Labyrinth - Solo Explorer Architecture
================================================================================
Quy hoạch giao diện và cơ chế điều khiển giống y hệt 100% với Bộ Chọn Hero:
  - Chiều ngang: Đúng 100 cột chuẩn (cols=100).
  - Chiều cao: Đúng 23 dòng (<= 35 dòng, chống trôi màn hình 100%).
  - Khung bên trái (34 cột): Danh sách vật phẩm có con trỏ sáng ▶, số lượng (xN),
    phím tắt [W/S] điều hướng, [Enter] sử dụng, [Q] đóng túi.
  - Khung bên phải (64 cột):
    * Bên trái: Mô hình Pixel Art kích thước lớn (29 cột x 12 dòng) chọn lọc
      từ các bảng sprite 1-bit (Bánh mì, Thịt khô, Hoa anh túc, Rượu, Cổ vật...).
    * Bên phải: Bảng thông số chi tiết (Loại, Hiệu ứng, Khắc phục chấn thương, Độ hiếm).
    * Phía dưới: Khung Giám Định Cổ Vật & Cốt Truyện 3 dòng sắc nét.
================================================================================
"""

import sys
import os
import re
import copy
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import demo_interactive_ui as dui
from item_model_catalog import ITEM_CATALOG

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

def render_pouch_screen(items, sel_idx, status_msg="", hero=None):
    """
    Kết xuất giao diện Tủ Đồ / Túi đồ sinh tồn chuẩn 100 cột,
    cấu trúc và tỷ lệ giống y hệt render_solo_select_screen.
    """
    cur_it = items[sel_idx]
    it_sprite = cur_it["sprite"]

    b1_top = "\033[1;30m+" + "-" * 32 + "+\033[0m"
    b2_top = "\033[1;30m+" + "-" * 62 + "+\033[0m"

    header_rows = [
        "\033[1;30m+" + "=" * 98 + "+\033[0m",
        f"\033[1;30m| \033[1;37m{fit_exact('FEAR & HUNGER: SURVIVAL POUCH & ITEM STASH - SELECT ITEM TO USE', 96)}\033[1;30m |\033[0m",
        "\033[1;30m+" + "=" * 98 + "+\033[0m",
        f"{b1_top}  {b2_top}"
    ]

    # Khung trái (30 ký tự nội dung)
    b1_lines = [
        "\033[1;33mSURVIVAL POUCH (W/S):\033[0m",
        ""
    ]
    for idx, it in enumerate(items):
        is_cur = (idx == sel_idx)
        num_str = f"{idx+1}" if idx < 9 else "0"
        qty_str = f"x{it['qty']}" if it['qty'] > 0 else "\033[1;31mHẾT\033[0m"
        tag = f"[{num_str}] {it['name'][:13]:<13} ({qty_str})"
        if is_cur:
            b1_lines.append(f"\033[1;32m▶ {tag}\033[0m")
        else:
            b1_lines.append(f"\033[90m  {tag}\033[0m")

    b1_lines.extend([
        "",
        "\033[1;33m[CONTROLS]:\033[0m",
        "\033[1;37m[W/S]\033[0m   : Navigate Items",
        "\033[1;32m[Enter]\033[0m : Administer / Use",
        "\033[1;31m[Q]\033[0m     : Close Pouch",
        ""
    ])

    # Dòng thông tin hero nếu có
    hero_line1 = ""
    hero_line2 = ""
    if hero:
        h_name = hero.get('name', 'HERO')[:6]
        h_hp = hero.get('hp', 100)
        h_mhp = hero.get('max_hp', 100)
        hero_line1 = f"\033[1;36mHERO   : {h_name} HP:{h_hp}/{h_mhp}\033[0m"
        h_mind = hero.get('mind', 100)
        h_hngr = hero.get('hunger', 0)
        deb_cnt = len(hero.get('debuffs', []))
        deb_str = f"{deb_cnt} debuff" if deb_cnt > 0 else "Lành lặn"
        hero_line2 = f"\033[1;35mMIND   : {h_mind} | ĐÓI:{h_hngr} ({deb_str})\033[0m"

    # Khung phải: 12 dòng Mô hình Sprite (29 cột) + 2 khoảng cách + Thông số (29 cột) = 60 cột
    stats_data = [
        f"\033[1;33mNAME   : \033[1;37m{cur_it['name']}\033[0m",
        f"\033[1;33mTYPE   : \033[1;37m{cur_it['type']}\033[0m",
        f"\033[1;32mQTY    : {cur_it['qty']} in Pouch (Max: {cur_it['max_qty']})\033[0m",
        f"\033[1;31mEFFECT : {cur_it['effect'][:20]}\033[0m",
        f"\033[1;36mCURES  : {cur_it['cure'][:20]}\033[0m",
        f"\033[1;37mTARGET : {cur_it['target'][:20]}\033[0m",
        f"\033[1;35mUSAGE  : {cur_it['usage'][:20]}\033[0m",
        f"\033[1;33mRARITY : {cur_it['rarity'][:20]}\033[0m",
        "",
        f"\033[1;32mSTATUS : Sẵn sàng sử dụng\033[0m" if cur_it['qty'] > 0 else "\033[1;31mSTATUS : Đã dùng hết vật phẩm!\033[0m",
        hero_line1,
        hero_line2
    ]

    b2_lines = []
    for r in range(12):
        sp_line = it_sprite[r] if r < len(it_sprite) else " " * 29
        stat_line = stats_data[r] if r < len(stats_data) else ""
        b2_lines.append(f"{fit_exact(sp_line, 29)}  {fit_exact(stat_line, 29)}")

    # Đường phân cách bên trong khung phải
    b2_lines.append("\033[1;30m" + "-" * 60 + "\033[0m")
    b2_lines.append("\033[1;33m[ITEM LORE & EXPEDITION UTILITY]:\033[0m")
    for l_line in cur_it["lore"][:3]:
        b2_lines.append(f"\033[1;37m{l_line}\033[0m")

    # Lắp ghép các dòng (17 dòng nội dung)
    all_rows = list(header_rows)
    for i in range(17):
        l1 = b1_lines[i] if i < len(b1_lines) else ""
        l2 = b2_lines[i] if i < len(b2_lines) else ""
        comb = f"\033[1;30m| \033[0m{fit_exact(l1, 30)}\033[1;30m |  | \033[0m{fit_exact(l2, 60)}\033[1;30m |\033[0m"
        all_rows.append(comb)

    all_rows.append(f"{b1_top}  {b2_top}")
    
    if status_msg:
        all_rows.append(f"\033[1;30m| \033[1;33m{fit_exact(status_msg, 96)}\033[1;30m |\033[0m")
    else:
        all_rows.append("\033[1;30m+" + "=" * 98 + "+\033[0m")

    return all_rows

def run_pouch_interactive(initial_items=None, hero=None, inv_dict=None, is_hardcore=False):
    """
    Vòng lặp tương tác túi đồ chuẩn 100 cột với điều khiển W/S, số, Enter, Q.
    Đồng bộ trực tiếp với hero và inv_dict nếu được truyền vào.
    """
    items = copy.deepcopy(initial_items if initial_items is not None else ITEM_CATALOG)
    if inv_dict is not None:
        for it in items:
            if it["id"] in inv_dict:
                it["qty"] = inv_dict[it["id"]]

    sel_idx = 0
    num_items = len(items)
    status_msg = ""
    last_used = None

    dui.clear_screen()
    print("\033[?25l", end="", flush=True)

    try:
        while True:
            frame = render_pouch_screen(items, sel_idx, status_msg, hero=hero)
            dui.atomic_blit(frame)

            if not (os.name == 'nt' and sys.stdin.isatty()):
                return items, items[sel_idx]

            ch = msvcrt.getch()
            while msvcrt.kbhit():
                msvcrt.getch()

            status_msg = ""

            # Phím Mũi tên
            if ch in (b'\x00', b'\xe0'):
                ext = msvcrt.getch()
                if ext in (b'H', b'K'):  # Lên hoặc Trái
                    sel_idx = (sel_idx - 1) % num_items
                elif ext in (b'P', b'M'):  # Xuống hoặc Phải
                    sel_idx = (sel_idx + 1) % num_items

            # Phím W/S / A/D
            elif ch in (b'w', b'W', b'a', b'A'):
                sel_idx = (sel_idx - 1) % num_items
            elif ch in (b's', b'S', b'd', b'D'):
                sel_idx = (sel_idx + 1) % num_items

            # Phím số 1-9, 0 (nhảy nhanh)
            elif ch in (b'1', b'2', b'3', b'4', b'5', b'6', b'7', b'8', b'9'):
                val = int(ch.decode('ascii')) - 1
                if val < num_items:
                    sel_idx = val
            elif ch in (b'0',):
                if num_items >= 10:
                    sel_idx = 9

            # Sử dụng vật phẩm [Enter] / [Space]
            elif ch in (b'\r', b'\n', b' '):
                cur_it = items[sel_idx]
                if cur_it["qty"] > 0:
                    cur_it["qty"] -= 1
                    if inv_dict is not None and cur_it["id"] in inv_dict:
                        inv_dict[cur_it["id"]] = cur_it["qty"]
                    last_used = cur_it

                    if cur_it["id"] == "totem":
                        if hero is not None:
                            if "debuffs" in hero:
                                hero["debuffs"].clear()
                            if "severed_limbs" in hero:
                                hero["severed_limbs"] = {"head": 100, "torso": 100, "arm_r": 100, "arm_l": 100, "leg_r": 100, "leg_l": 100}
                            hero["hp"] = hero.get("max_hp", 100)
                        status_msg = f"★ [KÍCH HOẠT TOTEM OF UNDYING]: Tái sinh toàn bộ tứ chi bị đứt! Sinh lực hồi phục 100%!"

                    elif cur_it["id"] == "bread":
                        if hero is not None:
                            hero["hunger"] = max(0, hero.get("hunger", 0) - 40)
                        status_msg = f"● [BÁNH MÌ MỐC]: Đã ăn lương khô! Cơn đói khát giảm -40 điểm!"

                    elif cur_it["id"] == "meat":
                        if hero is not None:
                            hero["hunger"] = max(0, hero.get("hunger", 0) - 60)
                            hero["hp"] = min(hero.get("max_hp", 100), hero.get("hp", 0) + 20)
                        status_msg = f"● [THỊT SẤY KHÔ]: Đã ăn thịt muối! -60 Đói và hồi phục +20 HP!"

                    elif cur_it["id"] == "ale":
                        if hero is not None:
                            hero["mind"] = min(hero.get("max_mind", 100), hero.get("mind", 100) + 35)
                        status_msg = f"● [RƯỢU CỔ]: Uống vại rượu sồi! +35 Mind, nỗi kinh hoàng tan biến!"

                    elif cur_it["id"] == "vial":
                        if hero is not None and "debuffs" in hero:
                            for deb in ["infection", "poison", "gangrene", "bleeding"]:
                                if deb in hero["debuffs"]:
                                    hero["debuffs"].remove(deb)
                        status_msg = f"● [BÌNH CỒN]: Rót cồn sát trùng! Xóa bỏ xuất huyết, hoại tử và độc tố!"

                    elif cur_it["id"] == "key":
                        status_msg = f"● [CHÌA KHÓA]: Cần đến Cổng Thoát Hiểm Phía Đông để tra chìa mở khóa!"
                else:
                    status_msg = f"✖ [HẾT VẬT PHẨM]: Bạn không còn {cur_it['name']} trong túi đồ!"

            # Đóng túi đồ [Q] / [Esc]
            elif ch in (b'q', b'Q', b'\x1b'):
                return items, last_used

    finally:
        print("\033[?25h", end="", flush=True)

def main():
    items, used = run_pouch_interactive()
    dui.clear_screen()
    print("\033[1;30m+====================================================================================================+\033[0m")
    print(f"\033[1;30m| \033[1;32m{fit_exact(' [ĐÓNG TỦ ĐỒ / TÚI SINH TỒN]: Đã quay trở về trạng thái khám phá hầm ngục!', 96)}\033[1;30m |\033[0m")
    print("\033[1;30m+====================================================================================================+\033[0m")
    print("\n  Số lượng vật phẩm hiện tại trong túi đồ:")
    for it in items:
        q_str = f"{it['qty']}/{it['max_qty']}"
        print(f"   - {it['name']:<18} : \033[1;33m{q_str}\033[0m ({it['type']})")
    print("\n\033[1;30m+----------------------------------------------------------------------------------------------------+\033[0m")
    print("  \033[1;37m[1]\033[0m Mở lại Tủ đồ & Túi sinh tồn")
    print("  \033[1;37m[Q]\033[0m Thoát ra ngoài")
    print("\033[1;30m+====================================================================================================+\033[0m")

    if os.name == 'nt' and sys.stdin.isatty():
        choice = input("\nLựa chọn của bạn [1/Q]: ").strip().lower()
        if choice == '1':
            main()
        else:
            print("[OK] Đã đóng túi đồ.")

if __name__ == "__main__":
    main()
