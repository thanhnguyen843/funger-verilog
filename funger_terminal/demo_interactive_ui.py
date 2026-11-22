#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
================================================================================
FEAR & HUNGER: TERMINAL LABYRINTH - COMBAT ARENA (DUAL TACTICAL CARDS EDITION)
================================================================================
Cải tiến toàn diện theo ý kiến người dùng:
1. NỬA TRÊN: Dual Tactical Cards (Hai Thẻ Chiến Thuật Song Song):
   - Thẻ Trái (Quái Vật): Máu tổng + Bảng Giải Phẫu Tứ Chi (Đầu, Thân, Tứ chi)
     Hiển thị rõ ràng trạng thái Cầm kiếm, Khiên, Đứng vững. Khi bị chặt tay hoặc
     bẻ gãy chân, dòng đó lập tức đổi trạng thái trực quan [ĐÃ BỊ CHẶT] / [BÒ LÊ LẾT].
   - Thẻ Phải (Đội Hình): Máu (HP), Tâm trí (MND), Độ đói (HNG), Thế trận & Nội tại
     kèm thanh tóm tắt đồng đội dự bị phía sau.
2. ĐỔI NHÂN VẬT THÔNG MINH (TACTICAL SQUAD SWITCH):
   - Khi chọn "Đổi Tướng", in ra Bảng Danh Sách Đội Hình đầy đủ (Cahara, D'arce,
     Enki, The Girl) với chỉ số Máu, Tâm trí, Đói và Chức nghiệp.
   - Dùng W/S điều hướng chọn người muốn đổi, Enter để chuyển quyền điều khiển!
   - Thẻ bên phải lập tức cập nhật thông tin vị tướng tiên phong mới.
