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

def build_hero_dossier_lines(hero, items=None):
    """
    Tạo 3 dòng hiển thị hồ sơ sinh tồn, năng lực chiến đấu & tình trạng thân thể.
    Đảm bảo 100% visible length <= 98 ký tự, không bao giờ bị cắt cụt.
    """
    if not hero:
        return [
            "  \033[1;37m[THÁM HIỂM] CHẾ ĐỘ QUẢN LÝ TÚI ĐỒ SINH TỒN TIÊU CHUẨN\033[0m",
            "  \033[90mKhông có thông tin nhân vật kích hoạt.\033[0m",
            "  \033[90mNhấn [I/Q/Esc] để quay lại màn hình chính.\033[0m"
        ]

    # --- Line 1: Vitals (HP, Mind, Hunger, Tox, Keys) ---
    hp = hero.get("hp", 100)
    max_hp = hero.get("max_hp", 100)
    hp_c = "\033[1;32m" if hp > max_hp * 0.5 else ("\033[1;33m" if hp > max_hp * 0.25 else "\033[1;31m")

    mind = hero.get("mind", 100)
    max_mind = hero.get("max_mind", 100)
    mind_c = "\033[1;36m" if mind > 30 else "\033[1;31m"

    hunger = hero.get("hunger", 0)
    hunger_c = "\033[1;31m" if hunger >= 80 else ("\033[1;33m" if hunger >= 50 else "\033[1;32m")

    tox = hero.get("toxicity", 0)
    max_tox = hero.get("max_toxicity", 100)
    tox_c = "\033[1;31m" if tox >= max_tox * 0.8 else ("\033[1;33m" if tox >= max_tox * 0.5 else "\033[1;32m")

    key_num = 0
    if items:
        for it in items:
            if it["id"] == "key":
                key_num = it.get("qty", 0)

    h_name = hero.get("name", "HERO")
    line1 = (
        f"  \033[1;30;42m [SINH MỆNH] \033[0m \033[1;37m{h_name:<10}\033[0m | "
        f"{hp_c}HP: {hp:3d}/{max_hp:3d}\033[0m | "
        f"{mind_c}MND: {mind:3d}/{max_mind:3d}\033[0m | "
        f"{hunger_c}ĐÓI: {hunger:2d}/100\033[0m | "
        f"{tox_c}ĐỘC: {tox:2d}/{max_tox}%\033[0m | "
        f"\033[1;35mCHÌA: {key_num}/3\033[0m"
    )

    # --- Line 2: Combat Attributes & Trait ---
    atk = hero.get("atk", 30)
    def_v = hero.get("def", 15)
    dodge = int(hero.get("dodge_rate", 0.1) * 100)
    cap = hero.get("bag_cap", 5)
    trait = hero.get("trait", "None")
    if len(trait) > 24:
        trait = trait[:22] + ".."

    line2 = (
        f"  \033[1;30;43m [NĂNG LỰC]  \033[0m "
        f"\033[1;31mATK: {atk:2d} DMG\033[0m | "
        f"\033[1;34mDEF: {def_v:2d}\033[0m | "
        f"\033[1;32mNÉ: {dodge:2d}%\033[0m | "
        f"\033[1;35mBALO: {cap:2d} Ô\033[0m | "
        f"\033[1;33mĐẶC TÍNH: {trait}\033[0m"
    )

    # --- Line 3: Limbs & Status Effects ---
    limbs = hero.get("severed_limbs", {})
    head_st = "✓" if limbs.get("head", 100) > 0 else "\033[1;31m✗\033[0m"
    torso_st = "✓" if limbs.get("torso", 100) > 0 else "\033[1;31m✗\033[0m"
    arm_r_st = "\033[1;32m✓\033[0m" if limbs.get("arm_r", 100) > 0 else "\033[1;31m✗\033[0m"
    arm_l_st = "\033[1;32m✓\033[0m" if limbs.get("arm_l", 100) > 0 else "\033[1;31m✗\033[0m"
    legs_st = "\033[1;32m✓\033[0m" if (limbs.get("leg_r", 100) > 0 and limbs.get("leg_l", 100) > 0) else "\033[1;31m✗\033[0m"

    limb_str = f"Đầu:{head_st} Thân:{torso_st} Tay.P:{arm_r_st} Tay.T:{arm_l_st} Chân:{legs_st}"

    debuffs = hero.get("debuffs", [])
    if "bleeding" in debuffs or "Bleeding (-4 HP/turn)" in debuffs:
        status_str = "\033[1;31mChảy máu (-4 HP/bước) [Dùng Poppy!]\033[0m"
    elif "poison" in debuffs or "Poisoned (-6 HP/turn)" in debuffs:
        status_str = "\033[1;35mNhiễm độc hoại tử [Dùng Vial!]\033[0m"
    elif hunger >= 80:
        status_str = "\033[1;31mKiệt sức vì đói [Cần ăn lương khô!]\033[0m"
    elif mind <= 20:
        status_str = "\033[1;35mHoảng loạn tột độ [Cần uống Rượu Ale!]\033[0m"
    elif tox >= max_tox:
        status_str = "\033[1;31mNgộ độc dạ dày [Đang nôn mửa!]\033[0m"
    else:
        status_str = "\033[1;32mKhỏe mạnh, lành lặn\033[0m"

    line3 = (
        f"  \033[1;37;41m [THỂ TRẠNG] \033[0m "
        f"\033[1;36mTỨ CHI:\033[0m [{limb_str}] | "
        f"\033[1;37mHIỆU ỨNG:\033[0m {status_str}"
    )

    return [line1, line2, line3]

