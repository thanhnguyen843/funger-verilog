#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
================================================================================
FEAR & HUNGER: TERMINAL LABYRINTH - INTERACTIVE COMBAT UI DEMO
================================================================================
Demo giao dien chien dau moi dap ung 100% y tuong nguoi dung:
1. 4 nut chinh lon, dieu huong bang W/S (hoac Mui ten Len/Xuong).
2. Chi sang duy nhat lua chon dang duoc tro toi, 3 lua chon con lai tat di (giam choi mat).
3. Phan cap 2-3 tang: Chon Action -> Xoa menu cu va in ra 4 sub-options (Danh, Thu, Doi tuong, Quay lai).
   Chon Danh -> Xoa va in ra cac vi tri nham danh (Dau, Than, Tay, Chan).
4. Bo cuc gian cach 1-2 dong, can le chuan xac 100 cot, khong loe loet.
5. Co icon nho va mui ten ro rang.
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

if os.name == 'nt':
    import msvcrt

# Game State Variables for Demo
monster = {
    "name": "SHADOW SWORDSMAN",
    "id": 8,
    "hp": 95,
    "max_hp": 95,
    "atk": 24,
    "def": 14,
    "head_hp": 24,
    "arm_r_hp": 30,
    "arm_l_hp": 30,
    "legs_hp": 35,
    "is_crawling": False,
    "is_disarmed": False
}

hero = {
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
    "is_guarding": False,
    "stance": "STANDARD BALANCED"
}

inventory = {
    "poppy": 2,      # +50 HP
    "weed": 1,       # +120 HP
    "bread": 3,      # -40 Hunger
    "ale": 2         # +35 Mind
}

combat_log = "Trận chiến bắt đầu! Shadow Swordsman rút kiếm bóng tối thủ thế."

# Menu State Machine
# Levels:
# "MAIN" -> Root 4 buttons
# "ACTION" -> Đánh, Thủ, Đổi tướng, Quay lại
# "TARGET_LIMB" -> Đầu, Thân, Tay phải, Tay trái, Đôi chân, Quay lại
# "SKILL" -> Black Orb, Leg Sweep, Devour, Quay lại
# "POUCH" -> Hoa Poppy, Thảo dược Weed, Bánh mì, Rượu Ale, Quay lại
# "TACTICS" -> Thế Berserk, Thế Iron Guard, Thế Agile, Tháo chạy, Quay lại

current_menu = "MAIN"
cursor_idx = 0

