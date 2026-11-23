#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
================================================================================
FEAR & HUNGER: TERMINAL LABYRINTH - TACTICAL ARENA (BALANCED HERO ROSTER)
================================================================================
Standardized Features:
1. Pokémon-Style Diagonal Combat Arena (100 Columns exact width).
2. Four Unique, Differentiated Heroes with Distinct Roles, Passives & Skills:
   - CAHARA: Mercenary Rogue (High Dodge, Item Stealing, 100% Flee).
   - D'ARCE: Holy Paladin Tank (Damage Reduction, Heavy Armor, Holy Heal).
   - ENKI: Occult Sorcerer Glass Cannon (Auto Mind Regen, 100% Armor Pierce).
   - THE GIRL: Ward Support & Evasion (Enemy ATK -30%, 100% Evasion, Mind Healing).
3. Tri-State Postural Morphology (Zero blood/gore, clean dismemberment, amber warning).
4. Uniform Spaced-Out Layout with Colons Aligned at Column 9.
5. 100% Icon-Free Gothic CRPG Navigation with W/S or Arrow Keys.
================================================================================
"""

import sys
import os
import time
import re
import unicodedata
import json
import random

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

def make_bar(curr, max_v, bar_len=16, color_code="32"):
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

MONSTER_SPRITE_INTACT = []
if RAW_MONSTER_8:
    for idx in range(12):
        if idx < len(RAW_MONSTER_8) and RAW_MONSTER_8[idx].strip():
            MONSTER_SPRITE_INTACT.append(f"\033[1;37m{RAW_MONSTER_8[idx]}\033[0m")
        else:
            MONSTER_SPRITE_INTACT.append(" " * 29)
else:
    MONSTER_SPRITE_INTACT = [
        "      \033[1;37m▄▀▀▀▄▄▀▀▀▄\033[0m             ",
        "     \033[1;37m▀▀ ▄ ▀▀ ▄ ▀\033[0m             ",
        "     \033[1;37m▀▀▄▄▄▀▀▄▄▄▀\033[0m             ",
        "      \033[1;37m▄▀▀▀▄▄▀▀▀▄\033[0m  \033[1;37m▄▀\033[0m(SWORD)  ",
        "      \033[1;37m▀ ▀▀▀▀▀▀ ▀\033[0m  \033[1;37m▀▀▀\033[0m        ",
        "      \033[1;37m▀  ▀▄ ▀▄ ▀\033[0m             ",
        "      \033[1;37m▀▀  ▀  ▀ ▀\033[0m             ",
        "                             ",
        "                             ",
        "                             ",
        "                             ",
        "                             "
    ]

# Standing Disarmed Sprite (Severed Sword Arm -> Amber Socket, Disarmed)
MONSTER_SPRITE_DISARMED = [
    "      \033[1;37m▄▀▀▀▄▄▀▀▀▄\033[0m             ",
    "     \033[1;37m▀▀ ▄ ▀▀ ▄ ▀\033[0m             ",
    "     \033[1;37m▀▀▄▄▄▀▀▄▄▄▀\033[0m             ",
    "      \033[1;37m▄▀▀▀▄▄▀▀\033[0m\033[1;33m▄▀\033[0m  (DISARMED) ",
    "      \033[1;37m▀ ▀▀▀▀▀▀ ▀\033[0m             ",
    "      \033[1;37m▀  ▀▄ ▀▄ ▀\033[0m             ",
    "      \033[1;37m▀▀  ▀  ▀ ▀\033[0m             ",
    "                             ",
    "                             ",
    "                             ",
    "                             ",
    "                             "
]

# Postural Crawling Sprite (White Body with Amber Severance Joints)
MONSTER_SPRITE_CRAWLING = [
    "                             ",
    "                             ",
    "                             ",
    "                             ",
    "      \033[1;37m▄▀▀▀▄▄▀▀▀▄\033[0m             ",
    "     \033[1;37m▀▀ ▄ ▀▀ ▄ ▀\033[0m             ",
    "     \033[1;37m▀▀▄▄▄▀▀▄▄▄▀\033[0m             ",
    "      \033[1;37m▄▀▀▀▄▄▀▀\033[0m\033[1;33m▄▀\033[0m  (DISARMED) ",
    "   \033[1;37m▄▀▀▀▀▀▀▀▀▀▀\033[0m\033[1;33m▀▀▀▄\033[0m (CROUCHED)",
    "   \033[1;37m▀▀▀▀\033[0m   \033[1;33m▀▀\033[0m  \033[1;37m▀▀▀▀\033[0m           ",
    "    \033[1;33m[DISARMED & CROUCHED]\033[0m    ",
    "                             "
]

# Postural Deactivated Sprite (Ash Gray Palette, Headless, Collapsed Silhouette)
MONSTER_SPRITE_DECAPITATED = [
    "                             ",
    "                             ",
    "                             ",
    "                             ",
    "                             ",
    "                             ",
    "      \033[90m▄▀▀▀▄▄▀▀▀▄\033[0m             ",
    "      \033[90m▀ ▀▀▀▀▀▀ ▀\033[0m             ",
    "   \033[90m▄▀▀▀▀▀▀▀▀▀▀▀▀▀▄\033[0m           ",
    "   \033[90m▀▀▀▀   ▀▀  ▀▀▀▀\033[0m           ",
    "   \033[90m[HEADLESS & NEUTRALIZED]\033[0m  ",
    "                             "
]

def format_model_row(sp_line):
    return " " * 6 + sp_line + " " * 7

# =============================================================================
# =============================================================================
# GAME DATA: MONSTER & BALANCED HERO ROSTER (4-PILLAR ARCHETYPE & TOXICITY SYSTEM)
# =============================================================================
monster = {
    "name": "SHADOW SWORDSMAN",
    "id": 8,
    "archetype": "ARMORED",     # NORMAL, SPECTRAL, ARMORED, AMBUSHER, TERROR
    "hp": 95,
    "max_hp": 95,
    "atk": 24,
    "def": 99,                 # High DEF for Armored archetype
    "debuff_arm_r": False,     # Disarmed
    "debuff_arm_l": False,     # Guard Broken
    "debuff_legs": False,      # Crouched / Crawling
    "debuff_decapitated": False # Neutralized
}

squad = [
    {
        "name": "CAHARA",
        "role": "Mercenary",
        "hp": 115,
        "max_hp": 115,
        "mind": 90,
        "max_mind": 100,
        "hunger": 20,
        "max_hunger": 100,
        "atk": 32,
        "def": 18,
        "toxicity": 0,
        "max_toxicity": 100,
        "buff": "",
        "is_guarding": False,
        "dodge_rate": 0.20,
        "passive": "Fast Hands (+20% Dodge, Flee, Trap Disarm)",
        "debuffs": []
    },
    {
        "name": "D'ARCE",
        "role": "Paladin",
        "hp": 150,
        "max_hp": 150,
        "mind": 85,
        "max_mind": 100,
        "hunger": 35,
        "max_hunger": 100,
        "atk": 28,
        "def": 32,
        "toxicity": 0,
        "max_toxicity": 100,
        "buff": "",
        "is_guarding": False,
        "dodge_rate": 0.05,
        "passive": "Iron Will (-25% DMG, Holy Smite Armor Break)",
        "debuffs": []
    },
    {
        "name": "ENKI",
        "role": "Occultist",
        "hp": 85,
        "max_hp": 85,
        "mind": 130,
        "max_mind": 130,
        "hunger": 15,
        "max_hunger": 100,
        "atk": 48,
        "def": 16,
        "toxicity": 0,
        "max_toxicity": 100,
        "buff": "",
        "is_guarding": False,
        "dodge_rate": 0.10,
        "passive": "Enlightenment (+5 MND/turn, True Magic)",
        "debuffs": []
    },
    {
        "name": "THE GIRL",
        "role": "Ward",
        "hp": 95,
        "max_hp": 95,
        "mind": 100,
        "max_mind": 100,
        "hunger": 10,
        "max_hunger": 100,
        "atk": 24,
        "def": 36,
        "toxicity": 0,
        "max_toxicity": 100,
        "buff": "",
        "is_guarding": False,
        "dodge_rate": 0.30,
        "passive": "Innocent Aura (Enemy ATK -30%, Dread Immune)",
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
    print()

    # -------------------------------------------------------------------------
    # ZONE 1: OPPONENT ZONE (TOP)
    # Left: Monster Tactical Card (54 cols)
    # Gap : 4 spaces
    # Right: Monster Sprite Model (42 cols)
    # Total: 54 + 4 + 42 = 100 columns
    # -------------------------------------------------------------------------
    c_mcard = "\033[1;33m" if current_menu == "TARGET_LIMB" else "\033[1;30m"
    m_border = f"{c_mcard}+" + "-" * 52 + f"+{c_mcard}\033[0m"

    if monster["debuff_decapitated"]:
        m_sprite = MONSTER_SPRITE_DECAPITATED
        m_model_sub = "\033[90m[NEUTRALIZED]\033[0m"
    elif monster["debuff_legs"]:
        m_sprite = MONSTER_SPRITE_CRAWLING
        m_model_sub = "\033[1;33m[CROUCHED]\033[0m"
    elif monster["debuff_arm_r"] or monster["debuff_arm_l"]:
        m_sprite = MONSTER_SPRITE_DISARMED
        m_model_sub = "\033[1;33m[DISARMED]\033[0m"
    else:
        m_sprite = MONSTER_SPRITE_INTACT
        m_model_sub = ""

    m_pct = int(max(0, monster["hp"]) / float(monster["max_hp"]) * 100)
    m_hp_bar = make_bar(monster["hp"], monster["max_hp"], 16, "31")

    has_monster_injury = (
        monster["debuff_decapitated"] or
        monster["debuff_legs"] or
        monster["debuff_arm_r"] or
        monster["debuff_arm_l"]
    )

    m_inj_header = "\033[1;33m  ANATOMY & DEBUFFS:\033[0m" if has_monster_injury else ""
    m_inj_1 = ""
    m_inj_2 = ""
    m_inj_3 = ""

    if monster["debuff_decapitated"]:
        m_inj_1 = "\033[90m  [HEAD]  Decapitated (Neutralized)\033[0m"
    elif monster["debuff_legs"]:
        m_inj_1 = "\033[1;33m  [LEGS]  Broken (Crouched, 100% Flee)\033[0m"
        m_inj_2 = "\033[1;33m  [HEAD]  Exposed (100% Decapitate Hit)\033[0m"
        if monster["debuff_arm_r"]:
            m_inj_3 = "\033[1;33m  [R-ARM] Severed (Disarmed, ATK -14)\033[0m"
    elif monster["debuff_arm_r"] or monster["debuff_arm_l"]:
        if monster["debuff_arm_r"]:
            m_inj_1 = "\033[1;33m  [R-ARM] Severed (Disarmed, ATK -14)\033[0m"
        if monster["debuff_arm_l"]:
            m_inj_2 = "\033[1;36m  [L-ARM] Severed (Guard Broken)\033[0m"

    arch = monster.get("archetype", "NORMAL")
    if arch == "SPECTRAL":
        trait_desc = "\033[1;35m  TRAIT : SPECTRAL (Immune to blades, Magic weak)\033[0m"
    elif arch == "ARMORED":
        trait_desc = "\033[1;36m  TRAIT : ARMORED (Deflects blades, Smite weak)\033[0m"
    elif arch == "AMBUSHER":
        trait_desc = "\033[1;31m  TRAIT : AMBUSHER (Lethal strike, Dodge weak)\033[0m"
    elif arch == "TERROR":
        trait_desc = "\033[1;35m  TRAIT : DREAD AURA (-25 Mind/turn, Ward calm)\033[0m"
    else:
        trait_desc = "\033[90m  TRAIT : STANDARD COMBATANT\033[0m"

    # 14 Rows of Monster Card (54 cols each) - Uniform Spacing
    m_card_rows = [
        m_border,
        make_card_row(f"\033[1;31m  FOE   : #{monster['id']:02d} {monster['name']:<17} \033[1;33m[{arch}]\033[0m", c_mcard),
        make_card_row("", c_mcard),
        make_card_row(f"  HP    : {m_hp_bar} \033[1;31m{monster['hp']:3d}/{monster['max_hp']:3d} ({m_pct:3d}%)\033[0m", c_mcard),
        make_card_row("", c_mcard),
        make_card_row(trait_desc, c_mcard),
        make_card_row("", c_mcard),
        make_card_row(m_inj_header, c_mcard),
        make_card_row(m_inj_1, c_mcard),
        make_card_row(m_inj_2, c_mcard),
        make_card_row(m_inj_3, c_mcard),
        make_card_row("", c_mcard),
        make_card_row("", c_mcard),
        m_border
    ]

    m_model_rows = [
        pad_str("          \033[1;31m[ENEMY]\033[0m", 42)
    ]
    for r in range(12):
        sp = m_sprite[r] if r < len(m_sprite) else " " * 29
        m_model_rows.append(format_model_row(sp))
    m_sub_pad = pad_str(f"       {m_model_sub}", 42) if m_model_sub else pad_str("", 42)
    m_model_rows.append(m_sub_pad)

    for r_idx in range(14):
        print(f"{m_card_rows[r_idx]}    {m_model_rows[r_idx]}\033[0m")

    print()

    # -------------------------------------------------------------------------
    # ZONE 2: PLAYER SQUAD ZONE (BOTTOM)
    # Left: Hero Sprite Model (42 cols)
    # Gap : 4 spaces
    # Right: Hero Tactical Card (54 cols)
    # Total: 42 + 4 + 54 = 100 columns
    # -------------------------------------------------------------------------
    c_hcard = "\033[1;32m" if current_menu in ("SWITCH_HERO", "POUCH", "TACTICS") else "\033[1;30m"
    h_border = f"{c_hcard}+" + "-" * 52 + f"+{c_hcard}\033[0m"

    hero_key = hero["name"]
    h_sprite = HERO_SPRITES.get(hero_key, HERO_SPRITES.get("CAHARA", []))

    h_pct = int(max(0, hero["hp"]) / float(hero["max_hp"]) * 100)
    h_hp_bar = make_bar(hero["hp"], hero["max_hp"], 16, "32")
    h_mnd_bar = make_bar(hero["mind"], hero["max_mind"], 12, "36")
    h_hng_bar = make_bar(hero["hunger"], hero["max_hunger"], 12, "33")

    h_tox = hero.get("toxicity", 0)
    h_tox_bar = make_bar(h_tox, 100, 12, "31" if h_tox >= 80 else ("33" if h_tox >= 50 else "32"))
    tox_badge = "\033[1;31m[INTOXICATED]\033[0m" if h_tox >= 100 else ("\033[1;33m[HIGH]\033[0m" if h_tox >= 80 else "\033[90m[SAFE]\033[0m")

    status_line = ""
    if hero.get("debuffs"):
        status_line = f"\033[1;31m  STATUS: {', '.join(hero['debuffs'])}\033[0m"
    elif hero.get("buff"):
        status_line = f"\033[1;32m  STATUS: {hero['buff']}\033[0m"
    else:
        status_line = f"\033[90m  STATUS: Battle Ready\033[0m"

    h_model_rows = [
        pad_str("          \033[1;32m[HERO]\033[0m", 42)
    ]
    for r in range(12):
        sp = h_sprite[r] if r < len(h_sprite) else " " * 29
        h_model_rows.append(format_model_row(sp))
    h_model_rows.append(pad_str("", 42))

    # 14 Rows of Hero Card (54 cols each) - Uniform Spacing
    h_card_rows = [
        h_border,
        make_card_row(f"\033[1;32m  HERO  : {hero['name']:<9} \033[90m[{hero['role']}]\033[0m", c_hcard),
        make_card_row("", c_hcard),
        make_card_row(f"  HP    : {h_hp_bar} \033[1;32m{hero['hp']:3d}/{hero['max_hp']:3d} ({h_pct:3d}%)\033[0m", c_hcard),
        make_card_row("", c_hcard),
        make_card_row(f"  MIND  : {h_mnd_bar} \033[1;36m{hero['mind']:3d}/{hero['max_mind']:3d}\033[0m", c_hcard),
        make_card_row("", c_hcard),
        make_card_row(f"  HUNGER: {h_hng_bar} \033[1;33m{hero['hunger']:3d}/{hero['max_hunger']:3d}\033[0m", c_hcard),
        make_card_row("", c_hcard),
        make_card_row(f"  TOXIC : {h_tox_bar} \033[1;{'31' if h_tox >= 80 else '32'}m{h_tox:3d}%\033[0m {tox_badge}", c_hcard),
        make_card_row("", c_hcard),
        make_card_row(f"\033[1;33m  PASSIV: {hero['passive'][:38]}\033[0m", c_hcard),
        make_card_row(status_line, c_hcard),
        h_border
    ]

    for r_idx in range(14):
        print(f"{h_model_rows[r_idx]}    {h_card_rows[r_idx]}\033[0m")

    print()

    # -------------------------------------------------------------------------
    # SECTION 3: COMBAT LOG BOX (100 COLUMNS)
    # -------------------------------------------------------------------------
    print("\033[1;30m+----------------------------------------------------------------------------------------------------+\033[0m")
    log_content = pad_str(f"\033[1;33m[LOG]\033[0m \033[1;37m{combat_log}\033[0m", 96)
    print(f"| {log_content} \033[1;30m|")
    print("\033[1;30m+----------------------------------------------------------------------------------------------------+\033[0m")
    print()

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

    for _ in range(max(0, 6 - len(options))):
        print()

    print()

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
# MENU DATA RESOLUTION WITH DIVERSE CHARACTER SKILLS
# =============================================================================
def get_current_menu_data():
    global active_hero_idx
    h = squad[active_hero_idx]

    if current_menu == "MAIN":
        return {
            "title": f"MAIN COMMANDS ({h['name']} - {h['role']})",
            "options": [
                {"label": "ACTION",   "desc": "-> Attack, Guard, Switch Vanguard, Flee"},
                {"label": "SKILL",    "desc": f"-> Unique class abilities ({h['name']})"},
                {"label": "ITEM",     "desc": "-> Poppy herb, Healing weed, Rations, Ale"},
                {"label": "TACTICS",  "desc": "-> Stances (Berserk / Iron Guard / Agile)"}
            ]
        }
    elif current_menu == "ACTION":
        flee_text = "Escape battle (\033[1;32m100% Guaranteed - Foe crawling\033[0m)" if monster["debuff_legs"] else "Escape battle (50% Chance)"
        if h["name"] == "CAHARA":
            flee_text = "Escape battle (\033[1;32m100% Guaranteed - Fast Hands Passive\033[0m)"
        return {
            "title": "ACTION > SELECT TACTICAL COMMAND",
            "options": [
                {"label": "ATTACK",  "desc": "-> Target specific limbs to disable foe"},
                {"label": "GUARD",   "desc": "-> Brace for impact (-70% incoming damage)"},
                {"label": "SWITCH",  "desc": "-> Open Squad Roster to change active vanguard"},
                {"label": "FLEE",    "desc": f"-> {flee_text}"},
                {"label": "BACK",    "desc": "-> Return to main commands"}
            ]
        }
    elif current_menu == "SWITCH_HERO":
        opts = []
        for idx, comp in enumerate(squad):
            is_active = (idx == active_hero_idx)
            tag = " \033[1;32m[ACTIVE]\033[0m" if is_active else " \033[90m[RESERVE]\033[0m"
            status_tag = "" if comp["hp"] > 0 else " \033[1;31m[DOWN]\033[0m"
            tox_val = comp.get("toxicity", 0)
            if tox_val >= 100:
                tox_str = "\033[1;31mTOX:MAX!\033[0m"
            elif tox_val >= 50:
                tox_str = f"\033[1;33mTOX:{tox_val:2d}%\033[0m"
            else:
                tox_str = f"\033[90mTOX:{tox_val:2d}%\033[0m"
            opts.append({
                "label": f"{comp['name']:<9} [{comp['role']:<9}]",
                "desc": f"HP:{comp['hp']:3d}/{comp['max_hp']:3d} MND:{comp['mind']:3d} {tox_str} | {comp['passive'][:20]}{status_tag}{tag}"
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
                {"label": "LEGS",       "desc": "-> 100% Hit | Break legs -> Force crouch (100% Flee)"},
                {"label": "BACK",       "desc": "-> Return to action menu"}
            ]
        }
    elif current_menu == "SKILL":
        if h["name"] == "CAHARA":
            return {
                "title": "SKILLS & ROGUE TECHNIQUES (CAHARA)",
                "options": [
                    {"label": "EN GARDE",     "desc": "-> 100% precision strike inflicting +35 limb DMG"},
                    {"label": "STEAL ITEM",   "desc": "-> Pickpocket foe: steal 1 Poppy/Bread from target"},
                    {"label": "SMOKE BOMB",   "desc": "-> Blind opponent: 100% flee battle immediately"},
                    {"label": "BACK",         "desc": "-> Return to main commands"}
                ]
            }
        elif h["name"] == "D'ARCE":
            return {
                "title": "HOLY KNIGHT VOWS & PRAYERS (D'ARCE)",
                "options": [
                    {"label": "DEFENSE STANCE", "desc": "-> Brace shield: block 75% dmg & restore 15 HP"},
                    {"label": "HEALING PRAYER", "desc": "-> Spend 15 Mind: restore +45 HP instantly"},
                    {"label": "HOLY SMITE",     "desc": "-> Empower blade: heavy physical slash for 42 DMG"},
                    {"label": "BACK",           "desc": "-> Return to main commands"}
                ]
            }
        elif h["name"] == "ENKI":
            return {
                "title": "HEXEN OCCULT & DARK SORCERY (ENKI)",
                "options": [
                    {"label": "BLACK ORB",       "desc": "-> Spend 15 Mind: pierce 100% armor for 50 DMG"},
                    {"label": "BLOOD SACRIFICE", "desc": "-> Convert 20 HP into +35 Mind points"},
                    {"label": "HEXEN BIND",      "desc": "-> Spend 10 Mind: paralyze foe, guaranteed head hit"},
                    {"label": "BACK",            "desc": "-> Return to main commands"}
                ]
            }
        else: # THE GIRL
            return {
                "title": "SUPPORT AURA & EVASIVE TACTICS (THE GIRL)",
                "options": [
                    {"label": "NIMBLE DODGE",   "desc": "-> Duck into shadows: 100% dodge enemy's next hit"},
                    {"label": "LOVING EMBRACE", "desc": "-> Comfort party: restore +35 Mind & calm nerves"},
                    {"label": "DISTRACT FOE",   "desc": "-> Wave lantern: reduce enemy attack power by 50%"},
                    {"label": "BACK",           "desc": "-> Return to main commands"}
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
            if monster["debuff_legs"] or hero["name"] == "CAHARA":
                combat_log = "ESCAPE SUCCESSFUL! Party safely retreats into the labyrinth corridors."
                time.sleep(1.2)
                sys.exit(0)
            else:
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
                combat_log = f"VANGUARD DEPLOYED! {squad[active_hero_idx]['name']} [{squad[active_hero_idx]['role']}] takes point."
            current_menu = "MAIN"
            cursor_idx = 0
        else:
            current_menu = "ACTION"
            cursor_idx = 2

    elif current_menu == "TARGET_LIMB":
        arch = monster.get("archetype", "NORMAL")
        if arch == "SPECTRAL" and cursor_idx != 5:
            combat_log = f"PHANTOM IMMUNITY! {hero['name']}'s blade passes harmlessly through spectral form! (0 DMG - Only Enki Occult Magic works!)"
            enemy_turn()
            current_menu = "MAIN"
            cursor_idx = 0
        elif arch == "ARMORED" and cursor_idx != 5:
            dmg = 2
            monster["hp"] = max(0, monster["hp"] - dmg)
            combat_log = f"ARMOR DEFLECTION! {hero['name']}'s blade clangs off steel armor for only {dmg} DMG! (Need D'ARCE Smite or ENKI Magic!)"
            enemy_turn()
            current_menu = "MAIN"
            cursor_idx = 0
        elif cursor_idx == 0:    # Head
            if monster["debuff_legs"]:
                dmg = monster["hp"]
                monster["hp"] = 0
                monster["debuff_decapitated"] = True
                combat_log = f"CRITICAL FINISH! Foe is crouched; {hero['name']} cleanly severs head! VICTORY!"
            else:
                if random.random() < 0.35:
                    dmg = monster["hp"]
                    monster["hp"] = 0
                    monster["debuff_decapitated"] = True
                    combat_log = f"DECAPITATION! Blade severs neck! Fatal blow for {dmg} DMG! VICTORY!"
                else:
                    dmg = 18
                    monster["hp"] = max(0, monster["hp"] - dmg)
                    combat_log = f"Glancing strike across the head for {dmg} DMG."
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
            combat_log = f"DISARMED! Weapon arm severed (-{dmg} HP). Foe's ATK reduced to 10!"
            enemy_turn()
            current_menu = "MAIN"
            cursor_idx = 0
        elif cursor_idx == 3:  # Left Arm
            dmg = 18
            monster["hp"] = max(0, monster["hp"] - dmg)
            monster["debuff_arm_l"] = True
            combat_log = f"SHIELD BROKEN! Left arm disabled (-{dmg} HP). Foe defense shattered!"
            enemy_turn()
            current_menu = "MAIN"
            cursor_idx = 0
        elif cursor_idx == 4:  # Legs
            dmg = 22
            monster["hp"] = max(0, monster["hp"] - dmg)
            monster["debuff_legs"] = True
            combat_log = f"LEGS BROKEN! -{dmg} HP. Foe collapses to floor -> 100% FLEE & 100% HEAD HIT!"
            enemy_turn()
            current_menu = "MAIN"
            cursor_idx = 0
        elif cursor_idx == 5:  # Back
            current_menu = "ACTION"
            cursor_idx = 0

    elif current_menu == "SKILL":
        h = squad[active_hero_idx]
        if h["name"] == "CAHARA":
            if cursor_idx == 0:    # En Garde
                dmg = 35
                monster["hp"] = max(0, monster["hp"] - dmg)
                combat_log = f"EN GARDE! Cahara executes swift lunging strike for {dmg} DMG!"
                enemy_turn()
            elif cursor_idx == 1:  # Steal
                stolen_item = "poppy" if random.random() < 0.5 else "bread"
                inventory[stolen_item] += 1
                combat_log = f"STEAL SUCCESS! Cahara pickpockets the foe and secures 1x {stolen_item.upper()}!"
                enemy_turn()
            elif cursor_idx == 2:  # Smoke bomb
                combat_log = "SMOKE BOMB! Dense fog blinds opponent. 100% ESCAPE SUCCESSFUL!"
                time.sleep(1.2)
                sys.exit(0)
            current_menu = "MAIN"
            cursor_idx = 0

        elif h["name"] == "D'ARCE":
            if cursor_idx == 0:    # Defense stance
                h["is_guarding"] = True
                h["hp"] = min(h["max_hp"], h["hp"] + 15)
                h["buff"] = "IRON VOW (-75% DMG)"
                combat_log = "DEFENSE STANCE! D'arce braces tower shield (+15 HP, -75% incoming DMG)!"
                enemy_turn()
            elif cursor_idx == 1:  # Healing prayer
                if h["mind"] >= 15:
                    h["mind"] -= 15
                    h["hp"] = min(h["max_hp"], h["hp"] + 45)
                    combat_log = "HEALING PRAYER! Sacred light restores +45 HP!"
                    enemy_turn()
                else:
                    combat_log = "Insufficient Mind points for Healing Prayer!"
            elif cursor_idx == 2:  # Holy smite
                dmg = 42
                if monster.get("archetype") == "ARMORED":
                    monster["archetype"] = "NORMAL"
                    monster["def"] = 14
                    combat_log = f"ARMOR SHATTERED! D'arce's Holy Smite fractures heavy steel plate for {dmg} DMG! Foe DEF shattered!"
                else:
                    combat_log = f"HOLY SMITE! Heavy sanctified downward cleave inflicts {dmg} DMG!"
                monster["hp"] = max(0, monster["hp"] - dmg)
                enemy_turn()
            current_menu = "MAIN"
            cursor_idx = 0

        elif h["name"] == "ENKI":
            if cursor_idx == 0:    # Black orb
                if h["mind"] >= 15:
                    h["mind"] -= 15
                    dmg = 50
                    monster["hp"] = max(0, monster["hp"] - dmg)
                    if monster.get("archetype") == "SPECTRAL":
                        combat_log = f"OCCULT PURGE! Black Orb tears apart phantom spirit for {dmg} True Magic DMG! (SPECTRAL WEAKNESS)!"
                    elif monster.get("archetype") == "ARMORED":
                        combat_log = f"DEFENSE BYPASS! Black Orb bypasses steel plate for {dmg} True Magic DMG!"
                    else:
                        combat_log = f"BLACK ORB! Dark sphere pierces 100% defense for {dmg} unblockable DMG!"
                    enemy_turn()
                else:
                    combat_log = "Insufficient Mind points for Black Orb!"
            elif cursor_idx == 1:  # Blood sacrifice
                if h["hp"] > 20:
                    h["hp"] -= 20
                    h["mind"] = min(h["max_mind"], h["mind"] + 35)
                    combat_log = "BLOOD SACRIFICE! Enki cuts own flesh (-20 HP) to harvest +35 Mind!"
                else:
                    combat_log = "HP too low for Blood Sacrifice!"
            elif cursor_idx == 2:  # Hexen bind
                if h["mind"] >= 10:
                    h["mind"] -= 10
                    monster["debuff_legs"] = True
                    combat_log = "HEXEN BIND! Occult shadows root the foe to floor (100% Head hit rate)!"
                    enemy_turn()
                else:
                    combat_log = "Insufficient Mind for Hexen Bind!"
            current_menu = "MAIN"
            cursor_idx = 0

        else: # THE GIRL
            if cursor_idx == 0:    # Nimble dodge
                h["buff"] = "NIMBLE DODGE (100% EVADE)"
                combat_log = "NIMBLE DODGE! The Girl slips into shadows, guaranteeing 100% evasion!"
                enemy_turn()
            elif cursor_idx == 1:  # Loving embrace
                for m in squad:
                    m["mind"] = min(m["max_mind"], m["mind"] + 35)
                combat_log = "LOVING EMBRACE! Heartwarming comfort restores +35 Mind to ENTIRE SQUAD and dispels terror!"
                enemy_turn()
            elif cursor_idx == 2:  # Distract foe
                monster["temp_debuff"] = "DISTRACTED (-50% ATK)"
                combat_log = "DISTRACT FOE! The Girl waves lantern: enemy's attack power halved by 50%!"
                enemy_turn()
            current_menu = "MAIN"
            cursor_idx = 0

    elif current_menu == "POUCH":
        if cursor_idx == 0:    # Poppy (+50 HP, +35 Toxicity)
            if inventory["poppy"] > 0:
                inventory["poppy"] -= 1
                if hero.get("toxicity", 0) >= 100:
                    hero["hp"] = max(1, hero["hp"] - 5)
                    combat_log = f"INTOXICATED! {hero['name']}'s stomach rejects Poppy! Vomited (0 HP healed, -5 toxic DMG)!"
                else:
                    hero["hp"] = min(hero["max_hp"], hero["hp"] + 50)
                    hero["toxicity"] = min(100, hero.get("toxicity", 0) + 35)
                    if "Bleeding (-4 HP/turn)" in hero["debuffs"]:
                        hero["debuffs"].remove("Bleeding (-4 HP/turn)")
                    if hero["toxicity"] >= 100:
                        combat_log = f"{hero['name']} consumes Poppy (+50 HP). TOXICITY AT 100%! Hero is now INTOXICATED!"
                    else:
                        combat_log = f"{hero['name']} consumes Poppy (+50 HP, +35% Toxicity [{hero['toxicity']}%])."
                enemy_turn()
            else:
                combat_log = "Out of White Poppy!"
            current_menu = "MAIN"
            cursor_idx = 0
        elif cursor_idx == 1:  # Weed (+120 HP, +50 Toxicity)
            if inventory["weed"] > 0:
                inventory["weed"] -= 1
                if hero.get("toxicity", 0) >= 100:
                    hero["hp"] = max(1, hero["hp"] - 5)
                    combat_log = f"INTOXICATED! {hero['name']} overdoses on Weed! Vomited (0 HP healed, -5 toxic DMG)!"
                else:
                    hero["hp"] = min(hero["max_hp"], hero["hp"] + 120)
                    hero["toxicity"] = min(100, hero.get("toxicity", 0) + 50)
                    if hero["toxicity"] >= 100:
                        combat_log = f"{hero['name']} uses Herbal Weed (+120 HP). TOXICITY AT 100%! Hero is now INTOXICATED!"
                    else:
                        combat_log = f"{hero['name']} uses Herbal Weed (+120 HP, +50% Toxicity [{hero['toxicity']}%])."
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
# ENEMY TURN & DAMAGE RESOLUTION WITH HERO PASSIVES
# =============================================================================
def enemy_turn():
    global combat_log, active_hero_idx
    hero = squad[active_hero_idx]

    if monster["hp"] <= 0 or monster["debuff_decapitated"]:
        combat_log += " | Foe neutralized! VICTORY!"
        return

    # 1. Bench detoxification: reserve heroes purge -25% toxicity per turn!
    purged_names = []
    for idx, comp in enumerate(squad):
        if idx != active_hero_idx and comp.get("toxicity", 0) > 0:
            comp["toxicity"] = max(0, comp["toxicity"] - 25)
            if comp["toxicity"] == 0:
                purged_names.append(comp["name"])
    if purged_names:
        combat_log += f" | Bench rest: {', '.join(purged_names)} detoxified (-25%)!"

    # 2. Active hero toxic nausea check
    if hero.get("toxicity", 0) >= 100:
        hero["hp"] = max(1, hero["hp"] - 5)
        combat_log += f" | {hero['name']} suffers intoxicated nausea (-5 HP)!"

    # 3. Terror Archetype Dread Aura check
    if monster.get("archetype") == "TERROR":
        if hero["name"] == "THE GIRL":
            combat_log += " | INNOCENT AURA! The Girl's serene calm repels Dread Aura (0 Mind lost)!"
        else:
            hero["mind"] = max(0, hero["mind"] - 25)
            combat_log += f" | DREAD AURA! Eldritch horror drains -25 Mind from {hero['name']}!"

    # Bleed effect
    if "Bleeding (-4 HP/turn)" in hero["debuffs"]:
        hero["hp"] = max(0, hero["hp"] - 4)

    # Passive 1: Enki automatically regenerates +5 Mind per turn!
    if hero["name"] == "ENKI" and hero["mind"] < hero["max_mind"]:
        hero["mind"] = min(hero["max_mind"], hero["mind"] + 5)

    # Passive 2: Check Dodge (Cahara 20%, The Girl 30%, Agile buff +35%, Nimble buff 100%)
    effective_dodge = hero.get("dodge_rate", 0.05)
    if "NIMBLE DODGE" in hero.get("buff", ""):
        hero["buff"] = ""
        combat_log += f" | {hero['name']} swiftly slips into shadows! Attack COMPLETELY EVADED!"
        return
    elif "AGILE DANCE" in hero.get("buff", ""):
        effective_dodge += 0.35

    if random.random() < effective_dodge:
        combat_log += f" | {hero['name']} deftly dodges the incoming attack! (+0 DMG)"
        return

    # Incoming Damage calculation with passives
    base_atk = monster["atk"]
    if monster.get("archetype") == "AMBUSHER" and not hero["is_guarding"]:
        base_atk = int(base_atk * 1.5)

    if hero["name"] == "THE GIRL":
        base_atk = int(base_atk * 0.70)
    if "DISTRACTED (-50% ATK)" in monster.get("temp_debuff", ""):
        base_atk = int(base_atk * 0.50)
        monster["temp_debuff"] = ""

    dmg = base_atk - (hero["def"] // 2)

    # D'arce Passive: Iron Will reduces physical damage by 25%
    if hero["name"] == "D'ARCE":
        dmg = int(dmg * 0.75)

    if hero["is_guarding"]:
        dmg = int(dmg * 0.25)
        hero["is_guarding"] = False

    dmg = max(3, dmg)
    hero["hp"] = max(0, hero["hp"] - dmg)
    ambush_tag = " [LETHAL AMBUSH]" if (monster.get("archetype") == "AMBUSHER" and not hero["is_guarding"]) else ""
    combat_log += f" | Foe strikes{ambush_tag}! {hero['name']} takes {dmg} DMG."

    # Chance foe inflicts bleeding scratch
    if random.random() < 0.35 and "Bleeding (-4 HP/turn)" not in hero["debuffs"]:
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
    print("\n>>> STARTING 4-HERO ROLE-LOCKED COMBAT ARENA SHOWCASE <<<\n")
    states = [
        ("MAIN", 0, "PILLAR 1 [AMBUSHER]: Cahara at Vanguard -> Fast Hands passive guarantees evasion vs lethal ambush!"),
        ("TARGET_LIMB", 1, "PILLAR 1 [SPECTRAL]: Ghost manifests -> Cahara physical attack deals 0 DMG (Blades pass harmlessly)!"),
        ("SKILL", 0, "PILLAR 1 & 3 [ENKI COUNTER]: Switch to ENKI -> Black Orb casts 50 True Magic DMG, tearing ghost apart!"),
        ("SKILL", 2, "PILLAR 1 & 3 [D'ARCE COUNTER]: Armored Titan (DEF 99) emerges -> Switch to D'ARCE -> Holy Smite shatters armor!"),
        ("SKILL", 1, "PILLAR 1 & 3 [THE GIRL COUNTER]: Terror Horror emits Dread Aura (-25 MND) -> Switch to THE GIRL -> Loving Embrace calms party!"),
        ("SWITCH_HERO", 0, "PILLAR 2 [TOXICITY & BENCH]: D'arce herb toxicity hits 100% (INTOXICATED) -> Swapped to Bench to detoxify (-25%/turn)!")
    ]

    global current_menu, cursor_idx, active_hero_idx, combat_log
    for idx, (m_state, c_idx, step_desc) in enumerate(states):
        current_menu = m_state
        cursor_idx = c_idx

        if idx == 0:
            active_hero_idx = 0
            monster["name"] = "SHADOW LURKER"
            monster["archetype"] = "AMBUSHER"
            monster["hp"] = 90
            combat_log = "AMBUSHER DETECTED! Foe leaps from dark shadows! Cahara's Fast Hands deftly dodges (+0 DMG)!"
        elif idx == 1:
            monster["name"] = "MAGE GHOST"
            monster["archetype"] = "SPECTRAL"
            monster["hp"] = 85
            combat_log = "PHANTOM IMMUNITY! Cahara's steel blade passes through ghostly mist! 0 DMG dealt! Need ENKI Occult Magic!"
        elif idx == 2:
            active_hero_idx = 2
            monster["hp"] = 35
            combat_log = "VANGUARD DEPLOYED! Enki casts BLACK ORB! 50 True Magic DMG tears the phantom spirit apart!"
        elif idx == 3:
            active_hero_idx = 1
            monster["name"] = "DARK CONSTRUCT"
            monster["archetype"] = "ARMORED"
            monster["hp"] = 55
            monster["def"] = 14
            combat_log = "VANGUARD DEPLOYED! D'arce casts HOLY SMITE! 42 DMG fractures heavy steel plate! Armor shattered!"
        elif idx == 4:
            active_hero_idx = 3
            monster["name"] = "ABYSSAL HORROR"
            monster["archetype"] = "TERROR"
            for m in squad:
                m["mind"] = min(m["max_mind"], m["mind"] + 35)
            combat_log = "VANGUARD DEPLOYED! The Girl's Innocent Aura repels dread! Loving Embrace restores +35 Mind to all!"
        elif idx == 5:
            squad[1]["toxicity"] = 100
            squad[1]["hp"] = 80
            squad[0]["toxicity"] = 25
            active_hero_idx = 0
            combat_log = "TOXICITY ACTIVE! D'arce at 100% (INTOXICATED) moved to bench. Resting purges -25% toxicity/turn!"

        render_screen()
        print(f"\n  \033[1;32m>>> [SHOWCASE]: {step_desc} <<<\033[0m")
        time.sleep(1.0)

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--showcase":
        run_showcase_trace()
    else:
        run_interactive_loop()
