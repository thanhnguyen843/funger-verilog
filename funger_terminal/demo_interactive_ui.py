#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
================================================================================
FEAR & HUNGER: TERMINAL LABYRINTH - SOLO EXPLORER COMBAT ARENA (V1.2)
================================================================================
Features:
1. Solo Explorer Mode (1 Playable Hero Run):
   - 8 Unique, Differentiated Heroes with Universal Damage & Distinct Affinities.
   - No 0 DMG immunities: every hero can damage all monsters with distinct affinities.
   - Deep asymmetrical attributes: Physical/Magic Resist %, Carry Capacity, Item Buffs.
2. Vertical Character Selector with Live 24-bit TrueColor/ANSI Model & Dossier:
   - Smooth W/S cursor navigation with real-time stats update (100 Columns exact).
3. Flicker-Free Terminal Rendering Engine:
   - Atomic Double-Buffered Blitting (\033[H + Frame Buffer) eliminating all strobing.
   - Console cursor suppression (\033[?25l) for silky smooth 60 FPS UX.
4. Tri-State Postural Morphology (Zero blood/gore, clean amber/ash joints).
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
# SPRITE RESOURCES (24-BIT TRUECOLOR ANSI OR EMBEDDED BLOCK FALLBACK)
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
# MASTER 8-HERO DATABASE (SOLO SURVIVORS: UNIVERSAL DAMAGE & ASYMMETRICAL AFFINITY)
# =============================================================================
ALL_HEROES = [
    {
        "id": 1,
        "name": "CAHARA",
        "role": "Mercenary Rogue",
        "hp": 120, "max_hp": 120,
        "mind": 95, "max_mind": 100,
        "hunger": 20, "max_hunger": 100,
        "atk": 32, "def": 18,
        "toxicity": 0, "max_toxicity": 100,
        "phys_resist_str": "Baseline (0%)",
        "magic_resist_str": "Baseline (0%)",
        "phys_mult": 1.0, "magic_mult": 1.0,
        "dodge_rate": 0.25,
        "trait": "Deep Pockets (2x Capacity)",
        "bag_cap": 10,
        "item_buff_str": "+25% Food & Herb Potency",
        "crit_rate": 0.35,
        "passive": "Deep Pockets (2x Bag), +25% Dodge",
        "skills": [
            {"label": "TWIN DAGGERS", "desc": "-> Rapid dual slice: 2x 18 Physical DMG"},
            {"label": "POISON DART",  "desc": "-> Occult Chem: 28 Magic DMG (bypasses DEF, poisons)"},
            {"label": "STEAL ITEM",   "desc": "-> Pickpocket foe: steal 1 Poppy/Bread from target"},
            {"label": "SMOKE BOMB",   "desc": "-> Blind opponent: 100% flee battle immediately"}
        ],
        "assessment": [
            "Extremely versatile survivor. Deep pockets allow carrying twice",
            "the supplies (up to 10 items). Poison darts pierce heavy armor,",
            "while 100% flee guarantee permits safe tactical retreats."
        ]
    },
    {
        "id": 2,
        "name": "D'ARCE",
        "role": "Holy Paladin",
        "hp": 155, "max_hp": 155,
        "mind": 85, "max_mind": 100,
        "hunger": 35, "max_hunger": 100,
        "atk": 30, "def": 34,
        "toxicity": 0, "max_toxicity": 100,
        "phys_resist_str": "+35% Armor (-35% Phys DMG)",
        "magic_resist_str": "-20% Vulnerable (Steel armor)",
        "phys_mult": 0.65, "magic_mult": 1.20,
        "dodge_rate": 0.05,
        "trait": "Iron Armor (-35% Phys DMG)",
        "bag_cap": 5,
        "item_buff_str": "Prayer heals with 0% Tox",
        "crit_rate": 0.15,
        "passive": "Iron Will (-35% DMG), 0% Tox Prayer",
        "skills": [
            {"label": "DEFENSE STANCE", "desc": "-> Guard blocks 75% dmg & restores +15 HP"},
            {"label": "HEALING PRAYER", "desc": "-> Spend 15 Mind: restore +45 HP with 0% TOXICITY!"},
            {"label": "HOLY SMITE",     "desc": "-> Holy Smite: 44 DMG (x1.4 vs Armored & Undead)"},
            {"label": "KNIGHT CHARGE",  "desc": "-> Heavy shield bash: 36 Phys DMG & disrupts foe"}
        ],
        "assessment": [
            "Supreme physical durability. Steel plate deflects 35% of blade",
            "blows. Holy Smite shatters armor and smites undead. Vulnerable",
            "to conductive magic and eldritch spells."
        ]
    },
    {
        "id": 3,
        "name": "ENKI",
        "role": "Dark Occultist",
        "hp": 90, "max_hp": 90,
        "mind": 130, "max_mind": 130,
        "hunger": 15, "max_hunger": 100,
        "atk": 48, "def": 14,
        "toxicity": 0, "max_toxicity": 100,
        "phys_resist_str": "-30% Frail (+30% Phys DMG)",
        "magic_resist_str": "+40% Warded (-40% Mag DMG)",
        "phys_mult": 1.30, "magic_mult": 0.60,
        "dodge_rate": 0.10,
        "trait": "Occult Mind (+5 Nrg/turn)",
        "bag_cap": 5,
        "item_buff_str": "Soul harvest from Herbs",
        "crit_rate": 0.20,
        "passive": "Occult Mind (+5 MND/t), Frail Body",
        "skills": [
            {"label": "BLACK ORB",       "desc": "-> 52 True Magic DMG (x1.5 vs Spectral/Armor, pierces DEF)"},
            {"label": "RITUAL DAGGER",   "desc": "-> Sacrificial thrust: 24 Phys DMG, siphons +15 Mind"},
            {"label": "BLOOD SACRIFICE", "desc": "-> Convert 20 HP into +40 Mind points"},
            {"label": "HEXEN BIND",      "desc": "-> Spend 10 Mind: paralyze foe, guaranteed head hit"}
        ],
        "assessment": [
            "Supreme arcane firepower. Black Orb demolishes spectral ghosts",
            "and bypasses heavy titan armor. High magic resistance protects",
            "against spells. Very frail against direct physical strikes."
        ]
    },
    {
        "id": 4,
        "name": "RAGNVALDR",
        "role": "Outlander Berserker",
        "hp": 170, "max_hp": 170,
        "mind": 70, "max_mind": 100,
        "hunger": 45, "max_hunger": 100,
        "atk": 42, "def": 22,
        "toxicity": 0, "max_toxicity": 150, # Beast gut: 150% max toxicity
        "phys_resist_str": "+15% Muscle (-15% Phys DMG)",
        "magic_resist_str": "-10% Primal (-10% Mag DEF)",
        "phys_mult": 0.85, "magic_mult": 1.10,
        "dodge_rate": 0.05,
        "trait": "Beast Gut (150% Tox) & Bloodlust",
        "bag_cap": 5,
        "item_buff_str": "Raw meat heals 2x HP (+60 HP)",
        "crit_rate": 0.25,
        "passive": "Beast Gut (Tox 150%), Bloodlust +50%",
        "skills": [
            {"label": "WAR AXE",      "desc": "-> Heavy cleave: 46 brutal Physical DMG"},
            {"label": "SPIRIT TOTEM", "desc": "-> Ancestral Spirit Magic: 32 Spirit Magic DMG"},
            {"label": "FERAL ROAR",   "desc": "-> Terrifying war cry: lowers foe ATK by 40%"},
            {"label": "DEVOUR FLESH", "desc": "-> Consume raw beast meat: restore +35 HP, cleanse bleed"}
        ],
        "assessment": [
            "Unstoppable juggernaut. Highest HP and physical cleave in game.",
            "Bloodlust boosts ATK by +50% when below 35% HP. Beast Gut allows",
            "150% drug tolerance. Bread satisfies less hunger."
        ]
    },
    {
        "id": 5,
        "name": "LE'GARDE",
        "role": "Tactician Commander",
        "hp": 135, "max_hp": 135,
        "mind": 100, "max_mind": 100,
        "hunger": 25, "max_hunger": 100,
        "atk": 34, "def": 20,
        "toxicity": 0, "max_toxicity": 100,
        "phys_resist_str": "Baseline (0%)",
        "magic_resist_str": "Baseline (0%)",
        "phys_mult": 1.0, "magic_mult": 1.0,
        "dodge_rate": 0.15,
        "trait": "Tactical Precision (+35% Sever)",
        "bag_cap": 5,
        "item_buff_str": "Vintage Ale gives +50% ATK 3t",
        "crit_rate": 0.35,
        "passive": "Tactician Focus, Ale gives +50% ATK",
        "skills": [
            {"label": "FENCING THRUST",   "desc": "-> Precision rapier thrust: 38 piercing Phys DMG"},
            {"label": "LEGION LIGHT",     "desc": "-> Solar Magic: 35 Magic DMG + lowers enemy ACC"},
            {"label": "TACTICAL FOCUS",   "desc": "-> Focus strike: +50% DMG on next hit & 100% crit"},
            {"label": "WAR CRY",          "desc": "-> Inspires self: +25 Mind, clears fear/doubt"}
        ],
        "assessment": [
            "Precision tactician. Vintage Ale turns him into a whirlwind of",
            "damage (+50% ATK for 3 turns). Rapier and Legion Light provide",
            "reliable coverage against armored and ghostly enemies."
        ]
    },
    {
        "id": 6,
        "name": "MOONLESS",
        "role": "Ancient Direhound",
        "hp": 130, "max_hp": 130,
        "mind": 80, "max_mind": 100,
        "hunger": 50, "max_hunger": 100,
        "atk": 36, "def": 18,
        "toxicity": 0, "max_toxicity": 100,
        "phys_resist_str": "+10% Hide (-10% Phys DMG)",
        "magic_resist_str": "Baseline (0%)",
        "phys_mult": 0.90, "magic_mult": 1.0,
        "dodge_rate": 0.30,
        "trait": "Feral Immunity (0% Herb Tox)",
        "bag_cap": 5,
        "item_buff_str": "Raw meat +40 HP (No alcohol)",
        "crit_rate": 0.30,
        "passive": "Feral Gut (0% Herb Tox), 30% Dodge",
        "skills": [
            {"label": "FERAL BITE",    "desc": "-> Vicious jaw crunch: 40 Phys DMG + Bleeding"},
            {"label": "MOON HOWL",     "desc": "-> Lunar Magic: 30 Magic DMG + 45% stun/crouch foe"},
            {"label": "SHADOW POUNCE", "desc": "-> Leap attack: 35 DMG (55 DMG on crouched foe)"},
            {"label": "SCENT DANGER",  "desc": "-> Warns party: +35% evasion for next 2 turns"}
        ],
        "assessment": [
            "High-speed predator. 30% natural evasion plus danger scent.",
            "Immune to plant toxins (0% toxicity from herbs). Bleeding bites",
            "and lunar howling handle both flesh and ghostly phantoms."
        ]
    },
    {
        "id": 7,
        "name": "THE GIRL",
        "role": "Innocent Ward",
        "hp": 100, "max_hp": 100,
        "mind": 100, "max_mind": 100,
        "hunger": 10, "max_hunger": 100,
        "atk": 24, "def": 26,
        "toxicity": 0, "max_toxicity": 100,
        "phys_resist_str": "Baseline (0%)",
        "magic_resist_str": "+30% Holy (-30% Mag DMG)",
        "phys_mult": 1.0, "magic_mult": 0.70,
        "dodge_rate": 0.35,
        "trait": "Pure Serenity (Dread Immune)",
        "bag_cap": 5,
        "item_buff_str": "Auto detox -10%/turn in battle",
        "crit_rate": 0.20,
        "passive": "Pure Serenity (-10% Tox/t), Dread-Imm",
        "skills": [
            {"label": "NIMBLE DODGE",   "desc": "-> Duck into shadows: 100% dodge enemy's next hit"},
            {"label": "LOVING EMBRACE", "desc": "-> Comfort self: restore +40 Mind & dispel terror"},
            {"label": "PURE LIGHT",     "desc": "-> Holy Radiance: 32 Magic DMG (x1.6 vs dark/ghosts)"},
            {"label": "DISTRACT FOE",   "desc": "-> Wave lantern: reduce enemy attack power by 50%"}
        ],
        "assessment": [
            "Evasive miracle worker. Highest base dodge (35%) and 100% immune",
            "to Dread Aura. Purges toxicity automatically each turn. Pure",
            "Light incinerates dark apparitions and ghostly specters."
        ]
    },
    {
        "id": 8,
        "name": "NAS'HRAH",
        "role": "Doom Wizard Head",
        "hp": 95, "max_hp": 95,
        "mind": 150, "max_mind": 150,
        "hunger": 0, "max_hunger": 100,
        "atk": 54, "def": 14,
        "toxicity": 0, "max_toxicity": 100,
        "phys_resist_str": "-20% Fragile (+20% Phys DMG)",
        "magic_resist_str": "+35% Arch-Mage (-35% Mag DMG)",
        "phys_mult": 1.20, "magic_mult": 0.65,
        "dodge_rate": 0.15,
        "trait": "Undead Relic (0 Hunger, 0% Tox)",
        "bag_cap": 5,
        "item_buff_str": "Vintage Ale +15 HP (Herbs rejected)",
        "crit_rate": 0.25,
        "passive": "Undead Relic (0 Hunger, 0% Tox, Fire)",
        "skills": [
            {"label": "COMBUSTION",      "desc": "-> Gro-goroth flame: 58 Unstoppable Fire Magic DMG"},
            {"label": "CURSE OF DECAY",  "desc": "-> Hex: 32 Dark Magic DMG + inflicts rotting flesh"},
            {"label": "HEAD GNAW",       "desc": "-> Flying tooth bite: 26 Phys DMG, siphons +15 HP"},
            {"label": "MOCK FOE",        "desc": "-> Insults foe: strips 50% enemy DEF"}
        ],
        "assessment": [
            "Incarnation of destruction. Unstoppable fire magic incinerates",
            "physical and ghostly foes alike. Immune to hunger and poison.",
            "Arrogant nature forbids guarding. Heals via blood and wine."
        ]
    }
]

import copy

# Active solo hero
active_hero = copy.deepcopy(ALL_HEROES[0])
active_hero["buff"] = ""
active_hero["is_guarding"] = False
active_hero["debuffs"] = []

# Inventory initialized for solo run (Cahara has 10 cap, others 5)
inventory = {
    "poppy": 3,      # +50 HP (+65 for Cahara)
    "weed": 2,       # +120 HP
    "bread": 4,      # -40 Hunger (-50 for Cahara, -20 for Ragnvaldr)
    "ale": 2         # +35 Mind (+50% ATK 3 turns for Le'garde)
}

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

combat_log = "Battle initiated. Shadow Swordsman unsheathes dark blade."
current_menu = "MAIN"
cursor_idx = 0
combat_outcome = None

# =============================================================================
# FLICKER-FREE ATOMIC TERMINAL BLITTING ENGINE (EXACT 100 COLUMNS & TAIL ERASE)
# =============================================================================
def fit_100_cols(s):
    w = display_width(s)
    if w < 100:
        return s + " " * (100 - w)
    elif w > 100:
        return fit_ansi(s, 100)
    return s

def atomic_blit(screen_rows):
    """Blits entire screen atomically via cursor home to eliminate flicker 100%."""
    formatted = [fit_100_cols(r) for r in screen_rows]
    frame_str = "\033[H" + "\n".join(formatted) + "\n\033[J"
    sys.stdout.write(frame_str)
    sys.stdout.flush()

# =============================================================================
# VERTICAL SOLO CHARACTER SELECTOR (W/S CURSOR WITH REAL-TIME DOSSIER PREVIEW)
# =============================================================================
def render_solo_select_screen(sel_idx):
    hero = ALL_HEROES[sel_idx]
    h_sprite = HERO_SPRITES.get(hero["name"], FALLBACK_SPRITES.get(hero["name"], [" " * 29] * 12))

    b1_top = "\033[1;30m+" + "-" * 32 + "+\033[0m"
    b2_top = "\033[1;30m+" + "-" * 62 + "+\033[0m"

    header_rows = [
        "\033[1;30m+====================================================================================================+\033[0m",
        f"\033[1;30m| \033[1;37m{fit_ansi('FEAR & HUNGER: SOLO SURVIVOR EXPEDITION - SELECT YOUR EXPLORER', 96)}\033[1;30m |\033[0m",
        "\033[1;30m+====================================================================================================+\033[0m",
        f"{b1_top}  {b2_top}"
    ]

    # Left Box Content (30 visible chars)
    b1_lines = [
        "\033[1;33mSELECT EXPLORER (W/S):\033[0m",
        ""
    ]
    for idx, h in enumerate(ALL_HEROES):
        is_cur = (idx == sel_idx)
        if is_cur:
            b1_lines.append(f"\033[1;32m▶ [{h['id']}] {h['name']:<9} ({h['role'].split()[0]:<9})\033[0m")
        else:
            b1_lines.append(f"\033[90m  [{h['id']}] {h['name']:<9} ({h['role'].split()[0]:<9})\033[0m")

    b1_lines.extend([
        "",
        "\033[1;33m[CONTROLS]:\033[0m",
        "\033[1;37m[W/S]\033[0m   : Navigate Heroes",
        "\033[1;32m[Enter]\033[0m : Embark Solo",
        "\033[1;31m[Q]\033[0m     : Exit Game",
        "",
        ""
    ])

    # Right Box Content: 12 rows of Model (29 cols) + 2 spaces + Stats (29 cols) = 60 cols
    stats_data = [
        f"\033[1;33mNAME   : \033[1;37m{hero['name']}\033[0m",
        f"\033[1;33mROLE   : \033[1;37m{hero['role']}\033[0m",
        f"\033[1;32mHP     : {hero['hp']:3d} / {hero['max_hp']:3d}\033[0m",
        f"\033[1;31mATK    : {hero['atk']:2d} ({hero['skills'][0]['label'][:13]})\033[0m",
        f"\033[1;36mDEF    : {hero['def']:2d}\033[0m",
        f"\033[1;37mPHYS-R : {hero['phys_resist_str'][:20]}\033[0m",
        f"\033[1;37mMAG-R  : {hero['magic_resist_str'][:20]}\033[0m",
        f"\033[1;35mDODGE  : {int(hero['dodge_rate']*100)}% Evasion\033[0m",
        f"\033[1;33mTRAIT  : {hero['trait'][:20]}\033[0m",
        f"\033[1;32mBUFF   : {hero['item_buff_str'][:20]}\033[0m",
        f"\033[1;36mSKILLS : {hero['skills'][0]['label'][:20]}\033[0m",
        f"         \033[1;36m{hero['skills'][1]['label'][:20]}\033[0m"
    ]

    b2_lines = []
    for r in range(12):
        sp_line = h_sprite[r] if r < len(h_sprite) else " " * 29
        stat_line = stats_data[r] if r < len(stats_data) else ""
        b2_lines.append(f"{fit_ansi(sp_line, 29)}  {fit_ansi(stat_line, 29)}")

    # Divider inside right box
    b2_lines.append("\033[1;30m" + "-" * 60 + "\033[0m")
    b2_lines.append("\033[1;33m[SOLO SURVIVAL ASSESSMENT]:\033[0m")
    for a_line in hero["assessment"][:3]:
        b2_lines.append(f"\033[1;37m{a_line}\033[0m")

    all_rows = list(header_rows)
    for i in range(17):
        l1 = b1_lines[i] if i < len(b1_lines) else ""
        l2 = b2_lines[i] if i < len(b2_lines) else ""
        comb = f"\033[1;30m| \033[0m{fit_ansi(l1, 30)}\033[1;30m |  | \033[0m{fit_ansi(l2, 60)}\033[1;30m |\033[0m"
        all_rows.append(comb)

    all_rows.append(f"{b1_top}  {b2_top}")
    all_rows.append("\033[1;30m" + "=" * 100 + "\033[0m")

    atomic_blit(all_rows)

def run_solo_select_interactive():
    global active_hero, inventory

    # Clear screen once on entry and hide cursor
    sys.stdout.write("\033[2J\033[H\033[?25l")
    sys.stdout.flush()

    sel_idx = 0
    num_heroes = len(ALL_HEROES)

    while True:
        render_solo_select_screen(sel_idx)

        if os.name == 'nt' and sys.stdin.isatty():
            ch = msvcrt.getch()
            # Drain trailing keys if held down to avoid lag
            while msvcrt.kbhit():
                discard = msvcrt.getch()

            if ch in (b'\x00', b'\xe0'):
                ext = msvcrt.getch()
                if ext == b'H':    # Up Arrow
                    sel_idx = (sel_idx - 1) % num_heroes
                elif ext == b'P':  # Down Arrow
                    sel_idx = (sel_idx + 1) % num_heroes
            elif ch in (b'w', b'W'):
                sel_idx = (sel_idx - 1) % num_heroes
            elif ch in (b's', b'S'):
                sel_idx = (sel_idx + 1) % num_heroes
            elif ch in (b'\r', b'\n', b' '):
                # Selected this hero!
                active_hero = copy.deepcopy(ALL_HEROES[sel_idx])
                active_hero["buff"] = ""
                active_hero["is_guarding"] = False
                active_hero["debuffs"] = []

                # Cahara gets 2x bag capacity
                if active_hero["name"] == "CAHARA":
                    inventory = {"poppy": 5, "weed": 3, "bread": 6, "ale": 3}
                else:
                    inventory = {"poppy": 3, "weed": 2, "bread": 4, "ale": 2}
                return active_hero, sel_idx
            elif ch in (b'q', b'Q', b'\x03'):
                sys.stdout.write("\033[?25h\n[OK] Exited Solo Selection.\n")
                return None, -1
            elif ch in (b'1', b'2', b'3', b'4', b'5', b'6', b'7', b'8'):
                sel_idx = int(ch.decode('ascii')) - 1
                render_solo_select_screen(sel_idx)
        else:
            line = sys.stdin.readline().strip().lower()
            if line in ('1', '2', '3', '4', '5', '6', '7', '8'):
                sel_idx = int(line) - 1
                active_hero = copy.deepcopy(ALL_HEROES[sel_idx])
                if active_hero["name"] == "CAHARA":
                    inventory = {"poppy": 5, "weed": 3, "bread": 6, "ale": 3}
                else:
                    inventory = {"poppy": 3, "weed": 2, "bread": 4, "ale": 2}
                return active_hero, sel_idx
            elif line == 'w':
                sel_idx = (sel_idx - 1) % num_heroes
            elif line == 's':
                sel_idx = (sel_idx + 1) % num_heroes
            elif line in ('', 'enter', 'e', ' '):
                active_hero = copy.deepcopy(ALL_HEROES[sel_idx])
                if active_hero["name"] == "CAHARA":
                    inventory = {"poppy": 5, "weed": 3, "bread": 6, "ale": 3}
                else:
                    inventory = {"poppy": 3, "weed": 2, "bread": 4, "ale": 2}
                return active_hero, sel_idx
            elif line in ('q', 'quit'):
                return None, -1

# =============================================================================
# RENDER SCREEN: COMPACT SOLO POKÉMON-STYLE COMBAT ARENA (29 ROWS, EXACT 100 COLS)
# =============================================================================
def render_screen():
    hero = active_hero
    screen_rows = []

    # -------------------------------------------------------------------------
    # MAIN HEADER (3 ROWS, EXACT 100 COLS)
    # -------------------------------------------------------------------------
    screen_rows.append("\033[1;30m+" + "=" * 98 + "+\033[0m")
    title_str = f"FEAR & HUNGER: SOLO SURVIVOR COMBAT ARENA - {hero['name']} [{hero['role']}]"
    pad_left = (96 - display_width(title_str)) // 2
    pad_right = 96 - display_width(title_str) - pad_left
    screen_rows.append(f"\033[1;30m| \033[1;37m{' ' * pad_left}{title_str}{' ' * pad_right}\033[1;30m |\033[0m")
    screen_rows.append("\033[1;30m+" + "=" * 98 + "+\033[0m")

    # -------------------------------------------------------------------------
    # ZONE 1: OPPONENT ZONE (7 ROWS, EXACT 100 COLS)
    # Left: Monster Tactical Card (54 cols) | Gap: 4 spaces | Right: Sprite (42 cols)
    # -------------------------------------------------------------------------
    c_mcard = "\033[1;33m" if current_menu == "TARGET_LIMB" else "\033[1;30m"
    m_border = f"{c_mcard}+" + "-" * 52 + f"+{c_mcard}\033[0m"

    if monster.get("debuff_decapitated"):
        m_sprite = MONSTER_SPRITE_DECAPITATED
        m_model_sub = "\033[90m[NEUTRALIZED]\033[0m"
    elif monster.get("debuff_legs"):
        m_sprite = MONSTER_SPRITE_CRAWLING
        m_model_sub = "\033[1;33m[CROUCHED]\033[0m"
    elif monster.get("debuff_arm_r") or monster.get("debuff_arm_l"):
        m_sprite = MONSTER_SPRITE_DISARMED
        m_model_sub = "\033[1;33m[DISARMED]\033[0m"
    else:
        m_sprite = MONSTER_SPRITE_INTACT
        m_model_sub = ""

    m_pct = int(max(0, monster["hp"]) / float(max(1, monster["max_hp"])) * 100)
    m_hp_bar = make_bar(monster["hp"], monster["max_hp"], 16, "31")

    arch = monster.get("archetype", "NORMAL")
    if arch == "SPECTRAL":
        trait_desc = "\033[1;35m  TRAIT : SPECTRAL (Blade-resistant, Magic weak)\033[0m"
    elif arch == "ARMORED":
        trait_desc = "\033[1;36m  TRAIT : ARMORED (Blade-deflecting, Smite weak)\033[0m"
    elif arch == "AMBUSHER":
        trait_desc = "\033[1;31m  TRAIT : AMBUSHER (Lethal strike, Dodge weak)\033[0m"
    elif arch == "TERROR":
        trait_desc = "\033[1;35m  TRAIT : DREAD AURA (-25 Mind/turn, Ward calm)\033[0m"
    else:
        trait_desc = "\033[90m  TRAIT : STANDARD COMBATANT\033[0m"

    if monster.get("debuff_decapitated"):
        m_status = "\033[90m  STATUS: [HEAD] Decapitated (Neutralized)\033[0m"
    elif monster.get("debuff_legs"):
        m_status = "\033[1;33m  STATUS: [LEGS] Broken (Crouched, 100% Hit)\033[0m"
    elif monster.get("debuff_arm_r"):
        m_status = "\033[1;33m  STATUS: [R-ARM] Severed (Disarmed, ATK -14)\033[0m"
    elif monster.get("debuff_arm_l"):
        m_status = "\033[1;36m  STATUS: [L-ARM] Severed (Guard Broken)\033[0m"
    else:
        m_status = "\033[90m  ANATOMY: All Limbs Functional & Intact\033[0m"

    m_card_rows = [
        m_border,
        make_card_row(f"\033[1;31m  FOE   : #{monster['id']:02d} {monster['name']:<17} \033[1;33m[{arch}]\033[0m", c_mcard),
        make_card_row(f"  HP    : {m_hp_bar} \033[1;31m{monster['hp']:3d}/{monster['max_hp']:3d} ({m_pct:3d}%)\033[0m", c_mcard),
        make_card_row(trait_desc, c_mcard),
        make_card_row(m_status, c_mcard),
        make_card_row("", c_mcard),
        m_border
    ]

    m_model_rows = [
        pad_str("          \033[1;31m[ENEMY]\033[0m", 42)
    ]
    for r in range(5):
        sp = m_sprite[r] if r < len(m_sprite) else " " * 29
        m_model_rows.append(format_model_row(sp))
    sub_tag = f"       {m_model_sub}" if m_model_sub else ""
    m_model_rows.append(pad_str(sub_tag, 42))

    for r_idx in range(7):
        screen_rows.append(f"{m_card_rows[r_idx]}    {m_model_rows[r_idx]}\033[0m")

    # -------------------------------------------------------------------------
    # ZONE 2: SOLO HERO ZONE (7 ROWS, EXACT 100 COLS)
    # Left: Hero Sprite Model (42 cols, NO [HERO] tag!) | Gap: 4 | Right: Card (54 cols)
    # -------------------------------------------------------------------------
    c_hcard = "\033[1;32m" if current_menu in ("POUCH", "TACTICS") else "\033[1;30m"
    h_border = f"{c_hcard}+" + "-" * 52 + f"+{c_hcard}\033[0m"

    hero_key = hero["name"]
    h_sprite = HERO_SPRITES.get(hero_key, FALLBACK_SPRITES.get(hero_key, [" " * 29] * 12))

    h_pct = int(max(0, hero["hp"]) / float(max(1, hero["max_hp"])) * 100)
    h_hp_bar = make_bar(hero["hp"], hero["max_hp"], 16, "32")
    h_mnd_bar = make_bar(hero["mind"], hero["max_mind"], 10, "36")

    h_tox = hero.get("toxicity", 0)
    max_t = hero.get("max_toxicity", 100)
    tox_badge = "\033[1;31m[INTOXICATED]\033[0m" if h_tox >= max_t else ("\033[1;33m[HIGH]\033[0m" if h_tox >= (max_t * 0.8) else "\033[90m[SAFE]\033[0m")

    # Only show status when an actual buff/debuff exists; NEVER show "Battle Ready"
    if hero.get("debuffs"):
        h_status = f"\033[1;31m  STATUS: {', '.join(hero['debuffs'])}\033[0m"
    elif hero.get("buff"):
        h_status = f"\033[1;32m  STATUS: {hero['buff']}\033[0m"
    else:
        h_status = f"\033[1;36m  PASSIV: {hero['passive'][:36]}\033[0m"

    h_card_rows = [
        h_border,
        make_card_row(f"\033[1;32m  HERO  : {hero['name']:<9} \033[90m[{hero['role']}]\033[0m", c_hcard),
        make_card_row(f"  HP    : {h_hp_bar} \033[1;32m{hero['hp']:3d}/{hero['max_hp']:3d} ({h_pct:3d}%)\033[0m", c_hcard),
        make_card_row(f"  MIND  : {h_mnd_bar} \033[1;36m{hero['mind']:3d}/{hero['max_mind']:3d}\033[0m | \033[90mTOXIC:\033[0m \033[1;{'31' if h_tox >= max_t else '32'}m{h_tox:2d}%\033[0m {tox_badge}", c_hcard),
        make_card_row(f"  ARMOR : \033[1;37m{hero['phys_resist_str'][:18]}\033[0m | \033[1;35m{int(hero['dodge_rate']*100)}% Dodge\033[0m", c_hcard),
        make_card_row(h_status, c_hcard),
        h_border
    ]

    h_model_rows = []
    for r in range(6):
        sp = h_sprite[r] if r < len(h_sprite) else " " * 29
        h_model_rows.append(format_model_row(sp))
    h_model_rows.append(pad_str("", 42))

    for r_idx in range(7):
        screen_rows.append(f"{h_model_rows[r_idx]}    {h_card_rows[r_idx]}\033[0m")

    # -------------------------------------------------------------------------
    # SECTION 3: COMBAT LOG BOX (3 ROWS, EXACT 100 COLS)
    # -------------------------------------------------------------------------
    screen_rows.append("\033[1;30m+" + "-" * 98 + "+\033[0m")
    log_text = f"\033[1;33m[LOG]\033[0m \033[1;37m{combat_log}\033[0m"
    screen_rows.append(f"\033[1;30m| \033[0m{fit_ansi(log_text, 94)}\033[1;30m |\033[0m")
    screen_rows.append("\033[1;30m+" + "-" * 98 + "+\033[0m")

    # -------------------------------------------------------------------------
    # SECTION 4: COMBAT COMMANDS MENU (6 ROWS, EXACT 100 COLS)
    # -------------------------------------------------------------------------
    menu_data = get_current_menu_data()
    title = menu_data["title"]
    options = menu_data["options"]

    screen_rows.append(f"  \033[1;37m{title}\033[0m")
    for idx, opt in enumerate(options):
        is_sel = (idx == cursor_idx)
        label = opt["label"]
        desc = opt["desc"]

        if is_sel:
            screen_rows.append(f"    \033[1;33m▶  [{idx+1}] \033[1;37;43m {label:<14} \033[0m \033[1;33m{desc}\033[0m")
        else:
            screen_rows.append(f"       \033[90m[{idx+1}]   {label:<14} {desc}\033[0m")

    for _ in range(max(0, 5 - len(options))):
        screen_rows.append("")

    # -------------------------------------------------------------------------
    # SECTION 5: FOOTER (3 ROWS, EXACT 100 COLS)
    # -------------------------------------------------------------------------
    screen_rows.append("\033[1;30m" + "=" * 98 + "\033[0m")
    if current_menu == "MAIN":
        screen_rows.append("  \033[90m[CONTROLS]:\033[0m \033[1;37m[W/S / 1-5]\033[0m Navigate  |  \033[1;37m[Enter/Space]\033[0m Select  |  \033[1;31m[Q]\033[0m Quit")
    else:
        screen_rows.append("  \033[90m[CONTROLS]:\033[0m \033[1;37m[W/S / 1-6]\033[0m Navigate  |  \033[1;37m[Enter/Space]\033[0m Confirm  |  \033[1;33m[B/Esc]\033[0m Back")
    screen_rows.append("\033[1;30m" + "=" * 98 + "\033[0m")

    atomic_blit(screen_rows)

# =============================================================================
# MENU DATA RESOLUTION (UNIFIED 5-OPTION CORE COMBAT MENU)
# =============================================================================
def get_current_menu_data():
    h = active_hero

    if current_menu == "MAIN":
        flee_pct = "100%" if (monster.get("debuff_legs") or h["name"] == "CAHARA") else "50%"
        return {
            "title": f"COMBAT COMMANDS ({h['name']} - {h['role']})",
            "options": [
                {"label": "ATTACK",  "desc": "-> Target specific limbs (Head / Torso / Arms / Legs)"},
                {"label": "GUARD",   "desc": "-> Brace for impact (-70% incoming damage)"},
                {"label": "SKILL",   "desc": f"-> Class abilities & magic ({h['name']})"},
                {"label": "ITEM",    "desc": f"-> Administer supplies from pouch (Cap: {h.get('bag_cap', 5)})"},
                {"label": "FLEE",    "desc": f"-> Disengage and retreat to corridor ({flee_pct} Chance)"}
            ]
        }
    elif current_menu == "TARGET_LIMB":
        crawl_hint = "\033[1;32m(100% Critical Finish!)\033[0m" if monster.get("debuff_legs") else "(35% Hit | Instant Decapitate)"
        return {
            "title": "ACTION > ATTACK > SELECT TARGET LIMB",
            "options": [
                {"label": "HEAD",       "desc": f"-> {crawl_hint}"},
                {"label": "TORSO",      "desc": "-> 100% Hit | Safe strike, heavy body damage"},
                {"label": "RIGHT ARM",  "desc": "-> 100% Hit | Sever sword arm -> Disarm foe"},
                {"label": "LEFT ARM",   "desc": "-> 100% Hit | Sever shield arm -> Shatter guard"},
                {"label": "LEGS",       "desc": "-> 100% Hit | Break legs -> Force crouch (100% Flee)"},
                {"label": "BACK",       "desc": "-> Return to main combat menu"}
            ]
        }
    elif current_menu == "SKILL":
        h_skills = h.get("skills", [])
        opts = []
        for sk in h_skills:
            opts.append({"label": sk["label"], "desc": sk["desc"]})
        opts.append({"label": "BACK", "desc": "-> Return to main combat menu"})
        return {
            "title": f"SKILLS & ABILITIES ({h['name']} - {h['role']})",
            "options": opts
        }
    elif current_menu == "POUCH":
        cap = h.get("bag_cap", 5)
        return {
            "title": f"ITEM POUCH & SURVIVAL SUPPLIES (Capacity: {cap})",
            "options": [
                {"label": f"WHITE POPPY [{inventory['poppy']}/{cap}]", "desc": "-> Restores HP & heals wounds"},
                {"label": f"MEDICINAL HERB [{inventory['weed']}/{cap}]", "desc": "-> Restores +120 HP potent medicine"},
                {"label": f"MOLDY BREAD [{inventory['bread']}/{cap}]",  "desc": "-> Dungeon rations | Relieves hunger"},
                {"label": f"VINTAGE ALE [{inventory['ale']}/{cap}]",    "desc": "-> Cleanses terror | Restores Mind"},
                {"label": "BACK",                                       "desc": "-> Return to main combat menu"}
            ]
        }
    elif current_menu == "TACTICS":
        return {
            "title": "COMBAT TACTICS & STANCES",
            "options": [
                {"label": "BERSERK",     "desc": "-> +50% Attack power, +30% damage taken"},
                {"label": "IRON GUARD",  "desc": "-> -70% Damage taken, restore 5% HP/turn"},
                {"label": "AGILE DANCE", "desc": "-> +35% Dodge rate, 100% flee chance"},
                {"label": "BACK",        "desc": "-> Return to main combat menu"}
            ]
        }
    return {"title": "MENU", "options": []}

# =============================================================================
# SELECTION LOGIC & COMBAT SIMULATION (SOLO EXPLORER)
# =============================================================================
def handle_selection():
    global current_menu, cursor_idx, combat_log, combat_outcome
    hero = active_hero

    if current_menu == "MAIN":
        if cursor_idx == 0:    # ATTACK -> Target Limb
            current_menu = "TARGET_LIMB"
            cursor_idx = 0
        elif cursor_idx == 1:  # GUARD -> Immediate Guard
            if hero["name"] == "NAS'HRAH":
                combat_log = "NAS'HRAH REFUSES TO GUARD! 'I am a god, I bow to no worm!'"
            else:
                hero["is_guarding"] = True
                hero["buff"] = "GUARD (-70% DMG)"
                combat_log = f"{hero['name']} raises guard! Incoming damage reduced by 70%."
            enemy_turn()
            current_menu = "MAIN"
            cursor_idx = 0
        elif cursor_idx == 2:  # SKILL -> Open Skill Menu
            current_menu = "SKILL"
            cursor_idx = 0
        elif cursor_idx == 3:  # ITEM -> Open Item Pouch
            current_menu = "POUCH"
            cursor_idx = 0
        elif cursor_idx == 4:  # FLEE -> Immediate Escape Attempt
            if monster.get("debuff_legs") or hero["name"] == "CAHARA":
                combat_log = "ESCAPE SUCCESSFUL! Safely retreated into dungeon corridors."
                combat_outcome = "FLEE"
            else:
                if random.random() < 0.5:
                    combat_log = "ESCAPE SUCCESSFUL! Retreating from the chamber."
                    combat_outcome = "FLEE"
                else:
                    combat_log = "ESCAPE FAILED! Foe blocks the corridor and retaliates!"
                    enemy_turn()
            current_menu = "MAIN"
            cursor_idx = 0

    elif current_menu == "TARGET_LIMB":
        if cursor_idx == 5: # Back
            current_menu = "MAIN"
            cursor_idx = 0
            return

        arch = monster.get("archetype", "NORMAL")
        base_slash = hero["atk"]
        if arch == "SPECTRAL":
            dmg = max(12, int(base_slash * 0.45))
            monster["hp"] = max(0, monster["hp"] - dmg)
            combat_log = f"SPIRIT SEVERANCE! {hero['name']}'s weapon disrupts ghostly mist for {dmg} DMG!"
            if monster["hp"] <= 0:
                combat_log += " | Foe neutralized! VICTORY!"
                combat_outcome = "VICTORY"
            else:
                enemy_turn()
            current_menu = "MAIN"
            cursor_idx = 0
            return
        elif arch == "ARMORED":
            dmg = max(10, int(base_slash * 0.35))
            monster["hp"] = max(0, monster["hp"] - dmg)
            combat_log = f"HEAVY CLANG! {hero['name']} strikes armor plate for {dmg} DMG!"
            if monster["hp"] <= 0:
                combat_log += " | Foe neutralized! VICTORY!"
                combat_outcome = "VICTORY"
            else:
                enemy_turn()
            current_menu = "MAIN"
            cursor_idx = 0
            return

        # Normal/Ambusher/Terror targets
        if cursor_idx == 0:    # Head
            if monster.get("debuff_legs"):
                monster["hp"] = 0
                monster["debuff_decapitated"] = True
                combat_log = f"CRITICAL FINISH! Foe is crouched; {hero['name']} cleanly severs head! VICTORY!"
                combat_outcome = "VICTORY"
            else:
                if random.random() < 0.35:
                    monster["hp"] = 0
                    monster["debuff_decapitated"] = True
                    combat_log = f"DECAPITATION! Fatal strike for {monster['max_hp']} DMG! VICTORY!"
                    combat_outcome = "VICTORY"
                else:
                    dmg = 20
                    monster["hp"] = max(0, monster["hp"] - dmg)
                    combat_log = f"Glancing strike across the head for {dmg} DMG."
                    if monster["hp"] <= 0:
                        combat_log += " | Foe neutralized! VICTORY!"
                        combat_outcome = "VICTORY"
                    else:
                        enemy_turn()
            current_menu = "MAIN"
            cursor_idx = 0
        elif cursor_idx == 1:  # Torso
            dmg = hero["atk"] - (monster["def"] // 2)
            dmg = max(24, dmg)
            monster["hp"] = max(0, monster["hp"] - dmg)
            combat_log = f"{hero['name']} strikes torso for {dmg} DMG."
            if monster["hp"] <= 0:
                combat_log += " | Foe neutralized! VICTORY!"
                combat_outcome = "VICTORY"
            else:
                enemy_turn()
            current_menu = "MAIN"
            cursor_idx = 0
        elif cursor_idx == 2:  # Right Arm
            dmg = 20
            monster["hp"] = max(0, monster["hp"] - dmg)
            monster["debuff_arm_r"] = True
            monster["atk"] = max(8, monster["atk"] - 14)
            combat_log = f"DISARMED! Weapon arm severed (-{dmg} HP). Foe's ATK reduced to {monster['atk']}!"
            if monster["hp"] <= 0:
                combat_log += " | Foe neutralized! VICTORY!"
                combat_outcome = "VICTORY"
            else:
                enemy_turn()
            current_menu = "MAIN"
            cursor_idx = 0
        elif cursor_idx == 3:  # Left Arm
            dmg = 18
            monster["hp"] = max(0, monster["hp"] - dmg)
            monster["debuff_arm_l"] = True
            combat_log = f"SHIELD BROKEN! Left arm disabled (-{dmg} HP). Foe defense shattered!"
            if monster["hp"] <= 0:
                combat_log += " | Foe neutralized! VICTORY!"
                combat_outcome = "VICTORY"
            else:
                enemy_turn()
            current_menu = "MAIN"
            cursor_idx = 0
        elif cursor_idx == 4:  # Legs
            dmg = 22
            monster["hp"] = max(0, monster["hp"] - dmg)
            monster["debuff_legs"] = True
            combat_log = f"LEGS BROKEN! -{dmg} HP. Foe collapses to floor -> 100% FLEE & 100% HEAD HIT!"
            if monster["hp"] <= 0:
                combat_log += " | Foe neutralized! VICTORY!"
                combat_outcome = "VICTORY"
            else:
                enemy_turn()
            current_menu = "MAIN"
            cursor_idx = 0

    elif current_menu == "SKILL":
        h = active_hero
        num_skills = len(h.get("skills", []))

        if cursor_idx == num_skills: # Back
            current_menu = "MAIN"
            cursor_idx = 0
            return

        # Execute hero-specific skill
        if h["name"] == "CAHARA":
            if cursor_idx == 0:    # Twin Daggers
                dmg = 38
                monster["hp"] = max(0, monster["hp"] - dmg)
                combat_log = f"TWIN DAGGERS! Cahara strikes with rapid dual thrusts for {dmg} DMG!"
                enemy_turn()
            elif cursor_idx == 1:  # Poison Dart
                dmg = 28
                monster["hp"] = max(0, monster["hp"] - dmg)
                combat_log = f"POISON DART! Toxic alchemy pierces defense for {dmg} Chem Magic DMG!"
                enemy_turn()
            elif cursor_idx == 2:  # Steal Item
                stolen_item = "poppy" if random.random() < 0.5 else "bread"
                cap = h.get("bag_cap", 10)
                if inventory[stolen_item] < cap:
                    inventory[stolen_item] += 1
                combat_log = f"STEAL SUCCESS! Pickpocketed 1x {stolen_item.upper()} from target!"
                enemy_turn()
            elif cursor_idx == 3:  # Smoke Bomb
                combat_log = "SMOKE BOMB! Dense fog blinds opponent. 100% ESCAPE SUCCESSFUL!"
                combat_outcome = "FLEE"

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
                dmg = 44
                if monster.get("archetype") == "ARMORED":
                    dmg = 56
                    monster["archetype"] = "NORMAL"
                    monster["def"] = 14
                    combat_log = f"ARMOR SHATTERED! Holy Smite fractures heavy steel plate for {dmg} DMG! DEF shattered!"
                elif monster.get("archetype") == "SPECTRAL":
                    dmg = 52
                    combat_log = f"SACRED RADIANCE! Holy Smite incinerates spectral ghost for {dmg} Divine Magic DMG!"
                else:
                    combat_log = f"HOLY SMITE! Heavy sanctified cleave inflicts {dmg} DMG!"
                monster["hp"] = max(0, monster["hp"] - dmg)
                enemy_turn()
            elif cursor_idx == 3:  # Knight Charge
                dmg = 36
                monster["hp"] = max(0, monster["hp"] - dmg)
                combat_log = f"KNIGHT CHARGE! D'arce slams forward with tower shield for {dmg} Phys DMG!"
                enemy_turn()

        elif h["name"] == "ENKI":
            if cursor_idx == 0:    # Black orb
                if h["mind"] >= 15:
                    h["mind"] -= 15
                    dmg = 52
                    if monster.get("archetype") in ("SPECTRAL", "ARMORED"):
                        dmg = int(dmg * 1.5)
                    monster["hp"] = max(0, monster["hp"] - dmg)
                    combat_log = f"BLACK ORB! Dark sphere pierces 100% defense for {dmg} True Magic DMG!"
                    enemy_turn()
                else:
                    combat_log = "Insufficient Mind points for Black Orb!"
            elif cursor_idx == 1:  # Ritual Dagger
                dmg = 24
                monster["hp"] = max(0, monster["hp"] - dmg)
                h["mind"] = min(h["max_mind"], h["mind"] + 15)
                combat_log = f"RITUAL DAGGER! Enki slices foe for {dmg} Phys DMG and siphons +15 Mind!"
                enemy_turn()
            elif cursor_idx == 2:  # Blood sacrifice
                if h["hp"] > 20:
                    h["hp"] -= 20
                    h["mind"] = min(h["max_mind"], h["mind"] + 40)
                    combat_log = "BLOOD SACRIFICE! Enki cuts own flesh (-20 HP) to harvest +40 Mind!"
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
                dmg = 46
                if "BLOODLUST" in hero.get("buff", "") or hero["hp"] < (hero["max_hp"] * 0.35):
                    dmg = int(dmg * 1.5)
                monster["hp"] = max(0, monster["hp"] - dmg)
                combat_log = f"WAR AXE! Ragnvaldr buries heavy axe into foe for {dmg} brutal Physical DMG!"
                enemy_turn()
            elif cursor_idx == 1:  # Spirit Totem (Ancestral Magic)
                if h["mind"] >= 10:
                    h["mind"] -= 10
                    dmg = 32
                    monster["hp"] = max(0, monster["hp"] - dmg)
                    combat_log = f"SPIRIT TOTEM! Northern ancestral spirits crush foe for {dmg} Spirit Magic DMG!"
                    enemy_turn()
                else:
                    combat_log = "Insufficient Mind points for Spirit Totem!"
            elif cursor_idx == 2:  # Feral Roar
                monster["atk"] = max(6, int(monster["atk"] * 0.6))
                combat_log = "FERAL ROAR! Barbarian roar intimidates foe (-40% enemy ATK power)!"
                enemy_turn()
            elif cursor_idx == 3:  # Devour Flesh
                h["hp"] = min(h["max_hp"], h["hp"] + 35)
                h["hunger"] = max(0, h["hunger"] - 25)
                combat_log = "DEVOUR FLESH! Ragnvaldr consumes raw meat (+35 HP, -25 Hunger)!"
                enemy_turn()

        elif h["name"] == "LE'GARDE":
            if cursor_idx == 0:    # Fencing Thrust
                dmg = 38
                if "TACTICAL FOCUS" in hero.get("buff", ""):
                    dmg = int(dmg * 1.5)
                    hero["buff"] = ""
                monster["hp"] = max(0, monster["hp"] - dmg)
                combat_log = f"FENCING THRUST! Precision rapier thrust deals {dmg} piercing DMG!"
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
            elif cursor_idx == 2:  # Tactical Focus
                h["buff"] = "TACTICAL FOCUS (+50% NEXT ATK)"
                combat_log = "TACTICAL FOCUS! Le'garde studies weak points (+50% DMG on next strike)!"
                enemy_turn()
            elif cursor_idx == 3:  # War Cry
                h["mind"] = min(h["max_mind"], h["mind"] + 25)
                combat_log = "WAR CRY! Le'garde rallies his spirit (+25 Mind, dispels terror)!"
                enemy_turn()

        elif h["name"] == "MOONLESS":
            if cursor_idx == 0:    # Feral Bite
                dmg = 40
                monster["hp"] = max(0, monster["hp"] - dmg)
                combat_log = f"FERAL BITE! Moonless tears into flesh for {dmg} Phys DMG + Bleeding!"
                enemy_turn()
            elif cursor_idx == 1:  # Moon Howl
                dmg = 30
                monster["hp"] = max(0, monster["hp"] - dmg)
                if random.random() < 0.45:
                    monster["debuff_legs"] = True
                    combat_log = f"MOON HOWL! Eerie lunar howling deals {dmg} Magic DMG and stuns foe (Crouched)!"
                else:
                    combat_log = f"MOON HOWL! Lunar psychic scream echoes through the dark for {dmg} Magic DMG!"
                enemy_turn()
            elif cursor_idx == 2:  # Shadow Pounce
                dmg = 35
                if monster["debuff_legs"]:
                    dmg = 55
                monster["hp"] = max(0, monster["hp"] - dmg)
                combat_log = f"SHADOW POUNCE! Moonless pounces from the gloom for {dmg} DMG!"
                enemy_turn()
            elif cursor_idx == 3:  # Scent Danger
                h["buff"] = "DANGER SCENT (+35% DODGE)"
                combat_log = "SCENT DANGER! Moonless sniffs danger in the air (+35% evasion)!"
                enemy_turn()

        elif h["name"] == "THE GIRL":
            if cursor_idx == 0:    # Nimble dodge
                h["buff"] = "NIMBLE DODGE (100% EVADE)"
                combat_log = "NIMBLE DODGE! The Girl slips into shadows, guaranteeing 100% evasion!"
                enemy_turn()
            elif cursor_idx == 1:  # Loving embrace
                h["mind"] = min(h["max_mind"], h["mind"] + 40)
                combat_log = "LOVING EMBRACE! Serene innocence restores +40 Mind and dispels all terror!"
                enemy_turn()
            elif cursor_idx == 2:  # Pure Light
                if h["mind"] >= 10:
                    h["mind"] -= 10
                    dmg = 32
                    if monster.get("archetype") in ("SPECTRAL", "TERROR"):
                        dmg = int(dmg * 1.6)
                    monster["hp"] = max(0, monster["hp"] - dmg)
                    combat_log = f"PURE LIGHT! Holy glow incinerates dark foe for {dmg} Sacred Light DMG!"
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
                    dmg = 58
                    monster["hp"] = max(0, monster["hp"] - dmg)
                    combat_log = f"COMBUSTION! Gro-goroth flame erupts for {dmg} Unstoppable Fire Magic DMG!"
                    enemy_turn()
                else:
                    combat_log = "Insufficient Mind for Combustion!"
            elif cursor_idx == 1:  # Curse of Decay
                if h["mind"] >= 15:
                    h["mind"] -= 15
                    dmg = 32
                    monster["hp"] = max(0, monster["hp"] - dmg)
                    combat_log = f"CURSE OF DECAY! Ancient hex inflicts {dmg} Dark Magic DMG and rotting flesh!"
                    enemy_turn()
                else:
                    combat_log = "Insufficient Mind for Curse of Decay!"
            elif cursor_idx == 2:  # Head Gnaw
                dmg = 26
                monster["hp"] = max(0, monster["hp"] - dmg)
                h["hp"] = min(h["max_hp"], h["hp"] + 15)
                combat_log = f"HEAD GNAW! Nas'hrah bites into foe for {dmg} Phys DMG and absorbs +15 HP life!"
                enemy_turn()
            elif cursor_idx == 3:  # Mock Foe
                monster["def"] = max(0, monster["def"] // 2)
                combat_log = "MOCK FOE! Nas'hrah insults the foe (-50% enemy DEF, foe enraged)!"
                enemy_turn()

        current_menu = "MAIN"
        cursor_idx = 0

    elif current_menu == "POUCH":
        max_t = hero.get("max_toxicity", 100)

        if cursor_idx == 0:    # Poppy
            if inventory["poppy"] > 0:
                inventory["poppy"] -= 1
                if hero["name"] == "NAS'HRAH":
                    combat_log = "NAS'HRAH SNEERS: 'I have no mortal stomach for your weeds!' (0 HP healed)."
                elif hero.get("toxicity", 0) >= max_t:
                    hero["hp"] = max(1, hero["hp"] - 5)
                    combat_log = f"INTOXICATED! {hero['name']}'s stomach rejects Poppy! Vomited (0 HP healed, -5 toxic DMG)!"
                else:
                    heal_amt = 65 if hero["name"] == "CAHARA" else 50
                    hero["hp"] = min(hero["max_hp"], hero["hp"] + heal_amt)
                    added_tox = 0 if hero["name"] == "MOONLESS" else (15 if hero["name"] == "RAGNVALDR" else 35)
                    hero["toxicity"] = min(max_t, hero.get("toxicity", 0) + added_tox)
                    if "Bleeding (-4 HP/turn)" in hero["debuffs"]:
                        hero["debuffs"].remove("Bleeding (-4 HP/turn)")
                    tox_note = f"+{added_tox}% Tox" if added_tox > 0 else "0% Tox (Canine Gut)"
                    combat_log = f"{hero['name']} consumes Poppy (+{heal_amt} HP, {tox_note} [{hero['toxicity']}%])."
                enemy_turn()
            else:
                combat_log = "Out of White Poppy!"
            current_menu = "MAIN"
            cursor_idx = 0

        elif cursor_idx == 1:  # Weed
            if inventory["weed"] > 0:
                inventory["weed"] -= 1
                if hero["name"] == "NAS'HRAH":
                    combat_log = "NAS'HRAH SNEERS: 'Mortal herbalism is beneath me!' (0 HP healed)."
                elif hero.get("toxicity", 0) >= max_t:
                    hero["hp"] = max(1, hero["hp"] - 5)
                    combat_log = f"INTOXICATED! {hero['name']} overdoses on Weed! Vomited (0 HP healed, -5 toxic DMG)!"
                else:
                    heal_amt = 150 if hero["name"] == "CAHARA" else 120
                    hero["hp"] = min(hero["max_hp"], hero["hp"] + heal_amt)
                    added_tox = 0 if hero["name"] == "MOONLESS" else (25 if hero["name"] == "RAGNVALDR" else 50)
                    hero["toxicity"] = min(max_t, hero.get("toxicity", 0) + added_tox)
                    tox_note = f"+{added_tox}% Tox" if added_tox > 0 else "0% Tox (Canine Gut)"
                    combat_log = f"{hero['name']} uses Herbal Weed (+{heal_amt} HP, {tox_note} [{hero['toxicity']}%])."
                enemy_turn()
            else:
                combat_log = "Out of Herbal Weed!"
            current_menu = "MAIN"
            cursor_idx = 0

        elif cursor_idx == 2:  # Bread
            if inventory["bread"] > 0:
                inventory["bread"] -= 1
                if hero["name"] == "NAS'HRAH":
                    combat_log = "NAS'HRAH requires no mortal bread! Hunger remains 0."
                elif hero["name"] == "RAGNVALDR":
                    hero["hunger"] = max(0, hero["hunger"] - 20)
                    combat_log = "Ragnvaldr eats bread (-20 Hunger - Outlander gut needs raw meat!)."
                elif hero["name"] == "CAHARA":
                    hero["hunger"] = max(0, hero["hunger"] - 50)
                    combat_log = "Cahara eats bread with gourmet relish (-50 Hunger - Deep Pockets buff!)."
                else:
                    hero["hunger"] = max(0, hero["hunger"] - 40)
                    combat_log = f"{hero['name']} eats Moldy Bread (-40 Hunger)."
            else:
                combat_log = "Out of Bread!"
            current_menu = "MAIN"
            cursor_idx = 0

        elif cursor_idx == 3:  # Ale
            if inventory["ale"] > 0:
                inventory["ale"] -= 1
                if hero["name"] == "MOONLESS":
                    combat_log = "Moonless sniffs the vintage ale and growls! Beasts cannot drink alcohol!"
                elif hero["name"] == "NAS'HRAH":
                    hero["mind"] = min(hero["max_mind"], hero["mind"] + 35)
                    hero["hp"] = min(hero["max_hp"], hero["hp"] + 15)
                    hero["buff"] = "DARK ECSTASY (+35 Mind, +15 HP)"
                    combat_log = "Nas'hrah drains the ale in dark ecstasy! (+35 Mind, +15 HP dark vitality)!"
                elif hero["name"] == "LE'GARDE":
                    hero["mind"] = min(hero["max_mind"], hero["mind"] + 35)
                    hero["buff"] = "TACTICAL STIMULANT (+50% ATK 3t)"
                    combat_log = "Le'garde drinks Vintage Ale (+35 Mind, +50% ATK STIMULANT FOR 3 TURNS)!"
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
# ENEMY TURN & DAMAGE RESOLUTION (SOLO SURVIVOR WITH DEFENSE AFFINITIES)
# =============================================================================
def enemy_turn():
    global combat_log, combat_outcome
    hero = active_hero
    hero["hp"] = max(0, hero.get("hp", 0))
    monster["hp"] = max(0, monster.get("hp", 0))
    hero["mind"] = max(0, hero.get("mind", 0))
    hero["toxicity"] = max(0, hero.get("toxicity", 0))

    if monster["hp"] <= 0 or monster.get("debuff_decapitated"):
        combat_log += " | Foe neutralized! VICTORY!"
        combat_outcome = "VICTORY"
        return

    # 1. Frontline auto-detox (The Girl: -10% tox/turn)
    if hero["name"] == "THE GIRL" and hero.get("toxicity", 0) > 0:
        hero["toxicity"] = max(0, hero["toxicity"] - 10)
        combat_log += " | Pure Serenity: The Girl purges -10% toxicity!"

    # 2. Intoxicated nausea check
    max_t = hero.get("max_toxicity", 100)
    if hero.get("toxicity", 0) >= max_t:
        hero["hp"] = max(1, hero["hp"] - 5)
        combat_log += f" | {hero['name']} suffers intoxicated nausea (-5 HP)!"

    # 3. Terror Archetype Dread Aura check
    if monster.get("archetype") == "TERROR":
        if hero["name"] in ("THE GIRL", "NAS'HRAH"):
            combat_log += f" | {hero['name']} repels Dread Aura (0 Mind lost)!"
        else:
            hero["mind"] = max(0, hero["mind"] - 25)
            combat_log += f" | DREAD AURA! Eldritch horror drains -25 Mind from {hero['name']}!"

    # 4. Bleed effect
    if "Bleeding (-4 HP/turn)" in hero["debuffs"]:
        hero["hp"] = max(0, hero["hp"] - 4)

    # 5. Passive: Enki automatically regenerates +5 Mind per turn
    if hero["name"] == "ENKI" and hero["mind"] < hero["max_mind"]:
        hero["mind"] = min(hero["max_mind"], hero["mind"] + 5)

    # 6. Check Dodge
    effective_dodge = hero.get("dodge_rate", 0.10)
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

    # 7. Incoming Damage calculation with character physical/magic multipliers
    base_atk = monster["atk"]
    if monster.get("archetype") == "AMBUSHER" and not hero["is_guarding"]:
        base_atk = int(base_atk * 1.5)

    if hero["name"] == "THE GIRL":
        base_atk = int(base_atk * 0.70)
    if "DISTRACTED (-50% ATK)" in monster.get("temp_debuff", ""):
        base_atk = int(base_atk * 0.50)
        monster["temp_debuff"] = ""

    dmg = base_atk - (hero["def"] // 2)

    # Apply character defense affinity (D'arce -35%, Ragnvaldr -15%, Enki +30% fragile, Nas'hrah +20%)
    phys_mult = hero.get("phys_mult", 1.0)
    dmg = int(dmg * phys_mult)

    if hero["is_guarding"]:
        dmg = int(dmg * 0.25)
        hero["is_guarding"] = False

    dmg = max(3, dmg)
    hero["hp"] = max(0, hero["hp"] - dmg)
    ambush_tag = " [LETHAL AMBUSH]" if (monster.get("archetype") == "AMBUSHER" and not hero["is_guarding"]) else ""
    combat_log += f" | Foe strikes{ambush_tag}! {hero['name']} takes {dmg} DMG."

    # Chance foe inflicts bleeding scratch (Nas'hrah immune)
    if random.random() < 0.35 and hero["name"] != "NAS'HRAH" and "Bleeding (-4 HP/turn)" not in hero["debuffs"]:
        hero["debuffs"].append("Bleeding (-4 HP/turn)")
        combat_log += " Claws inflict Bleeding (-4 HP/turn)!"

    # Down check
    if hero["hp"] == 0:
        combat_log += f" | {hero['name']} has fallen in the dark catacombs! DEFEAT!"
        combat_outcome = "DEFEAT"

# =============================================================================
# MAIN INTERACTIVE LOOP
# =============================================================================
def run_interactive_loop():
    global current_menu, cursor_idx, combat_outcome

    # Clear screen once on entry and hide cursor
    sys.stdout.write("\033[2J\033[H\033[?25l")
    sys.stdout.flush()

    while True:
        if combat_outcome is not None:
            render_screen()
            time.sleep(1.0)
            return combat_outcome, active_hero, inventory

        render_screen()
        menu_data = get_current_menu_data()
        num_options = len(menu_data["options"])

        if os.name == 'nt' and sys.stdin.isatty():
            ch = msvcrt.getch()
            while msvcrt.kbhit():
                discard = msvcrt.getch()

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
                sys.stdout.write("\033[?25h\n[OK] Exited Solo Combat Arena.\n")
                return "QUIT", active_hero, inventory
            elif ch in (b'1', b'2', b'3', b'4', b'5', b'6'):
                num = int(ch.decode('ascii')) - 1
                if num < num_options:
                    cursor_idx = num
                    handle_selection()
        else:
            raw = sys.stdin.readline()
            if not raw:
                break
            line = raw.strip().lower()
            if line == 'w':
                cursor_idx = (cursor_idx - 1) % num_options
            elif line == 's':
                cursor_idx = (cursor_idx + 1) % num_options
            elif line in ('', 'c', 'enter'):
                handle_selection()
            elif line in ('b', 'q'):
                return "QUIT", active_hero, inventory

    return combat_outcome or "QUIT", active_hero, inventory

def run_solo_combat(hero_obj, monster_id=8, monster_name="SHADOW SWORDSMAN", monster_archetype="ARMORED", monster_hp=95, monster_atk=24, monster_def=99, inv=None):
    global active_hero, monster, inventory, combat_log, current_menu, cursor_idx, combat_outcome
    active_hero = copy.deepcopy(hero_obj)
    active_hero["is_guarding"] = False
    active_hero["buff"] = active_hero.get("buff", "")
    active_hero["debuffs"] = active_hero.get("debuffs", [])

    if inv is not None:
        inventory = dict(inv)
    else:
        if active_hero["name"] == "CAHARA":
            inventory = {"poppy": 5, "weed": 3, "bread": 6, "ale": 3}
        else:
            inventory = {"poppy": 3, "weed": 2, "bread": 4, "ale": 2}

    monster = {
        "name": monster_name,
        "id": monster_id,
        "archetype": monster_archetype,
        "hp": monster_hp,
        "max_hp": monster_hp,
        "atk": monster_atk,
        "def": monster_def,
        "debuff_arm_r": False,
        "debuff_arm_l": False,
        "debuff_legs": False,
        "debuff_decapitated": False
    }

    combat_log = f"Battle initiated! {monster_name} unsheathes weapon!"
    current_menu = "MAIN"
    cursor_idx = 0
    combat_outcome = None

    return run_interactive_loop()

# =============================================================================
# SHOWCASE AUTO TRACE
# =============================================================================
def run_showcase_trace():
    print("\n>>> STARTING SOLO EXPLORER COMBAT ARENA SHOWCASE <<<\n")
    # Step 0: Render Solo Selection screen
    render_solo_select_screen(0)
    time.sleep(1.2)
    render_solo_select_screen(1)
    time.sleep(1.0)
    render_solo_select_screen(2)
    time.sleep(1.0)

    global current_menu, cursor_idx, active_hero, combat_log
    active_hero = copy.deepcopy(ALL_HEROES[1]) # Showcase as D'ARCE
    active_hero["buff"] = ""
    active_hero["is_guarding"] = False
    active_hero["debuffs"] = []

    states = [
        ("MAIN", 0, "SOLO STEP 1: D'arce steps into the arena alone with +35% Physical Armor!"),
        ("TARGET_LIMB", 1, "SOLO STEP 2: Armored Foe confronts D'arce -> Holy Smite shatters armor (x1.4 DMG)!"),
        ("SKILL", 1, "SOLO STEP 3: D'arce casts Healing Prayer -> Restores +45 HP with 0% drug toxicity!"),
        ("SKILL", 0, "SOLO STEP 4: Foe prepares heavy strike -> D'arce assumes Defense Stance (+15 HP, -75% DMG)!"),
        ("TARGET_LIMB", 4, "SOLO STEP 5: D'arce strikes Legs -> Foe legs broken, forced into crouch!"),
        ("TARGET_LIMB", 0, "SOLO STEP 6: Clean Decapitation on crouched opponent -> SOLO VICTORY!")
    ]

    for idx, (m_state, c_idx, step_desc) in enumerate(states):
        current_menu = m_state
        cursor_idx = c_idx

        if idx == 0:
            monster["name"] = "DARK KNIGHT"
            monster["archetype"] = "ARMORED"
            monster["hp"] = 90
            combat_log = "SOLO RUN ENGAGED! D'arce stands alone against Dark Knight (Armored)."
        elif idx == 1:
            monster["hp"] = 34
            monster["archetype"] = "NORMAL"
            monster["def"] = 14
            combat_log = "HOLY SMITE! D'arce's holy blade fractures heavy armor for 56 DMG! Defense shattered!"
        elif idx == 2:
            active_hero["hp"] = min(active_hero["max_hp"], active_hero["hp"] + 45)
            combat_log = "HEALING PRAYER! Sacred light restores +45 HP with 0% DRUG TOXICITY!"
        elif idx == 3:
            active_hero["is_guarding"] = True
            active_hero["hp"] = min(active_hero["max_hp"], active_hero["hp"] + 15)
            active_hero["buff"] = "IRON VOW (-75% DMG)"
            combat_log = "DEFENSE STANCE! Tower shield braced (+15 HP, -75% incoming damage)!"
        elif idx == 4:
            monster["hp"] = 12
            monster["debuff_legs"] = True
            combat_log = "LEGS BROKEN! Foe collapses to dungeon floor -> 100% HEAD HIT RATE!"
        elif idx == 5:
            monster["hp"] = 0
            monster["debuff_decapitated"] = True
            combat_log = "DECAPITATION! Blade severs neck! Foe neutralized! SOLO VICTORY!"

        render_screen()
        print(f"\n  \033[1;32m>>> [SHOWCASE]: {step_desc} <<<\033[0m")
        time.sleep(1.0)

    sys.stdout.write("\033[?25h\n")
    sys.stdout.flush()

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--showcase":
        run_showcase_trace()
    elif len(sys.argv) > 1 and sys.argv[1] == "--select":
        run_solo_select_interactive()
        run_interactive_loop()
    else:
        # Default: First show Solo Character Selector, then launch Solo Combat Arena!
        run_solo_select_interactive()
        run_interactive_loop()
