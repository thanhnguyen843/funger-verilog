#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
================================================================================
FEAR & HUNGER: TERMINAL LABYRINTH - POKÉMON-STYLE COMBAT ARENA
================================================================================
Refactored per user requirements:
1. Full English localization, concise military-grade CRPG style.
2. Monster initial intact state: no status/stance clutter.
3. Hero healthy state: no normal health text.
4. Buffs: display ONLY when active. If none, display nothing.
5. Injuries/Debuffs: display ONLY when wounded. If healthy, display nothing.
6. Leader/captain titles omitted.
7. Companions/teammates omitted from main card; only visible upon opening Switch Hero.
8. Authentic TrueColor 24-bit half-block sprites (29 chars x 12 lines).
9. Exact 100-column alignment with 4-space center gap (54 + 4 + 42 = 100).
10. Icon-free, distraction-free Gothic terminal menus.
================================================================================
"""

import sys
import os
import time
import re
import unicodedata
import json

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
    ea = unicodedata.east_asian_width(c)
    if ea in ('W', 'F'):
        return 2
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
# LOAD AUTHENTIC SPRITE MODELS (29 CHARACTERS WIDE, 12 HALF-BLOCK LINES)
# =============================================================================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SPRITES_FILE = os.path.join(BASE_DIR, "extracted_sprites.json")

HERO_SPRITES = {}
RAW_MONSTER_8 = []

if os.path.exists(SPRITES_FILE):
    try:
        with open(SPRITES_FILE, "r", encoding="utf-8") as f:
            sp_data = json.load(f)
            HERO_SPRITES = sp_data.get("heroes", {})
            RAW_MONSTER_8 = sp_data.get("monster_8", [])
    except Exception:
        pass

# Fallback basic models if json is not loaded
if not HERO_SPRITES:
    HERO_SPRITES = {
        "CAHARA": [
            "          ▄▀▀▀▀▀▀▀▄          ",
            "        ▀▀▀▀▀▀▀▀▀▀▀▀         ",
            "        ▄▀▀▀▀▀▀▀▀▀▀▀▄        ",
            "         ▀▀▀▀▀▀▀▀▀▀▀   ▄▀▀   ",
            "         ▄▀▀▀▀▀▀▀▀▀▄ ▄▀▀▀    ",
            "       ▄▀▀▀▀▀▀▀▀▀▀▀▀▀▄▄▄▀    ",
            "       ▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀   ",
            "      ▀▀▀▀▄▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀   ",
            "      ▀▀▄▀▀▀▀▀▀▀▀▀▀          ",
            "     ▀▀▀▀▀▀▀▀▀▀▀▀▀▀          ",
            "      ▀▀▀▀▀▀▀▀  ▀▀▀          ",
            "        ▀▀▀      ▀▀▀         "
        ],
        "D'ARCE": [
            "        ▄▀▀▀▀▀▀▀▄            ",
            "       ▀▀▀▀▀▀▀▀▀▀▀           ",
            "       ▀▀▀▀▀▀▀▀▀▀▀           ",
            "       ▀▀▀▀▀▀▀▀▀▀            ",
            "     ▀▀▄▄▀▀▀▀▀▀▀▀▄           ",
            "     ▀▀▀▀▀▀▀▀▀▀▀▀▀           ",
            "     ▀▀▀▀▀▀▀▀▀▀▀ ▀▀▀         ",
            "     ▀▀▀▀▀▀▀▀▀▀▀▄▀▀▀▀        ",
            "     ▀▀ ▀▀▀▀▀▀▀▀▀▄▀▀▀▀▀▀     ",
            "        ▀▀▀▀▀▀▀▀▀▀  ▀▀▀▀▀▄   ",
            "        ▀▀▀▀   ▀▀▀▀     ▀▀▀▄ ",
            "                 ▀▀       ▀▀▀"
        ],
        "ENKI": [
            "         ▄▀▀▀▀▀▀▀▄           ",
            "        ▀▀▀▀▀▀▀▀▀▀▄          ",
            "       ▀▀▀▀▀▀▀▀▀▀▀▀          ",
            "       ▀▀▀▀▀▀▀▀▀▀▀▀          ",
            "        ▀▀▀▀▀▀▀▀▀▀▀          ",
            "      ▄▀▀▀▀▀▀▀▀▀▀▀▀          ",
            "     ▄▀▀▀▀▀▀▀▀▀▀▀▀▀          ",
            "     ▀▀▀▀▀▀▀▀▀▀▀▀▀▀          ",
            "     ▀▀▀▀▀▀▀▀▀▀▀▀▀▀          ",
            "      ▀▀▀▀▀▀▀▀▀▀▀▀           ",
            "      ▄▀▀▀▀▀▀▀▀▀▀            ",
            "      ▀▀▀      ▀▀▀           "
        ],
        "THE GIRL": [
            "                             ",
            "        ▄▀▀▀▀▀▀▀▄            ",
            "       ▀▀▀▀▀▀▀▀▀▀▄           ",
            "      ▀▀▀▀▀▀▀▀▀▀▀▀           ",
            "      ▀▀▀▀▀▀▀▀▀▀▀▀           ",
            "        ▀▀▀▀▀▀▀▀▀            ",
            "       ▀▀▀▀▀▀▀▀▀▀▀           ",
            "       ▀▀▀▀▀▀▀▀▀▀▀           ",
            "        ▀▀▀▀▀▀▀▀▀            ",
            "        ▀▀▀▀▀▀▀▀             ",
            "        ▀▀▀   ▀▀             ",
            "                             "
        ]
    }

# Build Monster 8 variants (Intact, Crawling, Decapitated) in 12 lines x 29 columns
MONSTER_SPRITE_INTACT = []
if RAW_MONSTER_8:
    for idx in range(12):
        if idx < len(RAW_MONSTER_8) and RAW_MONSTER_8[idx].strip():
            MONSTER_SPRITE_INTACT.append(f"\033[1;31m{RAW_MONSTER_8[idx]}\033[0m")
        else:
            MONSTER_SPRITE_INTACT.append(" " * 29)
else:
    MONSTER_SPRITE_INTACT = [
        "      ▄▀▀▀▄▄▀▀▀▄             ",
        "     ▀▀ ▄ ▀▀ ▄ ▀             ",
        "     ▀▀▄▄▄▀▀▄▄▄▀             ",
        "      ▄▀▀▀▄▄▀▀▀▄             ",
        "      ▀ ▀▀▀▀▀▀ ▀             ",
        "      ▀  ▀▄ ▀▄ ▀             ",
        "      ▀▀  ▀  ▀ ▀             ",
        "                             ",
        "                             ",
        "                             ",
        "                             ",
        "                             "
    ]

# Crawling Sprite (Collapsed on floor, legs broken)
MONSTER_SPRITE_CRAWLING = [
    "                             ",
    "                             ",
    "                             ",
    "                             ",
    "                             ",
    "      \033[1;31m▄▀▀▀▄▄▀▀▀▄\033[0m             ",
    "     \033[1;31m▀▀ ▄ ▀▀ ▄ ▀\033[0m             ",
    "     \033[1;31m▀▀▄▄▄▀▀▄▄▄▀\033[0m             ",
    "      \033[1;31m▄▀▀▀▄▄▀▀▀▄\033[0m             ",
    "   \033[1;31m▄▀▀▀▀▀▀▀▀▀▀▀▀▀▄\033[0m           ",
    "   \033[1;31m▀▀▀▀   ▀▀  ▀▀▀▀\033[0m           ",
    "  \033[1;33m[LEGS BROKEN: CRAWLING]\033[0m    "
]

# Decapitated Sprite (Head severed, instant death)
MONSTER_SPRITE_DECAPITATED = [
    "                             ",
    "                             ",
    "     \033[1;31m[DECAPITATED]\033[0m           ",
    "        \033[1;31m▄████▄\033[0m               ",
    "    \033[1;31m▀▀▄▄▄▀████▄▄▄▀\033[0m           ",
    "     \033[1;31m▄▀▀▀▄▄▀▀▀▄\033[0m              ",
    "      \033[1;31m▀ ▀▀▀▀▀▀ ▀\033[0m             ",
    "   \033[1;31m▄▀▀▀▀▀▀▀▀▀▀▀▀▀▄\033[0m           ",
    "   \033[1;31m▀▀▀▀   ▀▀  ▀▀▀▀\033[0m           ",
    "      \033[1;31m(HEAD SEVERED)\033[0m         ",
    "                             ",
    "                             "
]

def format_model_row(sp_line):
    # Left pad 6 spaces, right pad 7 spaces -> 6 + 29 + 7 = 42 visible cols
    return " " * 6 + sp_line + " " * 7

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
    "type_desc": "Ancient Shadow Blade",
    "debuff_arm_r": False,     # Disarmed (Sword lost)
    "debuff_arm_l": False,     # Guard Broken (Shield lost)
    "debuff_legs": False,      # Crawling -> 100% flee, 100% head hit
    "debuff_decapitated": False # Head severed -> Instant death
}

squad = [
    {
        "name": "CAHARA",
        "role": "Mercenary",
        "hp": 125,
        "max_hp": 125,
        "mind": 100,
        "max_mind": 100,
        "hunger": 20,
        "max_hunger": 100,
        "atk": 33,
        "def": 21,
        "buff": "",
        "is_guarding": False,
        "debuffs": []
    },
    {
        "name": "D'ARCE",
        "role": "Paladin",
        "hp": 145,
        "max_hp": 145,
        "mind": 90,
        "max_mind": 100,
        "hunger": 35,
        "max_hunger": 100,
        "atk": 30,
        "def": 30,
        "buff": "",
        "is_guarding": False,
        "debuffs": []
    },
    {
        "name": "ENKI",
        "role": "Occultist",
        "hp": 95,
        "max_hp": 95,
        "mind": 100,
        "max_mind": 100,
        "hunger": 15,
        "max_hunger": 100,
        "atk": 48,
        "def": 24,
        "buff": "",
        "is_guarding": False,
        "debuffs": []
    },
    {
        "name": "THE GIRL",
        "role": "Ward",
        "hp": 105,
        "max_hp": 105,
        "mind": 80,
        "max_mind": 100,
        "hunger": 10,
        "max_hunger": 100,
        "atk": 30,
        "def": 39,
        "buff": "",
        "is_guarding": False,
        "debuffs": []
    }
]

active_hero_idx = 0

inventory = {
    "poppy": 2,      # +50 HP, cure bleeding scratch
    "weed": 1,       # +120 HP
    "bread": 3,      # -40 Hunger
    "ale": 2         # +35 Mind
}

combat_log = "Battle initiated. Shadow Swordsman unsheathes dark blade."

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
    # MAIN HEADER (100 COLUMNS)
    # -------------------------------------------------------------------------
    print("\033[1;30m+====================================================================================================+\033[0m")
    title_str = "FEAR & HUNGER: COMBAT ARENA - TACTICAL ARENA HUD"
    pad_left = (96 - len(title_str)) // 2
    pad_right = 96 - len(title_str) - pad_left
    print(f"\033[1;30m| \033[1;37m{' ' * pad_left}{title_str}{' ' * pad_right}\033[1;30m |\033[0m")
    print("\033[1;30m+====================================================================================================+\033[0m")
    print()  # 1 blank line spacing

    # -------------------------------------------------------------------------
    # ZONE 1: OPPONENT ZONE (TOP)
    # Left: Monster Tactical Card (54 cols)
    # Gap : 4 spaces
    # Right: Monster Sprite Model (42 cols)
    # Total: 54 + 4 + 42 = 100 columns
    # -------------------------------------------------------------------------
    c_mcard = "\033[1;33m" if current_menu == "TARGET_LIMB" else "\033[1;30m"
    m_border = f"{c_mcard}+" + "-" * 52 + f"+{c_mcard}\033[0m"

    # Select Monster Sprite (intact vs crawling vs decapitated)
    if monster["debuff_decapitated"]:
        m_sprite = MONSTER_SPRITE_DECAPITATED
        m_model_sub = "\033[1;31m[DECAPITATED]\033[0m"
    elif monster["debuff_legs"]:
        m_sprite = MONSTER_SPRITE_CRAWLING
        m_model_sub = "\033[1;33m[CRAWLING]\033[0m"
    else:
        m_sprite = MONSTER_SPRITE_INTACT
        m_model_sub = ""  # Clean, no posture text when intact

    # Monster HP & Stats
    m_pct = int(max(0, monster["hp"]) / float(monster["max_hp"]) * 100)
    m_hp_bar = make_bar(monster["hp"], monster["max_hp"], 12, "31")
    atk_note = ""
    if monster["debuff_arm_r"] and monster["debuff_arm_l"]:
        atk_note = "\033[1;31m(DISARMED & WEAKENED)\033[0m"
    elif monster["debuff_arm_r"]:
        atk_note = "\033[1;33m(DISARMED)\033[0m"
    elif monster["debuff_arm_l"]:
        atk_note = "\033[1;36m(GUARD BROKEN)\033[0m"

    # Monster Injuries / Debuffs (Only display if injured!)
    has_monster_injury = (
        monster["debuff_decapitated"] or
        monster["debuff_legs"] or
        monster["debuff_arm_r"] or
        monster["debuff_arm_l"]
    )

    m_inj_header = "\033[1;31m  INJURIES & DEBUFFS:\033[0m" if has_monster_injury else ""
    m_inj_1 = ""
    m_inj_2 = ""
    m_inj_3 = ""

    if monster["debuff_decapitated"]:
        m_inj_1 = "\033[1;31m  [HEAD] Decapitated -> Fatal strike (Dead)\033[0m"
    elif monster["debuff_legs"]:
        m_inj_1 = "\033[1;33m  [LEGS] Broken -> Crawling (100% Flee)\033[0m"
        m_inj_2 = "\033[1;31m  -> Decapitation hit rate boosted to 100%!\033[0m"
        if monster["debuff_arm_r"]:
            m_inj_3 = "\033[1;33m  [RIGHT ARM] Severed -> Disarmed (ATK -14)\033[0m"
    elif monster["debuff_arm_r"] or monster["debuff_arm_l"]:
        if monster["debuff_arm_r"]:
            m_inj_1 = "\033[1;33m  [RIGHT ARM] Severed -> Disarmed (ATK -14)\033[0m"
        if monster["debuff_arm_l"]:
            m_inj_2 = "\033[1;36m  [LEFT ARM] Severed -> Shield broken\033[0m"

    # 14 Rows of Monster Card (54 cols each) - Spaced out for readability
    m_card_rows = [
        m_border,
        make_card_row(f"\033[1;31m FOE   : #{monster['id']:02d} {monster['name']:<18}\033[90m[Opponent]\033[0m", c_mcard),
        make_card_row("", c_mcard),
        make_card_row(f" HP    : {m_hp_bar} \033[1;31m{monster['hp']:3d}/{monster['max_hp']:3d} ({m_pct:3d}%)\033[0m", c_mcard),
        make_card_row("", c_mcard),
        make_card_row(f" STATS : ATK {monster['atk']:2d}   |   DEF {monster['def']:2d} {atk_note}\033[0m", c_mcard),
        make_card_row("", c_mcard),
        make_card_row(f" TYPE  : {monster['type_desc']}", c_mcard),
        make_card_row("", c_mcard),
        make_card_row(m_inj_header, c_mcard),
        make_card_row(m_inj_1, c_mcard),
        make_card_row(m_inj_2, c_mcard),
        make_card_row(m_inj_3, c_mcard),
        m_border
    ]

    # 14 Rows of Monster Model (42 cols each)
    m_model_rows = [
        pad_str("          \033[1;31m[ENEMY]\033[0m", 42)
    ]
    for r in range(12):
        sp = m_sprite[r] if r < len(m_sprite) else " " * 29
        m_model_rows.append(format_model_row(sp))
    # Line 13: Subtitle if wounded/decapitated, else blank
    m_sub_pad = pad_str(f"       {m_model_sub}", 42) if m_model_sub else pad_str("", 42)
    m_model_rows.append(m_sub_pad)

    # Print Top Zone (Card Left + Model Right) with 4-space gap
    for r_idx in range(14):
        left_str = m_card_rows[r_idx]
        right_str = m_model_rows[r_idx]
        print(f"{left_str}    {right_str}\033[0m")

    print()  # 1 blank line spacing

    # -------------------------------------------------------------------------
    # ZONE 2: PLAYER SQUAD ZONE (BOTTOM)
    # Left: Hero Sprite Model (42 cols)
    # Gap : 4 spaces
    # Right: Hero Tactical Card (54 cols)
    # Total: 42 + 4 + 54 = 100 columns
    # -------------------------------------------------------------------------
    c_hcard = "\033[1;32m" if current_menu in ("SWITCH_HERO", "POUCH", "TACTICS") else "\033[1;30m"
    h_border = f"{c_hcard}+" + "-" * 52 + f"+{c_hcard}\033[0m"

    # Select Hero Sprite
    hero_key = hero["name"]
    h_sprite = HERO_SPRITES.get(hero_key, HERO_SPRITES.get("CAHARA", []))

    # Hero Bars & Stats
    h_pct = int(max(0, hero["hp"]) / float(hero["max_hp"]) * 100)
    h_hp_bar = make_bar(hero["hp"], hero["max_hp"], 12, "32")
    h_mnd_bar = make_bar(hero["mind"], hero["max_mind"], 10, "36")
    h_hng_bar = make_bar(hero["hunger"], hero["max_hunger"], 10, "33")

    # Hero Buff string (Only display if active!)
    h_buff_row = ""
    if hero.get("buff"):
        h_buff_row = f"\033[1;32m  BUFF  : {hero['buff']}\033[0m"

    # Hero Injury / Debuffs string (Only display if injured!)
    h_injury_row = ""
    if hero.get("debuffs"):
        h_injury_row = f"\033[1;31m  INJURY: {', '.join(hero['debuffs'])}\033[0m"

    # 14 Rows of Hero Model (42 cols each)
    h_model_rows = [
        pad_str("          \033[1;32m[HERO]\033[0m", 42)
    ]
    for r in range(12):
        sp = h_sprite[r] if r < len(h_sprite) else " " * 29
        h_model_rows.append(format_model_row(sp))
    # Line 13: Omit leader/captain labels, leave clean
    h_model_rows.append(pad_str("", 42))

    # 14 Rows of Hero Card (54 cols each) - Spaced out for readability
    # No stance, no captain tag, no companions summary (only shown in Switch Hero menu)
    h_card_rows = [
        h_border,
        make_card_row(f"\033[1;32m HERO  : {hero['name']:<10}\033[90m[{hero['role']}]\033[0m", c_hcard),
        make_card_row("", c_hcard),
        make_card_row(f" HP    : {h_hp_bar} \033[1;32m{hero['hp']:3d}/{hero['max_hp']:3d} ({h_pct:3d}%)\033[0m", c_hcard),
        make_card_row("", c_hcard),
        make_card_row(f" MIND  : {h_mnd_bar} \033[1;36m{hero['mind']:3d}/{hero['max_mind']:3d}\033[0m", c_hcard),
        make_card_row(f" HUNGER: {h_hng_bar} \033[1;33m{hero['hunger']:3d}/{hero['max_hunger']:3d}\033[0m", c_hcard),
        make_card_row("", c_hcard),
        make_card_row(f" STATS : ATK {hero['atk']:2d}   |   DEF {hero['def']:2d}", c_hcard),
        make_card_row("", c_hcard),
        make_card_row(h_buff_row, c_hcard),
        make_card_row(h_injury_row, c_hcard),
        make_card_row("", c_hcard),
        h_border
    ]

    # Print Bottom Zone (Model Left + Card Right) with 4-space gap
    for r_idx in range(14):
        left_str = h_model_rows[r_idx]
        right_str = h_card_rows[r_idx]
        print(f"{left_str}    {right_str}\033[0m")

    print()  # 1 blank line spacing

    # -------------------------------------------------------------------------
    # SECTION 3: COMBAT LOG BOX (100 COLUMNS)
    # -------------------------------------------------------------------------
    print("\033[1;30m+----------------------------------------------------------------------------------------------------+\033[0m")
    log_content = pad_str(f"\033[1;33m[LOG]\033[0m \033[1;37m{combat_log}\033[0m", 96)
    print(f"| {log_content} \033[1;30m|")
    print("\033[1;30m+----------------------------------------------------------------------------------------------------+\033[0m")
    print()  # 1 blank line spacing

    # -------------------------------------------------------------------------
    # SECTION 4: 4-BUTTON MENU (IN ENGLISH, NO ICONS, IN-PLACE REPLACEMENT)
    # -------------------------------------------------------------------------
    menu_data = get_current_menu_data()
    title = menu_data["title"]
    options = menu_data["options"]

    print(f"  \033[1;37m{title}\033[0m")
    print("  \033[90m(Use W / S or Arrow keys to navigate, Enter to confirm):\033[0m")
    print()

    for idx, opt in enumerate(options):
        is_sel = (idx == cursor_idx)
        label = opt["label"]
        desc = opt["desc"]

        if is_sel:
            print(f"    \033[1;33m▶  [{idx+1}] \033[1;37;43m {label:<22} \033[0m \033[1;33m{desc}\033[0m")
        else:
            print(f"       \033[90m[{idx+1}]   {label:<22} {desc}\033[0m")

    # Consistent menu height (6 lines)
    for _ in range(max(0, 6 - len(options))):
        print()

    print()  # 1 blank line spacing

    # -------------------------------------------------------------------------
    # FOOTER: CONTROL GUIDE (100 COLUMNS)
    # -------------------------------------------------------------------------
    print("\033[1;30m====================================================================================================\033[0m")
    if current_menu == "MAIN":
        print("  \033[90m[CONTROLS]:\033[0m \033[1;37m[W/S]\033[0m Navigate  |  \033[1;37m[Enter/Space]\033[0m Select Submenu  |  \033[1;31m[Q]\033[0m Quit")
    else:
        print("  \033[90m[CONTROLS]:\033[0m \033[1;37m[W/S]\033[0m Navigate  |  \033[1;37m[Enter/Space]\033[0m Confirm Action  |  \033[1;33m[B/Esc]\033[0m Back")
    print("\033[1;30m====================================================================================================\033[0m")
    sys.stdout.flush()

# =============================================================================
# MENU DATA RESOLUTION (CLEAN ENGLISH, ZERO ICONS)
# =============================================================================
def get_current_menu_data():
    if current_menu == "MAIN":
        return {
            "title": "MAIN COMMANDS",
            "options": [
                {"label": "ACTION",   "desc": "-> Attack, Guard, Switch Vanguard, Flee"},
                {"label": "SKILL",    "desc": "-> Hexen occult magic & combat skills"},
                {"label": "ITEM",     "desc": "-> Poppy herb, Healing weed, Rations, Ale"},
                {"label": "TACTICS",  "desc": "-> Stances (Berserk / Iron Guard / Agile)"}
            ]
        }
    elif current_menu == "ACTION":
        flee_text = "Escape battle (\033[1;32m100% Guaranteed - Foe crawling\033[0m)" if monster["debuff_legs"] else "Escape battle (50% Chance)"
        return {
            "title": "ACTION > SELECT TACTICAL COMMAND",
            "options": [
                {"label": "ATTACK",  "desc": "-> Target specific limbs to cripple foe"},
                {"label": "GUARD",   "desc": "-> Brace for impact (-70% incoming damage)"},
                {"label": "SWITCH",  "desc": "-> Open Squad Roster to change active vanguard"},
                {"label": "FLEE",    "desc": f"-> {flee_text}"},
                {"label": "BACK",    "desc": "-> Return to main commands"}
            ]
        }
    elif current_menu == "SWITCH_HERO":
        opts = []
        for idx, h in enumerate(squad):
            is_active = (idx == active_hero_idx)
            tag = " \033[1;32m[ACTIVE]\033[0m" if is_active else " \033[90m[RESERVE]\033[0m"
            status_tag = "" if h["hp"] > 0 else " \033[1;31m[DOWN]\033[0m"
            opts.append({
                "label": f"{h['name']:<9} [{h['role']:<9}]",
                "desc": f"HP: {h['hp']:3d}/{h['max_hp']:3d} | MND: {h['mind']:3d} | HNG: {h['hunger']:2d}{status_tag}{tag}"
            })
        opts.append({"label": "BACK", "desc": "-> Keep current vanguard, return to action menu"})
        return {
            "title": "ACTION > SQUAD ROSTER (DEPLOY VANGUARD)",
            "options": opts
        }
    elif current_menu == "TARGET_LIMB":
        crawl_hint = "\033[1;32m(100% Critical Finish!)\033[0m" if monster["debuff_legs"] else "(25% Hit | Instant Decapitate)"
        return {
            "title": "ACTION > ATTACK > SELECT TARGET LIMB",
            "options": [
                {"label": "HEAD",       "desc": f"-> {crawl_hint}"},
                {"label": "TORSO",      "desc": "-> 100% Hit | Safe strike, heavy body damage"},
                {"label": "RIGHT ARM",  "desc": "-> 100% Hit | Sever sword arm -> Disarm foe"},
                {"label": "LEFT ARM",   "desc": "-> 100% Hit | Sever shield arm -> Weaken attack"},
                {"label": "LEGS",       "desc": "-> 100% Hit | Break legs -> Force crawl (100% Flee)"},
                {"label": "BACK",       "desc": "-> Return to action menu"}
            ]
        }
    elif current_menu == "SKILL":
        return {
            "title": "SKILLS & HEXEN OCCULT MAGIC",
            "options": [
                {"label": "BLACK ORB",  "desc": "-> 15 Mind | Pierce 100% enemy defense (45 DMG)"},
                {"label": "LEG SWEEP",  "desc": "-> 10 HP | Break enemy legs immediately (15 DMG)"},
                {"label": "DEVOUR",     "desc": "-> Bite enemy for 20 DMG | Reduce 40 Hunger"},
                {"label": "BACK",       "desc": "-> Return to main commands"}
            ]
        }
    elif current_menu == "POUCH":
        return {
            "title": "ITEM POUCH & SURVIVAL SUPPLIES",
            "options": [
                {"label": f"WHITE POPPY [{inventory['poppy']}]", "desc": "-> Flower bud | Restore +50 HP & cure bleeding"},
                {"label": f"HERBAL WEED [{inventory['weed']}]",  "desc": "-> Healing herb | Restore +120 HP"},
                {"label": f"MOLDY BREAD [{inventory['bread']}]", "desc": "-> Dungeon rations | Reduce 40 Hunger"},
                {"label": f"VINTAGE ALE [{inventory['ale']}]",   "desc": "-> Fermented ale | Restore +35 Mind"},
                {"label": "BACK",                                 "desc": "-> Return to main commands"}
            ]
        }
    elif current_menu == "TACTICS":
        return {
            "title": "COMBAT TACTICS & STANCES",
            "options": [
                {"label": "BERSERK",     "desc": "-> +50% Attack power, +30% damage taken"},
                {"label": "IRON GUARD",  "desc": "-> -70% Damage taken, restore 5% HP/turn"},
                {"label": "AGILE DANCE", "desc": "-> +35% Dodge rate, 100% flee chance"},
                {"label": "BACK",        "desc": "-> Return to main commands"}
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
        if cursor_idx == 0:    # Attack
            current_menu = "TARGET_LIMB"
            cursor_idx = 0
        elif cursor_idx == 1:  # Guard
            hero["is_guarding"] = True
            hero["buff"] = "GUARD (-70% DMG)"
            combat_log = f"{hero['name']} raises guard! Incoming damage reduced by 70%."
            enemy_turn()
            current_menu = "MAIN"
            cursor_idx = 0
        elif cursor_idx == 2:  # Switch
            current_menu = "SWITCH_HERO"
            cursor_idx = active_hero_idx
        elif cursor_idx == 3:  # Flee
            if monster["debuff_legs"]:
                combat_log = "ESCAPE SUCCESSFUL! Foe is crawling and cannot pursue."
                time.sleep(1.2)
                sys.exit(0)
            else:
                import random
                if random.random() < 0.5:
                    combat_log = "ESCAPE SUCCESSFUL! Party retreats into dungeon corridors."
                    time.sleep(1.2)
                    sys.exit(0)
                else:
                    combat_log = "ESCAPE FAILED! Foe blocks the corridor and retaliates!"
                    enemy_turn()
                    current_menu = "MAIN"
                    cursor_idx = 0
        elif cursor_idx == 4:  # Back
            current_menu = "MAIN"
            cursor_idx = 0

    elif current_menu == "SWITCH_HERO":
        if cursor_idx < len(squad):
            if cursor_idx == active_hero_idx:
                combat_log = f"{squad[cursor_idx]['name']} is already at the vanguard."
            elif squad[cursor_idx]["hp"] <= 0:
                combat_log = f"{squad[cursor_idx]['name']} is unconscious and cannot fight."
            else:
                active_hero_idx = cursor_idx
                combat_log = f"VANGUARD DEPLOYED! {squad[active_hero_idx]['name']} takes point."
            current_menu = "MAIN"
            cursor_idx = 0
        else:
            current_menu = "ACTION"
            cursor_idx = 2

    elif current_menu == "TARGET_LIMB":
        if cursor_idx == 0:    # Head
            if monster["debuff_legs"]:
                dmg = monster["hp"]
                monster["hp"] = 0
                monster["debuff_decapitated"] = True
                combat_log = f"CRITICAL FINISH! Foe is crawling; {hero['name']} decapitates target! VICTORY!"
            else:
                import random
                if random.random() < 0.35:
                    dmg = monster["hp"]
                    monster["hp"] = 0
                    monster["debuff_decapitated"] = True
                    combat_log = f"DECAPITATION! Blade severs neck! Fatal blow for {dmg} DMG! VICTORY!"
                else:
                    dmg = 18
                    monster["hp"] = max(0, monster["hp"] - dmg)
                    combat_log = f"Glancing blow across the head for {dmg} DMG."
            enemy_turn()
            current_menu = "MAIN"
            cursor_idx = 0
        elif cursor_idx == 1:  # Torso
            dmg = hero["atk"] - (monster["def"] // 2)
            dmg = max(24, dmg)
            monster["hp"] = max(0, monster["hp"] - dmg)
            combat_log = f"{hero['name']} strikes torso for {dmg} DMG."
            enemy_turn()
            current_menu = "MAIN"
            cursor_idx = 0
        elif cursor_idx == 2:  # Right Arm
            dmg = 20
            monster["hp"] = max(0, monster["hp"] - dmg)
            monster["debuff_arm_r"] = True
            monster["atk"] = max(8, monster["atk"] - 14)
            combat_log = f"SEVERED RIGHT ARM! -{dmg} HP. Foe drops weapon -> DISARMED (ATK reduced to 10)!"
            enemy_turn()
            current_menu = "MAIN"
            cursor_idx = 0
        elif cursor_idx == 3:  # Left Arm
            dmg = 18
            monster["hp"] = max(0, monster["hp"] - dmg)
            monster["debuff_arm_l"] = True
            combat_log = f"SEVERED LEFT ARM! -{dmg} HP. Foe's shield broken!"
            enemy_turn()
            current_menu = "MAIN"
            cursor_idx = 0
        elif cursor_idx == 4:  # Legs
            dmg = 22
            monster["hp"] = max(0, monster["hp"] - dmg)
            monster["debuff_legs"] = True
            combat_log = f"BROKEN LEGS! -{dmg} HP. Foe collapses to CRAWL -> 100% FLEE & 100% HEAD HIT!"
            enemy_turn()
            current_menu = "MAIN"
            cursor_idx = 0
        elif cursor_idx == 5:  # Back
            current_menu = "ACTION"
            cursor_idx = 0

    elif current_menu == "SKILL":
        if cursor_idx == 0:    # Black Orb
            if hero["mind"] >= 15:
                hero["mind"] -= 15
                dmg = 45
                monster["hp"] = max(0, monster["hp"] - dmg)
                combat_log = f"BLACK ORB! Dark orb pierces 100% armor for {dmg} DMG!"
                enemy_turn()
            else:
                combat_log = "Insufficient Mind points for Black Orb!"
            current_menu = "MAIN"
            cursor_idx = 0
        elif cursor_idx == 1:  # Leg sweep
            dmg = 15
            monster["hp"] = max(0, monster["hp"] - dmg)
            monster["debuff_legs"] = True
            combat_log = f"LEG SWEEP! Sweeping kick breaks enemy legs -> CRAWLING!"
            enemy_turn()
            current_menu = "MAIN"
            cursor_idx = 0
        elif cursor_idx == 2:  # Devour
            dmg = 20
            monster["hp"] = max(0, monster["hp"] - dmg)
            hero["hunger"] = max(0, hero["hunger"] - 40)
            combat_log = f"DEVOUR! {hero['name']} bites enemy for {dmg} DMG. Hunger reduced by 40!"
            enemy_turn()
            current_menu = "MAIN"
            cursor_idx = 0
        elif cursor_idx == 3:  # Back
            current_menu = "MAIN"
            cursor_idx = 0

    elif current_menu == "POUCH":
        if cursor_idx == 0:    # Poppy
            if inventory["poppy"] > 0:
                inventory["poppy"] -= 1
                hero["hp"] = min(hero["max_hp"], hero["hp"] + 50)
                if "Bleeding (-4 HP/turn)" in hero["debuffs"]:
                    hero["debuffs"].remove("Bleeding (-4 HP/turn)")
                combat_log = f"{hero['name']} consumes White Poppy (+50 HP, bleeding stopped)."
                enemy_turn()
            else:
                combat_log = "Out of White Poppy!"
            current_menu = "MAIN"
            cursor_idx = 0
        elif cursor_idx == 1:  # Weed
            if inventory["weed"] > 0:
                inventory["weed"] -= 1
                hero["hp"] = min(hero["max_hp"], hero["hp"] + 120)
                combat_log = f"{hero['name']} uses Herbal Weed (+120 HP)."
                enemy_turn()
            else:
                combat_log = "Out of Herbal Weed!"
            current_menu = "MAIN"
            cursor_idx = 0
        elif cursor_idx == 2:  # Bread
            if inventory["bread"] > 0:
                inventory["bread"] -= 1
                hero["hunger"] = max(0, hero["hunger"] - 40)
                combat_log = f"{hero['name']} eats Moldy Bread (-40 Hunger)."
            else:
                combat_log = "Out of Bread!"
            current_menu = "MAIN"
            cursor_idx = 0
        elif cursor_idx == 3:  # Ale
            if inventory["ale"] > 0:
                inventory["ale"] -= 1
                hero["mind"] = min(hero["max_mind"], hero["mind"] + 35)
                hero["buff"] = "STEADY NERVES (+35 Mind)"
                combat_log = f"{hero['name']} drinks Vintage Ale (+35 Mind)."
            else:
                combat_log = "Out of Ale!"
            current_menu = "MAIN"
            cursor_idx = 0
        elif cursor_idx == 4:  # Back
            current_menu = "MAIN"
            cursor_idx = 0

    elif current_menu == "TACTICS":
        if cursor_idx == 0:    # Berserk
            hero["buff"] = "BERSERK (+50% ATK)"
            combat_log = f"{hero['name']} enters BERSERK stance (+50% ATK, +30% DMG taken)."
            current_menu = "MAIN"
            cursor_idx = 0
        elif cursor_idx == 1:  # Iron Guard
            hero["buff"] = "IRON GUARD (-70% DMG)"
            combat_log = f"{hero['name']} assumes IRON GUARD stance (-70% incoming DMG)."
            current_menu = "MAIN"
            cursor_idx = 0
        elif cursor_idx == 2:  # Agile
            hero["buff"] = "AGILE DANCE (+35% DODGE)"
            combat_log = f"{hero['name']} assumes AGILE DANCE (+35% Dodge, 100% Flee)."
            current_menu = "MAIN"
            cursor_idx = 0
        elif cursor_idx == 3:  # Back
            current_menu = "MAIN"
            cursor_idx = 0

# =============================================================================
# ENEMY TURN & DAMAGE RESOLUTION
# =============================================================================
def enemy_turn():
    global combat_log, active_hero_idx
    hero = squad[active_hero_idx]

    if monster["hp"] <= 0 or monster["debuff_decapitated"]:
        combat_log += " | Foe collapses into pool of blood! VICTORY!"
        return

    # Bleed effect
    if "Bleeding (-4 HP/turn)" in hero["debuffs"]:
        hero["hp"] = max(0, hero["hp"] - 4)

    dmg = monster["atk"] - (hero["def"] // 2)
    if hero["is_guarding"]:
        dmg = int(dmg * 0.3)
        hero["is_guarding"] = False

    dmg = max(4, dmg)
    hero["hp"] = max(0, hero["hp"] - dmg)
    combat_log += f" | Foe strikes back! {hero['name']} takes {dmg} DMG."

    # Chance foe inflicts bleeding scratch
    import random
    if random.random() < 0.4 and "Bleeding (-4 HP/turn)" not in hero["debuffs"]:
        hero["debuffs"].append("Bleeding (-4 HP/turn)")
        combat_log += " Claws inflict Bleeding (-4 HP/turn)!"

    # Down check
    if hero["hp"] == 0:
        combat_log += f" | {hero['name']} is knocked down!"
        for idx, comp in enumerate(squad):
            if comp["hp"] > 0:
                active_hero_idx = idx
                combat_log += f" -> {comp['name']} steps up to vanguard!"
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
                print("\n[OK] Exited Combat UI Demo.")
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
    print("\n>>> STARTING POKÉMON-STYLE COMBAT ARENA SHOWCASE <<<\n")
    states = [
        ("MAIN", 0, "STEP 1: POKÉMON-STYLE COMBAT ARENA - Clean layout, 100 columns, no icon clutter"),
        ("ACTION", 0, "STEP 2: Select 'Action' -> Prepare to target limbs"),
        ("TARGET_LIMB", 2, "STEP 3: Sever 'Right Arm' -> Foe drops sword, DISARMED (ATK reduced to 10)"),
        ("TARGET_LIMB", 4, "STEP 4: Break 'Legs' -> Foe collapses to CRAWL (100% Flee & 100% Decapitate)"),
        ("SWITCH_HERO", 1, "STEP 5: Squad Roster -> Switch D'ARCE to Vanguard"),
        ("TARGET_LIMB", 0, "STEP 6: D'ARCE decapitates crawling foe -> 100% CRITICAL FINISH! VICTORY!")
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
            combat_log = "SEVERED RIGHT ARM! Foe drops weapon -> DISARMED (ATK reduced to 10)!"
        elif idx == 3: # Step 4: break legs
            monster["debuff_legs"] = True
            monster["hp"] = 53
            combat_log = "BROKEN LEGS! Foe collapses to CRAWL -> 100% FLEE & 100% DECAPITATE!"
        elif idx == 4: # Step 5: switch to D'arce
            active_hero_idx = 1
            combat_log = "VANGUARD DEPLOYED! D'ARCE [Paladin] takes point."
        elif idx == 5: # Step 6: decapitate head
            monster["debuff_decapitated"] = True
            monster["hp"] = 0
            combat_log = "CRITICAL FINISH! Foe is crawling; D'ARCE decapitates target! VICTORY!"

        render_screen()
        print(f"\n  \033[1;32m>>> [SHOWCASE]: {step_desc} <<<\033[0m")
        time.sleep(1.0)

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--showcase":
        run_showcase_trace()
    else:
        run_interactive_loop()
