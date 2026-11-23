#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
================================================================================
FEAR & HUNGER: TERMINAL LABYRINTH - TACTICAL ARENA (BALANCED HERO ROSTER)
================================================================================
Features:
1. Onboarding & Expedition Draft Guide:
   - 8 Explorers with hybrid damage profiles (Physical & Magic on every hero).
   - Any 4-hero squad combination is mathematically guaranteed softlock-proof!
   - Deep asymmetrical metabolic & survival passives for all 8 heroes.
2. Pokémon-Style Diagonal Combat Arena (Exact 100 Columns width).
3. Tri-State Postural Morphology (Zero blood/gore, clean amber/ash joints).
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
        os.system('mode con: cols=104 lines=54 >nul 2>&1')
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

def fit_ansi(s, max_len):
    """Safely clamps and pads string with ANSI escape codes to exact visible length."""
    cur_w = display_width(s)
    if cur_w == max_len:
        return s
    if cur_w < max_len:
        return s + ' ' * (max_len - cur_w)
    # Truncate safely without cutting ANSI escape sequences
    vis_len = 0
    res = []
    idx = 0
    ansi_prefix = re.compile(r'^\x1b\[[0-9;]*[mGKH]')
    while idx < len(s):
        m = ansi_prefix.match(s[idx:])
        if m:
            res.append(m.group(0))
            idx += m.end()
        else:
            c = s[idx]
            w = char_width(c)
            if vis_len + w > max_len:
                break
            res.append(c)
            vis_len += w
            idx += 1
    padded = ''.join(res) + '\033[0m'
    actual_w = display_width(padded)
    if actual_w < max_len:
        padded += ' ' * (max_len - actual_w)
    return padded

def pad_str(s, n):
    return fit_ansi(s, n)

def make_card_row(content, c_card):
    return f"{c_card}| {fit_ansi(content, 50)} {c_card}|"

def make_bar(curr, max_v, bar_len=16, color_code="32"):
    if max_v <= 0:
        ratio = 0
    else:
        ratio = max(0.0, min(1.0, curr / float(max_v)))
    filled = int(ratio * bar_len)
    empty = bar_len - filled
    return f"\033[{color_code}m" + "█" * filled + "\033[90m" + "░" * empty + "\033[0m"

# =============================================================================
# SPRITE RESOURCES (LOAD EXTRACTED 24-BIT ANSI OR USE EMBEDDED FALLBACK)
# =============================================================================
HERO_SPRITES = {}
RAW_MONSTER_8 = []
try:
    sprite_json_path = os.path.join(os.path.dirname(__file__), "extracted_sprites.json")
    if os.path.exists(sprite_json_path):
        with open(sprite_json_path, "r", encoding="utf-8") as f:
            sp_data = json.load(f)
            HERO_SPRITES = sp_data.get("heroes", {})
            RAW_MONSTER_8 = sp_data.get("monster_8", [])
except Exception:
    pass

FALLBACK_SPRITES = {
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
    "RAGNVALDR": [
        "         ▄▀▀▀▀▀▀▀▄           ",
        "        ▀▀▀▀▀▀▀▀▀▀▀          ",
        "       ▄▀▀▀▀▀▀▀▀▀▀▀▄         ",
        "       ▀▀▀▀▀▀▀▀▀▀▀▀▀   ▄█▄   ",
        "      ▄▀▀▀▀▀▀▀▀▀▀▀▀▀▄  ███   ",
        "     ▄▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▄ ███   ",
        "     ▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀ ███   ",
        "     ▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▄ █    ",
        "      ▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀       ",
        "      ▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀        ",
        "       ▀▀▀▀▀   ▀▀▀▀▀         ",
        "       ▀▀▀▀     ▀▀▀▀         "
    ],
    "LE'GARDE": [
        "        ▄▀▀▀▀▀▀▀▄            ",
        "       ▀▀▀▀▀▀▀▀▀▀▀           ",
        "       ▀▀▀▀▀▀▀▀▀▀▀           ",
        "       ▀▀▀▀▀▀▀▀▀▀▀           ",
        "     ▄▀▀▀▀▀▀▀▀▀▀▀▀▀▄         ",
        "     ▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀  ▄█▀    ",
        "     ▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀ ▄█▀     ",
        "     ▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀█▀      ",
        "      ▀▀▀▀▀▀▀▀▀▀▀▀▀▀         ",
        "      ▀▀▀▀▀▀▀▀▀▀▀▀▀▀         ",
        "       ▀▀▀▀    ▀▀▀▀          ",
        "       ▀▀▀      ▀▀▀          "
    ],
    "MOONLESS": [
        "                             ",
        "                             ",
        "         ▄▀▄   ▄▀▄           ",
        "        ▀▀▀▀▀▀▀▀▀▀▀          ",
        "       ▀▀▀▀▀▀▀▀▀▀▀▀▀         ",
        "      ▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀        ",
        "     ▄▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▄       ",
        "     ▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀       ",
        "     ▀▀ ▀▀▀▀▀▀▀▀▀▀▀ ▀▀       ",
        "     ▀   ▀▀▀▀▀▀▀▀▀   ▀       ",
        "         ▀▀▀   ▀▀▀           ",
        "                             "
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
    ],
    "NAS'HRAH": [
        "                             ",
        "        ▄▀▀▀▀▀▀▀▄            ",
        "       ▀▀▀▀▀▀▀▀▀▀▀           ",
        "      ▀▀ ▀▀▀▀▀▀▀ ▀▀   (FLAME)",
        "      ▀▀ █ ▀▀▀ █ ▀▀  \033[1;31m(🔥🔥)\033[0m ",
        "      ▀▀▀▀▀▀▀▀▀▀▀▀▀          ",
        "       ▀▀▀▀▀▀▀▀▀▀▀           ",
        "        ▀▀ ▀▀▀ ▀▀            ",
        "         ▀  ▀  ▀             ",
        "         (HOVER)             ",
        "                             ",
        "                             "
    ]
}

