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

def build_hero_showcase_boxes(hero, items=None):
    """
    Kết xuất khối hiển thị đôi (Split Box) chuẩn xác 100 cột:
    - Bên trái: Khung Model nhân vật (36 cột).
    - Khoảng cách: 2 cột khoảng trống ('  ').
    - Bên phải: Khung Hồ sơ & Các chỉ số dạng Thanh máu (Health/Mind/Hunger/Toxicity Bars) (62 cột).
    Tổng chiều cao: Đúng 13 dòng.
    """
    c_border = "\033[1;30m"
    c_reset = "\033[0m"

    if not hero:
        b_top = f"{c_border}+" + "-" * 98 + f"+{c_reset}"
        blank_row = f"{c_border}|" + (" " * 98) + f"|{c_reset}"
        no_info = f"{c_border}|  \033[90mKhông có thông tin nhân vật kích hoạt.\033[0m" + (" " * 56) + f"{c_border}|{c_reset}"
        rows = [b_top]
        for _ in range(11):
            rows.append(blank_row if _ != 5 else no_info)
        rows.append(b_top)
        return rows

    h_name = hero.get("name", "HERO")
    role = hero.get("role", "Explorer")
    h_sprite = dui.HERO_SPRITES.get(h_name, dui.FALLBACK_SPRITES.get(h_name, [" " * 29] * 12))

    # --- Left Model Box (36 cols) ---
    b_top_left = f"{c_border}+" + "-" * 34 + f"+{c_reset}"
    b_bot_left = f"{c_border}+" + "-" * 34 + f"+{c_reset}"

    model_rows = []
    for r in range(11):
        sp = h_sprite[r] if r < len(h_sprite) else " " * 29
        sp_fmt = dui.format_model_row(sp)
        sp_pad = dui.fit_ansi(sp_fmt, 32)
        model_rows.append(f"{c_border}| {c_reset}{sp_pad}{c_border} |{c_reset}")

    # --- Right Stats & Bars Box (62 cols) ---
    b_top_right = f"{c_border}+" + "-" * 60 + f"+{c_reset}"
    b_bot_right = f"{c_border}+" + "-" * 60 + f"+{c_reset}"

    hp = hero.get("hp", 100)
    max_hp = hero.get("max_hp", 100)
    hp_pct = int(hp / max(1, max_hp) * 100)
    hp_bar = dui.make_bar(hp, max_hp, 14, "32" if hp_pct > 50 else ("33" if hp_pct > 25 else "31"))
    hp_tag = "\033[1;32m[Khỏe]\033[0m" if hp_pct > 70 else ("\033[1;33m[Bị thương]\033[0m" if hp_pct > 30 else "\033[1;31m[Nguy kịch]\033[0m")

    mind = hero.get("mind", 100)
    max_mind = hero.get("max_mind", 100)
    mind_pct = int(mind / max(1, max_mind) * 100)
    mind_bar = dui.make_bar(mind, max_mind, 14, "36" if mind_pct > 30 else "31")
    mind_tag = "\033[1;36m[Tỉnh táo]\033[0m" if mind_pct > 50 else ("\033[1;33m[Bất an]\033[0m" if mind_pct > 20 else "\033[1;35m[Hoảng loạn]\033[0m")

    hunger = hero.get("hunger", 0)
    hunger_bar = dui.make_bar(hunger, 100, 14, "31" if hunger >= 80 else ("33" if hunger >= 50 else "32"))
    hunger_tag = "\033[1;31m[Kiệt sức]\033[0m" if hunger >= 80 else ("\033[1;33m[Cảnh báo đói]\033[0m" if hunger >= 50 else "\033[1;32m[No đủ]\033[0m")

    tox = hero.get("toxicity", 0)
    max_tox = hero.get("max_toxicity", 100)
    tox_pct = int(tox / max(1, max_tox) * 100)
    tox_bar = dui.make_bar(tox, max_tox, 14, "31" if tox_pct >= 80 else ("33" if tox_pct >= 50 else "35"))
    tox_tag = "\033[1;31m[Ngộ độc!]\033[0m" if tox >= max_tox else ("\033[1;33m[Nhiễm độc]\033[0m" if tox_pct >= 50 else "\033[90m[An toàn]\033[0m")

    atk = hero.get("atk", 30)
    def_v = hero.get("def", 15)
    dodge = int(hero.get("dodge_rate", 0.1) * 100)
    cap = hero.get("bag_cap", 5)

    key_num = 0
    if items:
        for it in items:
            if it.get("id") == "key":
                key_num = it.get("qty", 0)

    limbs = hero.get("severed_limbs", {})
    head_st = "✓" if limbs.get("head", 100) > 0 else "\033[1;31m✗\033[0m"
    torso_st = "✓" if limbs.get("torso", 100) > 0 else "\033[1;31m✗\033[0m"
    arm_r_st = "\033[1;32m✓\033[0m" if limbs.get("arm_r", 100) > 0 else "\033[1;31m✗\033[0m"
    arm_l_st = "\033[1;32m✓\033[0m" if limbs.get("arm_l", 100) > 0 else "\033[1;31m✗\033[0m"
    legs_st = "\033[1;32m✓\033[0m" if (limbs.get("leg_r", 100) > 0 and limbs.get("leg_l", 100) > 0) else "\033[1;31m✗\033[0m"
    limb_str = f"Đầu:{head_st} Thân:{torso_st} Tay.P:{arm_r_st} Tay.T:{arm_l_st} Chân:{legs_st}"

    trait = hero.get("trait", "None")
    if len(trait) > 36:
        trait = trait[:34] + ".."

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

    stats_lines = [
        f"\033[1;32mHERO  : \033[1;37m{h_name:<11} \033[90m[{role}]\033[0m",
        f"HP    : {hp_bar} \033[1;32m{hp:3d}/{max_hp:3d}\033[0m ({hp_pct:3d}%) {hp_tag}",
        f"MIND  : {mind_bar} \033[1;36m{mind:3d}/{max_mind:3d}\033[0m ({mind_pct:3d}%) {mind_tag}",
        f"ĐÓI   : {hunger_bar} \033[1;33m{hunger:3d}/100\033[0m ({hunger:2d}%) {hunger_tag}",
        f"ĐỘC   : {tox_bar} \033[1;35m{tox:3d}/{max_tox}%\033[0m ({tox_pct:2d}%) {tox_tag}",
        f"\033[1;37mN.LỰC : \033[1;31mATK: {atk:2d} DMG\033[0m | \033[1;34mDEF: {def_v:2d}\033[0m | \033[1;32mNÉ: {dodge:2d}%\033[0m | \033[1;35mBALO: {cap:2d} Ô\033[0m",
        f"\033[1;36mCHÌA  : CỔNG ĐÔNG [ {key_num}/3 Runic Keys ]\033[0m",
        f"\033[1;36mTỨ CHI: \033[0m[{limb_str}\033[0m]",
        f"\033[1;33mTRAIT : \033[0m{trait}",
        f"\033[1;37mH.ỨNG : \033[0m{status_str}",
        f"\033[90mTRANG BỊ: Vũ khí cận chiến & Túi thám hiểm sinh tồn\033[0m"
    ]

    stats_rows = []
    for sl in stats_lines:
        sl_pad = dui.fit_ansi(sl, 58)
        stats_rows.append(f"{c_border}| {c_reset}{sl_pad}{c_border} |{c_reset}")

    combined = []
    combined.append(f"{b_top_left}  {b_top_right}")
    for r in range(11):
        combined.append(f"{model_rows[r]}  {stats_rows[r]}")
    combined.append(f"{b_bot_left}  {b_bot_right}")

    return combined

