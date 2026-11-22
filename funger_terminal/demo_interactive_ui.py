#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
================================================================================
FEAR & HUNGER: TERMINAL LABYRINTH - ĐẤU TRƯỜNG CHÉO PHONG CÁCH POKÉMON
(POKÉMON-STYLE DIAGONAL COMBAT ARENA & DYNAMIC DEBUFF SYSTEM)
================================================================================
Thiết kế chuẩn công thái học và triết lý đấu trường chéo kinh điển:
1. BỐ CỤC ĐỐI KHÁNG CHÉO (POKÉMON DIAGONAL ARENA - CHUẨN 100 CỘT TUYỆT ĐỐI):
   - NỬA TRÊN (KHỐI ĐỐI THỦ):
     * Bên Trái (Cột 1-54): Thẻ Thông Tin Quái Vật (Thanh Máu Tổng Lớn + Ô Debuff Động).
     * Bên Phải (Cột 61-100): Model Pixel Art Quái Vật Khổ Lớn (Đứng Uy Phong / Bò Lê Lết).
   - NỬA DƯỚI (KHỐI PHE MÌNH):
     * Bên Trái (Cột 1-40): Model Pixel Art Anh Hùng Khổ Lớn (Nhìn Hướng Về Đối Thủ).
     * Bên Phải (Cột 47-100): Thẻ Thông Tin Tiên Phong (Máu, Tâm Trí, Đói, Thế Trận, Đồng Đội).
2. CƠ CHẾ 1 THANH MÁU TỔNG + Ô DEBUFF TỨ CHI ĐỘNG (XÓA BỎ 5 THANH MÁU CON RÁC MẮT):
   - Mọi đòn đánh đều trừ thẳng vào Máu Tổng (Sinh Lực).
   - Ô Debuff ban đầu hoàn toàn sạch sẽ, hiển thị thể trạng lành lặn.
   - Chặt tay phải -> Debuff: [TAY PHẢI: ĐÃ CHẶT ĐỨT] (Rơi kiếm, tước vũ khí, giảm ATK).
   - Chặt tay trái -> Debuff: [TAY TRÁI: ĐÃ CHẶT ĐỨT] (Phá khiên, giảm 50% uy lực).
   - Bẻ gãy chân  -> Debuff: [ĐÔI CHÂN: ĐÃ BỊ BẺ GÃY] -> ÉP BÒ LÊ LẾT!
     * 100% THÁO CHẠY THOÁT THÂN THÀNH CÔNG!
     * TỶ LỆ TRẢM ĐẦU TĂNG LÊN 100% KẾT LIỄU!
     * Model quái lập tức chuyển sang sprite BÒ LÊ LẾT!
3. BẢNG ĐIỀU ĐỘNG ĐỘI HÌNH MINH BẠCH (TACTICAL ROSTER SWITCH):
   - Khi chọn "Đổi Tướng", hiện bảng 4 nhân vật với HP, Tâm trí, Đói.
   - Đổi sang nhân vật nào thì Model và Thẻ Nửa Dưới lập tức cập nhật theo người đó.
4. MENU 4 NÚT CON TRỎ W/S IN ĐÈ TẠI CHỖ:
   - Highlight 1 mục duy nhất, không chói mắt, căn lề thẳng tắp chuẩn 100 cột.