for k, v in FALLBACK_SPRITES.items():
    if k not in HERO_SPRITES or not HERO_SPRITES[k]:
        HERO_SPRITES[k] = v

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
# MASTER 8-HERO DATABASE (HYBRID DAMAGE PROFILES & ASYMMETRICAL METABOLISM)
# =============================================================================
ALL_HEROES = [
    {
        "id": 1,
        "name": "CAHARA",
        "role": "Mercenary",
        "title": "Swift Rogue",
        "hp": 115, "max_hp": 115,
        "mind": 90, "max_mind": 100,
        "hunger": 20, "max_hunger": 100,
        "atk": 32, "def": 18,
        "toxicity": 0, "max_toxicity": 100,
        "bench_detox": 50, "frontline_detox": 0,
        "herb_poppy_tox": 35, "herb_weed_tox": 50,
        "bread_hunger": 40,
        "dmg_profile": "Phys / Occult",
        "phys_score": 4, "magic_score": 2,
        "dodge_rate": 0.20,
        "passive": "Swift Detox (-50%/rest), +20% Dodge",
        "metabolic_desc": "Swift metabolism purges -50% Tox on bench. +20% Dodge. 100% flee.",
        "skills": [
            {"label": "TWIN DAGGERS", "desc": "-> Rapid dual slice: 2x 18 Physical DMG"},
            {"label": "POISON DART",  "desc": "-> Occult Chem: 25 Magic DMG (pierces DEF, poisons)"},
            {"label": "STEAL ITEM",   "desc": "-> Pickpocket foe: steal 1 Poppy/Bread from target"},
            {"label": "SMOKE BOMB",   "desc": "-> Blind opponent: 100% flee battle immediately"}
        ]
    },
    {
        "id": 2,
        "name": "D'ARCE",
        "role": "Paladin",
        "title": "Holy Knight",
        "hp": 150, "max_hp": 150,
        "mind": 85, "max_mind": 100,
        "hunger": 35, "max_hunger": 100,
        "atk": 28, "def": 32,
        "toxicity": 0, "max_toxicity": 100,
        "bench_detox": 25, "frontline_detox": 0,
        "herb_poppy_tox": 35, "herb_weed_tox": 45,
        "bread_hunger": 40,
        "dmg_profile": "Phys / Smite",
        "phys_score": 3, "magic_score": 3,
        "dodge_rate": 0.05,
        "passive": "Iron Will (-25% DMG), 0% Tox Prayer",
        "metabolic_desc": "Takes -25% Phys DMG. Holy Prayer heals with 0% Tox. Weed gives +45% Tox.",
        "skills": [
            {"label": "DEFENSE STANCE", "desc": "-> Brace shield: block 75% dmg & restore 15 HP"},
            {"label": "HEALING PRAYER", "desc": "-> Spend 15 Mind: restore +45 HP with 0% TOXICITY!"},
            {"label": "HOLY SMITE",     "desc": "-> Holy Magic strike: 42 DMG, breaks Armored DEF"},
            {"label": "KNIGHT CHARGE",  "desc": "-> Heavy shield bash: 34 Phys DMG & disrupts foe"}
        ]
    },
    {
        "id": 3,
        "name": "ENKI",
        "role": "Occultist",
        "title": "Dark Priest",
        "hp": 85, "max_hp": 85,
        "mind": 130, "max_mind": 130,
        "hunger": 15, "max_hunger": 100,
        "atk": 48, "def": 16,
        "toxicity": 0, "max_toxicity": 100,
        "bench_detox": 25, "frontline_detox": 0,
        "herb_poppy_tox": 45, "herb_weed_tox": 50,
        "bread_hunger": 40,
        "dmg_profile": "Magic / Dagger",
        "phys_score": 2, "magic_score": 5,
        "dodge_rate": 0.10,
        "passive": "Occult Mind (+5 MND/t), Frail Body",
        "metabolic_desc": "Regenerates +5 Mind/turn. Black Orb ignores defense. Weed gives +50% Tox.",
        "skills": [
            {"label": "BLACK ORB",       "desc": "-> Spend 15 Mind: 50 True Magic DMG (ignores 100% DEF)"},
            {"label": "RITUAL DAGGER",   "desc": "-> Sacrificial thrust: 24 Phys DMG, siphons +10 Mind"},
            {"label": "BLOOD SACRIFICE", "desc": "-> Convert 20 HP into +35 Mind points"},
            {"label": "HEXEN BIND",      "desc": "-> Spend 10 Mind: paralyze foe, guaranteed head hit"}
        ]
    },
    {
        "id": 4,
        "name": "RAGNVALDR",
        "role": "Barbarian",
        "title": "Outlander Berserker",
        "hp": 155, "max_hp": 155,
        "mind": 70, "max_mind": 100,
        "hunger": 45, "max_hunger": 100,
        "atk": 38, "def": 22,
        "toxicity": 0, "max_toxicity": 150, # Beast Gut: 150% max toxicity!
        "bench_detox": 25, "frontline_detox": 0,
        "herb_poppy_tox": 15, "herb_weed_tox": 25, # High poison resistance!
        "bread_hunger": 20, # Outlander needs meat; bread only satisfies 20 hunger!
        "dmg_profile": "Phys / Totem",
        "phys_score": 5, "magic_score": 2,
        "dodge_rate": 0.05,
        "passive": "Beast Gut (Tox 150%), Bloodlust +50%",
        "metabolic_desc": "Max Tox 150%, herbs +15%/+25% Tox. +50% ATK when <35% HP. Bread heals 20 Hng.",
        "skills": [
            {"label": "WAR AXE",      "desc": "-> Brutal cleave: 44 heavy Physical DMG"},
            {"label": "SPIRIT TOTEM", "desc": "-> Ancestral Spirit Magic: 10 Mind -> 30 Spirit Magic DMG"},
            {"label": "FERAL ROAR",   "desc": "-> Terrifying war cry: lowers foe ATK by 40%"},
            {"label": "DEVOUR FLESH", "desc": "-> Consume raw beast meat: restore +30 HP, -25 Hunger"}
        ]
    },
    {
        "id": 5,
        "name": "LE'GARDE",
        "role": "Commander",
        "title": "Tactician Leader",
        "hp": 130, "max_hp": 130,
        "mind": 100, "max_mind": 100,
        "hunger": 25, "max_hunger": 100,
        "atk": 30, "def": 20,
        "toxicity": 0, "max_toxicity": 100,
        "bench_detox": 25, "frontline_detox": 0,
        "herb_poppy_tox": 35, "herb_weed_tox": 50,
        "bread_hunger": 40,
        "dmg_profile": "Phys / Solar",
        "phys_score": 4, "magic_score": 3,
        "dodge_rate": 0.15,
        "passive": "Charisma (+15% ATK, Squad +10 Mind)",
        "metabolic_desc": "All allies +15% ATK in combat. +10 Mind to squad on victory. Pride: -20 MND if down.",
        "skills": [
            {"label": "FENCING THRUST",   "desc": "-> Precision rapier thrust: 36 piercing Phys DMG"},
            {"label": "LEGION LIGHT",     "desc": "-> Solar Magic: 15 Mind -> 35 Magic DMG + lowers enemy ACC"},
            {"label": "TACTICAL COMMAND", "desc": "-> Directs squad: Vanguard's next attack deals +50% DMG"},
            {"label": "WAR CRY",          "desc": "-> Inspires squad: +15 Mind, clears fear/doubt"}
        ]
    },
    {
        "id": 6,
        "name": "MOONLESS",
        "role": "Direhound",
        "title": "Ancient Shadow Wolf",
        "hp": 115, "max_hp": 115,
        "mind": 80, "max_mind": 100,
        "hunger": 50, "max_hunger": 100,
        "atk": 34, "def": 18,
        "toxicity": 0, "max_toxicity": 100,
        "bench_detox": 25, "frontline_detox": 0,
        "herb_poppy_tox": 0, "herb_weed_tox": 0, # Feral gut: 0% toxicity from herbs!
        "bread_hunger": 40,
        "alcohol_immune": True, # Cannot drink alcohol!
        "dmg_profile": "Phys / Howl",
        "phys_score": 4, "magic_score": 2,
        "dodge_rate": 0.25,
        "passive": "Feral Gut (0% Herb Tox), Swift Bite",
        "metabolic_desc": "0% Toxicity from herbs! Canine metabolism. Cannot drink Ale. High hunger.",
        "skills": [
            {"label": "FERAL BITE",    "desc": "-> Vicious jaw crunch: 38 Phys DMG + Bleeding"},
            {"label": "MOON HOWL",     "desc": "-> Lunar Magic: 28 Magic DMG + 40% chance to stun foe"},
            {"label": "SHADOW POUNCE", "desc": "-> Leap attack: 32 DMG, 100% knockdown on crouched foe"},
            {"label": "SCENT DANGER",  "desc": "-> Warns party: +35% squad dodge rate next turn"}
        ]
    },
    {
        "id": 7,
        "name": "THE GIRL",
        "role": "Ward",
        "title": "Innocent Vessel",
        "hp": 95, "max_hp": 95,
        "mind": 100, "max_mind": 100,
        "hunger": 10, "max_hunger": 100,
        "atk": 20, "def": 36,
        "toxicity": 0, "max_toxicity": 100,
        "bench_detox": 25, "frontline_detox": 10, # Purges -10% tox/turn while active frontline!
        "herb_poppy_tox": 35, "herb_weed_tox": 50,
        "bread_hunger": 40,
        "dread_immune": True, # Dread immune!
        "dmg_profile": "Light / Support",
        "phys_score": 1, "magic_score": 4,
        "dodge_rate": 0.30,
        "passive": "Pure Serenity (-10% Tox/t), Dread-Imm",
        "metabolic_desc": "Immune to Dread. Auto purges -10% Tox/turn even while active frontline!",
        "skills": [
            {"label": "NIMBLE DODGE",   "desc": "-> Duck into shadows: 100% dodge enemy's next hit"},
            {"label": "LOVING EMBRACE", "desc": "-> Comfort party: restore +35 Mind & calm nerves"},
            {"label": "PURE LIGHT",     "desc": "-> Holy Radiance: 10 Mind -> 28 Magic DMG vs darkness"},
            {"label": "DISTRACT FOE",   "desc": "-> Wave lantern: reduce enemy attack power by 50%"}
        ]
    },
    {
        "id": 8,
        "name": "NAS'HRAH",
        "role": "Doom Mage",
        "title": "Immortal Severed Head",
        "hp": 90, "max_hp": 90,
        "mind": 150, "max_mind": 150,
        "hunger": 0, "max_hunger": 100,
        "atk": 52, "def": 14,
        "toxicity": 0, "max_toxicity": 100,
        "bench_detox": 25, "frontline_detox": 0,
        "herb_immune": True, # Cannot consume mortal herbs!
        "hunger_immune": True, # Cannot starve!
        "dread_immune": True, # Ancient arch-mage fears nothing!
        "dmg_profile": "Magic / Bite",
        "phys_score": 2, "magic_score": 5,
        "dodge_rate": 0.15,
        "passive": "Undead Relic (0 Hunger, 0% Tox, Fire)",
        "metabolic_desc": "0 Hunger (cannot starve). 0% Herb Tox. Burns everything. Refuses to guard.",
        "skills": [
            {"label": "COMBUSTION",      "desc": "-> 20 Mind: 55 Unstoppable Fire Magic DMG to foe"},
            {"label": "CURSE OF DECAY",  "desc": "-> 15 Mind: 30 Dark Magic DMG + inflicts continuous decay"},
            {"label": "HEAD GNAW",       "desc": "-> Flying tooth strike: 24 Phys DMG, siphons +15 HP"},
            {"label": "MOCK FOE",        "desc": "-> Insults foe: strips 50% enemy DEF (foe attacks right now)"}
        ]
    }
]