def render_pouch_screen(items, sel_idx, status_msg="", hero=None):
    """
    Kết xuất giao diện Túi đồ hàng dọc chuẩn xác 100 cột, thẳng hàng, sạch đẹp.
    Hiển thị Khối đôi: Model nhân vật (trái) + Thanh máu & Chỉ số sinh tồn (phải).
    Phía dưới là danh mục 8 vật phẩm túi đồ sinh tồn.
    Tổng số dòng: Đúng 27 dòng (an toàn tuyệt đối trên mọi độ phân giải terminal, <= 35 dòng).
    """
    c_border = "\033[1;30m"
    c_reset = "\033[0m"
    screen_rows = []

    # 1. Top Banner (1 dòng)
    h_name = hero.get("name", "HERO") if hero else "HERO"
    role = hero.get("role", "Explorer") if hero else "Explorer"
    title_text = f"TÚI ĐỒ SINH TỒN & HỒ SƠ THÁM HIỂM - {h_name} [{role}]"
    rem_len = max(0, 93 - dui.display_width(title_text))
    screen_rows.append(f"{c_border}+=[ \033[1;33m{title_text}{c_border} ]" + "=" * rem_len + f"+{c_reset}")

    # 2. Khối đôi: Model bên trái & Thanh máu bên phải (13 dòng)
    showcase_rows = build_hero_showcase_boxes(hero, items)
    screen_rows.extend(showcase_rows)

    # 3. Phân cách & 8 mục vật phẩm hàng dọc (9 dòng)
    screen_rows.append(f"{c_border}+" + "-" * 98 + f"+{c_reset}")
    for idx, it in enumerate(items):
        is_cur = (idx == sel_idx)
        cur_icon = "▶" if is_cur else " "
        num_str = f"[{idx + 1}]"
        name_str = it["name"]
        tag_str = it.get("tag", "")
        desc_str = it.get("desc", "")
        qty_val = it.get("qty", 0)

        if it["id"] == "close":
            qty_str = "      "
            avail = True
        else:
            qty_str = f"[x {qty_val}]"
            avail = (qty_val > 0)

        if is_cur:
            color = "\033[1;33m"
            cur_color = "\033[1;33m"
        elif avail:
            color = "\033[1;37m"
            cur_color = "\033[90m"
        else:
            color = "\033[90m"
            cur_color = "\033[90m"

        line = f"  {cur_color}{cur_icon}{c_reset} {color}{num_str:<4} {name_str:<18} {qty_str:<7} {tag_str:<13} {desc_str}{c_reset}"
        screen_rows.append(f"{c_border}|{c_reset}" + dui.fit_ansi(line, 98) + f"{c_border}|{c_reset}")

    # 4. Hộp thông báo trạng thái hành động (2 dòng)
    screen_rows.append(f"{c_border}+" + "-" * 98 + f"+{c_reset}")
    if status_msg:
        notif = f"  {status_msg}"
    else:
        notif = "  \033[90mChọn một vật phẩm và nhấn [Enter] để sử dụng, hoặc nhấn [8/I/Esc] để quay lại.\033[0m"
    screen_rows.append(f"{c_border}|{c_reset}" + dui.fit_ansi(notif, 98) + f"{c_border}|{c_reset}")

    # 5. Thanh điều khiển chân trang (2 dòng)
    screen_rows.append(f"{c_border}+" + "=" * 98 + f"+{c_reset}")
    footer = "  \033[90m[ĐIỀU KHIỂN]:\033[0m \033[1;37m[W/S / Mũi tên]\033[0m Chọn  |  \033[1;37m[1..8]\033[0m Phím tắt  |  \033[1;32m[Enter]\033[0m Dùng  |  \033[1;31m[I/Esc/Q]\033[0m Đóng"
    screen_rows.append(f"{c_border}|{c_reset}" + dui.fit_ansi(footer, 98) + f"{c_border}|{c_reset}")

    return screen_rows

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