================================================================================
"""

import sys
import os
import time
import re
import unicodedata

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

ANSI_REGEX = re.compile(r'\x1b\[[0-9;]*[mGKH]')

def char_width(c):
    # Emojis and fullwidth East Asian characters occupy 2 terminal columns
    ea = unicodedata.east_asian_width(c)
    if ea in ('W', 'F'):
        return 2
    # Variation selectors (e.g. \ufe0f in 🛡️) and non-spacing marks take 0 columns
    if unicodedata.category(c) in ('Mn', 'Me', 'Cf'):
        return 0
    return 1

def display_width(s):
    clean = ANSI_REGEX.sub('', s)
    return sum(char_width(c) for c in clean)

def pad_str(s, n):
    cur = display_width(s)
    if cur < n:
        return s + " " * (n - cur)
    return s

def make_card_row(content, c_card):
    return f"{c_card}| {pad_str(content, 50)} {c_card}|"

def make_bar(curr, max_v, bar_len=12, color_code="32"):
    if max_v <= 0:
        ratio = 0
    else:
        ratio = max(0.0, min(1.0, curr / float(max_v)))
    filled = int(ratio * bar_len)
    if filled == 0 and curr > 0:
        filled = 1
    empty = bar_len - filled
    return f"\033[1;{color_code}m" + "█" * filled + "\033[90m" + "░" * empty + "\033[0m"

# =============================================================================
# SPRITE PIXEL ART MODELS (12-14 chars wide, 8 half-block lines tall)
# =============================================================================
# Monster Sprites (Shadow Swordsman)
MONSTER_SPRITE_INTACT = [
    "\033[1;31m   ▄▀▀▀▀▀▄  \033[0m",
    "\033[1;31m  ▀  \033[1;37m█ █\033[1;31m  ▀ \033[0m",
    "\033[1;31m  ▀▀▄▀▀▀▀▄▀▀\033[0m",
    "\033[1;31m   ▀▀ ▀ ▀▀  \033[0m",
    "\033[1;31m    ▀▀▀▀▀   \033[0m",
    "\033[1;31m    ▀▀▀▀▀▄  \033[0m",
    "\033[1;31m    ▀ ▀ ▀   \033[0m",
    "\033[1;31m    ▀   ▀   \033[0m"
]

MONSTER_SPRITE_CRAWLING = [
    "\033[1;31m            \033[0m",
    "\033[1;31m            \033[0m",
    "\033[1;31m   ▄▀▀▀▀▀▄  \033[0m",
    "\033[1;31m  ▀  \033[1;37m█ █\033[1;31m  ▀ \033[0m",
    "\033[1;31m  ▀▀▄▀▀▀▀▄▀▀\033[0m",
    "\033[1;31m   ▀▀ ▀ ▀▀  \033[0m",
    "\033[1;31m ▄▀▀▀▀▀▀▀▀▀▄\033[0m",
    "\033[1;31m ▀▀▀▀  ▀▀▀▀ \033[0m"
]

MONSTER_SPRITE_DECAPITATED = [
    "\033[1;30m            \033[0m",
    "\033[1;30m            \033[0m",
    "\033[1;31m(ĐẦU ĐÃ LÌA CỔ)\033[0m",
    "\033[1;31m    ▄██▄    \033[0m",
    "\033[1;31m ▀▀▄▀████▄▀▀\033[0m",
    "\033[1;31m  ▀▀ ▀ ▀▀   \033[0m",
    "\033[1;31m▄▀▀▀▀▀▀▀▀▀▄ \033[0m",
    "\033[1;31m▀▀▀▀  ▀▀▀▀  \033[0m"
]

# Hero Sprites
HERO_SPRITES = {
    "CAHARA": [
        "\033[1;32m    ▄▀▀▀▄   \033[0m",
        "\033[1;32m   ▀▀▀▀▀▀▀  \033[0m",
        "\033[1;32m   ▄▀▀▀▀▀▄  \033[0m",
        "\033[1;32m    ▀▀▀▀▀   \033[0m",
        "\033[1;32m  ▄▀▀▀▀▀▀▀▄ \033[0m",
        "\033[1;32m  ▀▀▀▀▀▀▀▀▀ \033[0m",
        "\033[1;32m   ▀▀   ▀▀  \033[0m",
        "\033[1;32m   ▀▀   ▀▀  \033[0m"
    ],
    "D'ARCE": [
        "\033[1;33m   ▄▀▀▀▀▀▄  \033[0m",
        "\033[1;33m  ▀▀▀▀▀▀▀▀▀ \033[0m",
        "\033[1;33m  ▀▀▀▀▀▀▀▀▀ \033[0m",
        "\033[1;33m ▀▄▄▀▀▀▀▀▄▀ \033[0m",
        "\033[1;33m ▀▀▀▀▀▀▀▀▀▀ \033[0m",
        "\033[1;33m ▀▀▀▀▀▀▀▀▀▀ \033[0m",
        "\033[1;33m  ▀▀▀  ▀▀▀  \033[0m",
        "\033[1;33m   ▀    ▀   \033[0m"
    ],
    "ENKI": [
        "\033[1;35m    ▄▀▀▀▄   \033[0m",
        "\033[1;35m   ▀▀▀▀▀▀▀  \033[0m",
        "\033[1;35m  ▀▀▀▀▀▀▀▀▀ \033[0m",
        "\033[1;35m   ▀▀▀▀▀▀▀  \033[0m",
        "\033[1;35m   ▄▀▀▀▀▀▄  \033[0m",
        "\033[1;35m  ▄▀▀▀▀▀▀▀▄ \033[0m",
        "\033[1;35m  ▀▀▀▀▀▀▀▀▀ \033[0m",
        "\033[1;35m  ▀▀▀   ▀▀▀ \033[0m"
    ],
    "THE GIRL": [
        "\033[1;36m            \033[0m",
        "\033[1;36m    ▄▀▀▀▄   \033[0m",
        "\033[1;36m   ▀▀▀▀▀▀▀  \033[0m",
        "\033[1;36m   ▄▀▀▀▀▀▄  \033[0m",
        "\033[1;36m    ▀▀▀▀▀   \033[0m",
        "\033[1;36m   ▄▀▀▀▀▀▄  \033[0m",
        "\033[1;36m   ▀▀▀▀▀▀▀  \033[0m",
        "\033[1;36m    ▀   ▀   \033[0m"
    ]
}

# =============================================================================
# GAME DATA
# =============================================================================
monster = {
    "name": "SHADOW SWORDSMAN",
    "id": 8,
    "hp": 95,
    "max_hp": 95,
    "atk": 24,
    "def": 14,
    # Debuff flags
    "debuff_arm_r": False,     # Disarmed (Rơi kiếm, tước vũ khí)
    "debuff_arm_l": False,     # Guard Broken (Phá khiên)
    "debuff_legs": False,      # Crawling -> 100% flee, 100% head hit
    "debuff_decapitated": False # Head severed -> Instant death
}

squad = [
    {
        "name": "CAHARA",
        "role": "Mercenary / Swift Rogue",
        "hp": 125,
        "max_hp": 125,
        "mind": 100,
        "max_mind": 100,
        "hunger": 20,
        "max_hunger": 100,
        "atk": 33,
        "def": 21,
        "stance": "STANDARD BALANCED",
        "passive": "Bàn Tay Nhanh (-80% Bẫy)",
        "is_guarding": False,
        "debuffs": []
    },
    {
        "name": "D'ARCE",
        "role": "Holy Knight / Guardian",
        "hp": 145,
        "max_hp": 145,
        "mind": 90,
        "max_mind": 100,
        "hunger": 35,
        "max_hunger": 100,
        "atk": 30,
        "def": 30,
        "stance": "IRON GUARD (-70% DMG)",
        "passive": "Ý Chí Thép (Miễn Hoảng Loạn)",
        "is_guarding": False,
        "debuffs": []
    },
    {
        "name": "ENKI",
        "role": "Dark Priest / Occult Mage",
        "hp": 95,
        "max_hp": 95,
        "mind": 100,
        "max_mind": 100,
        "hunger": 15,
        "max_hunger": 100,
        "atk": 48,
        "def": 24,
        "stance": "OCCULT CONCENTRATION",
        "passive": "Khai Sáng (+5 MND/lượt)",
        "is_guarding": False,
        "debuffs": []
    },
    {
        "name": "THE GIRL",
        "role": "Innocent Ward / Nimble",
        "hp": 105,
        "max_hp": 105,
        "mind": 80,
        "max_mind": 100,
        "hunger": 10,
        "max_hunger": 100,
        "atk": 30,
        "def": 39,
        "stance": "AGILE DANCE (+35% DODGE)",
        "passive": "Thơ Dại (Quái giảm 30% DMG)",
        "is_guarding": False,
        "debuffs": []
    }
]

active_hero_idx = 0

inventory = {
    "poppy": 2,      # +50 HP, xóa vết thương cào
    "weed": 1,       # +120 HP
    "bread": 3,      # -40 Hunger
    "ale": 2         # +35 Mind, xóa hoảng loạn
}

combat_log = "Trận chiến bắt đầu! Shadow Swordsman rút thanh kiếm bóng tối thủ thế sát khí."

current_menu = "MAIN"
cursor_idx = 0

# =============================================================================
# RENDER SCREEN: POKÉMON-STYLE DIAGONAL ARENA (EXACT 100 COLUMNS)
# =============================================================================
def render_screen():
    global active_hero_idx
    hero = squad[active_hero_idx]

    sys.stdout.write("\033[2J\033[H")

    # -------------------------------------------------------------------------
    # MAIN HEADER BREADCRUMB (100 COLUMNS)
    # -------------------------------------------------------------------------
    print("\033[1;30m+====================================================================================================+\033[0m")
    print("\033[1;30m| \033[1;37m        FEAR & HUNGER: TERMINAL LABYRINTH - ĐẤU TRƯỜNG CHÉO (POKÉMON STYLE)                 \033[1;30m|\033[0m")
    print("\033[1;30m+====================================================================================================+\033[0m")
    print()  # 1 blank line spacing

    # -------------------------------------------------------------------------
    # ZONE 1: OPPONENT ZONE (TOP)
    # Left: Monster Tactical Card (54 cols)
    # Gap : 6 spaces
    # Right: Monster Sprite Model (40 cols)
    # Total: 54 + 6 + 40 = 100 columns
    # -------------------------------------------------------------------------
    c_mcard = "\033[1;33m" if current_menu == "TARGET_LIMB" else "\033[1;30m"
    m_border = f"{c_mcard}+" + "-" * 52 + f"+{c_mcard}\033[0m"

    # Select Monster Sprite (intact vs crawling vs decapitated)
    if monster["debuff_decapitated"]:
        m_sprite = MONSTER_SPRITE_DECAPITATED
        m_stance = "\033[1;31mTư Thế: ĐÃ BỊ TRẢM ĐẦU!\033[0m"
    elif monster["debuff_legs"]:
        m_sprite = MONSTER_SPRITE_CRAWLING
        m_stance = "\033[1;31mTư Thế: Đang Bò Lê Lết\033[0m"
    else:
        m_sprite = MONSTER_SPRITE_INTACT
        m_stance = "\033[90mTư Thế: Thủ Kiếm Sát Khí\033[0m"

    # Monster HP & Stats
    m_pct = int(max(0, monster["hp"]) / float(monster["max_hp"]) * 100)
    m_hp_bar = make_bar(monster["hp"], monster["max_hp"], 12, "31")
    atk_note = ""
    if monster["debuff_arm_r"] and monster["debuff_arm_l"]:
        atk_note = "\033[1;31m(MẤT 2 TAY: TÀN PHẾ)\033[0m"
    elif monster["debuff_arm_r"]:
        atk_note = "\033[1;33m(TƯỚC KIẾM: GIẢM CÔNG)\033[0m"
    elif monster["debuff_arm_l"]:
        atk_note = "\033[1;36m(PHÁ KHIÊN)\033[0m"

    # Prepare Monster Debuffs
    m_db_1 = ""
    m_db_2 = ""
    m_db_3 = ""

    if monster["debuff_decapitated"]:
        m_db_1 = "\033[1;31m💀 [TRẢM ĐẦU TỨC THÌ] QUÁI VẬT ĐÃ BỊ KẾT LIỄU!\033[0m"
        m_db_2 = "\033[90m   Thủ cấp lìa khỏi cổ, kẻ địch hoàn toàn tiêu diệt.\033[0m"
    elif monster["debuff_legs"]:
        m_db_1 = "\033[1;31m⚠️ [ĐÔI CHÂN: ĐÃ BẺ GÃY] -> Bò Lê Lết\033[0m"
        m_db_2 = "\033[1;32m   -> 100% THÁO CHẠY THOÁT THÂN THÀNH CÔNG!\033[0m"
        m_db_3 = "\033[1;31m   -> TỶ LỆ TRẢM ĐẦU TĂNG VỌT LÊN 100%!\033[0m"
    elif monster["debuff_arm_r"] or monster["debuff_arm_l"]:
        if monster["debuff_arm_r"]:
            m_db_1 = "\033[1;33m⚠️ [TAY PHẢI: ĐÃ CHẶT ĐỨT] -> Rơi Kiếm (TƯỚC KHÍ)\033[0m"
        if monster["debuff_arm_l"]:
            m_db_2 = "\033[1;36m⚠️ [TAY TRÁI: ĐÃ CHẶT ĐỨT] -> Phá Khiên (-50% Uy Lực)\033[0m"
    else:
        m_db_1 = "\033[90m• Thân thể lành lặn, chưa dính chấn thương nào.\033[0m"
        m_db_2 = "\033[90m  Nhắm đánh vào tứ chi để gài Debuff chiến thuật!\033[0m"

    # 10 Rows of Monster Card (54 display width each)
    m_card_rows = [
        m_border,
        make_card_row(f"\033[1;31m👹 #{monster['id']:02d} {monster['name']:<18}\033[90m[Standard Foe]\033[0m", c_mcard),
        make_card_row(f" \033[1;37mSinh Lực : {m_hp_bar} \033[1;31m{monster['hp']:3d}/{monster['max_hp']:3d} HP ({m_pct:3d}%)\033[0m", c_mcard),
        make_card_row(f" \033[1;37mCông/Thủ : ATK: {monster['atk']:2d} | DEF: {monster['def']:2d} {atk_note}\033[0m", c_mcard),
        make_card_row("", c_mcard),
        make_card_row("\033[1;33mTRẠNG THÁI & DEBUFF TỨ CHI:\033[0m", c_mcard),
        make_card_row(m_db_1, c_mcard),
        make_card_row(m_db_2, c_mcard),
        make_card_row(m_db_3, c_mcard),
        m_border
    ]

    # 10 Rows of Monster Model (40 display width each)
    m_model_rows = [
        pad_str("           \033[1;31m[ĐỐI THỦ: QUÁI VẬT]\033[0m", 40)
    ]
    for r in range(8):
        sp = m_sprite[r] if r < len(m_sprite) else "            "
        m_model_rows.append(pad_str(f"              {sp}", 40))
    m_model_rows.append(pad_str(f"       {m_stance}", 40))

    # Print Top Zone (Card Left + Model Right)
    for r_idx in range(10):
        left_str = m_card_rows[r_idx]
        right_str = m_model_rows[r_idx]
        print(f"{left_str}      {right_str}\033[0m")

    print()  # 1 blank line spacing

    # -------------------------------------------------------------------------
    # ZONE 2: PLAYER SQUAD ZONE (BOTTOM)
    # Left: Hero Sprite Model (40 cols)
    # Gap : 6 spaces
    # Right: Hero Tactical Card (54 cols)
    # Total: 40 + 6 + 54 = 100 columns
    # -------------------------------------------------------------------------
    c_hcard = "\033[1;32m" if current_menu in ("SWITCH_HERO", "POUCH", "TACTICS") else "\033[1;30m"
    h_border = f"{c_hcard}+" + "-" * 52 + f"+{c_hcard}\033[0m"

    # Select Hero Sprite
    h_sprite = HERO_SPRITES.get(hero["name"], HERO_SPRITES["CAHARA"])

    # Hero Bars & Stats
    h_pct = int(max(0, hero["hp"]) / float(hero["max_hp"]) * 100)
    h_hp_bar = make_bar(hero["hp"], hero["max_hp"], 12, "32")
    h_mnd_bar = make_bar(hero["mind"], hero["max_mind"], 10, "36")
    h_hng_bar = make_bar(hero["hunger"], hero["max_hunger"], 10, "33")

    # Hero Debuffs string
    if hero["debuffs"]:
        h_db_str = "\033[1;31m⚠️ " + ", ".join(hero["debuffs"]) + "\033[0m"
    else:
        h_db_str = "\033[1;32m• Thể trạng sung mãn, khỏe mạnh.\033[0m"

    # Reserve Squad string
    res_list = []
    for idx, comp in enumerate(squad):
        if idx != active_hero_idx:
            short_name = comp["name"][:5]
            res_list.append(f"{short_name}:{comp['hp']:3d}")
    res_str = " | ".join(res_list)

    # 10 Rows of Hero Model (40 display width each)
    h_model_rows = [
        pad_str("          \033[1;32m[TIÊN PHONG: PHE MÌNH]\033[0m", 40)
    ]
    for r in range(8):
        sp = h_sprite[r] if r < len(h_sprite) else "            "
        h_model_rows.append(pad_str(f"              {sp}", 40))
    h_model_rows.append(pad_str("        \033[1;37mVị Trí: Đội Trưởng Tiên Phong\033[0m", 40))

    # 10 Rows of Hero Card (54 display width each)
    h_card_rows = [
        h_border,
        make_card_row(f"\033[1;32m🛡️ {hero['name']:<12}\033[90m[{hero['role'][:22]}]\033[0m", c_hcard),
        make_card_row(f" \033[1;37mSinh Lực : {h_hp_bar} \033[1;32m{hero['hp']:3d}/{hero['max_hp']:3d} HP ({h_pct:3d}%)\033[0m", c_hcard),
        make_card_row(f" \033[1;37mTâm Trí  : {h_mnd_bar} \033[1;36m{hero['mind']:3d}/{hero['max_mind']:3d} MND\033[0m", c_hcard),
        make_card_row(f" \033[1;37mCơn Đói  : {h_hng_bar} \033[1;33m{hero['hunger']:3d}/{hero['max_hunger']:3d} HNG\033[0m", c_hcard),
        make_card_row(f" \033[1;37mThế Trận : \033[1;37m{hero['stance']}\033[0m", c_hcard),
        make_card_row(f" \033[1;37mNội Tại  : \033[90m{hero['passive']}\033[0m", c_hcard),
        make_card_row(f" \033[1;37mDebuff Ta: {h_db_str}", c_hcard),
        make_card_row(f" \033[1;37mĐồng Đội : \033[90m{res_str}\033[0m", c_hcard),
        h_border
    ]

    # Print Bottom Zone (Model Left + Card Right)
    for r_idx in range(10):
        left_str = h_model_rows[r_idx]
        right_str = h_card_rows[r_idx]
        print(f"{left_str}      {right_str}\033[0m")

    print()  # 1 blank line spacing

    # -------------------------------------------------------------------------
    # SECTION 3: COMBAT LOG BOX (100 COLUMNS)
    # -------------------------------------------------------------------------
    print("\033[1;30m+----------------------------------------------------------------------------------------------------+\033[0m")
    print(f"| \033[1;33m🔔 BẢNG TIN CHIẾN SỰ:\033[0m \033[1;37m{pad_str(combat_log, 75)}\033[1;30m |")
    print("\033[1;30m+----------------------------------------------------------------------------------------------------+\033[0m")
    print()  # 1 blank line spacing

    # -------------------------------------------------------------------------
    # SECTION 4: DYNAMIC 4-BUTTON MENU (IN-PLACE REPLACEMENT)
    # -------------------------------------------------------------------------
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

    # Consistent menu height (6 lines)
    for _ in range(max(0, 6 - len(options))):
        print()

    print()  # 1 blank line spacing

    # -------------------------------------------------------------------------
    # FOOTER: CONTROL GUIDE (100 COLUMNS)
    # -------------------------------------------------------------------------
    print("\033[1;30m====================================================================================================\033[0m")
    if current_menu == "MAIN":
        print("  \033[90m[ĐIỀU HƯỚNG]:\033[0m \033[1;37m[W/S]\033[0m Lên/Xuống  |  \033[1;37m[Enter / Space]\033[0m Mở Menu Con  |  \033[1;31m[Q]\033[0m Thoát Demo")
    else:
        print("  \033[90m[ĐIỀU HƯỚNG]:\033[0m \033[1;37m[W/S]\033[0m Lên/Xuống  |  \033[1;37m[Enter / Space]\033[0m Chọn Lệnh  |  \033[1;33m[B / Esc]\033[0m Quay Lại Menu")
    print("\033[1;30m====================================================================================================\033[0m")
    sys.stdout.flush()

# =============================================================================
# MENU DATA RESOLUTION
# =============================================================================
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
        flee_text = "Tháo chạy khỏi trận (\033[1;32m100% THOÁT THÀNH CÔNG VÌ QUÁI ĐANG BÒ!\033[0m)" if monster["debuff_legs"] else "Tháo chạy khỏi trận (50/50 nguy hiểm)"
        return {
            "title": "HÀNH ĐỘNG > CHỌN LOẠI TÁC CHIẾN (SUBMENU 1)",
            "options": [
                {"icon": "🎯", "label": "TẤN CÔNG (ATTACK)",      "desc": "-> Chọn bộ phận cơ thể để nhắm đánh & gài Debuff"},
                {"icon": "🛡️", "label": "PHÒNG THỦ (GUARD)",     "desc": "-> Giảm 70% sát thương nhận vào ở hiệp này, hồi nhẹ HP"},
                {"icon": "🔄", "label": "ĐỔI TƯỚNG (SWITCH)",     "desc": "-> Mở Bảng Danh Sách Đội Hình để chọn tướng tiên phong"},
                {"icon": "🏃", "label": "THÁO CHẠY (FLEE)",       "desc": f"-> {flee_text}"},
                {"icon": "↩️", "label": "QUAY LẠI (BACK)",       "desc": "-> Trở về Danh mục Lệnh chính bên ngoài"}
            ]
        }
    elif current_menu == "SWITCH_HERO":
        opts = []
        for idx, h in enumerate(squad):
            is_active = (idx == active_hero_idx)
            tag = " \033[1;32m[TIÊN PHONG]\033[0m" if is_active else ""
            st_icon = "🟢" if h["hp"] > 0 else "💀"
            opts.append({
                "icon": st_icon,
                "label": f"{h['name']} [{h['role'][:10]}]",
                "desc": f"HP: {h['hp']:3d}/{h['max_hp']:3d} | MND: {h['mind']:3d} | HNG: {h['hunger']:2d}{tag}"
            })
        opts.append({"icon": "↩️", "label": "QUAY LẠI (BACK)", "desc": "-> Giữ nguyên đội hình, quay lại menu Hành Động"})
        return {
            "title": "HÀNH ĐỘNG > BẢNG ĐIỀU ĐỘNG ĐỘI HÌNH (TACTICAL ROSTER SWITCH)",
            "options": opts
        }
    elif current_menu == "TARGET_LIMB":
        crawl_hint = "\033[1;32m(100% TRÚNG KẾT LIỄU!)\033[0m" if monster["debuff_legs"] else "(25% Trúng | TRẢM ĐẦU TỨC THÌ)"
        return {
            "title": "HÀNH ĐỘNG > TẤN CÔNG > CHỌN VỊ TRÍ NHẮM ĐÁNH (GÀI DEBUFF)",
            "options": [
                {"icon": "💀", "label": "ĐẦU (HEAD)",            "desc": f"-> {crawl_hint}"},
                {"icon": "🎯", "label": "THÂN (TORSO)",          "desc": "-> 100% Trúng | Đòn đánh an toàn, trừ lượng máu tổng lớn"},
                {"icon": "🗡️", "label": "TAY PHẢI (R-ARM)",      "desc": "-> 100% Trúng | Chặt đứt tay cầm kiếm -> TƯỚC VŨ KHÍ"},
                {"icon": "🛡️", "label": "TAY TRÁI (L-ARM)",      "desc": "-> 100% Trúng | Phá khiên/tay phụ -> GIẢM 50% CÔNG QUÁI"},
                {"icon": "🦵", "label": "ĐÔI CHÂN (LEGS)",        "desc": "-> 100% Trúng | Bẻ gãy chân -> ÉP BÒ (100% CHẠY TRỐN!)"},
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
                {"icon": "🌸", "label": f"HOA POPPY [{inventory['poppy']}]",  "desc": "-> Búp hoa anh túc | Hồi +50 HP & Xóa vết thương cào"},
                {"icon": "🌿", "label": f"THẢO DƯỢC [{inventory['weed']}]",  "desc": "-> Thảo dược quý | Đại hồi phục +120 HP"},
                {"icon": "🍞", "label": f"BÁNH MÌ [{inventory['bread']}]",    "desc": "-> Lương khô ngục tối | Giảm ngay 40 điểm Hunger"},
                {"icon": "🍺", "label": f"RƯỢU ALE [{inventory['ale']}]",     "desc": "-> Rượu lên men cổ | Khôi phục +35 Mind & Xóa hoảng loạn"},
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
                {"icon": "↩️", "label": "QUAY LẠI (BACK)",       "desc": "-> Trở về Danh mục Lệnh chính bên ngoài"}
            ]
        }
    return {"title": "MENU", "options": []}

# =============================================================================
# SELECTION LOGIC & COMBAT SIMULATION
# =============================================================================
def handle_selection():
    global current_menu, cursor_idx, combat_log, active_hero_idx
    hero = squad[active_hero_idx]

    if current_menu == "MAIN":
        if cursor_idx == 0:
            current_menu = "ACTION"
            cursor_idx = 0
        elif cursor_idx == 1:
            current_menu = "SKILL"
            cursor_idx = 0
        elif cursor_idx == 2:
            current_menu = "POUCH"
            cursor_idx = 0
        elif cursor_idx == 3:
            current_menu = "TACTICS"
            cursor_idx = 0

    elif current_menu == "ACTION":
        if cursor_idx == 0:    # Tấn công
            current_menu = "TARGET_LIMB"
            cursor_idx = 0
        elif cursor_idx == 1:  # Phòng thủ
            hero["is_guarding"] = True
            combat_log = f"{hero['name']} giương khiên thủ thế! Giảm 70% sát thương nhận vào lượt này."
            enemy_turn()
            current_menu = "MAIN"
            cursor_idx = 0
        elif cursor_idx == 2:  # Đổi tướng
            current_menu = "SWITCH_HERO"
            cursor_idx = active_hero_idx
        elif cursor_idx == 3:  # Tháo chạy
            if monster["debuff_legs"]:
                combat_log = "THÁO CHẠY THÀNH CÔNG 100%! Quái vật đã bị gãy chân bò lê lết, không thể đuổi theo!"
                time.sleep(1.2)
                sys.exit(0)
            else:
                import random
                if random.random() < 0.5:
                    combat_log = "May mắn thoát hiểm! Đội thám hiểm tháo chạy thành công về hành lang mê cung."
                    time.sleep(1.2)
                    sys.exit(0)
                else:
                    combat_log = "THÁO CHẠY THẤT BẠI! Quái vật chặn đứng lối thoát và chém phản đòn!"
                    enemy_turn()
                    current_menu = "MAIN"
                    cursor_idx = 0
        elif cursor_idx == 4:  # Quay lại
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
            current_menu = "ACTION"
            cursor_idx = 2

    elif current_menu == "TARGET_LIMB":
        if cursor_idx == 0:    # Đầu
            if monster["debuff_legs"]:
                dmg = monster["hp"]
                monster["hp"] = 0
                monster["debuff_decapitated"] = True
                combat_log = f"CRITICAL INSTAKILL! Quái đang bò, {hero['name']} trảm ngọt đầu đối thủ! Gây {dmg} DMG! CHIẾN THẮNG!"
            else:
                import random
                if random.random() < 0.35:
                    dmg = monster["hp"]
                    monster["hp"] = 0
                    monster["debuff_decapitated"] = True
                    combat_log = f"TRẢM ĐẦU TỨC THÌ (DECAPITATION)! Lưỡi gươm phạt đứt cổ quái vật! Gây {dmg} DMG! CHIẾN THẮNG!"
                else:
                    dmg = 18
                    monster["hp"] = max(0, monster["hp"] - dmg)
                    combat_log = f"Đòn chém sượt qua đầu quái vật! Gây {dmg} sát thương sứt mẻ."
            enemy_turn()
            current_menu = "MAIN"
            cursor_idx = 0
        elif cursor_idx == 1:  # Thân
            dmg = hero["atk"] - (monster["def"] // 2)
            dmg = max(24, dmg)
            monster["hp"] = max(0, monster["hp"] - dmg)
            combat_log = f"{hero['name']} chém thẳng vào ngực đối thủ! Trừ {dmg} Máu Tổng."
            enemy_turn()
            current_menu = "MAIN"
            cursor_idx = 0
        elif cursor_idx == 2:  # Tay phải
            dmg = 20
            monster["hp"] = max(0, monster["hp"] - dmg)
            monster["debuff_arm_r"] = True
            monster["atk"] = max(8, monster["atk"] - 14)
            combat_log = f"CHẶT ĐỨT TAY PHẢI! Trừ {dmg} Máu Tổng. Kiếm quỷ rơi xuống sàn đá -> TƯỚC VŨ KHÍ!"
            enemy_turn()
            current_menu = "MAIN"
            cursor_idx = 0
        elif cursor_idx == 3:  # Tay trái
            dmg = 18
            monster["hp"] = max(0, monster["hp"] - dmg)
            monster["debuff_arm_l"] = True
            combat_log = f"CHẶT ĐỨT TAY TRÁI! Trừ {dmg} Máu Tổng. Khiên tối vỡ nát -> GIẢM 50% SỨC CÔNG!"
            enemy_turn()
            current_menu = "MAIN"
            cursor_idx = 0
        elif cursor_idx == 4:  # Đôi chân
            dmg = 22
            monster["hp"] = max(0, monster["hp"] - dmg)
            monster["debuff_legs"] = True
            combat_log = f"BẺ GÃY CHÂN QUÁI! Trừ {dmg} Máu Tổng. Quái vật sụp đổ bò lê lết -> 100% CHẠY TRỐN & ĐẦU 100%!"
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
                combat_log = "Không đủ điểm Tâm Trí (Mind) để thi triển ma pháp Black Orb!"
            current_menu = "MAIN"
            cursor_idx = 0
        elif cursor_idx == 1:  # Leg sweep
            dmg = 15
            monster["hp"] = max(0, monster["hp"] - dmg)
            monster["debuff_legs"] = True
            combat_log = "LEG SWEEP! Cú quét trụ thần tốc bẻ gãy chân quái vật -> BÒ LÊ LẾT 100%!"
            enemy_turn()
            current_menu = "MAIN"
            cursor_idx = 0
        elif cursor_idx == 2:  # Devour
            dmg = 20
            monster["hp"] = max(0, monster["hp"] - dmg)
            hero["hunger"] = max(0, hero["hunger"] - 40)
            combat_log = f"DEVOUR! {hero['name']} cắn xé máu thịt quái gây {dmg} DMG! Độ đói giảm mạnh -40 Hunger!"
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
                # Clear wound debuff
                if "Vết thương cào (-4 HP)" in hero["debuffs"]:
                    hero["debuffs"].remove("Vết thương cào (-4 HP)")
                combat_log = f"{hero['name']} nhai Hoa Anh Túc (White Poppy)! Hồi phục +50 HP & làm lành vết thương cào."
                enemy_turn()
            else:
                combat_log = "Đã hết Hoa Anh Túc trong túi đồ!"
            current_menu = "MAIN"
            cursor_idx = 0
        elif cursor_idx == 1:  # Weed
            if inventory["weed"] > 0:
                inventory["weed"] -= 1
                hero["hp"] = min(hero["max_hp"], hero["hp"] + 120)
                combat_log = f"{hero['name']} đốt Thảo Dược quý (Weed)! Đại hồi phục +120 HP sinh lực."
                enemy_turn()
            else:
                combat_log = "Đã hết Thảo Dược trong túi đồ!"
            current_menu = "MAIN"
            cursor_idx = 0
        elif cursor_idx == 2:  # Bread
            if inventory["bread"] > 0:
                inventory["bread"] -= 1
                hero["hunger"] = max(0, hero["hunger"] - 40)
                combat_log = f"{hero['name']} ăn Bánh Mì mốc (Moldy Bread)! Giảm ngay -40 điểm Đói."
            else:
                combat_log = "Đã hết Bánh Mì trong túi đồ!"
            current_menu = "MAIN"
            cursor_idx = 0
        elif cursor_idx == 3:  # Ale
            if inventory["ale"] > 0:
                inventory["ale"] -= 1
                hero["mind"] = min(hero["max_mind"], hero["mind"] + 35)
                combat_log = f"{hero['name']} uống Rượu Ale cay nồng! Hồi phục +35 Mind & trấn an tinh thần."
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
            combat_log = f"{hero['name']} vào THẾ IRON GUARD! Dựng khiên sắt, giảm 70% sát thương nhận vào."
            current_menu = "MAIN"
            cursor_idx = 0
        elif cursor_idx == 2:  # Agile
            hero["stance"] = "AGILE DANCE (+35% DODGE)"
            combat_log = f"{hero['name']} chuyển sang THẾ AGILE DANCE! Thân pháp thoăn thoắt, tăng 35% né đòn."
            current_menu = "MAIN"
            cursor_idx = 0
        elif cursor_idx == 3:  # Quay lại
            current_menu = "MAIN"
            cursor_idx = 0

# =============================================================================
# ENEMY TURN & DAMAGE RESOLUTION
# =============================================================================
def enemy_turn():
    global combat_log, active_hero_idx
    hero = squad[active_hero_idx]

    if monster["hp"] <= 0 or monster["debuff_decapitated"]:
        combat_log += " | Quái vật gục ngã trên vũng máu! CHIẾN THẮNG OANH LIỆT!"
        return

    # Turn bleed from wound debuff
    if "Vết thương cào (-4 HP)" in hero["debuffs"]:
        hero["hp"] = max(0, hero["hp"] - 4)

    dmg = monster["atk"] - (hero["def"] // 2)
    if hero["is_guarding"]:
        dmg = int(dmg * 0.3)
        hero["is_guarding"] = False

    dmg = max(4, dmg)
    hero["hp"] = max(0, hero["hp"] - dmg)
    combat_log += f" | Quái phản kích! {hero['name']} mất {dmg} HP."

    # Chance monster inflicts scratch wound debuff on player
    import random
    if random.random() < 0.4 and "Vết thương cào (-4 HP)" not in hero["debuffs"]:
        hero["debuffs"].append("Vết thương cào (-4 HP)")
        combat_log += " Móng vuốt quỷ để lại VẾT THƯƠNG CÀO (-4 HP mỗi lượt)!"

    # Hero Down check
    if hero["hp"] == 0:
        combat_log += f" | ⚠️ HERO DOWN! {hero['name']} đã gục ngã!"
        for idx, comp in enumerate(squad):
            if comp["hp"] > 0:
                active_hero_idx = idx
                combat_log += f" -> {comp['name']} khẩn cấp nhảy lên thế chỗ!"
                break

# =============================================================================
# MAIN INTERACTIVE LOOP
# =============================================================================
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

# =============================================================================
# SHOWCASE AUTO TRACE
# =============================================================================
def run_showcase_trace():
    print("\n>>> BẮT ĐẦU SHOWCASE ĐẤU TRƯỜNG CHÉO POKÉMON (POKÉMON-STYLE DIAGONAL ARENA) <<<\n")
    states = [
        ("MAIN", 0, "BƯỚC 1: BỐ CỤC CHÉO POKÉMON - Quái Ở Nửa Trên (Thẻ Trái, Model Phải) | Ta Ở Nửa Dưới (Model Trái, Thẻ Phải)"),
        ("ACTION", 0, "BƯỚC 2: Vào 'Hành Động' -> Chuẩn bị nhắm đánh tứ chi quái"),
        ("TARGET_LIMB", 2, "BƯỚC 3: Chọn chặt 'Tay Phải' -> Quái rơi kiếm, bị tước vũ khí, ATK giảm mạnh!"),
        ("TARGET_LIMB", 4, "BƯỚC 4: Chọn bẻ gãy 'Đôi Chân' -> Quái sụp xuống BÒ LÊ LẾT (100% Chạy Trốn & Đầu 100%!)"),
        ("SWITCH_HERO", 1, "BƯỚC 5: BẢNG ĐIỀU ĐỘNG ĐỘI HÌNH - Xem rõ chỉ số 4 tướng, chuyển D'arce lên Tiên Phong"),
        ("TARGET_LIMB", 0, "BƯỚC 6: D'arce trảm ngọt đầu quái đang bò -> 100% CRITICAL INSTAKILL KẾT LIỄU!")
    ]

    global current_menu, cursor_idx, active_hero_idx, combat_log
    for idx, (m_state, c_idx, step_desc) in enumerate(states):
        current_menu = m_state
        cursor_idx = c_idx

        # Simulate actions at each step
        if idx == 2: # Step 3: cut right arm
            monster["debuff_arm_r"] = True
            monster["atk"] = 10
            monster["hp"] = 75
            combat_log = "CHẶT ĐỨT TAY PHẢI! Shadow Swordsman rơi kiếm đen xuống sàn đá -> TƯỚC VŨ KHÍ, ATK GIẢM XUỐNG 10!"
        elif idx == 3: # Step 4: break legs
            monster["debuff_legs"] = True
            monster["hp"] = 53
            combat_log = "BẺ GÃY ĐÔI CHÂN! Quái vật gục xuống BÒ LÊ LẾT -> 100% THÁO CHẠY THOÁT & 100% TRẢM ĐẦU!"
        elif idx == 4: # Step 5: switch to D'arce
            active_hero_idx = 1
            combat_log = "CHUYỂN GIAO TIÊN PHONG! D'ARCE [Holy Knight] bước lên chỉ huy tác chiến!"
        elif idx == 5: # Step 6: decapitate head
            monster["debuff_decapitated"] = True
            monster["hp"] = 0
            combat_log = "CRITICAL INSTAKILL! Quái đang bò, D'ARCE trảm ngọt đầu đối thủ! CHIẾN THẮNG OANH LIỆT!"

        render_screen()
        print(f"\n  \033[1;32m>>> [MINH HỌA]: {step_desc} <<<\033[0m")
        time.sleep(1.0)

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--showcase":
        run_showcase_trace()
    else:
        run_interactive_loop()