# Preset squad definitions
PRESET_SQUADS = {
    1: [0, 1, 2, 6], # Cahara, D'arce, Enki, The Girl (Balanced Vanguard)
    2: [3, 2, 5, 7], # Ragnvaldr, Enki, Moonless, Nas'hrah (Berserker Occult)
    3: [4, 1, 0, 6]  # Le'garde, D'arce, Cahara, The Girl (Royal Legion)
}

import copy
def create_squad_from_indices(indices):
    sq = []
    for idx in indices:
        h = copy.deepcopy(ALL_HEROES[idx])
        h["buff"] = ""
        h["is_guarding"] = False
        h["debuffs"] = []
        sq.append(h)
    return sq

squad = create_squad_from_indices(PRESET_SQUADS[1])
active_hero_idx = 0

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
# EVALUATE SQUAD BALANCE (GUARANTEED SOFTLOCK-PROOF)
# =============================================================================
def evaluate_squad_balance(squad_list):
    total_phys = sum(h.get("phys_score", 3) for h in squad_list)
    total_magic = sum(h.get("magic_score", 3) for h in squad_list)
    phys_stars = "★" * min(5, max(1, total_phys // 3)) + "☆" * (5 - min(5, max(1, total_phys // 3)))
    magic_stars = "★" * min(5, max(1, total_magic // 3)) + "☆" * (5 - min(5, max(1, total_magic // 3)))
    has_phys = total_phys >= 4
    has_magic = total_magic >= 4
    if has_phys and has_magic:
        status = "\033[1;32m[BALANCED: ALL ARCHETYPES COVERED - SOFTLOCK PROOF GUARANTEED!]\033[0m"
    elif not has_magic:
        status = "\033[1;31m[WARNING: LOW MAGIC - VULNERABLE TO SPECTRAL GHOSTS]\033[0m"
    else:
        status = "\033[1;31m[WARNING: LOW PHYSICAL - VULNERABLE TO ARMORED TITANS]\033[0m"
    return total_phys, total_magic, phys_stars, magic_stars, status

# =============================================================================
# ONBOARDING & EXPEDITION DRAFT SCREEN (EXACT 100 COLUMNS)
# =============================================================================
def render_draft_guide(selected_indices, custom_msg=""):
    sys.stdout.write("\033[2J\033[H")
    print("\033[1;30m+====================================================================================================+\033[0m")
    title_str = "FEAR & HUNGER: EXPEDITION DRAFT & CHARACTER ONBOARDING GUIDE"
    pad_left = (96 - len(title_str)) // 2
    pad_right = 96 - len(title_str) - pad_left
    print(f"\033[1;30m| \033[1;37m{' ' * pad_left}{title_str}{' ' * pad_right}\033[1;30m |\033[0m")
    print("\033[1;30m+====================================================================================================+\033[0m")
    print("\033[1;30m| \033[1;33mID | NAME      | ROLE      | HP/ATK/DEF  | DAMAGE TYPE    | METABOLIC PASSIVE                    \033[1;30m|\033[0m")
    print("\033[1;30m+----------------------------------------------------------------------------------------------------+\033[0m")

    for h in ALL_HEROES:
        is_in_squad = (h["id"] - 1) in selected_indices
        c_tag = "\033[1;32m" if is_in_squad else "\033[90m"
        star_mark = "▶" if is_in_squad else " "
        stats_str = f"{h['hp']:3d}/{h['atk']:2d}/{h['def']:2d}"
        line = f"{star_mark}#{h['id']} | {h['name']:<9} | {h['role']:<9} | {stats_str:<11} | {h['dmg_profile']:<14} | {h['passive']:<36}"
        print(f"\033[1;30m| \033[0m{c_tag}{fit_ansi(line, 96)}\033[1;30m |\033[0m")

    print("\033[1;30m+----------------------------------------------------------------------------------------------------+\033[0m")
    preset_line = "\033[1;33m[PRESETS]:\033[0m \033[1;37m[1]\033[0m Balanced Vanguard  |  \033[1;37m[2]\033[0m Berserker Occult  |  \033[1;37m[3]\033[0m Royal Legion"
    print(f"\033[1;30m| \033[0m{fit_ansi(preset_line, 96)}\033[1;30m |\033[0m")
    custom_line = "           \033[1;37m[C]\033[0m Custom Squad Selection (Enter 4 Hero IDs: 1 to 8)"
    print(f"\033[1;30m| \033[0m{fit_ansi(custom_line, 96)}\033[1;30m |\033[0m")
    print("\033[1;30m+----------------------------------------------------------------------------------------------------+\033[0m")

    temp_squad = [ALL_HEROES[i] for i in selected_indices]
    names_str = ", ".join(f"#{h['id']} {h['name']}" for h in temp_squad)
    sq_line = f"\033[1;36m[CURRENT SQUAD]:\033[0m \033[1;37m{names_str}\033[0m"
    print(f"\033[1;30m| \033[0m{fit_ansi(sq_line, 96)}\033[1;30m |\033[0m")

    tot_p, tot_m, p_stars, m_stars, status_desc = evaluate_squad_balance(temp_squad)
    ratings_line = f"\033[1;35m[RATINGS]:\033[0m PHYSICAL: {p_stars} ({tot_p}/20)  |  MAGIC: {m_stars} ({tot_m}/20)"
    print(f"\033[1;30m| \033[0m{fit_ansi(ratings_line, 96)}\033[1;30m |\033[0m")

    status_line = f"\033[1;33m[BALANCE CHECK]:\033[0m {status_desc}"
    print(f"\033[1;30m| \033[0m{fit_ansi(status_line, 96)}\033[1;30m |\033[0m")

    if custom_msg:
        c_msg_line = f"\033[1;31m[PROMPT]:\033[0m \033[1;37m{custom_msg}\033[0m"
        print(f"\033[1;30m| \033[0m{fit_ansi(c_msg_line, 96)}\033[1;30m |\033[0m")
    else:
        empty_l = ""
        print(f"\033[1;30m| \033[0m{fit_ansi(empty_l, 96)}\033[1;30m |\033[0m")

    print("\033[1;30m+====================================================================================================+\033[0m")
    print("  \033[90m[CONTROLS]:\033[0m \033[1;37m[1/2/3]\033[0m Select Preset  |  \033[1;37m[C]\033[0m Custom Draft  |  \033[1;32m[Enter/Space]\033[0m Deploy Squad  |  \033[1;31m[Q]\033[0m Quit")
    print("\033[1;30m====================================================================================================\033[0m")
    sys.stdout.flush()

def run_draft_interactive():
    global squad, active_hero_idx
    selected_indices = list(PRESET_SQUADS[1])

    while True:
        render_draft_guide(selected_indices)
        if os.name == 'nt':
            ch = msvcrt.getch()
            if ch in (b'1', b'2', b'3'):
                p_num = int(ch.decode('ascii'))
                selected_indices = list(PRESET_SQUADS[p_num])
            elif ch in (b'c', b'C'):
                sys.stdout.write("\n  \033[1;33mEnter 4 Hero IDs separated by space (e.g. 1 4 6 8):\033[0m ")
                sys.stdout.flush()
                try:
                    line = input().strip()
                    nums = [int(x) - 1 for x in re.findall(r'\d+', line)]
                    if len(nums) == 4 and all(0 <= x < len(ALL_HEROES) for x in nums) and len(set(nums)) == 4:
                        selected_indices = nums
                    else:
                        print("  \033[1;31mInvalid selection! Must enter 4 unique numbers from 1 to 8.\033[0m")
                        time.sleep(1.2)
                except Exception:
                    pass
            elif ch in (b'\r', b'\n', b' '):
                # Confirm and deploy squad!
                squad = create_squad_from_indices(selected_indices)
                active_hero_idx = 0
                break
            elif ch in (b'q', b'Q', b'\x03'):
                print("\n[OK] Exited Squad Draft.")
                sys.exit(0)
        else:
            line = sys.stdin.readline().strip().lower()
            if line in ('1', '2', '3'):
                selected_indices = list(PRESET_SQUADS[int(line)])
            elif line.startswith('c'):
                sys.stdout.write("Enter 4 IDs: ")
                sys.stdout.flush()
                l_nums = [int(x) - 1 for x in re.findall(r'\d+', sys.stdin.readline())]
                if len(l_nums) == 4:
                    selected_indices = l_nums
            elif line in ('', 'enter'):
                squad = create_squad_from_indices(selected_indices)
                active_hero_idx = 0
                break
            elif line in ('q', 'quit'):
                sys.exit(0)

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
    max_t = hero.get("max_toxicity", 100)
    h_tox_bar = make_bar(h_tox, max_t, 12, "31" if h_tox >= max_t else ("33" if h_tox >= (max_t * 0.8) else "32"))
    tox_badge = "\033[1;31m[INTOXICATED]\033[0m" if h_tox >= max_t else ("\033[1;33m[HIGH]\033[0m" if h_tox >= (max_t * 0.8) else "\033[90m[SAFE]\033[0m")

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
        make_card_row(f"  TOXIC : {h_tox_bar} \033[1;{'31' if h_tox >= max_t else '32'}m{h_tox:3d}%\033[0m {tox_badge}", c_hcard),
        make_card_row("", c_hcard),
        make_card_row(f"\033[1;33m  PASSIV: {hero['passive']}\033[0m", c_hcard),
        make_card_row(status_line, c_hcard),
        h_border
    ]

    for r_idx in range(14):
        print(f"{h_model_rows[r_idx]}    {h_card_rows[r_idx]}\033[0m")

    print()

    # -------------------------------------------------------------------------
    # SECTION 3: COMBAT LOG BOX (EXACT 100 COLUMNS, 2-ROW WRAP TO PREVENT TRUNCATION)
    # -------------------------------------------------------------------------
    print("\033[1;30m+----------------------------------------------------------------------------------------------------+\033[0m")
    import textwrap
    wrapped = textwrap.wrap(combat_log, width=88)
    if not wrapped:
        wrapped = [""]

    line1 = f"\033[1;33m[LOG]\033[0m \033[1;37m{wrapped[0]}\033[0m"
    print(f"\033[1;30m| \033[0m{fit_ansi(line1, 96)}\033[1;30m |\033[0m")

    if len(wrapped) > 1:
        line2 = f"      \033[1;37m{' '.join(wrapped[1:])}\033[0m"
        print(f"\033[1;30m| \033[0m{fit_ansi(line2, 96)}\033[1;30m |\033[0m")
    else:
        line2 = ""
        print(f"\033[1;30m| \033[0m{fit_ansi(line2, 96)}\033[1;30m |\033[0m")

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
            max_t = comp.get("max_toxicity", 100)
            if tox_val >= max_t:
                tox_str = "\033[1;31mTOX:MAX!\033[0m"
            elif tox_val >= (max_t * 0.5):
                tox_str = f"\033[1;33mTOX:{tox_val:2d}%\033[0m"
            else:
                tox_str = f"\033[90mTOX:{tox_val:2d}%\033[0m"
            opts.append({
                "label": f"{comp['name']:<9} [{comp['role']:<9}]",
                "desc": f"HP:{comp['hp']:3d}/{comp['max_hp']:3d} MND:{comp['mind']:3d} {tox_str} | {comp['passive']}{status_tag}{tag}"
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
        h_skills = h.get("skills", [])
        opts = []
        for sk in h_skills:
            opts.append({"label": sk["label"], "desc": sk["desc"]})
        opts.append({"label": "BACK", "desc": "-> Return to main commands"})
        return {
            "title": f"SKILLS & ABILITIES ({h['name']} - {h['role']})",
            "options": opts
        }
    elif current_menu == "POUCH":
        return {
            "title": "ITEM POUCH & SURVIVAL SUPPLIES",
            "options": [
                {"label": f"WHITE POPPY [{inventory['poppy']}]", "desc": "-> Flower bud | Restore +50 HP & cure bleeding"},
                {"label": f"HERBAL WEED [{inventory['weed']}]",  "desc": "-> Healing herb | Restore +120 HP"},
                {"label": f"MOLDY BREAD [{inventory['bread']}]", "desc": "-> Dungeon rations | Reduce Hunger"},
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
            if hero["name"] == "NAS'HRAH":
                combat_log = "NAS'HRAH REFUSES TO GUARD! 'I am a god, I bow to no worm!'"
            else:
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
            combat_log = f"PHANTOM IMMUNITY! {hero['name']}'s blade passes harmlessly through spectral form! (0 DMG - Need Magic Attack!)"
            enemy_turn()
            current_menu = "MAIN"
            cursor_idx = 0
        elif arch == "ARMORED" and cursor_idx != 5:
            dmg = 2
            monster["hp"] = max(0, monster["hp"] - dmg)
            combat_log = f"ARMOR DEFLECTION! {hero['name']}'s blade clangs off steel plate for only {dmg} DMG! (Need Smite or Magic!)"
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
        num_skills = len(h.get("skills", []))

        if cursor_idx == num_skills: # Back
            current_menu = "MAIN"
            cursor_idx = 0
            return

        # Execute hero-specific skill
        if h["name"] == "CAHARA":
            if cursor_idx == 0:    # Twin Daggers
                dmg = 36
                monster["hp"] = max(0, monster["hp"] - dmg)
                combat_log = f"TWIN DAGGERS! Cahara strikes twice with rapid thrusts for {dmg} DMG!"
                enemy_turn()
            elif cursor_idx == 1:  # Poison Dart
                dmg = 25
                monster["hp"] = max(0, monster["hp"] - dmg)
                if monster.get("archetype") == "ARMORED":
                    combat_log = f"POISON DART! Occult toxic dart slips through armor seams for {dmg} Chem Magic DMG!"
                elif monster.get("archetype") == "SPECTRAL":
                    combat_log = f"OCCULT CHEM! Ghost dissipates from toxic alchemy for {dmg} Magic DMG!"
                else:
                    combat_log = f"POISON DART! Venomous needle hits for {dmg} Magic DMG!"
                enemy_turn()
            elif cursor_idx == 2:  # Steal Item
                stolen_item = "poppy" if random.random() < 0.5 else "bread"
                inventory[stolen_item] += 1
                combat_log = f"STEAL SUCCESS! Cahara pickpockets the foe and secures 1x {stolen_item.upper()}!"
                enemy_turn()
            elif cursor_idx == 3:  # Smoke Bomb
                combat_log = "SMOKE BOMB! Dense fog blinds opponent. 100% ESCAPE SUCCESSFUL!"
                time.sleep(1.2)
                sys.exit(0)

        elif h["name"] == "D'ARCE":
            if cursor_idx == 0:    # Defense stance
                h["is_guarding"] = True
                h["hp"] = min(h["max_hp"], h["hp"] + 15)
                h["buff"] = "IRON VOW (-75% DMG)"
                combat_log = "DEFENSE STANCE! D'arce braces tower shield (+15 HP, -75% incoming DMG)!"
                enemy_turn()
            elif cursor_idx == 1:  # Healing prayer (0% toxicity!)
                if h["mind"] >= 15:
                    h["mind"] -= 15
                    h["hp"] = min(h["max_hp"], h["hp"] + 45)
                    combat_log = "HEALING PRAYER! Sacred divine light restores +45 HP with 0% TOXICITY!"
                    enemy_turn()
                else:
                    combat_log = "Insufficient Mind points for Healing Prayer!"
            elif cursor_idx == 2:  # Holy smite
                dmg = 42
                if monster.get("archetype") == "ARMORED":
                    monster["archetype"] = "NORMAL"
                    monster["def"] = 14
                    combat_log = f"ARMOR SHATTERED! D'arce's Holy Smite fractures heavy steel plate for {dmg} DMG! Foe DEF shattered!"
                elif monster.get("archetype") == "SPECTRAL":
                    combat_log = f"SACRED RADIANCE! Holy Smite incinerates spectral ghost for {dmg} Divine Magic DMG!"
                else:
                    combat_log = f"HOLY SMITE! Heavy sanctified cleave inflicts {dmg} DMG!"
                monster["hp"] = max(0, monster["hp"] - dmg)
                enemy_turn()
            elif cursor_idx == 3:  # Knight Charge
                dmg = 34
                monster["hp"] = max(0, monster["hp"] - dmg)
                combat_log = f"KNIGHT CHARGE! D'arce slams forward with tower shield for {dmg} Phys DMG!"
                enemy_turn()

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
            elif cursor_idx == 1:  # Ritual Dagger
                dmg = 24
                monster["hp"] = max(0, monster["hp"] - dmg)
                h["mind"] = min(h["max_mind"], h["mind"] + 10)
                combat_log = f"RITUAL DAGGER! Enki slices foe for {dmg} Phys DMG and siphons +10 Mind!"
                enemy_turn()
            elif cursor_idx == 2:  # Blood sacrifice
                if h["hp"] > 20:
                    h["hp"] -= 20
                    h["mind"] = min(h["max_mind"], h["mind"] + 35)
                    combat_log = "BLOOD SACRIFICE! Enki cuts own flesh (-20 HP) to harvest +35 Mind!"
                else:
                    combat_log = "HP too low for Blood Sacrifice!"
            elif cursor_idx == 3:  # Hexen bind
                if h["mind"] >= 10:
                    h["mind"] -= 10
                    monster["debuff_legs"] = True
                    combat_log = "HEXEN BIND! Occult shadows root the foe to floor (100% Head hit rate)!"
                    enemy_turn()
                else:
                    combat_log = "Insufficient Mind for Hexen Bind!"

        elif h["name"] == "RAGNVALDR":
            if cursor_idx == 0:    # War Axe
                dmg = 44
                if "BLOODLUST" in hero.get("buff", "") or hero["hp"] < (hero["max_hp"] * 0.35):
                    dmg = int(dmg * 1.5)
                monster["hp"] = max(0, monster["hp"] - dmg)
                combat_log = f"WAR AXE! Ragnvaldr buries heavy axe into foe for {dmg} brutal Physical DMG!"
                enemy_turn()
            elif cursor_idx == 1:  # Spirit Totem (Ancestral Magic)
                if h["mind"] >= 10:
                    h["mind"] -= 10
                    dmg = 30
                    monster["hp"] = max(0, monster["hp"] - dmg)
                    if monster.get("archetype") == "SPECTRAL":
                        combat_log = f"ANCESTRAL PURGE! Spirit Totem smashes ghost with spiritual energy for {dmg} Magic DMG!"
                    else:
                        combat_log = f"SPIRIT TOTEM! Northern ancestral spirits crush foe for {dmg} Spirit Magic DMG!"
                    enemy_turn()
                else:
                    combat_log = "Insufficient Mind points for Spirit Totem!"
            elif cursor_idx == 2:  # Feral Roar
                monster["atk"] = max(6, int(monster["atk"] * 0.6))
                combat_log = "FERAL ROAR! Barbarian roar intimidates foe (-40% enemy ATK power)!"
                enemy_turn()
            elif cursor_idx == 3:  # Devour Flesh
                h["hp"] = min(h["max_hp"], h["hp"] + 30)
                h["hunger"] = max(0, h["hunger"] - 25)
                combat_log = "DEVOUR FLESH! Ragnvaldr consumes raw meat (+30 HP, -25 Hunger)!"
                enemy_turn()

        elif h["name"] == "LE'GARDE":
            if cursor_idx == 0:    # Fencing Thrust
                dmg = 36
                monster["hp"] = max(0, monster["hp"] - dmg)
                combat_log = f"FENCING THRUST! Le'garde pierces weak point for {dmg} Phys DMG!"
                enemy_turn()
            elif cursor_idx == 1:  # Legion Light
                if h["mind"] >= 15:
                    h["mind"] -= 15
                    dmg = 35
                    monster["hp"] = max(0, monster["hp"] - dmg)
                    combat_log = f"LEGION LIGHT! Blinding solar ray burns foe for {dmg} Solar Magic DMG!"
                    enemy_turn()
                else:
                    combat_log = "Insufficient Mind for Legion Light!"
            elif cursor_idx == 2:  # Tactical Command
                h["buff"] = "TACTICAL FOCUS (+50% NEXT ATK)"
                combat_log = "TACTICAL COMMAND! Le'garde coordinates formation (+50% DMG on next strike)!"
                enemy_turn()
            elif cursor_idx == 3:  # War Cry
                for m in squad:
                    m["mind"] = min(m["max_mind"], m["mind"] + 15)
                combat_log = "WAR CRY! Le'garde inspires the squad (+15 Mind to all allies)!"
                enemy_turn()

        elif h["name"] == "MOONLESS":
            if cursor_idx == 0:    # Feral Bite
                dmg = 38
                monster["hp"] = max(0, monster["hp"] - dmg)
                combat_log = f"FERAL BITE! Moonless tears into flesh for {dmg} Phys DMG!"
                enemy_turn()
            elif cursor_idx == 1:  # Moon Howl
                dmg = 28
                monster["hp"] = max(0, monster["hp"] - dmg)
                if random.random() < 0.40:
                    monster["debuff_legs"] = True
                    combat_log = f"MOON HOWL! Eerie lunar howling deals {dmg} Magic DMG and paralyses foe (Crouched)!"
                else:
                    combat_log = f"MOON HOWL! Lunar psychic scream echoes through the dark for {dmg} Magic DMG!"
                enemy_turn()
            elif cursor_idx == 2:  # Shadow Pounce
                dmg = 32
                if monster["debuff_legs"]:
                    dmg = 50
                monster["hp"] = max(0, monster["hp"] - dmg)
                combat_log = f"SHADOW POUNCE! Moonless pounces from the gloom for {dmg} DMG!"
                enemy_turn()
            elif cursor_idx == 3:  # Scent Danger
                h["buff"] = "DANGER SCENT (+35% DODGE)"
                combat_log = "SCENT DANGER! Moonless sniffs danger in the air (+35% party evasion)!"
                enemy_turn()

        elif h["name"] == "THE GIRL":
            if cursor_idx == 0:    # Nimble dodge
                h["buff"] = "NIMBLE DODGE (100% EVADE)"
                combat_log = "NIMBLE DODGE! The Girl slips into shadows, guaranteeing 100% evasion!"
                enemy_turn()
            elif cursor_idx == 1:  # Loving embrace
                for m in squad:
                    m["mind"] = min(m["max_mind"], m["mind"] + 35)
                combat_log = "LOVING EMBRACE! Heartwarming comfort restores +35 Mind to ENTIRE SQUAD and dispels terror!"
                enemy_turn()
            elif cursor_idx == 2:  # Pure Light
                if h["mind"] >= 10:
                    h["mind"] -= 10
                    dmg = 28
                    monster["hp"] = max(0, monster["hp"] - dmg)
                    combat_log = f"PURE LIGHT! Holy glow illuminates darkness for {dmg} Sacred Light DMG!"
                    enemy_turn()
                else:
                    combat_log = "Insufficient Mind for Pure Light!"
            elif cursor_idx == 3:  # Distract foe
                monster["temp_debuff"] = "DISTRACTED (-50% ATK)"
                combat_log = "DISTRACT FOE! The Girl waves lantern: enemy's attack power halved by 50%!"
                enemy_turn()

        elif h["name"] == "NAS'HRAH":
            if cursor_idx == 0:    # Combustion
                if h["mind"] >= 20:
                    h["mind"] -= 20
                    dmg = 55
                    monster["hp"] = max(0, monster["hp"] - dmg)
                    combat_log = f"COMBUSTION! Gro-goroth flame erupts for {dmg} Unstoppable Fire Magic DMG!"
                    enemy_turn()
                else:
                    combat_log = "Insufficient Mind for Combustion!"
            elif cursor_idx == 1:  # Curse of Decay
                if h["mind"] >= 15:
                    h["mind"] -= 15
                    dmg = 30
                    monster["hp"] = max(0, monster["hp"] - dmg)
                    combat_log = f"CURSE OF DECAY! Ancient hex inflicts {dmg} Dark Magic DMG and rotting flesh!"
                    enemy_turn()
                else:
                    combat_log = "Insufficient Mind for Curse of Decay!"
            elif cursor_idx == 2:  # Head Gnaw
                dmg = 24
                monster["hp"] = max(0, monster["hp"] - dmg)
                h["hp"] = min(h["max_hp"], h["hp"] + 15)
                combat_log = f"HEAD GNAW! Nas'hrah bites into foe for {dmg} Phys DMG and absorbs +15 HP life!"
                enemy_turn()
            elif cursor_idx == 3:  # Mock Foe
                monster["def"] = max(0, monster["def"] // 2)
                combat_log = "MOCK FOE! Nas'hrah insults the foe (-50% enemy DEF, enemy enraged)!"
                enemy_turn()

        current_menu = "MAIN"
        cursor_idx = 0

    elif current_menu == "POUCH":
        max_t = hero.get("max_toxicity", 100)

        if cursor_idx == 0:    # Poppy
            if inventory["poppy"] > 0:
                inventory["poppy"] -= 1
                if hero.get("herb_immune", False):
                    combat_log = f"{hero['name']} SNEERS: 'I have no mortal stomach for your weeds!' (0 HP healed)."
                elif hero.get("toxicity", 0) >= max_t:
                    hero["hp"] = max(1, hero["hp"] - 5)
                    combat_log = f"INTOXICATED! {hero['name']}'s stomach rejects Poppy! Vomited (0 HP healed, -5 toxic DMG)!"
                else:
                    hero["hp"] = min(hero["max_hp"], hero["hp"] + 50)
                    added_tox = hero.get("herb_poppy_tox", 35)
                    hero["toxicity"] = min(max_t, hero.get("toxicity", 0) + added_tox)
                    if "Bleeding (-4 HP/turn)" in hero["debuffs"]:
                        hero["debuffs"].remove("Bleeding (-4 HP/turn)")
                    if hero["toxicity"] >= max_t:
                        combat_log = f"{hero['name']} consumes Poppy (+50 HP). TOXICITY AT {max_t}%! Hero is INTOXICATED!"
                    else:
                        tox_note = f"+{added_tox}% Tox" if added_tox > 0 else "0% Tox (Canine Gut)"
                        combat_log = f"{hero['name']} consumes Poppy (+50 HP, {tox_note} [{hero['toxicity']}%])."
                enemy_turn()
            else:
                combat_log = "Out of White Poppy!"
            current_menu = "MAIN"
            cursor_idx = 0

        elif cursor_idx == 1:  # Weed
            if inventory["weed"] > 0:
                inventory["weed"] -= 1
                if hero.get("herb_immune", False):
                    combat_log = f"{hero['name']} SNEERS: 'Mortal herbalism is beneath me!' (0 HP healed)."
                elif hero.get("toxicity", 0) >= max_t:
                    hero["hp"] = max(1, hero["hp"] - 5)
                    combat_log = f"INTOXICATED! {hero['name']} overdoses on Weed! Vomited (0 HP healed, -5 toxic DMG)!"
                else:
                    hero["hp"] = min(hero["max_hp"], hero["hp"] + 120)
                    added_tox = hero.get("herb_weed_tox", 50)
                    hero["toxicity"] = min(max_t, hero.get("toxicity", 0) + added_tox)
                    if hero["toxicity"] >= max_t:
                        combat_log = f"{hero['name']} uses Herbal Weed (+120 HP). TOXICITY AT {max_t}%! Hero is INTOXICATED!"
                    else:
                        tox_note = f"+{added_tox}% Tox" if added_tox > 0 else "0% Tox (Canine Gut)"
                        combat_log = f"{hero['name']} uses Herbal Weed (+120 HP, {tox_note} [{hero['toxicity']}%])."
                enemy_turn()
            else:
                combat_log = "Out of Herbal Weed!"
            current_menu = "MAIN"
            cursor_idx = 0

        elif cursor_idx == 2:  # Bread
            if inventory["bread"] > 0:
                inventory["bread"] -= 1
                if hero.get("hunger_immune", False):
                    combat_log = f"{hero['name']} requires no mortal bread! Hunger remains 0."
                else:
                    hunger_relief = hero.get("bread_hunger", 40)
                    hero["hunger"] = max(0, hero["hunger"] - hunger_relief)
                    if hunger_relief < 40:
                        combat_log = f"{hero['name']} eats Moldy Bread (-{hunger_relief} Hunger - Outlander gut needs raw meat!)."
                    else:
                        combat_log = f"{hero['name']} eats Moldy Bread (-{hunger_relief} Hunger)."
            else:
                combat_log = "Out of Bread!"
            current_menu = "MAIN"
            cursor_idx = 0

        elif cursor_idx == 3:  # Ale
            if inventory["ale"] > 0:
                inventory["ale"] -= 1
                if hero.get("alcohol_immune", False):
                    combat_log = "Moonless sniffs the vintage ale and growls! Beasts cannot drink alcohol!"
                elif hero["name"] == "NAS'HRAH":
                    hero["mind"] = min(hero["max_mind"], hero["mind"] + 35)
                    hero["hp"] = min(hero["max_hp"], hero["hp"] + 10)
                    hero["buff"] = "DARK ECSTASY (+35 Mind, +10 HP)"
                    combat_log = "Nas'hrah drains the ale in dark ecstasy! (+35 Mind, +10 HP dark vitality)!"
                else:
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
        # Le'garde Passive: +10 Mind to entire squad on victory!
        if any(m["name"] == "LE'GARDE" for m in squad):
            for m in squad:
                m["mind"] = min(m["max_mind"], m["mind"] + 10)
            combat_log += " | Le'garde's Charisma inspires squad (+10 Mind to all allies)!"
        return

    # 1. Bench detoxification: reserve heroes purge toxicity!
    purged_names = []
    for idx, comp in enumerate(squad):
        if idx != active_hero_idx and comp.get("toxicity", 0) > 0:
            detox_rate = comp.get("bench_detox", 25)
            comp["toxicity"] = max(0, comp["toxicity"] - detox_rate)
            if comp["toxicity"] == 0:
                purged_names.append(comp["name"])
    if purged_names:
        combat_log += f" | Bench rest: {', '.join(purged_names)} detoxified!"

    # 2. Frontline auto detoxification (The Girl passive: -10% tox/turn even active!)
    if hero.get("frontline_detox", 0) > 0 and hero.get("toxicity", 0) > 0:
        hero["toxicity"] = max(0, hero["toxicity"] - hero["frontline_detox"])
        combat_log += f" | Pure Serenity: {hero['name']} purges -{hero['frontline_detox']}% toxicity on frontline!"

    # 3. Active hero toxic nausea check
    max_t = hero.get("max_toxicity", 100)
    if hero.get("toxicity", 0) >= max_t:
        hero["hp"] = max(1, hero["hp"] - 5)
        combat_log += f" | {hero['name']} suffers intoxicated nausea (-5 HP)!"

    # 4. Terror Archetype Dread Aura check
    if monster.get("archetype") == "TERROR":
        if hero.get("dread_immune", False):
            combat_log += f" | {hero['name']} repels Dread Aura (0 Mind lost)!"
        else:
            hero["mind"] = max(0, hero["mind"] - 25)
            combat_log += f" | DREAD AURA! Eldritch horror drains -25 Mind from {hero['name']}!"

    # 5. Bleed effect
    if "Bleeding (-4 HP/turn)" in hero["debuffs"]:
        hero["hp"] = max(0, hero["hp"] - 4)

    # 6. Passive: Enki automatically regenerates +5 Mind per turn!
    if hero["name"] == "ENKI" and hero["mind"] < hero["max_mind"]:
        hero["mind"] = min(hero["max_mind"], hero["mind"] + 5)

    # 7. Check Dodge (Cahara 20%, The Girl 30%, Agile buff +35%, Nimble buff 100%)
    effective_dodge = hero.get("dodge_rate", 0.05)
    if "NIMBLE DODGE" in hero.get("buff", ""):
        hero["buff"] = ""
        combat_log += f" | {hero['name']} swiftly slips into shadows! Attack COMPLETELY EVADED!"
        return
    elif "AGILE DANCE" in hero.get("buff", ""):
        effective_dodge += 0.35
    elif "DANGER SCENT" in hero.get("buff", ""):
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
        # Le'garde Pride Downside
        if hero["name"] == "LE'GARDE":
            for m in squad:
                m["mind"] = max(0, m["mind"] - 20)
            combat_log += " | Commander fell! Squad panics (-20 Mind to all allies)!"

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
    print("\n>>> STARTING 8-HERO ONBOARDING & COMBAT ARENA SHOWCASE <<<\n")
    # Step 0: Render Draft Guide preview
    render_draft_guide(list(PRESET_SQUADS[1]), custom_msg="[SHOWCASE DEMO]: Presets 1-3 & Custom Draft Available")
    time.sleep(1.2)

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
    elif len(sys.argv) > 1 and sys.argv[1] == "--draft":
        run_draft_interactive()
        run_interactive_loop()
    else:
        # Default: First show draft selection, then start combat arena!
        run_draft_interactive()
        run_interactive_loop()
