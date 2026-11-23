#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
================================================================================
VERTICAL SURVIVAL POUCH - TÚI ĐỒ SINH TỒN HÀNG DỌC CHUẨN 100 CỘT
Fear & Hunger: Terminal Labyrinth - Solo Explorer Architecture
================================================================================
- Thiết kế hàng dọc tối giản, thẳng hàng, sạch đẹp, không lộn xộn.
- Điều khiển bằng W/S / Mũi tên lên xuống, Enter để sử dụng, I/Q/Esc để đóng.
- Chuẩn hóa 100 cột tuyệt đối, không tràn màn hình, không trôi dòng (<= 22 dòng).
- Đồng bộ hóa 100% thời gian thực với hero và inventory.
================================================================================
"""

import sys
import os
import re
import copy
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import demo_interactive_ui as dui

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

# BẢNG VẬT PHẨM CHUẨN HÓA CỦA GAME (7 VẬT PHẨM CHÍNH THỨC + NÚT ĐÓNG)
ITEM_CATALOG = [
    {
        "id": "totem",
        "name": "TOTEM OF UNDYING",
        "tag": "[CỔ VẬT]",
        "qty": 1,
        "desc": "Hồi sinh khi chết, đầy HP & mọc lại tứ chi"
    },
    {
        "id": "poppy",
        "name": "POPPY FLOWER",
        "tag": "[DƯỢC LIỆU]",
        "qty": 3,
        "desc": "Hồi +50 HP & cầm máu"
    },
    {
        "id": "weed",
        "name": "MEDICINAL HERB",
        "tag": "[THẢO DƯỢC]",
        "qty": 2,
        "desc": "Hồi +120 HP, giảm đau nhức"
    },
    {
        "id": "bread",
        "name": "MOLDY BREAD",
        "tag": "[LƯƠNG KHÔ]",
        "qty": 4,
        "desc": "Giảm -40 Đói (chống kiệt sức)"
    },
    {
        "id": "meat",
        "name": "DRIED MEAT",
        "tag": "[LƯƠNG KHÔ]",
        "qty": 2,
        "desc": "Giảm -60 Đói & hồi +20 HP"
    },
    {
        "id": "vial",
        "name": "ALCHEMICAL VIAL",
        "tag": "[CỒN THUỐC]",
        "qty": 2,
        "desc": "Hồi +35 Mind, tẩy độc & hoại tử"
    },
    {
        "id": "key",
        "name": "RUNIC KEY",
        "tag": "[CHÌA KHÓA]",
        "qty": 0,
        "desc": "Chìa khóa Cổng Đông (cần 3 chìa)"
    },
    {
        "id": "close",
        "name": "[ ĐÓNG TÚI ĐỒ ]",
        "tag": "[QUAY LẠI]",
        "qty": 0,
        "desc": "Quay lại"
    }
]

def render_pouch_screen(items, sel_idx, status_msg="", hero=None):
    """
    Kết xuất giao diện Túi đồ hàng dọc chuẩn xác 100 cột, thẳng hàng, sạch đẹp.
    Tổng số dòng: Đúng 21 dòng (an toàn tuyệt đối trên mọi độ phân giải terminal).
    """
    rows = []
    rows.append("\033[1;30m+" + "=" * 98 + "+\033[0m")
    title = "                    TÚI ĐỒ SINH TỒN - SURVIVAL POUCH & INVENTORY SUPPLIES"
    rows.append("\033[1;30m|\033[1;33m" + fit_exact(title, 98) + "\033[1;30m|\033[0m")
    rows.append("\033[1;30m+" + "-" * 98 + "+\033[0m")

    # Dòng chỉ số Explorer
    if hero:
        h_name = f"{hero.get('name', 'HERO')} [{hero.get('role', 'Explorer')}]"
        h_hp = f"HP: {hero.get('hp', 100):3d}/{hero.get('max_hp', 100):3d}"
        h_mind = f"MIND: {hero.get('mind', 100):3d}/{hero.get('max_mind', 100):3d}"
        h_hunger = f"HUNGER: {hero.get('hunger', 0):2d}/100"
        key_num = 0
        for it in items:
            if it["id"] == "key":
                key_num = it.get("qty", 0)
        h_keys = f"KEYS: {key_num}/3"
        status_line = f"  \033[1;32m[THÁM HIỂM]\033[0m \033[1;37m{h_name:<24}\033[0m | \033[1;32m{h_hp}\033[0m | \033[1;36m{h_mind}\033[0m | \033[1;33m{h_hunger}\033[0m | \033[1;35m{h_keys}\033[0m"
    else:
        status_line = "  \033[1;37mCHẾ ĐỘ QUẢN LÝ TÚI ĐỒ SINH TỒN TIÊU CHUẨN\033[0m"
    rows.append("\033[1;30m|\033[0m" + fit_exact(status_line, 98) + "\033[1;30m|\033[0m")
    rows.append("\033[1;30m+" + "=" * 98 + "+\033[0m")
    rows.append("\033[1;30m|" + (" " * 98) + "|\033[0m")

    # Hiển thị 8 mục hàng dọc thẳng hàng
    for idx, it in enumerate(items):
        is_cur = (idx == sel_idx)
        cur_icon = "▶" if is_cur else " "
        num_str = f"[{idx + 1}]"
        name_str = it["name"]
        tag_str = it.get("tag", "")
        desc_str = it.get("desc", "")

        if it["id"] == "close":
            qty_str = "      "
            avail = True
        else:
            qty_str = f"[x {it.get('qty', 0)}]"
            avail = (it.get("qty", 0) > 0)

        # Định dạng màu sắc
        if is_cur:
            color = "\033[1;33m"  # Vàng sáng nổi bật khi chọn
            cur_color = "\033[1;33m"
        elif avail:
            color = "\033[1;37m"  # Trắng rõ nét khi còn hàng
            cur_color = "\033[90m"
        else:
            color = "\033[90m"    # Xám khi hết hàng
            cur_color = "\033[90m"

        line = f"  {cur_color}{cur_icon}\033[0m {color}{num_str:<4} {name_str:<18} {qty_str:<7} {tag_str:<13} {desc_str}\033[0m"
        rows.append("\033[1;30m|\033[0m" + fit_exact(line, 98) + "\033[1;30m|\033[0m")

    rows.append("\033[1;30m|" + (" " * 98) + "|\033[0m")
    rows.append("\033[1;30m+" + "-" * 98 + "+\033[0m")

    # Dòng thông báo kết quả hành động
    if status_msg:
        notif = f"  {status_msg}"
    else:
        notif = "  \033[1;36m● [HƯỚNG DẪN]: Dùng [W/S] hoặc phím số [1..8] để chọn, nhấn [Enter] để sử dụng.\033[0m"
    rows.append("\033[1;30m|\033[0m" + fit_exact(notif, 98) + "\033[1;30m|\033[0m")
    rows.append("\033[1;30m+" + "=" * 98 + "+\033[0m")

    # Dòng phím tắt điều khiển
    ctrl = "  \033[1;37m[W/S / Mũi tên]\033[0m Lên/Xuống  |  \033[1;37m[1..8]\033[0m Chọn nhanh  |  \033[1;32m[Enter]\033[0m Sử dụng  |  \033[1;31m[I/Esc/Q]\033[0m Đóng túi"
    rows.append("\033[1;30m|\033[0m" + fit_exact(ctrl, 98) + "\033[1;30m|\033[0m")
    rows.append("\033[1;30m+" + "=" * 98 + "+\033[0m")

    return rows

def run_pouch_interactive(initial_items=None, hero=None, inv_dict=None, is_hardcore=False):
    """
    Vòng lặp tương tác túi đồ hàng dọc chuẩn 100 cột với điều khiển W/S, số, Enter, Q/Esc.
    Đồng bộ trực tiếp với hero và inv_dict.
    """
    items = copy.deepcopy(initial_items if initial_items is not None else ITEM_CATALOG)
    if inv_dict is not None:
        for it in items:
            if it["id"] in inv_dict:
                it["qty"] = inv_dict[it["id"]]
            elif it["id"] == "vial" and "ale" in inv_dict and "vial" not in inv_dict:
                it["qty"] = inv_dict["ale"]

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
                # Non-tty / automated testing
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

            # Phím W/S
            elif ch in (b'w', b'W'):
                sel_idx = (sel_idx - 1) % num_items
            elif ch in (b's', b'S'):
                sel_idx = (sel_idx + 1) % num_items

            # Phím số 1-8
            elif ch in (b'1', b'2', b'3', b'4', b'5', b'6', b'7', b'8'):
                val = int(ch.decode('ascii')) - 1
                if val < num_items:
                    sel_idx = val

            # Sử dụng vật phẩm [Enter] / [Space]
            elif ch in (b'\r', b'\n', b' '):
                cur_it = items[sel_idx]

                if cur_it["id"] == "close":
                    return items, last_used

                if cur_it.get("qty", 0) > 0:
                    if cur_it["id"] == "key":
                        status_msg = f"\033[1;36m● [CHÌA KHÓA]: Có {cur_it['qty']}/3 Runic Key. Cần mang đến Cổng Thoát Hiểm Phía Đông!\033[0m"
                        continue

                    cur_it["qty"] -= 1
                    if inv_dict is not None:
                        if cur_it["id"] in inv_dict:
                            inv_dict[cur_it["id"]] = cur_it["qty"]
                        if cur_it["id"] == "vial" and "ale" in inv_dict:
                            inv_dict["ale"] = cur_it["qty"]

                    last_used = cur_it

                    if cur_it["id"] == "totem":
                        if hero is not None:
                            if "debuffs" in hero:
                                hero["debuffs"].clear()
                            if "severed_limbs" in hero:
                                hero["severed_limbs"] = {"head": 100, "torso": 100, "arm_r": 100, "arm_l": 100, "leg_r": 100, "leg_l": 100}
                            hero["hp"] = hero.get("max_hp", 100)
                        status_msg = f"\033[1;33m★ [TOTEM OF UNDYING]: Tái sinh toàn bộ tứ chi bị đứt! Sinh lực hồi phục 100% ({hero.get('hp', 100)}/{hero.get('max_hp', 100)})!\033[0m"

                    elif cur_it["id"] == "poppy":
                        heal = 65 if (hero and hero.get("name") == "CAHARA") else (30 if is_hardcore else 50)
                        if hero is not None:
                            hero["hp"] = min(hero.get("max_hp", 100), hero.get("hp", 0) + heal)
                            if "bleeding" in hero.get("debuffs", []):
                                hero["debuffs"].remove("bleeding")
                            if "Bleeding (-4 HP/turn)" in hero.get("debuffs", []):
                                hero["debuffs"].remove("Bleeding (-4 HP/turn)")
                        status_msg = f"\033[1;32m● [HOA ANH TÚC]: Đã đắp dược liệu! Hồi phục +{heal} HP & cầm máu hoàn toàn! ({hero.get('hp', 0)}/{hero.get('max_hp', 100)})\033[0m"

                    elif cur_it["id"] == "weed":
                        heal = 75 if is_hardcore else 120
                        if hero is not None:
                            hero["hp"] = min(hero.get("max_hp", 100), hero.get("hp", 0) + heal)
                        status_msg = f"\033[1;32m● [THẢO DƯỢC]: Hít khói dược thảo! Hồi phục +{heal} HP & làm dịu cơn đau! ({hero.get('hp', 0)}/{hero.get('max_hp', 100)})\033[0m"

                    elif cur_it["id"] == "bread":
                        if hero is not None:
                            hero["hunger"] = max(0, hero.get("hunger", 0) - 40)
                        status_msg = f"\033[1;33m● [BÁNH MÌ MỐC]: Đã ăn lương khô! Cơn đói khát giảm -40 điểm! (Hiện tại: {hero.get('hunger', 0)}/100)\033[0m"

                    elif cur_it["id"] == "meat":
                        if hero is not None:
                            hero["hunger"] = max(0, hero.get("hunger", 0) - 60)
                            hero["hp"] = min(hero.get("max_hp", 100), hero.get("hp", 0) + 20)
                        status_msg = f"\033[1;33m● [THỊT SẤY KHÔ]: Đã ăn thịt sấy muối! Giảm -60 Đói & hồi phục +20 HP! ({hero.get('hp', 0)} HP, {hero.get('hunger', 0)}/100 Đói)\033[0m"

                    elif cur_it["id"] == "vial":
                        if hero is not None:
                            hero["mind"] = min(hero.get("max_mind", 100), hero.get("mind", 100) + 35)
                            if "debuffs" in hero:
                                for deb in ["infection", "poison", "gangrene", "bleeding", "Bleeding (-4 HP/turn)"]:
                                    if deb in hero["debuffs"]:
                                        hero["debuffs"].remove(deb)
                        status_msg = f"\033[1;36m● [BÌNH CỒN / RƯỢU CỔ]: Rót cồn sát trùng! Xóa bỏ hoại tử/độc tố và hồi +35 Mind! ({hero.get('mind', 100)}/{hero.get('max_mind', 100)})\033[0m"

                else:
                    status_msg = f"\033[1;31m✖ [HẾT VẬT PHẨM]: Bạn không còn {cur_it['name']} trong túi đồ!\033[0m"

            # Đóng túi đồ [Q] / [Esc] / [I]
            elif ch in (b'q', b'Q', b'\x1b', b'i', b'I'):
                return items, last_used

    finally:
        print("\033[?25h", end="", flush=True)

def main():
    items, used = run_pouch_interactive()

if __name__ == "__main__":
    main()