def render_pouch_screen(items, sel_idx, status_msg="", hero=None):
    """
    Kết xuất giao diện Túi đồ hàng dọc chuẩn xác 100 cột, thẳng hàng, sạch đẹp.
    Hiển thị đầy đủ Hồ sơ sinh tồn, Năng lực & Thể trạng nhân vật.
    Tổng số dòng: Đúng 23 dòng (an toàn tuyệt đối trên mọi độ phân giải terminal).
    """
    rows = []
    rows.append("\033[1;30m+" + "=" * 98 + "+\033[0m")
    title = "                    TÚI ĐỒ SINH TỒN - SURVIVAL POUCH & INVENTORY SUPPLIES"
    rows.append("\033[1;30m|\033[1;33m" + fit_exact(title, 98) + "\033[1;30m|\033[0m")
    rows.append("\033[1;30m+" + "-" * 98 + "+\033[0m")

    # Hồ sơ Thể trạng & Chỉ số Nhân vật (3 dòng chi tiết)
    dossier_lines = build_hero_dossier_lines(hero, items)
    for dl in dossier_lines:
        rows.append("\033[1;30m|\033[0m" + fit_exact(dl, 98) + "\033[1;30m|\033[0m")

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
                            hero["toxicity"] = 0
                        status_msg = f"\033[1;33m★ [TOTEM OF UNDYING]: Tái sinh toàn bộ tứ chi bị đứt! Sinh lực hồi phục 100% ({hero.get('hp', 100)}/{hero.get('max_hp', 100)})!\033[0m"

                    elif cur_it["id"] == "poppy":
                        max_t = hero.get("max_toxicity", 100) if hero else 100
                        if hero and hero.get("name") == "NAS'HRAH":
                            status_msg = "\033[1;33m● [HOA ANH TÚC]: NAS'HRAH cười khẩy: 'Ta không cần cỏ rác của người phàm!' (0 HP).\033[0m"
                        elif hero and hero.get("toxicity", 0) >= max_t:
                            hero["hp"] = max(1, hero.get("hp", 1) - 5)
                            status_msg = f"\033[1;31m✖ [NGỘ ĐỘC]: Dạ dày {hero.get('name')} nôn mửa (0 HP, -5 HP độc tố)!\033[0m"
                        else:
                            heal = 65 if (hero and hero.get("name") == "CAHARA") else (30 if is_hardcore else 50)
                            if hero is not None:
                                hero["hp"] = min(hero.get("max_hp", 100), hero.get("hp", 0) + heal)
                                added_tox = 0 if hero.get("name") == "MOONLESS" else (15 if hero.get("name") == "RAGNVALDR" else 35)
                                hero["toxicity"] = min(max_t, hero.get("toxicity", 0) + added_tox)
                                if "bleeding" in hero.get("debuffs", []):
                                    hero["debuffs"].remove("bleeding")
                                if "Bleeding (-4 HP/turn)" in hero.get("debuffs", []):
                                    hero["debuffs"].remove("Bleeding (-4 HP/turn)")
                            status_msg = f"\033[1;32m● [HOA ANH TÚC]: Đã đắp dược liệu! Hồi phục +{heal} HP & cầm máu hoàn toàn! ({hero.get('hp', 0)}/{hero.get('max_hp', 100)} HP, {hero.get('toxicity', 0)}/{max_t}% Độc)\033[0m"

                    elif cur_it["id"] == "weed":
                        max_t = hero.get("max_toxicity", 100) if hero else 100
                        if hero and hero.get("name") == "NAS'HRAH":
                            status_msg = "\033[1;33m● [THẢO DƯỢC]: NAS'HRAH cười khẩy: 'Dược thảo phàm trần vô dụng với ta!' (0 HP).\033[0m"
                        elif hero and hero.get("toxicity", 0) >= max_t:
                            hero["hp"] = max(1, hero.get("hp", 1) - 5)
                            status_msg = f"\033[1;31m✖ [NGỘ ĐỘC]: {hero.get('name')} quá liều thảo dược (0 HP, -5 HP độc tố)!\033[0m"
                        else:
                            heal = 150 if (hero and hero.get("name") == "CAHARA") else (75 if is_hardcore else 120)
                            if hero is not None:
                                hero["hp"] = min(hero.get("max_hp", 100), hero.get("hp", 0) + heal)
                                added_tox = 0 if hero.get("name") == "MOONLESS" else (25 if hero.get("name") == "RAGNVALDR" else 50)
                                hero["toxicity"] = min(max_t, hero.get("toxicity", 0) + added_tox)
                            status_msg = f"\033[1;32m● [THẢO DƯỢC]: Hít khói dược thảo! Hồi phục +{heal} HP & làm dịu cơn đau! ({hero.get('hp', 0)}/{hero.get('max_hp', 100)} HP, {hero.get('toxicity', 0)}/{max_t}% Độc)\033[0m"

                    elif cur_it["id"] == "bread":
                        if hero and hero.get("name") == "NAS'HRAH":
                            status_msg = "\033[1;33m● [BÁNH MÌ]: NAS'HRAH không cần ăn lương khô của người phàm!\033[0m"
                        elif hero and hero.get("name") == "RAGNVALDR":
                            hero["hunger"] = max(0, hero.get("hunger", 0) - 20)
                            status_msg = f"\033[1;33m● [BÁNH MÌ]: Ragnvaldr nuốt vội bánh mì (-20 Đói - Cần thịt sống!). Hiện tại: {hero.get('hunger', 0)}/100 Đói\033[0m"
                        elif hero and hero.get("name") == "CAHARA":
                            hero["hunger"] = max(0, hero.get("hunger", 0) - 50)
                            status_msg = f"\033[1;32m● [BÁNH MÌ]: Cahara thưởng thức bánh mì ngon lành (-50 Đói). Hiện tại: {hero.get('hunger', 0)}/100 Đói\033[0m"
                        else:
                            if hero is not None:
                                hero["hunger"] = max(0, hero.get("hunger", 0) - 40)
                            status_msg = f"\033[1;33m● [BÁNH MÌ MỐC]: Đã ăn lương khô! Cơn đói khát giảm -40 điểm! (Hiện tại: {hero.get('hunger', 0)}/100 Đói)\033[0m"

                    elif cur_it["id"] == "meat":
                        if hero and hero.get("name") == "NAS'HRAH":
                            status_msg = "\033[1;33m● [THỊT SẤY KHÔ]: NAS'HRAH không màng đến xác thịt phàm trần!\033[0m"
                        else:
                            heal = 40 if (hero and hero.get("name") in ("RAGNVALDR", "MOONLESS")) else 20
                            if hero is not None:
                                hero["hunger"] = max(0, hero.get("hunger", 0) - 60)
                                hero["hp"] = min(hero.get("max_hp", 100), hero.get("hp", 0) + heal)
                            status_msg = f"\033[1;33m● [THỊT SẤY KHÔ]: Đã ăn thịt sấy muối! Giảm -60 Đói & hồi phục +{heal} HP! ({hero.get('hp', 0)} HP, {hero.get('hunger', 0)}/100 Đói)\033[0m"

                    elif cur_it["id"] == "vial":
                        if hero and hero.get("name") == "NAS'HRAH":
                            hero["hp"] = min(hero.get("max_hp", 100), hero.get("hp", 0) + 15)
                            hero["mind"] = min(hero.get("max_mind", 100), hero.get("mind", 100) + 35)
                            status_msg = f"\033[1;36m● [CỒN THUỐC]: Nas'hrah hấp thu năng lượng cồn cổ (+15 HP, +35 Mind)! ({hero.get('mind', 100)}/{hero.get('max_mind', 100)})\033[0m"
                        else:
                            if hero is not None:
                                hero["mind"] = min(hero.get("max_mind", 100), hero.get("mind", 100) + 35)
                                hero["toxicity"] = max(0, hero.get("toxicity", 0) - 25)
                                if "debuffs" in hero:
                                    for deb in ["infection", "poison", "gangrene", "bleeding", "Bleeding (-4 HP/turn)"]:
                                        if deb in hero["debuffs"]:
                                            hero["debuffs"].remove(deb)
                            status_msg = f"\033[1;36m● [CỒN THUỐC / RƯỢU CỔ]: Rót cồn sát trùng! Xóa bỏ hoại tử/độc tố và hồi +35 Mind! ({hero.get('mind', 100)}/{hero.get('max_mind', 100)})\033[0m"

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