3. NỬA DƯỚI: Menu 4 nút lớn W/S, highlight 1 mục duy nhất, in đè tại chỗ.
================================================================================
"""

import sys
import os
import time

# Enable Windows ANSI Virtual Terminal Support & UTF-8
if os.name == 'nt':
    try:
        import ctypes
        kernel32 = ctypes.windll.kernel32
        hOut = kernel32.GetStdHandle(-11)
        mode = ctypes.c_ulong()
        if kernel32.GetConsoleMode(hOut, ctypes.byref(mode)):
            kernel32.SetConsoleMode(hOut, mode.value | 0x0004)
        kernel32.SetConsoleOutputCP(65001)
        kernel32.SetConsoleCP(65001)
    except Exception:
        pass
    import msvcrt

# Monster State
monster = {
    "name": "SHADOW SWORDSMAN",
    "id": 8,
    "hp": 95,
    "max_hp": 95,
    "atk": 24,
    "def": 14,
    "head_hp": 24,
    "head_max": 24,
    "torso_hp": 95,
    "torso_max": 95,
    "arm_r_hp": 30,
    "arm_r_max": 30,
    "arm_l_hp": 30,
    "arm_l_max": 30,
    "legs_hp": 35,
    "legs_max": 35,
    "is_crawling": False,
    "is_disarmed": False,
    "is_guard_broken": False,
    "is_decapitated": False
}

# 4 Playable Companions in the Squad
squad = [
    {
        "name": "CAHARA",
        "role": "Mercenary (Swift Rogue)",
        "hp": 125,
        "max_hp": 125,
        "mind": 100,
        "max_mind": 100,
        "hunger": 20,
        "max_hunger": 100,
        "atk": 33,
        "def": 21,
        "passive": "Bàn Tay Nhanh (-80% Mimic, +15% Né)",
        "stance": "STANDARD BALANCED",
        "is_guarding": False
    },
    {
        "name": "D'ARCE",
        "role": "Holy Knight (Guardian)",
        "hp": 145,
        "max_hp": 145,
        "mind": 90,
        "max_mind": 100,
        "hunger": 35,
        "max_hunger": 100,
        "atk": 30,
        "def": 30,
        "passive": "Thiết Thuẫn Hoàng Gia (Thủ -85% DMG)",
        "stance": "IRON GUARD BASTION",
        "is_guarding": False
    },
    {
        "name": "ENKI",
        "role": "Dark Priest (Occult Mage)",
        "hp": 95,
        "max_hp": 95,
        "mind": 100,
        "max_mind": 100,
        "hunger": 15,
        "max_hunger": 100,
        "atk": 48,
        "def": 24,
        "passive": "Tâm Trí Cổ Thuật (Phép Xuyên 100% DEF)",
        "stance": "STANDARD BALANCED",
        "is_guarding": False
    },
    {
        "name": "THE GIRL",
        "role": "Innocent Ward (Nimble)",
        "hp": 105,
        "max_hp": 105,
        "mind": 80,
        "max_mind": 100,
        "hunger": 10,
        "max_hunger": 100,
        "atk": 30,
        "def": 39,
        "passive": "Hộ Mệnh Ngây Thơ (25% Quái Bỏ Qua, 35% Né)",
        "stance": "AGILE DANCE",
        "is_guarding": False
    }
]

active_hero_idx = 0

inventory = {
    "poppy": 2,      # +50 HP
    "weed": 1,       # +120 HP
    "bread": 3,      # -40 Hunger
    "ale": 2         # +35 Mind
}

combat_log = "Trận chiến bắt đầu! Shadow Swordsman rút kiếm bóng tối thủ thế."

current_menu = "MAIN"
cursor_idx = 0

import re

ANSI_REGEX = re.compile(r'\x1b\[[0-9;]*[mGKH]')

def visible_len(s):
    return len(ANSI_REGEX.sub('', s))

def pad_str(s, n):
    cur = visible_len(s)
    if cur < n:
        return s + " " * (n - cur)
    return s

def make_bar(curr, max_v, bar_len=10, color_code="32"):
    if max_v <= 0:
        ratio = 0
    else:
        ratio = max(0.0, min(1.0, curr / float(max_v)))
    filled = int(ratio * bar_len)
    if filled == 0 and curr > 0:
        filled = 1
    empty = bar_len - filled
    return f"\033[1;{color_code}m" + "█" * filled + "\033[90m" + "░" * empty + "\033[0m"

def render_screen():
    global active_hero_idx
    hero = squad[active_hero_idx]

    sys.stdout.write("\033[2J\033[H")

    # =========================================================================
    # HEADER
    # =========================================================================
    print("\033[1;30m+====================================================================================================+\033[0m")
    print("\033[1;30m| \033[1;37m        FEAR & HUNGER: TERMINAL LABYRINTH - ĐẤU TRƯỜNG CHIẾN THUẬT (DUAL TACTICAL CARDS)           \033[1;30m|\033[0m")
    print("\033[1;30m+====================================================================================================+\033[0m")
    print()  # Breathing room: 1 blank line

    # =========================================================================
    # SECTION 1: DUAL TACTICAL CARDS (50 columns Left vs 49 columns Right)
    # =========================================================================
    # Card Left: Monster & Limb Anatomy
    m_hp_bar = make_bar(monster["hp"], monster["max_hp"], 12, "31")

    # Limbs bars & labels
    if monster["is_decapitated"]:
        head_line = "\033[1;31m[ĐẦU / HEAD]  : [TRẢM ĐẦU TỨC THÌ] 💀 KẾT LIỄU       \033[0m"
    else:
        hb = make_bar(monster["head_hp"], monster["head_max"], 6, "31")
        chint = "100% Trúng!" if monster["is_crawling"] else "25% Trảm"
        head_line = f"• [ĐẦU / HEAD]  : {hb} \033[1;31m{monster['head_hp']:2d}/{monster['head_max']:2d}\033[0m ({chint}) "

    tb = make_bar(monster["torso_hp"], monster["torso_max"], 6, "33")
    torso_line = f"• [THÂN / TORSO]: {tb} \033[1;33m{monster['torso_hp']:2d}/{monster['torso_max']:2d}\033[0m (Vùng Cốt Lõi) "

    if monster["is_disarmed"]:
        arm_r_line = "\033[1;33m• [TAY PHẢI]    : [ĐÃ BỊ CHẶT] ⚔️ ĐÃ TƯỚC KHÍ        \033[0m"
    else:
        arb = make_bar(monster["arm_r_hp"], monster["arm_r_max"], 6, "36")
        arm_r_line = f"• [TAY PHẢI]    : {arb} \033[1;36m{monster['arm_r_hp']:2d}/{monster['arm_r_max']:2d}\033[0m 🗡️ Kiếm Quỷ   "

    if monster["is_guard_broken"]:
        arm_l_line = "\033[1;33m• [TAY TRÁI]    : [ĐÃ BỊ CHẶT] 🛡️ PHÁ KHIÊN (-50% ATK)\033[0m"
    else:
        alb = make_bar(monster["arm_l_hp"], monster["arm_l_max"], 6, "36")
        arm_l_line = f"• [TAY TRÁI]    : {alb} \033[1;36m{monster['arm_l_hp']:2d}/{monster['arm_l_max']:2d}\033[0m 🛡️ Khiên Tối   "

    if monster["is_crawling"]:
        legs_line = "\033[1;31m• [ĐÔI CHÂN]    : [BỊ BẺ GÃY] ⚠️ BÒ LÊ LẾT (ĐẦU 100%)\033[0m"
    else:
        lb = make_bar(monster["legs_hp"], monster["legs_max"], 6, "32")
        legs_line = f"• [ĐÔI CHÂN]    : {lb} \033[1;32m{monster['legs_hp']:2d}/{monster['legs_max']:2d}\033[0m 🦵 Đứng Vững   "

    # Card Right: Active Hero & Squad overview
    h_hp_bar = make_bar(hero["hp"], hero["max_hp"], 10, "32")
    h_mnd_bar = make_bar(hero["mind"], hero["max_mind"], 8, "36")
    h_hng_bar = make_bar(hero["hunger"], hero["max_hunger"], 8, "33")

    # Reserve companions status strip
    reserves = []
    for idx, c in enumerate(squad):
        if idx != active_hero_idx:
            status_icon = "🟢" if c["hp"] > 0 else "💀"
            short_name = c["name"][:5]
            reserves.append(f"{short_name}:{c['hp']:3d}HP{status_icon}")
    reserve_str = " | ".join(reserves)

    # Context-Aware Card Highlighting:
    # If in TARGET_LIMB, left card border is highlighted Amber!
    # If in SWITCH_HERO or POUCH, right card border is highlighted Green!
    c_left = "\033[1;33m" if current_menu == "TARGET_LIMB" else "\033[1;30m"
    c_right = "\033[1;32m" if current_menu in ("SWITCH_HERO", "POUCH") else "\033[1;30m"

    top_border = f"{c_left}+" + "-" * 49 + f"+{c_right}" + "-" * 48 + f"+{c_left}\033[0m"
    bot_border = f"{c_left}+" + "-" * 49 + f"+{c_right}" + "-" * 48 + f"+{c_left}\033[0m"

    l_rows = [
        f"\033[1;31m👹 QUÁI VẬT: #{monster['id']:02d} {monster['name']:<18}\033[90m[Standard]\033[0m",
        f" Sinh Lực Tổng : {m_hp_bar} \033[1;31m{monster['hp']:3d}/{monster['max_hp']:3d} HP\033[0m",
        f" Công / Thủ    : ATK: {monster['atk']:2d} | DEF: {monster['def']:2d}",
        "",
        "\033[1;37mGIẢI PHẪU TỨ CHI (LIMB ANATOMY):\033[0m",
        head_line,
        torso_line,
        arm_r_line,
        arm_l_line,
        legs_line
    ]

    r_rows = [
        f"\033[1;32m🛡️ TIÊN PHONG: {hero['name']:<10}\033[90m[{hero['role'][:18]}]\033[0m",
        f" Máu (HP)    : {h_hp_bar} \033[1;32m{hero['hp']:3d}/{hero['max_hp']:3d} HP\033[0m",
        f" Tâm Trí(MND): {h_mnd_bar} \033[1;36m{hero['mind']:3d}/100\033[0m | Đói: {h_hng_bar}\033[1;33m{hero['hunger']:2d}\033[0m",
        f" Thế Trận    : \033[1;37m{hero['stance'][:20]:<20}\033[0m",
        f" Nội Tại     : \033[90m{hero['passive'][:30]:<30}\033[0m",
        "",
        "\033[1;37mĐỒNG ĐỘI DỰ BỊ PHÍA SAU:\033[0m",
        f"\033[1;37m{reserve_str}\033[0m",
        "\033[90m(Bấm [Hành Động] -> [Đổi Tướng] để chọn người)\033[0m",
        ""
    ]

    print(top_border)
    for row_idx in range(len(l_rows)):
        l_text = pad_str(l_rows[row_idx], 47)
        r_text = pad_str(r_rows[row_idx], 46)
        print(f"{c_left}| {l_text} |{c_right} {r_text} |{c_left}\033[0m")
    print(bot_border)
    print()  # Breathing room: 1 blank line

    # =========================================================================
    # SECTION 2: COMBAT LOG BOX
    # =========================================================================
    print("\033[1;30m+----------------------------------------------------------------------------------------------------+\033[0m")
    print(f"| \033[1;33m🔔 BẢNG TIN CHIẾN SỰ:\033[0m \033[1;37m{combat_log:<75}\033[1;30m |\033[0m")
    print("\033[1;30m+----------------------------------------------------------------------------------------------------+\033[0m")
    print()  # Breathing room: 1 blank line

    # =========================================================================
    # SECTION 3: HIERARCHICAL DYNAMIC MENU
    # =========================================================================
    menu_data = get_current_menu_data()
    title = menu_data["title"]
    options = menu_data["options"]

    print(f"  \033[1;37m{title}\033[0m")
    print("  \033[90m(Dùng phím W / S hoặc Mũi tên để di chuyển, phím Enter để chọn):\033[0m")
    print()

    for idx, opt in enumerate(options):
        is_sel = (idx == cursor_idx)
        icon = opt["icon"]
        label = opt["label"]
        desc = opt["desc"]

        if is_sel:
            print(f"    \033[1;33m▶  [{idx+1}] {icon}  \033[1;37;43m {label:<22} \033[0m \033[1;33m{desc}\033[0m")
        else:
            print(f"       \033[90m[{idx+1}] {icon}   {label:<22} {desc}\033[0m")

    # Consistent spacing
    pad_lines = 6 - len(options)
    for _ in range(max(0, pad_lines)):
        print()

    print()  # Breathing room: 1 blank line

    # =========================================================================
    # FOOTER: CONTROL GUIDE
    # =========================================================================
    print("\033[1;30m====================================================================================================\033[0m")
    if current_menu == "MAIN":
        print("  \033[90m[ĐIỀU HƯỚNG]:\033[0m \033[1;37m[W/S]\033[0m Lên/Xuống  |  \033[1;37m[Enter / Space]\033[0m Mở Menu Con  |  \033[1;31m[Q]\033[0m Thoát Demo")
    else:
        print("  \033[90m[ĐIỀU HƯỚNG]:\033[0m \033[1;37m[W/S]\033[0m Lên/Xuống  |  \033[1;37m[Enter / Space]\033[0m Chọn Lệnh  |  \033[1;33m[B / Esc]\033[0m Quay Lại Menu")
    print("\033[1;30m====================================================================================================\033[0m")
    sys.stdout.flush()

def get_current_menu_data():
    if current_menu == "MAIN":
        return {
            "title": "DANH MỤC LỆNH CHÍNH (MAIN ACTION WHEEL)",
            "options": [
                {"icon": "⚔️", "label": "HÀNH ĐỘNG (ACTION)",     "desc": "-> Đánh, Phòng thủ, Đổi tướng thám hiểm"},
                {"icon": "⚡", "label": "KỸ NĂNG (SKILLS)",      "desc": "-> Bí thuật ma pháp Hexen & Đòn võ kỹ đặc thù"},
                {"icon": "🎒", "label": "TÚI ĐỒ (INVENTORY)",     "desc": "-> Thảo dược Poppy/Weed, Lương khô, Rượu Ale"},
                {"icon": "🛡️", "label": "CHIẾN THUẬT (TACTICS)",  "desc": "-> Đổi thế trận (Berserk/Guard) hoặc Tháo chạy"}
            ]
        }
    elif current_menu == "ACTION":
        return {
            "title": "HÀNH ĐỘNG > CHỌN LOẠI TÁC CHIẾN (SUBMENU 1)",
            "options": [
                {"icon": "🎯", "label": "TẤN CÔNG (ATTACK)",      "desc": "-> Chọn bộ phận cơ thể để nhắm đánh (Đầu, Thân, Tứ chi)"},
                {"icon": "🛡️", "label": "PHÒNG THỦ (GUARD)",     "desc": "-> Giảm 70% sát thương nhận vào ở hiệp này, hồi nhẹ HP"},
                {"icon": "🔄", "label": "ĐỔI TƯỚNG (SWITCH)",     "desc": "-> Mở Bảng Danh Sách Đội Hình để chọn tướng tiên phong"},
                {"icon": "↩️", "label": "QUAY LẠI (BACK)",       "desc": "-> Trở về Danh mục Lệnh chính bên ngoài"}
            ]
        }
    elif current_menu == "SWITCH_HERO":
        opts = []
        for idx, h in enumerate(squad):
            is_active = (idx == active_hero_idx)
            tag = " \033[1;32m[ĐANG TIÊN PHONG]\033[0m" if is_active else ""
            st_icon = "🟢" if h["hp"] > 0 else "💀"
            opts.append({
                "icon": st_icon,
                "label": f"{h['name']} [{h['role'][:12]}]",
                "desc": f"HP: {h['hp']:3d}/{h['max_hp']:3d} | MND: {h['mind']:3d} | HNG: {h['hunger']:2d}{tag}"
            })
        opts.append({"icon": "↩️", "label": "QUAY LẠI (BACK)", "desc": "-> Giữ nguyên đội hình, quay lại menu Hành Động"})
        return {
            "title": "HÀNH ĐỘNG > BẢNG ĐIỀU ĐỘNG ĐỘI HÌNH (TACTICAL ROSTER SWITCH)",
            "options": opts
        }
    elif current_menu == "TARGET_LIMB":
        crawl_hint = "\033[1;32m(100% TRÚNG VÌ QUÁI ĐANG BÒ!)\033[0m" if monster["is_crawling"] else "(25% Trúng | TRẢM ĐẦU TỨC THÌ)"
        return {
            "title": "HÀNH ĐỘNG > TẤN CÔNG > CHỌN VỊ TRÍ NHẮM ĐÁNH (SUBMENU 2)",
            "options": [
                {"icon": "💀", "label": "ĐẦU (HEAD)",            "desc": f"-> {crawl_hint}"},
                {"icon": "🎯", "label": "THÂN (TORSO)",          "desc": "-> 100% Trúng | Đòn đánh an toàn, bào mòn máu tổng"},
                {"icon": "🗡️", "label": "TAY PHẢI (R-ARM)",      "desc": "-> 100% Trúng | Chặt đứt tay cầm vũ khí -> TƯỚC VŨ KHÍ"},
                {"icon": "🛡️", "label": "TAY TRÁI (L-ARM)",      "desc": "-> 100% Trúng | Phá khiên/tay phụ -> GIẢM 50% CÔNG QUÁI"},
                {"icon": "🦵", "label": "ĐÔI CHÂN (LEGS)",        "desc": "-> 100% Trúng | Bẻ gãy chân -> ÉP QUÁI BÒ LÊ LẾT"},
                {"icon": "↩️", "label": "QUAY LẠI (BACK)",       "desc": "-> Quay lại menu Hành Động"}
            ]
        }
    elif current_menu == "SKILL":
        return {
            "title": "KỸ NĂNG & MA PHÁP HEXEN (SUBMENU)",
            "options": [
                {"icon": "🔮", "label": "BLACK ORB",             "desc": "-> Tiêu tốn 15 Mind | Bắn phép XUYÊN 100% GIÁP DEF"},
                {"icon": "🌪️", "label": "LEG SWEEP",             "desc": "-> Tiêu tốn 10 HP | Bẻ gãy chân quái với tỷ lệ 100%"},
                {"icon": "🩸", "label": "DEVOUR (CẮN XÉ)",       "desc": "-> Cắn quái vật 20 DMG | Giảm ngay 40 điểm Hunger"},
                {"icon": "↩️", "label": "QUAY LẠI (BACK)",       "desc": "-> Trở về Danh mục Lệnh chính bên ngoài"}
            ]
        }
    elif current_menu == "POUCH":
        return {
            "title": "TÚI ĐỒ & VẬT PHẨM SINH TỒN (SUBMENU)",
            "options": [
                {"icon": "🌸", "label": f"HOA POPPY [{inventory['poppy']}]",  "desc": "-> Búp hoa anh túc trắng | Hồi phục +50 HP"},
                {"icon": "🌿", "label": f"THẢO DƯỢC [{inventory['weed']}]",  "desc": "-> Thảo dược quý | Đại hồi phục +120 HP"},
                {"icon": "🍞", "label": f"BÁNH MÌ [{inventory['bread']}]",    "desc": "-> Lương khô ngục tối | Giảm ngay 40 điểm Hunger"},
                {"icon": "🍺", "label": f"RƯỢU ALE [{inventory['ale']}]",     "desc": "-> Rượu lên men cổ | Khôi phục +35 điểm Mind"},
                {"icon": "↩️", "label": "QUAY LẠI (BACK)",       "desc": "-> Trở về Danh mục Lệnh chính bên ngoài"}
            ]
        }
    elif current_menu == "TACTICS":
        return {
            "title": "CHIẾN THUẬT & THẾ TRẬN TÁC CHIẾN (SUBMENU)",
            "options": [
                {"icon": "💥", "label": "THẾ BERSERK",           "desc": "-> +50% Sức Công Kích, nhưng nhận thêm 30% sát thương"},
                {"icon": "🛡️", "label": "THẾ IRON GUARD",        "desc": "-> Chặn 70% sát thương nhận vào, tự hồi 5% HP mỗi lượt"},
                {"icon": "💨", "label": "THẾ AGILE DANCE",       "desc": "-> Tăng 35% tỷ lệ né tránh, 100% tháo chạy thành công"},
                {"icon": "🏃", "label": "THÁO CHẠY (FLEE)",       "desc": "-> Cố gắng rút lui khỏi trận đánh về hành lang mê cung"},
                {"icon": "↩️", "label": "QUAY LẠI (BACK)",       "desc": "-> Trở về Danh mục Lệnh chính bên ngoài"}
            ]
        }
    return {"title": "MENU", "options": []}

def handle_selection():
    global current_menu, cursor_idx, combat_log, active_hero_idx
    hero = squad[active_hero_idx]

    if current_menu == "MAIN":
        if cursor_idx == 0:    # Hành động
            current_menu = "ACTION"
            cursor_idx = 0
        elif cursor_idx == 1:  # Kỹ năng
            current_menu = "SKILL"
            cursor_idx = 0
        elif cursor_idx == 2:  # Túi đồ
            current_menu = "POUCH"
            cursor_idx = 0
        elif cursor_idx == 3:  # Chiến thuật
            current_menu = "TACTICS"
            cursor_idx = 0

    elif current_menu == "ACTION":
        if cursor_idx == 0:    # Tấn công -> mở Target Limb
            current_menu = "TARGET_LIMB"
            cursor_idx = 0
        elif cursor_idx == 1:  # Phòng thủ
            hero["is_guarding"] = True
            combat_log = f"{hero['name']} giương khiên thủ thế! Sát thương nhận vào giảm 70% trong lượt này."
            enemy_turn()
            current_menu = "MAIN"
            cursor_idx = 0
        elif cursor_idx == 2:  # Đổi tướng -> mở bảng Tactical Roster Switch
            current_menu = "SWITCH_HERO"
            cursor_idx = active_hero_idx
        elif cursor_idx == 3:  # Quay lại
            current_menu = "MAIN"
            cursor_idx = 0

    elif current_menu == "SWITCH_HERO":
        if cursor_idx < len(squad):
            if cursor_idx == active_hero_idx:
                combat_log = f"{squad[cursor_idx]['name']} đã đang ở vị trí tiên phong!"
            elif squad[cursor_idx]["hp"] <= 0:
                combat_log = f"{squad[cursor_idx]['name']} đã gục ngã, không thể đổi lên tiên phong!"
            else:
                active_hero_idx = cursor_idx
                combat_log = f"CHUYỂN GIAO TIÊN PHONG! {squad[active_hero_idx]['name']} [{squad[active_hero_idx]['role']}] bước lên chỉ huy tác chiến!"
            current_menu = "MAIN"
            cursor_idx = 0
        else:
            # Quay lại
            current_menu = "ACTION"
            cursor_idx = 2

    elif current_menu == "TARGET_LIMB":
        if cursor_idx == 0:    # Đầu
            if monster["is_crawling"]:
                dmg = monster["hp"]
                monster["hp"] = 0
                monster["head_hp"] = 0
                monster["is_decapitated"] = True
                combat_log = f"CRITICAL INSTAKILL! Quái đang bò, {hero['name']} trảm ngọt đầu đối thủ! Gây {dmg} DMG!"
            else:
                import random
                if random.random() < 0.35:
                    dmg = monster["hp"]
                    monster["hp"] = 0
                    monster["head_hp"] = 0
                    monster["is_decapitated"] = True
                    combat_log = f"TRẢM ĐẦU TỨC THÌ (DECAPITATION)! Lưỡi gươm phạt đứt cổ quái vật! Gây {dmg} DMG!"
                else:
                    dmg = 15
                    monster["hp"] = max(0, monster["hp"] - dmg)
                    monster["head_hp"] = max(0, monster["head_hp"] - 12)
                    combat_log = f"Đòn chém sượt qua đầu quái vật! Gây {dmg} sát thương sứt mẻ."
            enemy_turn()
            current_menu = "MAIN"
            cursor_idx = 0
        elif cursor_idx == 1:  # Thân
            dmg = hero["atk"] - (monster["def"] // 2)
            dmg = max(18, dmg)
            monster["hp"] = max(0, monster["hp"] - dmg)
            monster["torso_hp"] = max(0, monster["torso_hp"] - dmg)
            combat_log = f"{hero['name']} đâm thẳng vào ngực đối thủ! Gây {dmg} DMG sát thương chuẩn."
            enemy_turn()
            current_menu = "MAIN"
            cursor_idx = 0
        elif cursor_idx == 2:  # Tay phải
            monster["arm_r_hp"] = 0
            monster["is_disarmed"] = True
            monster["atk"] = max(10, monster["atk"] - 10)
            combat_log = "CHẶT ĐỨT TAY PHẢI! Thanh kiếm quỷ rơi xuống đất, quái vật bị tước vũ khí!"
            enemy_turn()
            current_menu = "MAIN"
            cursor_idx = 0
        elif cursor_idx == 3:  # Tay trái
            monster["arm_l_hp"] = 0
            monster["is_guard_broken"] = True
            monster["atk"] = max(8, monster["atk"] - 6)
            combat_log = "PHÁ HỦY TAY TRÁI! Khiên bảo vệ vỡ nát, sức tấn công của quái giảm 50%!"
            enemy_turn()
            current_menu = "MAIN"
            cursor_idx = 0
        elif cursor_idx == 4:  # Đôi chân
            monster["legs_hp"] = 0
            monster["is_crawling"] = True
            combat_log = "BẺ GÃY CHÂN QUÁI! Shadow Swordsman đổ gục xuống sàn đá, rơi vào thế BÒ LÊ LẾT!"
            enemy_turn()
            current_menu = "MAIN"
            cursor_idx = 0
        elif cursor_idx == 5:  # Quay lại
            current_menu = "ACTION"
            cursor_idx = 0

    elif current_menu == "SKILL":
        if cursor_idx == 0:    # Black Orb
            if hero["mind"] >= 15:
                hero["mind"] -= 15
                dmg = 45
                monster["hp"] = max(0, monster["hp"] - dmg)
                combat_log = f"BLACK ORB! Hắc cầu xé toang hư không bắn XUYÊN 100% GIÁP! Gây {dmg} DMG!"
                enemy_turn()
            else:
                combat_log = "Không đủ điểm Tâm Trí (Mind) để thi triển ma pháp hắc ám Black Orb!"
            current_menu = "MAIN"
            cursor_idx = 0
        elif cursor_idx == 1:  # Leg sweep
            monster["legs_hp"] = 0
            monster["is_crawling"] = True
            combat_log = "LEG SWEEP! Cú gạt chân hoàn hảo ép đối phương lập tức bò lê lết!"
            enemy_turn()
            current_menu = "MAIN"
            cursor_idx = 0
        elif cursor_idx == 2:  # Devour
            monster["hp"] = max(0, monster["hp"] - 20)
            hero["hunger"] = max(0, hero["hunger"] - 40)
            combat_log = f"DEVOUR! {hero['name']} cắn xé máu thịt quái gây 20 DMG! Độ đói giảm mạnh -40 Hunger!"
            enemy_turn()
            current_menu = "MAIN"
            cursor_idx = 0
        elif cursor_idx == 3:  # Quay lại
            current_menu = "MAIN"
            cursor_idx = 0

    elif current_menu == "POUCH":
        if cursor_idx == 0:    # Poppy
            if inventory["poppy"] > 0:
                inventory["poppy"] -= 1
                hero["hp"] = min(hero["max_hp"], hero["hp"] + 50)
                combat_log = f"{hero['name']} nhai Hoa Anh Túc trắng (White Poppy)! Vết thương khép lại, hồi phục +50 HP."
                enemy_turn()
            else:
                combat_log = "Đã hết Hoa Anh Túc trong túi đồ!"
            current_menu = "MAIN"
            cursor_idx = 0
        elif cursor_idx == 1:  # Weed
            if inventory["weed"] > 0:
                inventory["weed"] -= 1
                hero["hp"] = min(hero["max_hp"], hero["hp"] + 120)
                combat_log = f"{hero['name']} đốt Thảo Dược quý (Marijuana Weed)! Khí huyết dâng trào, hồi phục +120 HP."
                enemy_turn()
            else:
                combat_log = "Đã hết Thảo Dược trong túi đồ!"
            current_menu = "MAIN"
            cursor_idx = 0
        elif cursor_idx == 2:  # Bread
            if inventory["bread"] > 0:
                inventory["bread"] -= 1
                hero["hunger"] = max(0, hero["hunger"] - 40)
                combat_log = f"{hero['name']} nuốt vội mẩu Bánh Mì mốc (Moldy Bread)! Dạ dày ấm lại, giảm -40 điểm Đói."
            else:
                combat_log = "Đã hết Bánh Mì trong túi đồ!"
            current_menu = "MAIN"
            cursor_idx = 0
        elif cursor_idx == 3:  # Ale
            if inventory["ale"] > 0:
                inventory["ale"] -= 1
                hero["mind"] = min(hero["max_mind"], hero["mind"] + 35)
                combat_log = f"{hero['name']} nốc một ngụm Bình Rượu Ale cay nồng! Tinh thần tỉnh táo, hồi phục +35 Mind."
            else:
                combat_log = "Đã hết Rượu Ale trong túi đồ!"
            current_menu = "MAIN"
            cursor_idx = 0
        elif cursor_idx == 4:  # Quay lại
            current_menu = "MAIN"
            cursor_idx = 0

    elif current_menu == "TACTICS":
        if cursor_idx == 0:    # Berserk
            hero["stance"] = "BERSERK (+50% ATK)"
            combat_log = f"{hero['name']} kích hoạt THẾ BERSERK! Mắt đỏ rực, lực sát thương tăng vọt +50%!"
            current_menu = "MAIN"
            cursor_idx = 0
        elif cursor_idx == 1:  # Iron Guard
            hero["stance"] = "IRON GUARD (-70% DMG)"
            combat_log = f"{hero['name']} vào THẾ IRON GUARD! Dựng khiên sắt, giảm 70% mọi sát thương nhận vào."
            current_menu = "MAIN"
            cursor_idx = 0
        elif cursor_idx == 2:  # Agile
            hero["stance"] = "AGILE DANCE (+35% DODGE)"
            combat_log = f"{hero['name']} chuyển sang THẾ AGILE DANCE! Thân pháp thoăn thoắt, tăng 35% tỷ lệ né đòn."
            current_menu = "MAIN"
            cursor_idx = 0
        elif cursor_idx == 3:  # Flee
            combat_log = "Tháo chạy thành công khỏi cuộc giao tranh! Trở về hành lang an toàn."
            time.sleep(1)
            sys.exit(0)
        elif cursor_idx == 4:  # Quay lại
            current_menu = "MAIN"
            cursor_idx = 0

def enemy_turn():
    global combat_log, active_hero_idx
    hero = squad[active_hero_idx]

    if monster["hp"] <= 0:
        combat_log += " | Quái vật gục ngã trên vũng máu! CHIẾN THẮNG!"
        return

    dmg = monster["atk"] - (hero["def"] // 2)
    if hero["is_guarding"]:
        dmg = int(dmg * 0.3)
        hero["is_guarding"] = False

    dmg = max(4, dmg)
    hero["hp"] = max(0, hero["hp"] - dmg)
    combat_log += f" | Quái phản kích chém trúng giáp! {hero['name']} mất {dmg} HP."

    # Hero Down check
    if hero["hp"] == 0:
        combat_log += f" | ⚠️ HERO DOWN! {hero['name']} đã gục ngã!"
        # Auto swap to next living companion
        for idx, comp in enumerate(squad):
            if comp["hp"] > 0:
                active_hero_idx = idx
                combat_log += f" -> {comp['name']} khẩn cấp nhảy lên thế chỗ!"
                break

def run_interactive_loop():
    global current_menu, cursor_idx

    while True:
        render_screen()
        menu_data = get_current_menu_data()
        num_options = len(menu_data["options"])

        if os.name == 'nt':
            ch = msvcrt.getch()
            if ch in (b'\x00', b'\xe0'):
                ext = msvcrt.getch()
                if ext == b'H':    # Up Arrow
                    cursor_idx = (cursor_idx - 1) % num_options
                elif ext == b'P':  # Down Arrow
                    cursor_idx = (cursor_idx + 1) % num_options
            elif ch in (b'w', b'W'):
                cursor_idx = (cursor_idx - 1) % num_options
            elif ch in (b's', b'S'):
                cursor_idx = (cursor_idx + 1) % num_options
            elif ch in (b'\r', b'\n', b' '):  # Enter or Space
                handle_selection()
            elif ch in (b'b', b'B', b'\x1b'):  # Back / Escape
                if current_menu != "MAIN":
                    current_menu = "MAIN"
                    cursor_idx = 0
            elif ch in (b'q', b'Q', b'\x03'):  # Quit
                print("\n[OK] Thoát chế độ Demo UI. Hẹn gặp lại!")
                break
            elif ch in (b'1', b'2', b'3', b'4', b'5', b'6'):
                num = int(ch.decode('ascii')) - 1
                if num < num_options:
                    cursor_idx = num
                    handle_selection()
        else:
            line = sys.stdin.readline().strip().lower()
            if line == 'w':
                cursor_idx = (cursor_idx - 1) % num_options
            elif line == 's':
                cursor_idx = (cursor_idx + 1) % num_options
            elif line in ('', 'c', 'enter'):
                handle_selection()
            elif line in ('b', 'q'):
                break

def run_showcase_trace():
    print("\n>>> BẮT ĐẦU SHOWCASE TỰ ĐỘNG CHUỖI GIAO DIỆN MỚI <<<\n")
    states = [
        ("MAIN", 0, "BƯỚC 1: DUAL CARDS & MENU GỐC - Thẻ quái vật & Thẻ tiên phong Cahara"),
        ("ACTION", 2, "BƯỚC 2: Vào 'Hành Động' -> Chọn 'Đổi Tướng'"),
        ("SWITCH_HERO", 1, "BƯỚC 3: MỞ BẢNG ĐIỀU ĐỘNG ĐỘI HÌNH - D'arce đang sáng (xem HP/MND/HNG rõ ràng)"),
        ("TARGET_LIMB", 2, "BƯỚC 4: Vào 'Tấn Công' -> Chọn chặt 'Tay Phải' của quái để tước kiếm quỷ"),
        ("POUCH", 0, "BƯỚC 5: Mở 'Túi Đồ' cắn thuốc hồi phục sinh lực")
    ]

    global current_menu, cursor_idx
    for m_state, c_idx, step_desc in states:
        current_menu = m_state
        cursor_idx = c_idx
        render_screen()
        print(f"\n  \033[1;32m>>> [MINH HỌA]: {step_desc} <<<\033[0m")
        time.sleep(1.2)

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--showcase":
        run_showcase_trace()
    else:
        run_interactive_loop()