def make_bar(curr, max_v, bar_len=14, color_code="32"):
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
    # Clear terminal screen
    sys.stdout.write("\033[2J\033[H")

    # =========================================================================
    # HEADER
    # =========================================================================
    print("\033[1;30m+====================================================================================================+\033[0m")
    print("\033[1;30m| \033[1;37m        FEAR & HUNGER: TERMINAL LABYRINTH - ĐẤU TRƯỜNG CHIẾN THUẬT (DEMO UI MỚI)                   \033[1;30m|\033[0m")
    print("\033[1;30m+====================================================================================================+\033[0m")
    print()  # Breathing room: 1 blank line

    # =========================================================================
    # SECTION 1: COMBAT ARENA (Monster Left vs Hero Right)
    # =========================================================================
    m_bar = make_bar(monster["hp"], monster["max_hp"], 12, "31")
    h_bar = make_bar(hero["hp"], hero["max_hp"], 12, "32")
    m_mind = make_bar(hero["mind"], hero["max_mind"], 10, "36")
    m_hng = make_bar(hero["hunger"], hero["max_hunger"], 10, "33")

    m_status = "Đang cầm Cursed Blade"
    if monster["is_crawling"]:
        m_status = "\033[1;31mBỊ BẺ GÃY CHÂN (BÒ LÊ LẾT)\033[0m"
    elif monster["is_disarmed"]:
        m_status = "\033[1;33mBỊ TƯỚC VŨ KHÍ (DISARMED)\033[0m"

    h_guard_txt = "\033[1;32m[ĐANG THỦ -70%]\033[0m" if hero["is_guarding"] else "\033[90mBình thường\033[0m"

    print("  \033[1;37m[ĐỐI THỦ / MONSTER]\033[0m                                 \033[1;30m|\033[0m  \033[1;37m[THÁM HIỂM / ACTIVE EXPLORER]\033[0m")
    print(f"  \033[1;31m👹 #{monster['id']:02d} {monster['name']:<24}\033[0m \033[1;30m|\033[0m  \033[1;32m🛡️ {hero['name']:<12}\033[0m \033[90m[{hero['role']}]\033[0m")
    print(f"  Sinh Lực : {m_bar} \033[1;31m{monster['hp']:3d}/{monster['max_hp']:3d} HP\033[0m \033[1;30m|\033[0m  Máu (HP) : {h_bar} \033[1;32m{hero['hp']:3d}/{hero['max_hp']:3d} HP\033[0m")
    print(f"  Công/Thủ : ATK: {monster['atk']:2d} | DEF: {monster['def']:2d}                  \033[1;30m|\033[0m  Tâm Trí  : {m_mind} \033[1;36m{hero['mind']:3d}/100 Mind\033[0m")
    print(f"  Bộ Phận  : Đầu | Thân | Tay P | Tay T | Chân     \033[1;30m|\033[0m  Độ Đói   : {m_hng} \033[1;33m{hero['hunger']:3d}/100 Hng\033[0m")
    print(f"  Trạng Thái: {m_status:<36} \033[1;30m|\033[0m  Thế Trận : \033[1;37m{hero['stance']:<16}\033[0m | Thủ: {h_guard_txt}")
    print()  # Breathing room: 1 blank line

    # =========================================================================
    # SECTION 2: COMBAT LOG BOX (Clear, high-contrast, strictly aligned)
    # =========================================================================
    print("\033[1;30m+----------------------------------------------------------------------------------------------------+\033[0m")
    print(f"| \033[1;33m🔔 BẢNG TIN CHIẾN SỰ:\033[0m \033[1;37m{combat_log:<75}\033[1;30m |\033[0m")
    print("\033[1;30m+----------------------------------------------------------------------------------------------------+\033[0m")
    print()  # Breathing room: 1 blank line

    # =========================================================================
    # SECTION 3: HIERARCHICAL MENU BOX (Dynamic In-Place Replacement)
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
            # Highlighted line: Vivid Amber / Gold + Clear Pointer Arrow '▶'
            print(f"    \033[1;33m▶  [{idx+1}] {icon}  \033[1;37;43m {label:<22} \033[0m \033[1;33m{desc}\033[0m")
        else:
            # Dimmed line: Dark Gray muted text (Eliminates eye strain)
            print(f"       \033[90m[{idx+1}] {icon}   {label:<22} {desc}\033[0m")

    # Fill remaining space so menu height is consistent across levels
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
        print("  \033[90m[ĐIỀU HƯỚNG]:\033[0m \033[1;37m[W/S]\033[0m Lên/Xuống  |  \033[1;37m[Enter / Space]\033[0m Chọn Lệnh  |  \033[1;33m[B / Esc]\033[0m Quay Lại Menu Chính")
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
                {"icon": "🔄", "label": "ĐỔI TƯỚNG (SWITCH)",     "desc": "-> Chuyển quyền điều khiển sang đồng đội còn sống khác"},
                {"icon": "↩️", "label": "QUAY LẠI (BACK)",       "desc": "-> Trở về Danh mục Lệnh chính bên ngoài"}
            ]
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
    global current_menu, cursor_idx, combat_log

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
            combat_log = "Cahara giương kiếm thủ thế! Sát thương nhận vào giảm 70% trong lượt này."
            enemy_turn()
            current_menu = "MAIN"
            cursor_idx = 0
        elif cursor_idx == 2:  # Đổi tướng
            combat_log = "Chuyển giao quyền tác chiến sang D'arce [Holy Knight]!"
            current_menu = "MAIN"
            cursor_idx = 0
        elif cursor_idx == 3:  # Quay lại
            current_menu = "MAIN"
            cursor_idx = 0

    elif current_menu == "TARGET_LIMB":
        if cursor_idx == 0:    # Đầu
            if monster["is_crawling"]:
                dmg = monster["hp"]
                monster["hp"] = 0
                combat_log = f"CRITICAL INSTAKILL! Quái đang bò, Cahara trảm ngọt đầu đối thủ! Gây {dmg} DMG!"
            else:
                # 25% chance in demo, let's trigger decapitation or miss
                import random
                if random.random() < 0.35:
                    dmg = monster["hp"]
                    monster["hp"] = 0
                    combat_log = f"TRẢM ĐẦU TỨC THÌ (DECAPITATION)! Lưỡi gươm phạt đứt cổ quái vật! Gây {dmg} DMG!"
                else:
                    dmg = 15
                    monster["hp"] = max(0, monster["hp"] - dmg)
                    combat_log = f"Đòn chém sượt qua đầu quái vật! Gây {dmg} sát thương sứt mẻ."
            enemy_turn()
            current_menu = "MAIN"
            cursor_idx = 0
        elif cursor_idx == 1:  # Thân
            dmg = 32
            monster["hp"] = max(0, monster["hp"] - dmg)
            combat_log = f"Cahara đâm thẳng vào ngực đối thủ! Gây {dmg} DMG sát thương chuẩn."
            enemy_turn()
            current_menu = "MAIN"
            cursor_idx = 0
        elif cursor_idx == 2:  # Tay phải
            monster["is_disarmed"] = True
            monster["atk"] = max(10, monster["atk"] - 10)
            combat_log = "CHẶT ĐỨT TAY PHẢI! Thanh kiếm quỷ rơi xuống đất, quái vật bị tước vũ khí!"
            enemy_turn()
            current_menu = "MAIN"
            cursor_idx = 0
        elif cursor_idx == 3:  # Tay trái
            monster["atk"] = max(8, monster["atk"] - 6)
            combat_log = "PHÁ HỦY TAY TRÁI! Khiên bảo vệ vỡ nát, sức tấn công của quái giảm 50%!"
            enemy_turn()
            current_menu = "MAIN"
            cursor_idx = 0
        elif cursor_idx == 4:  # Đôi chân
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
                combat_log = f"BLACK ORB! Hắc cầu xé toang hư không bắn XUYÊN GIÁP! Gây {dmg} phép DMG!"
                enemy_turn()
            else:
                combat_log = "Không đủ điểm Tâm Trí (Mind) để thi triển ma pháp hắc ám Black Orb!"
            current_menu = "MAIN"
            cursor_idx = 0
        elif cursor_idx == 1:  # Leg sweep
            monster["is_crawling"] = True
            combat_log = "LEG SWEEP! Cú gạt chân hoàn hảo ép đối phương lập tức bò lê lết!"
            enemy_turn()
            current_menu = "MAIN"
            cursor_idx = 0
        elif cursor_idx == 2:  # Devour
            monster["hp"] = max(0, monster["hp"] - 20)
            hero["hunger"] = max(0, hero["hunger"] - 40)
            combat_log = "DEVOUR! Cắn xé máu thịt quái gây 20 DMG! Độ đói giảm mạnh -40 Hunger!"
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
                combat_log = "Nhai Hoa Anh Túc trắng (White Poppy)! Vết thương khép miệng, hồi phục +50 HP."
                enemy_turn()
            else:
                combat_log = "Đã hết Hoa Anh Túc trong túi đồ!"
            current_menu = "MAIN"
            cursor_idx = 0
        elif cursor_idx == 1:  # Weed
            if inventory["weed"] > 0:
                inventory["weed"] -= 1
                hero["hp"] = min(hero["max_hp"], hero["hp"] + 120)
                combat_log = "Đốt Thảo Dược quý (Marijuana Weed)! Khí huyết dâng trào, hồi phục +120 HP."
                enemy_turn()
            else:
                combat_log = "Đã hết Thảo Dược trong túi đồ!"
            current_menu = "MAIN"
            cursor_idx = 0
        elif cursor_idx == 2:  # Bread
            if inventory["bread"] > 0:
                inventory["bread"] -= 1
                hero["hunger"] = max(0, hero["hunger"] - 40)
                combat_log = "Nuốt vội mẩu Bánh Mì mốc (Moldy Bread)! Dạ dày ấm lại, giảm -40 điểm Đói."
            else:
                combat_log = "Đã hết Bánh Mì trong túi đồ!"
            current_menu = "MAIN"
            cursor_idx = 0
        elif cursor_idx == 3:  # Ale
            if inventory["ale"] > 0:
                inventory["ale"] -= 1
                hero["mind"] = min(hero["max_mind"], hero["mind"] + 35)
                combat_log = "Nốc một ngụm Bình Rượu Ale cay nồng! Tinh thần tỉnh táo, hồi phục +35 Mind."
            else:
                combat_log = "Đã hết Rượu Ale trong túi đồ!"
            current_menu = "MAIN"
            cursor_idx = 0
        elif cursor_idx == 4:  # Quay lại
            current_menu = "MAIN"
            cursor_idx = 0

    elif current_menu == "TACTICS":
        if cursor_idx == 0:    # Berserk
            hero["stance"] = "BERSERK OFFENSE (+50% ATK)"
            combat_log = "Kích hoạt THẾ BERSERK! Mắt đỏ rực, lực sát thương tăng vọt +50%!"
            current_menu = "MAIN"
            cursor_idx = 0
        elif cursor_idx == 1:  # Iron Guard
            hero["stance"] = "IRON GUARD (-70% DMG)"
            combat_log = "Vào THẾ IRON GUARD! Dựng khiên sắt, giảm 70% mọi sát thương nhận vào."
            current_menu = "MAIN"
            cursor_idx = 0
        elif cursor_idx == 2:  # Agile
            hero["stance"] = "AGILE DANCE (+35% DODGE)"
            combat_log = "Chuyển sang THẾ AGILE DANCE! Thân pháp thoăn thoắt, tăng 35% tỷ lệ né đòn."
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
    global combat_log
    if monster["hp"] <= 0:
        combat_log += " | Quái vật gục ngã trên vũng máu! CHIẾN THẮNG!"
        return

    dmg = monster["atk"] - (hero["def"] // 2)
    if hero["is_guarding"]:
        dmg = int(dmg * 0.3)
        hero["is_guarding"] = False

    dmg = max(4, dmg)
    hero["hp"] = max(0, hero["hp"] - dmg)
    combat_log += f" | Quái phản kích chém trúng giáp! Cahara mất {dmg} HP."

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
    """Chế độ tự động in ra chuỗi diễn biến UI để kiểm tra không cần nhấn phím"""
    print("\n>>> BẮT ĐẦU SHOWCASE TỰ ĐỘNG CHUỖI GIAO DIỆN MỚI <<<\n")
    states = [
        ("MAIN", 0, "BƯỚC 1: MENU CHÍNH - Con trỏ ở [1] HÀNH ĐỘNG (Sáng màu vàng, 3 mục dưới tắt)"),
        ("MAIN", 1, "BƯỚC 2: Bấm 'S' di chuyển xuống - [2] KỸ NĂNG sáng lên, mục 1 tắt đi"),
        ("ACTION", 0, "BƯỚC 3: Chọn 'Hành Động' - Xóa menu cũ, in ra 4 lựa chọn con (Đánh, Thủ, Đổi, Về)"),
        ("TARGET_LIMB", 0, "BƯỚC 4: Chọn 'Tấn Công' - Xóa đi và in ra các bộ phận nhắm đánh (Đầu, Thân, Tứ chi)"),
        ("POUCH", 0, "BƯỚC 5: Trở ra mở 'Túi Đồ' - In ra danh sách thuốc Poppy, Bread, Ale với số lượng rõ ràng")
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
