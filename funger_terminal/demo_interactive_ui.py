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
        os.system('mode con: cols=100 lines=36 >nul 2>&1')
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
ALL_MONSTER_SPRITES = {}
try:
    sprite_json_path = os.path.join(os.path.dirname(__file__), "extracted_sprites.json")
    if os.path.exists(sprite_json_path):
        with open(sprite_json_path, "r", encoding="utf-8") as f:
            sp_data = json.load(f)
            HERO_SPRITES = sp_data.get("heroes", {})
            RAW_MONSTER_8 = sp_data.get("monster_8", [])
    mon_json_path = os.path.join(os.path.dirname(__file__), "all_monster_sprites.json")
    if os.path.exists(mon_json_path):
        with open(mon_json_path, "r", encoding="utf-8") as f:
            ALL_MONSTER_SPRITES = json.load(f)
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
    return pad_str(" " * 6 + sp_line, 42)

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
            {"label": "TWIN DAGGERS", "desc": "-> 12 Mind | Rapid dual slice: 38 Phys DMG"},
            {"label": "POISON DART",  "desc": "-> 15 Mind | Occult Chem: 28 Magic DMG (Poisons foe)"},
            {"label": "STEAL ITEM",   "desc": "-> 15 Mind | Pickpocket: Steal 1 Poppy/Bread from target"},
            {"label": "SMOKE BOMB",   "desc": "-> 20 Mind | Blind opponent: 100% flee battle immediately"}
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
            {"label": "DEFENSE STANCE", "desc": "-> 10 Mind | Tower shield: -75% DMG & +15 HP"},
            {"label": "HEALING PRAYER", "desc": "-> 20 Mind | Restore +45 HP with 0% TOXICITY!"},
            {"label": "HOLY SMITE",     "desc": "-> 22 Mind | Sanctified cleave: 44 DMG (x1.4 vs Armor/Undead)"},
            {"label": "KNIGHT CHARGE",  "desc": "-> 12 Mind, -8 HP Recoil | Heavy shield bash: 38 Phys DMG"}
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
            {"label": "BLACK ORB",       "desc": "-> 25 Mind | 52 True Magic DMG (Pierces DEF, x1.5 Spectral)"},
            {"label": "RITUAL DAGGER",   "desc": "-> 0 Mind | Sacrificial thrust: 20 DMG, siphons +15 Mind"},
            {"label": "BLOOD SACRIFICE", "desc": "-> -20 HP | Convert flesh into +40 Mind points"},
            {"label": "HEXEN BIND",      "desc": "-> 15 Mind | Paralyze foe limbs, guaranteed head hit"}
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
            {"label": "WAR AXE",      "desc": "-> 14 Mind (or -15 HP) | Brutal cleave: 48 Phys DMG"},
            {"label": "SPIRIT TOTEM", "desc": "-> 16 Mind | Ancestral Spirit Magic: 32 Spirit DMG"},
            {"label": "FERAL ROAR",   "desc": "-> 14 Mind | Terrifying war cry: lowers foe ATK by 40%"},
            {"label": "DEVOUR FLESH", "desc": "-> +15% Toxicity | Consume raw meat: +35 HP, -25 Hunger"}
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
            {"label": "FENCING THRUST",   "desc": "-> 12 Mind | Precision rapier thrust: 38 piercing Phys DMG"},
            {"label": "LEGION LIGHT",     "desc": "-> 20 Mind | Solar Magic: 35 Magic DMG + lowers foe ACC"},
            {"label": "TACTICAL FOCUS",   "desc": "-> 15 Mind | Focus strike: +50% DMG on next strike"},
            {"label": "WAR CRY",          "desc": "-> 14 Mind | Shatters 35% of enemy DEF, +10 Mind"}
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
            {"label": "FERAL BITE",    "desc": "-> +15 Hunger | Savage jaw crunch: 40 Phys DMG + Bleed"},
            {"label": "MOON HOWL",     "desc": "-> 15 Mind | Lunar Magic: 30 Magic DMG + 45% crouch foe"},
            {"label": "SHADOW POUNCE", "desc": "-> 12 Mind | Leap attack: 35 DMG (55 DMG on crouched foe)"},
            {"label": "SCENT DANGER",  "desc": "-> 10 Mind | Danger scent: +35% evasion for 2 turns"}
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
            {"label": "NIMBLE DODGE",   "desc": "-> 12 Mind | Duck into shadows: 100% dodge enemy next hit"},
            {"label": "LOVING EMBRACE", "desc": "-> 15 Mind | Comfort self: restore +35 HP & dispel terror"},
            {"label": "PURE LIGHT",     "desc": "-> 20 Mind | Holy Radiance: 32 Magic DMG (x1.6 vs dark/ghosts)"},
            {"label": "DISTRACT FOE",   "desc": "-> 10 Mind | Wave lantern: enemy attack power halved 50%"}
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
            {"label": "COMBUSTION",      "desc": "-> 25 Mind | Gro-goroth flame: 62 Unstoppable Fire DMG"},
            {"label": "CURSE OF DECAY",  "desc": "-> 20 Mind | Hex: 32 Dark Magic DMG + rotting flesh DoT"},
            {"label": "HEAD GNAW",       "desc": "-> 0 Mind | Flying tooth bite: 24 Phys DMG, siphons +15 HP"},
            {"label": "MOCK FOE",        "desc": "-> 15 Mind | Insults foe: strips 50% enemy DEF"}
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

def clear_screen():
    if os.name == 'nt':
        os.system('cls')
    sys.stdout.write("\033[2J\033[3J\033[H\033[?25l")
    sys.stdout.flush()

def atomic_blit(screen_rows):
    """Blits entire screen atomically via cursor home to eliminate flicker 100%."""
    formatted = [fit_100_cols(r) for r in screen_rows]
    frame_str = "\033[H" + "\n".join(formatted) + "\033[J"
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
        "\033[1;30m+" + "=" * 98 + "+\033[0m",
        f"\033[1;30m| \033[1;37m{fit_ansi('FEAR & HUNGER: SOLO SURVIVOR EXPEDITION - SELECT YOUR EXPLORER', 96)}\033[1;30m |\033[0m",
        "\033[1;30m+" + "=" * 98 + "+\033[0m",
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
    all_rows.append("\033[1;30m+" + "=" * 98 + "+\033[0m")

    atomic_blit(all_rows)

def run_solo_select_interactive():
    global active_hero, inventory

    # Clear screen cleanly on entry and hide cursor
    clear_screen()

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
                clear_screen()
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
                clear_screen()
                sys.stdout.write("\033[?25h\n[OK] Exited Solo Selection.\n")
                return None, -1
            elif ch in (b'1', b'2', b'3', b'4', b'5', b'6', b'7', b'8'):
                sel_idx = int(ch.decode('ascii')) - 1
                render_solo_select_screen(sel_idx)
        else:
            line = sys.stdin.readline().strip().lower()
            if line in ('w', 'up'):
                sel_idx = (sel_idx - 1) % num_heroes
            elif line in ('s', 'down'):
                sel_idx = (sel_idx + 1) % num_heroes
            elif line in ('1', '2', '3', '4', '5', '6', '7', '8'):
                sel_idx = int(line) - 1
                render_solo_select_screen(sel_idx)
            elif line in ('', 'enter', 'select', 'c'):
                clear_screen()
                active_hero = copy.deepcopy(ALL_HEROES[sel_idx])
                if active_hero["name"] == "CAHARA":
                    inventory = {"poppy": 5, "weed": 3, "bread": 6, "ale": 3}
                else:
                    inventory = {"poppy": 3, "weed": 2, "bread": 4, "ale": 2}
                return active_hero, sel_idx
            elif line in ('q', 'quit'):
                clear_screen()
                return None, -1
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
    # MAIN HEADER (EXACT 100 COLS)
    # -------------------------------------------------------------------------
    title_str = f"FEAR & HUNGER: SOLO SURVIVOR COMBAT ARENA - {hero['name']} [{hero['role']}]"
    if current_menu == "POUCH":
        rem_len = max(0, 94 - display_width(title_str))
        screen_rows.append(f"\033[1;30m+[ \033[1;37m{title_str}\033[1;30m ]" + "-" * rem_len + "+\033[0m")
    else:
        screen_rows.append("\033[1;30m+" + "=" * 98 + "+\033[0m")
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

    mid_str = str(monster.get("id", 8))
    mon_data = ALL_MONSTER_SPRITES.get(mid_str)
    if mon_data:
        if monster.get("debuff_decapitated") or monster.get("hp", 1) <= 0:
            m_sprite = mon_data.get("dead", mon_data.get("normal", []))
            m_model_sub = "\033[90m[NEUTRALIZED]\033[0m"
        elif monster.get("debuff_legs") or monster.get("debuff_arm_r") or monster.get("debuff_arm_l") or monster.get("hp", 100) <= (monster.get("max_hp", 100) * 0.5):
            m_sprite = mon_data.get("injured", mon_data.get("normal", []))
            m_model_sub = "\033[1;33m[INJURED / POSTURE COLLAPSE]\033[0m"
        else:
            m_sprite = mon_data.get("normal", [])
            m_model_sub = ""
    else:
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
        make_card_row(f"  POSTUR: {m_model_sub if m_model_sub else '\033[1;32m[NORMAL COMBAT POSTURE]\033[0m'}", c_mcard),
        make_card_row(f"  COMBAT: \033[1;31mATK: {monster.get('atk', 20):2d} DMG\033[0m | \033[1;36mDEF: {monster.get('def', 10):2d}\033[0m", c_mcard),
    ]
    if current_menu not in ("POUCH", "TARGET_LIMB"):
        m_card_rows.append(make_card_row("", c_mcard))
    m_card_rows.append(m_border)

    m_model_rows = [
        pad_str(f"     \033[1;31m[ENEMY]\033[0m {m_model_sub}", 42)
    ]
    # Dynamic sprite windowing: strip leading empty lines so injured/crouched sprites show full body
    v_start = 0
    for idx, r in enumerate(m_sprite):
        if ANSI_REGEX.sub('', r).strip():
            v_start = idx
            break
    sprite_limit = 7 if current_menu in ("POUCH", "TARGET_LIMB") else 8
    sprite_window = m_sprite[v_start : v_start + sprite_limit]
    for r in range(sprite_limit):
        sp = sprite_window[r] if r < len(sprite_window) else " " * 24
        m_model_rows.append(format_model_row(sp))

    z1_height = 8 if current_menu in ("POUCH", "TARGET_LIMB") else 9
    for r_idx in range(z1_height):
        screen_rows.append(f"{m_card_rows[r_idx]}    {m_model_rows[r_idx]}\033[0m")

    # -------------------------------------------------------------------------
    # ZONE 2: SOLO HERO ZONE (11 ROWS, EXACT 100 COLS - FULL INTACT MODEL)
    # Left: Hero Sprite Model (42 cols, FULL 11 ROWS!) | Gap: 4 | Right: Card (54 cols)
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

    # Only show status when an actual buff/debuff exists; otherwise show passive
    if hero.get("debuffs"):
        h_status = f"\033[1;31m  STATUS: {', '.join(hero['debuffs'])}\033[0m"
    elif hero.get("buff"):
        h_status = f"\033[1;32m  STATUS: {hero['buff']}\033[0m"
    else:
        h_status = f"\033[1;36m  PASSIV: {hero['passive'][:42]}\033[0m"

    stance_desc = "\033[1;32m  STANCE: Defensive Guard (-70% Incoming DMG)\033[0m" if hero.get("is_guarding") else "\033[90m  STANCE: Balanced Combat Stance\033[0m"

    h_card_rows = [
        h_border,
        make_card_row(f"\033[1;32m  HERO  : {hero['name']:<9} \033[90m[{hero['role']}]\033[0m", c_hcard),
        make_card_row(f"  HP    : {h_hp_bar} \033[1;32m{hero['hp']:3d}/{hero['max_hp']:3d} ({h_pct:3d}%)\033[0m", c_hcard),
        make_card_row(f"  MIND  : {h_mnd_bar} \033[1;36m{hero['mind']:3d}/{hero['max_mind']:3d}\033[0m | \033[90mTOXIC:\033[0m \033[1;{'31' if h_tox >= max_t else '32'}m{h_tox:2d}%\033[0m {tox_badge}", c_hcard),
        make_card_row(f"  ARMOR : \033[1;37m{hero['phys_resist_str'][:20]}\033[0m | \033[1;35m{int(hero['dodge_rate']*100)}% Dodge\033[0m", c_hcard),
        make_card_row(f"  MAG-R : \033[1;37m{hero['magic_resist_str'][:20]}\033[0m | \033[1;31mATK: {hero['atk']:2d} DMG\033[0m", c_hcard),
        make_card_row(f"  TRAIT : \033[1;33m{hero['trait'][:42]}\033[0m", c_hcard),
        make_card_row(f"  SKILLS: \033[1;36m{hero['skills'][0]['label'][:18]}\033[0m / \033[1;36m{hero['skills'][1]['label'][:18]}\033[0m", c_hcard),
        make_card_row(h_status, c_hcard),
        make_card_row(stance_desc, c_hcard),
        h_border
    ]

    h_model_rows = []
    for r in range(11):
        sp = h_sprite[r] if r < len(h_sprite) else " " * 29
        h_model_rows.append(format_model_row(sp))

    for r_idx in range(11):
        screen_rows.append(f"{h_model_rows[r_idx]}    {h_card_rows[r_idx]}\033[0m")

    # -------------------------------------------------------------------------
    # SECTION 3: COMBAT LOG BOX (3 ROWS, EXACT 100 COLS)
    # -------------------------------------------------------------------------
    screen_rows.append("\033[1;30m+" + "-" * 98 + "+\033[0m")
    log_text = f"\033[1;33m[LOG]\033[0m \033[1;37m{combat_log}\033[0m"
    screen_rows.append(f"\033[1;30m| \033[0m{fit_ansi(log_text, 96)}\033[1;30m |\033[0m")
    screen_rows.append("\033[1;30m+" + "-" * 98 + "+\033[0m")

    # -------------------------------------------------------------------------
    # SECTION 4: COMBAT COMMANDS MENU (EXACT 100 COLS)
    # -------------------------------------------------------------------------
    menu_data = get_current_menu_data()
    title = menu_data["title"]
    options = menu_data["options"]

    screen_rows.append(f"  \033[1;37m{title}\033[0m")
    if current_menu == "POUCH":
        for idx, opt in enumerate(options):
            is_sel = (idx == cursor_idx)
            name_str = opt.get("label", "")
            tag_str = opt.get("tag", "")
            desc_str = opt.get("desc", "")
            qty_val = opt.get("qty", 0)

            if opt.get("id") == "close":
                qty_str = "      "
                avail = True
            else:
                qty_str = f"[x {qty_val}]"
                avail = (qty_val > 0)

            num_str = f"[{idx+1}]"

            if is_sel:
                cur_icon = "▶"
                color = "\033[1;33m"
                cur_color = "\033[1;33m"
            elif avail:
                cur_icon = " "
                color = "\033[1;37m"
                cur_color = "\033[90m"
            else:
                cur_icon = " "
                color = "\033[90m"
                cur_color = "\033[90m"

            line = f"  {cur_color}{cur_icon}\033[0m {color}{num_str:<4} {name_str:<18} {qty_str:<7} {tag_str:<13} {desc_str}\033[0m"
            screen_rows.append(fit_ansi(line, 98))
    else:
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
    screen_rows.append("\033[1;30m" + "=" * 100 + "\033[0m")
    if current_menu == "MAIN":
        screen_rows.append("  \033[90m[CONTROLS]:\033[0m \033[1;37m[W/S / 1-5]\033[0m Navigate  |  \033[1;37m[Enter/Space]\033[0m Select  |  \033[1;31m[Q]\033[0m Quit")
    elif current_menu == "POUCH":
        screen_rows.append("  \033[90m[CONTROLS]:\033[0m \033[1;37m[W/S / 1-8]\033[0m Di chuyển  |  \033[1;32m[Enter/Space]\033[0m Sử dụng  |  \033[1;33m[B/Esc/8]\033[0m Quay lại")
    else:
        screen_rows.append("  \033[90m[CONTROLS]:\033[0m \033[1;37m[W/S / 1-6]\033[0m Navigate  |  \033[1;37m[Enter/Space]\033[0m Confirm  |  \033[1;33m[B/Esc]\033[0m Back")
    screen_rows.append("\033[1;30m" + "=" * 100 + "\033[0m")

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
        p_opts = [
            {
                "id": "totem",
                "label": "TOTEM OF UNDYING",
                "tag": "[CỔ VẬT]",
                "qty": inventory.get("totem", 0),
                "desc": "Hồi sinh khi chết, đầy HP & mọc lại tứ chi"
            },
            {
                "id": "poppy",
                "label": "POPPY FLOWER",
                "tag": "[DƯỢC LIỆU]",
                "qty": inventory.get("poppy", 0),
                "desc": "Hồi +50 HP & cầm máu"
            },
            {
                "id": "weed",
                "label": "MEDICINAL HERB",
                "tag": "[THẢO DƯỢC]",
                "qty": inventory.get("weed", 0),
                "desc": "Hồi +120 HP, giảm đau nhức"
            },
            {
                "id": "bread",
                "label": "MOLDY BREAD",
                "tag": "[LƯƠNG KHÔ]",
                "qty": inventory.get("bread", 0),
                "desc": "Giảm -40 Đói (chống kiệt sức)"
            },
            {
                "id": "meat",
                "label": "DRIED MEAT",
                "tag": "[LƯƠNG KHÔ]",
                "qty": inventory.get("meat", 0),
                "desc": "Giảm -60 Đói & hồi +20 HP"
            },
            {
                "id": "vial",
                "label": "ALCHEMICAL VIAL",
                "tag": "[CỒN THUỐC]",
                "qty": inventory.get("vial", inventory.get("ale", 0)),
                "desc": "Hồi +35 Mind, tẩy độc & hoại tử"
            },
            {
                "id": "key",
                "label": "RUNIC KEY",
                "tag": "[CHÌA KHÓA]",
                "qty": inventory.get("key", 0),
                "desc": "Chìa khóa Cổng Đông (cần 3 chìa)"
            },
            {
                "id": "close",
                "label": "[ ĐÓNG TÚI ĐỒ ]",
                "tag": "[QUAY LẠI]",
                "qty": 0,
                "desc": "Quay lại"
            }
        ]
        return {
            "title": "TÚI ĐỒ SINH TỒN - SURVIVAL POUCH & INVENTORY SUPPLIES",
            "options": p_opts
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
            if cursor_idx == 0:    # Twin Daggers (Cost: 12 Mind)
                if h.get("mind", 0) >= 12:
                    h["mind"] -= 12
                    dmg = 38
                    monster["hp"] = max(0, monster["hp"] - dmg)
                    combat_log = f"TWIN DAGGERS! (-12 Mind) Cahara strikes with rapid dual thrusts for {dmg} DMG!"
                    enemy_turn()
                else:
                    combat_log = f"\033[1;31m[INSUFFICIENT MIND]: Twin Daggers requires 12 Mind (Have: {h.get('mind', 0)}). Drink Vintage Ale!\033[0m"
                    return
            elif cursor_idx == 1:  # Poison Dart (Cost: 15 Mind)
                if h.get("mind", 0) >= 15:
                    h["mind"] -= 15
                    dmg = 28
                    monster["hp"] = max(0, monster["hp"] - dmg)
                    monster["atk"] = max(4, monster.get("atk", 20) - 5)
                    combat_log = f"POISON DART! (-15 Mind) Toxic alchemy deals {dmg} Chem DMG and weakens foe (-5 ATK)!"
                    enemy_turn()
                else:
                    combat_log = f"\033[1;31m[INSUFFICIENT MIND]: Poison Dart requires 15 Mind (Have: {h.get('mind', 0)}). Drink Vintage Ale!\033[0m"
                    return
            elif cursor_idx == 2:  # Steal Item (Cost: 15 Mind)
                if h.get("mind", 0) >= 15:
                    h["mind"] -= 15
                    stolen_item = "poppy" if random.random() < 0.5 else "bread"
                    cap = h.get("bag_cap", 10)
                    if inventory[stolen_item] < cap:
                        inventory[stolen_item] += 1
                    combat_log = f"STEAL SUCCESS! (-15 Mind) Pickpocketed 1x {stolen_item.upper()} from target!"
                    enemy_turn()
                else:
                    combat_log = f"\033[1;31m[INSUFFICIENT MIND]: Steal requires 15 Mind (Have: {h.get('mind', 0)}). Drink Vintage Ale!\033[0m"
                    return
            elif cursor_idx == 3:  # Smoke Bomb (Cost: 20 Mind)
                if h.get("mind", 0) >= 20:
                    h["mind"] -= 20
                    combat_log = "SMOKE BOMB! (-20 Mind) Dense fog blinds opponent. 100% ESCAPE SUCCESSFUL!"
                    combat_outcome = "FLEE"
                else:
                    combat_log = f"\033[1;31m[INSUFFICIENT MIND]: Smoke Bomb requires 20 Mind (Have: {h.get('mind', 0)}). Drink Vintage Ale!\033[0m"
                    return

        elif h["name"] == "D'ARCE":
            if cursor_idx == 0:    # Defense stance (Cost: 10 Mind)
                if h.get("mind", 0) >= 10:
                    h["mind"] -= 10
                    h["is_guarding"] = True
                    h["hp"] = min(h["max_hp"], h["hp"] + 15)
                    h["buff"] = "IRON VOW (-75% DMG)"
                    combat_log = "DEFENSE STANCE! (-10 Mind) D'arce braces tower shield (+15 HP, -75% incoming DMG)!"
                    enemy_turn()
                else:
                    combat_log = f"\033[1;31m[INSUFFICIENT MIND]: Defense Stance requires 10 Mind (Have: {h.get('mind', 0)}).\033[0m"
                    return
            elif cursor_idx == 1:  # Healing prayer (Cost: 20 Mind)
                if h.get("mind", 0) >= 20:
                    h["mind"] -= 20
                    h["hp"] = min(h["max_hp"], h["hp"] + 45)
                    combat_log = "HEALING PRAYER! (-20 Mind) Sacred divine light restores +45 HP with 0% TOXICITY!"
                    enemy_turn()
                else:
                    combat_log = f"\033[1;31m[INSUFFICIENT MIND]: Healing Prayer requires 20 Mind (Have: {h.get('mind', 0)}).\033[0m"
                    return
            elif cursor_idx == 2:  # Holy smite (Cost: 22 Mind)
                if h.get("mind", 0) >= 22:
                    h["mind"] -= 22
                    dmg = 44
                    if monster.get("archetype") == "ARMORED":
                        dmg = 56
                        monster["archetype"] = "NORMAL"
                        monster["def"] = 14
                        combat_log = f"ARMOR SHATTERED! (-22 Mind) Holy Smite fractures steel plate for {dmg} DMG! DEF shattered!"
                    elif monster.get("archetype") == "SPECTRAL":
                        dmg = 52
                        combat_log = f"SACRED RADIANCE! (-22 Mind) Holy Smite incinerates spectral ghost for {dmg} Divine DMG!"
                    else:
                        combat_log = f"HOLY SMITE! (-22 Mind) Heavy sanctified cleave inflicts {dmg} DMG!"
                    monster["hp"] = max(0, monster["hp"] - dmg)
                    enemy_turn()
                else:
                    combat_log = f"\033[1;31m[INSUFFICIENT MIND]: Holy Smite requires 22 Mind (Have: {h.get('mind', 0)}).\033[0m"
                    return
            elif cursor_idx == 3:  # Knight Charge (Cost: 12 Mind + 8 Recoil HP)
                if h.get("mind", 0) >= 12:
                    h["mind"] -= 12
                    h["hp"] = max(1, h["hp"] - 8)
                    dmg = 38
                    monster["hp"] = max(0, monster["hp"] - dmg)
                    combat_log = f"KNIGHT CHARGE! (-12 Mind, -8 Recoil HP) D'arce slams forward with tower shield for {dmg} DMG!"
                    enemy_turn()
                else:
                    combat_log = f"\033[1;31m[INSUFFICIENT MIND]: Knight Charge requires 12 Mind (Have: {h.get('mind', 0)}).\033[0m"
                    return

        elif h["name"] == "ENKI":
            if cursor_idx == 0:    # Black orb (Cost: 25 Mind)
                if h.get("mind", 0) >= 25:
                    h["mind"] -= 25
                    dmg = 52
                    if monster.get("archetype") in ("SPECTRAL", "ARMORED"):
                        dmg = int(dmg * 1.5)
                    monster["hp"] = max(0, monster["hp"] - dmg)
                    combat_log = f"BLACK ORB! (-25 Mind) Dark sphere pierces 100% defense for {dmg} True Magic DMG!"
                    enemy_turn()
                else:
                    combat_log = f"\033[1;31m[INSUFFICIENT MIND]: Black Orb requires 25 Mind (Have: {h.get('mind', 0)}).\033[0m"
                    return
            elif cursor_idx == 1:  # Ritual Dagger (0 Mind Cost, Siphons +15 Mind)
                dmg = 20
                monster["hp"] = max(0, monster["hp"] - dmg)
                h["mind"] = min(h["max_mind"], h.get("mind", 0) + 15)
                combat_log = f"RITUAL DAGGER! Enki slices foe for {dmg} Phys DMG and siphons +15 Mind!"
                enemy_turn()
            elif cursor_idx == 2:  # Blood sacrifice (-20 HP -> +40 Mind)
                if h["hp"] > 20:
                    h["hp"] -= 20
                    h["mind"] = min(h["max_mind"], h.get("mind", 0) + 40)
                    combat_log = "BLOOD SACRIFICE! Enki cuts own flesh (-20 HP) to harvest +40 Mind!"
                    enemy_turn()
                else:
                    combat_log = "\033[1;31m[HP TOO LOW]: Need >20 HP for Blood Sacrifice!\033[0m"
                    return
            elif cursor_idx == 3:  # Hexen bind (Cost: 15 Mind)
                if h.get("mind", 0) >= 15:
                    h["mind"] -= 15
                    monster["debuff_legs"] = True
                    combat_log = "HEXEN BIND! (-15 Mind) Occult shadows root the foe to floor (100% Head hit rate)!"
                    enemy_turn()
                else:
                    combat_log = f"\033[1;31m[INSUFFICIENT MIND]: Hexen Bind requires 15 Mind (Have: {h.get('mind', 0)}).\033[0m"
                    return

        elif h["name"] == "RAGNVALDR":
            if cursor_idx == 0:    # War Axe (Cost: 14 Mind, or 15 HP Blood Price if Mind < 14)
                if h.get("mind", 0) >= 14:
                    h["mind"] -= 14
                    cost_msg = "(-14 Mind)"
                else:
                    h["hp"] = max(1, h["hp"] - 15)
                    cost_msg = "(-15 HP Blood Price!)"
                dmg = 48
                if "BLOODLUST" in h.get("buff", "") or h["hp"] < (h["max_hp"] * 0.35):
                    dmg = int(dmg * 1.5)
                monster["hp"] = max(0, monster["hp"] - dmg)
                combat_log = f"WAR AXE! {cost_msg} Ragnvaldr buries heavy axe into foe for {dmg} brutal Phys DMG!"
                enemy_turn()
            elif cursor_idx == 1:  # Spirit Totem (Cost: 16 Mind)
                if h.get("mind", 0) >= 16:
                    h["mind"] -= 16
                    dmg = 32
                    monster["hp"] = max(0, monster["hp"] - dmg)
                    combat_log = f"SPIRIT TOTEM! (-16 Mind) Northern ancestral spirits crush foe for {dmg} Spirit Magic DMG!"
                    enemy_turn()
                else:
                    combat_log = f"\033[1;31m[INSUFFICIENT MIND]: Spirit Totem requires 16 Mind (Have: {h.get('mind', 0)}).\033[0m"
                    return
            elif cursor_idx == 2:  # Feral Roar (Cost: 14 Mind)
                if h.get("mind", 0) >= 14:
                    h["mind"] -= 14
                    monster["atk"] = max(6, int(monster["atk"] * 0.6))
                    combat_log = "FERAL ROAR! (-14 Mind) Barbarian roar intimidates foe (-40% enemy ATK power)!"
                    enemy_turn()
                else:
                    combat_log = f"\033[1;31m[INSUFFICIENT MIND]: Feral Roar requires 14 Mind (Have: {h.get('mind', 0)}).\033[0m"
                    return
            elif cursor_idx == 3:  # Devour Flesh (+15% Toxicity, +35 HP, -25 Hunger)
                max_tox = h.get("max_toxicity", 150)
                h["toxicity"] = min(max_tox, h.get("toxicity", 0) + 15)
                h["hp"] = min(h["max_hp"], h["hp"] + 35)
                h["hunger"] = max(0, h.get("hunger", 0) - 25)
                combat_log = "DEVOUR FLESH! (+15% Toxicity) Ragnvaldr consumes raw meat (+35 HP, -25 Hunger)!"
                enemy_turn()

        elif h["name"] == "LE'GARDE":
            if cursor_idx == 0:    # Fencing Thrust (Cost: 12 Mind)
                if h.get("mind", 0) >= 12:
                    h["mind"] -= 12
                    dmg = 38
                    if "TACTICAL FOCUS" in h.get("buff", ""):
                        dmg = int(dmg * 1.5)
                        h["buff"] = ""
                    monster["hp"] = max(0, monster["hp"] - dmg)
                    combat_log = f"FENCING THRUST! (-12 Mind) Precision rapier thrust deals {dmg} piercing Phys DMG!"
                    enemy_turn()
                else:
                    combat_log = f"\033[1;31m[INSUFFICIENT MIND]: Fencing Thrust requires 12 Mind (Have: {h.get('mind', 0)}).\033[0m"
                    return
            elif cursor_idx == 1:  # Legion Light (Cost: 20 Mind)
                if h.get("mind", 0) >= 20:
                    h["mind"] -= 20
                    dmg = 35
                    monster["hp"] = max(0, monster["hp"] - dmg)
                    combat_log = f"LEGION LIGHT! (-20 Mind) Blinding solar ray burns foe for {dmg} Solar Magic DMG!"
                    enemy_turn()
                else:
                    combat_log = f"\033[1;31m[INSUFFICIENT MIND]: Legion Light requires 20 Mind (Have: {h.get('mind', 0)}).\033[0m"
                    return
            elif cursor_idx == 2:  # Tactical Focus (Cost: 15 Mind)
                if h.get("mind", 0) >= 15:
                    h["mind"] -= 15
                    h["buff"] = "TACTICAL FOCUS (+50% NEXT ATK)"
                    combat_log = "TACTICAL FOCUS! (-15 Mind) Le'garde studies weak points (+50% DMG on next strike)!"
                    enemy_turn()
                else:
                    combat_log = f"\033[1;31m[INSUFFICIENT MIND]: Tactical Focus requires 15 Mind (Have: {h.get('mind', 0)}).\033[0m"
                    return
            elif cursor_idx == 3:  # War Cry (Cost: 14 Mind)
                if h.get("mind", 0) >= 14:
                    h["mind"] -= 14
                    monster["def"] = max(0, int(monster.get("def", 14) * 0.65))
                    combat_log = "WAR CRY! (-14 Mind) Le'garde rallies: enemy armor weakened (-35% DEF)!"
                    enemy_turn()
                else:
                    combat_log = f"\033[1;31m[INSUFFICIENT MIND]: War Cry requires 14 Mind (Have: {h.get('mind', 0)}).\033[0m"
                    return

        elif h["name"] == "MOONLESS":
            if cursor_idx == 0:    # Feral Bite (Cost: +15 Hunger)
                h["hunger"] = min(100, h.get("hunger", 0) + 15)
                dmg = 40
                monster["hp"] = max(0, monster["hp"] - dmg)
                combat_log = f"FERAL BITE! (+15 Hunger) Moonless tears into flesh for {dmg} Phys DMG + Bleeding!"
                enemy_turn()
            elif cursor_idx == 1:  # Moon Howl (Cost: 15 Mind)
                if h.get("mind", 0) >= 15:
                    h["mind"] -= 15
                    dmg = 30
                    monster["hp"] = max(0, monster["hp"] - dmg)
                    if random.random() < 0.45:
                        monster["debuff_legs"] = True
                        combat_log = f"MOON HOWL! (-15 Mind) Eerie howling deals {dmg} Magic DMG and stuns foe (Crouched)!"
                    else:
                        combat_log = f"MOON HOWL! (-15 Mind) Lunar psychic scream echoes for {dmg} Magic DMG!"
                    enemy_turn()
                else:
                    combat_log = f"\033[1;31m[INSUFFICIENT MIND]: Moon Howl requires 15 Mind (Have: {h.get('mind', 0)}).\033[0m"
                    return
            elif cursor_idx == 2:  # Shadow Pounce (Cost: 12 Mind)
                if h.get("mind", 0) >= 12:
                    h["mind"] -= 12
                    dmg = 35
                    if monster.get("debuff_legs"):
                        dmg = 55
                    monster["hp"] = max(0, monster["hp"] - dmg)
                    combat_log = f"SHADOW POUNCE! (-12 Mind) Moonless pounces from the gloom for {dmg} DMG!"
                    enemy_turn()
                else:
                    combat_log = f"\033[1;31m[INSUFFICIENT MIND]: Shadow Pounce requires 12 Mind (Have: {h.get('mind', 0)}).\033[0m"
                    return
            elif cursor_idx == 3:  # Scent Danger (Cost: 10 Mind)
                if h.get("mind", 0) >= 10:
                    h["mind"] -= 10
                    h["buff"] = "DANGER SCENT (+35% DODGE)"
                    combat_log = "SCENT DANGER! (-10 Mind) Moonless sniffs danger in the air (+35% evasion)!"
                    enemy_turn()
                else:
                    combat_log = f"\033[1;31m[INSUFFICIENT MIND]: Scent Danger requires 10 Mind (Have: {h.get('mind', 0)}).\033[0m"
                    return

        elif h["name"] == "THE GIRL":
            if cursor_idx == 0:    # Nimble dodge (Cost: 12 Mind)
                if h.get("mind", 0) >= 12:
                    h["mind"] -= 12
                    h["buff"] = "NIMBLE DODGE (100% EVADE)"
                    combat_log = "NIMBLE DODGE! (-12 Mind) The Girl slips into shadows, guaranteeing 100% evasion!"
                    enemy_turn()
                else:
                    combat_log = f"\033[1;31m[INSUFFICIENT MIND]: Nimble Dodge requires 12 Mind (Have: {h.get('mind', 0)}).\033[0m"
                    return
            elif cursor_idx == 1:  # Loving embrace (Cost: 15 Mind)
                if h.get("mind", 0) >= 15:
                    h["mind"] -= 15
                    h["hp"] = min(h["max_hp"], h["hp"] + 35)
                    combat_log = "LOVING EMBRACE! (-15 Mind) Serene innocence restores +35 HP and dispels terror!"
                    enemy_turn()
                else:
                    combat_log = f"\033[1;31m[INSUFFICIENT MIND]: Loving Embrace requires 15 Mind (Have: {h.get('mind', 0)}).\033[0m"
                    return
            elif cursor_idx == 2:  # Pure Light (Cost: 20 Mind)
                if h.get("mind", 0) >= 20:
                    h["mind"] -= 20
                    dmg = 32
                    if monster.get("archetype") in ("SPECTRAL", "TERROR"):
                        dmg = int(dmg * 1.6)
                    monster["hp"] = max(0, monster["hp"] - dmg)
                    combat_log = f"PURE LIGHT! (-20 Mind) Holy glow incinerates dark foe for {dmg} Sacred Light DMG!"
                    enemy_turn()
                else:
                    combat_log = f"\033[1;31m[INSUFFICIENT MIND]: Pure Light requires 20 Mind (Have: {h.get('mind', 0)}).\033[0m"
                    return
            elif cursor_idx == 3:  # Distract foe (Cost: 10 Mind)
                if h.get("mind", 0) >= 10:
                    h["mind"] -= 10
                    monster["temp_debuff"] = "DISTRACTED (-50% ATK)"
                    combat_log = "DISTRACT FOE! (-10 Mind) The Girl waves lantern: enemy's attack power halved 50%!"
                    enemy_turn()
                else:
                    combat_log = f"\033[1;31m[INSUFFICIENT MIND]: Distract requires 10 Mind (Have: {h.get('mind', 0)}).\033[0m"
                    return

        elif h["name"] == "NAS'HRAH":
            if cursor_idx == 0:    # Combustion (Cost: 25 Mind)
                if h.get("mind", 0) >= 25:
                    h["mind"] -= 25
                    dmg = 62
                    monster["hp"] = max(0, monster["hp"] - dmg)
                    combat_log = f"COMBUSTION! (-25 Mind) Gro-goroth flame erupts for {dmg} Unstoppable Fire Magic DMG!"
                    enemy_turn()
                else:
                    combat_log = f"\033[1;31m[INSUFFICIENT MIND]: Combustion requires 25 Mind (Have: {h.get('mind', 0)}).\033[0m"
                    return
            elif cursor_idx == 1:  # Curse of Decay (Cost: 20 Mind)
                if h.get("mind", 0) >= 20:
                    h["mind"] -= 20
                    dmg = 32
                    monster["hp"] = max(0, monster["hp"] - dmg)
                    combat_log = f"CURSE OF DECAY! (-20 Mind) Ancient hex inflicts {dmg} Dark Magic DMG and rotting flesh!"
                    enemy_turn()
                else:
                    combat_log = f"\033[1;31m[INSUFFICIENT MIND]: Curse of Decay requires 20 Mind (Have: {h.get('mind', 0)}).\033[0m"
                    return
            elif cursor_idx == 2:  # Head Gnaw (0 Mind Cost, Siphons +15 HP & +10 Mind)
                dmg = 24
                monster["hp"] = max(0, monster["hp"] - dmg)
                h["hp"] = min(h["max_hp"], h["hp"] + 15)
                h["mind"] = min(h["max_mind"], h.get("mind", 0) + 10)
                combat_log = f"HEAD GNAW! Nas'hrah bites into foe for {dmg} Phys DMG and absorbs +15 HP life & +10 Mind!"
                enemy_turn()
            elif cursor_idx == 3:  # Mock Foe (Cost: 15 Mind)
                if h.get("mind", 0) >= 15:
                    h["mind"] -= 15
                    monster["def"] = max(0, monster.get("def", 14) // 2)
                    combat_log = "MOCK FOE! (-15 Mind) Nas'hrah insults the foe (-50% enemy DEF, foe enraged)!"
                    enemy_turn()
                else:
                    combat_log = f"\033[1;31m[INSUFFICIENT MIND]: Mock Foe requires 15 Mind (Have: {h.get('mind', 0)}).\033[0m"
                    return

        current_menu = "MAIN"
        cursor_idx = 0

    elif current_menu == "POUCH":
        menu_data = get_current_menu_data()
        opts = menu_data["options"]
        if cursor_idx >= len(opts):
            cursor_idx = 0
            current_menu = "MAIN"
            return

        chosen = opts[cursor_idx]
        item_id = chosen.get("id", "")
        chosen_opt = chosen.get("label", "")
        max_t = hero.get("max_toxicity", 100)

        if item_id == "close" or "BACK" in chosen_opt or "ĐÓNG" in chosen_opt:
            current_menu = "MAIN"
            cursor_idx = 0
            return

        elif item_id == "key":
            combat_log = f"\033[1;36m● [CHÌA KHÓA]: Có {inventory.get('key', 0)}/3 Runic Key. Cần mang đến Cổng Đông!\033[0m"
            return

        elif item_id == "totem":
            if inventory.get("totem", 0) > 0:
                inventory["totem"] -= 1
                hero["hp"] = hero["max_hp"]
                if "debuffs" in hero:
                    hero["debuffs"].clear()
                if "severed_limbs" in hero:
                    hero["severed_limbs"] = {"head": 100, "torso": 100, "arm_r": 100, "arm_l": 100, "leg_r": 100, "leg_l": 100}
                combat_log = f"\033[1;33m★ [TOTEM OF UNDYING]! Tái sinh toàn bộ tứ chi & hồi 100% HP cho {hero['name']}!\033[0m"
                enemy_turn()
            else:
                combat_log = "\033[1;31m[HẾT VẬT PHẨM]: Không còn Totem of Undying trong túi đồ!\033[0m"
            current_menu = "MAIN"
            cursor_idx = 0

        elif item_id == "poppy":
            if inventory.get("poppy", 0) > 0:
                inventory["poppy"] -= 1
                if hero["name"] == "NAS'HRAH":
                    combat_log = "NAS'HRAH cười khẩy: 'Ta không cần cỏ rác của người phàm!' (0 HP)."
                elif hero.get("toxicity", 0) >= max_t:
                    hero["hp"] = max(1, hero["hp"] - 5)
                    combat_log = f"NGỘ ĐỘC! Dạ dày {hero['name']} nôn mửa (0 HP, -5 HP độc tố)!"
                else:
                    heal_amt = 65 if hero["name"] == "CAHARA" else 50
                    hero["hp"] = min(hero["max_hp"], hero["hp"] + heal_amt)
                    added_tox = 0 if hero["name"] == "MOONLESS" else (15 if hero["name"] == "RAGNVALDR" else 35)
                    hero["toxicity"] = min(max_t, hero.get("toxicity", 0) + added_tox)
                    if "bleeding" in hero.get("debuffs", []):
                        hero["debuffs"].remove("bleeding")
                    if "Bleeding (-4 HP/turn)" in hero.get("debuffs", []):
                        hero["debuffs"].remove("Bleeding (-4 HP/turn)")
                    combat_log = f"● [HOA ANH TÚC]: {hero['name']} đắp dược liệu (+{heal_amt} HP, cầm máu hoàn toàn)."
                enemy_turn()
            else:
                combat_log = "\033[1;31m[HẾT VẬT PHẨM]: Không còn Poppy Flower trong túi đồ!\033[0m"
            current_menu = "MAIN"
            cursor_idx = 0

        elif item_id == "weed":
            if inventory.get("weed", 0) > 0:
                inventory["weed"] -= 1
                if hero["name"] == "NAS'HRAH":
                    combat_log = "NAS'HRAH cười khẩy: 'Dược thảo phàm trần vô dụng với ta!' (0 HP)."
                elif hero.get("toxicity", 0) >= max_t:
                    hero["hp"] = max(1, hero["hp"] - 5)
                    combat_log = f"NGỘ ĐỘC! {hero['name']} quá liều thảo dược (0 HP, -5 HP độc tố)!"
                else:
                    heal_amt = 150 if hero["name"] == "CAHARA" else 120
                    hero["hp"] = min(hero["max_hp"], hero["hp"] + heal_amt)
                    added_tox = 0 if hero["name"] == "MOONLESS" else (25 if hero["name"] == "RAGNVALDR" else 50)
                    hero["toxicity"] = min(max_t, hero.get("toxicity", 0) + added_tox)
                    combat_log = f"● [THẢO DƯỢC]: {hero['name']} hít khói dược thảo (+{heal_amt} HP, giảm đau nhức)."
                enemy_turn()
            else:
                combat_log = "\033[1;31m[HẾT VẬT PHẨM]: Không còn Medicinal Herb trong túi đồ!\033[0m"
            current_menu = "MAIN"
            cursor_idx = 0

        elif item_id == "bread":
            if inventory.get("bread", 0) > 0:
                inventory["bread"] -= 1
                if hero["name"] == "NAS'HRAH":
                    combat_log = "NAS'HRAH không cần ăn lương khô của người phàm!"
                elif hero["name"] == "RAGNVALDR":
                    hero["hunger"] = max(0, hero.get("hunger", 0) - 20)
                    combat_log = "Ragnvaldr nuốt vội bánh mì (-20 Đói - Cần thịt sống!)."
                elif hero["name"] == "CAHARA":
                    hero["hunger"] = max(0, hero.get("hunger", 0) - 50)
                    combat_log = "Cahara thưởng thức bánh mì ngon lành (-50 Đói)."
                else:
                    hero["hunger"] = max(0, hero.get("hunger", 0) - 40)
                    combat_log = f"● [BÁNH MÌ]: {hero['name']} ăn bánh mì (-40 Đói)."
                enemy_turn()
            else:
                combat_log = "\033[1;31m[HẾT VẬT PHẨM]: Không còn Moldy Bread trong túi đồ!\033[0m"
            current_menu = "MAIN"
            cursor_idx = 0

        elif item_id == "meat":
            if inventory.get("meat", 0) > 0:
                inventory["meat"] -= 1
                hero["hunger"] = max(0, hero.get("hunger", 0) - 60)
                hero["hp"] = min(hero["max_hp"], hero["hp"] + 20)
                combat_log = f"● [THỊT SẤY]: {hero['name']} ăn thịt sấy muối (+20 HP, -60 Đói)."
                enemy_turn()
            else:
                combat_log = "\033[1;31m[HẾT VẬT PHẨM]: Không còn Dried Meat trong túi đồ!\033[0m"
            current_menu = "MAIN"
            cursor_idx = 0

        elif item_id == "vial":
            qty_vial = inventory.get("vial", 0) or inventory.get("ale", 0)
            if qty_vial > 0:
                if "vial" in inventory: inventory["vial"] = max(0, inventory["vial"] - 1)
                if "ale" in inventory: inventory["ale"] = max(0, inventory["ale"] - 1)
                hero["mind"] = min(hero["max_mind"], hero.get("mind", 100) + 35)
                if "debuffs" in hero:
                    for deb in ["infection", "poison", "gangrene", "bleeding", "Bleeding (-4 HP/turn)"]:
                        if deb in hero["debuffs"]:
                            hero["debuffs"].remove(deb)
                combat_log = f"● [CỒN THUỐC]: {hero['name']} dùng cồn sát trùng (+35 Mind, tẩy độc & hoại tử)."
                enemy_turn()
            else:
                combat_log = "\033[1;31m[HẾT VẬT PHẨM]: Không còn Alchemical Vial trong túi đồ!\033[0m"
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
# COIN FLIP OF FATE (FEAR & HUNGER SIGNATURE GAMBLE ENGINE)
# =============================================================================
def run_coin_flip_interactive(title="COIN FLIP OF FATE", threat_actor="MONSTER", attack_name="LETHAL CLEAVE"):
    """
    Fear & Hunger Coin Flip: Bet life on HEADS (Sylvian) or TAILS (Gro-goroth).
    Returns True if player correctly predicts the coin face, False otherwise.
    """
    if not (os.name == 'nt' and sys.stdin.isatty()):
        # Headless / Automated test environment fallback (50% true RNG)
        user_bet = random.choice([0, 1])
        landed = random.choice([0, 1])
        return (user_bet == landed)

    coin_choice = 0 # 0: Heads, 1: Tails

    while True:
        rows = []
        rows.append("\033[1;30m+" + "=" * 98 + "+\033[0m")
        header_text = f"  !!! LETHAL THREAT DETECTED: {threat_actor:<18} PREPARES [{attack_name:<20}] !!!"
        rows.append(f"\033[41;1;37m|{fit_ansi(header_text, 98)}|\033[0m")
        sub_text = "  COIN FLIP OF FATE: PARRY COMPLETELY OR SUFFER CATASTROPHIC MUTILATION !"
        rows.append(f"\033[41;1;37m|{fit_ansi(sub_text, 98)}|\033[0m")
        rows.append("\033[1;30m+" + "=" * 98 + "+\033[0m")
        rows.append("")
        rows.append("  \033[1;33mBET YOUR LIFE UPON THE COIN:\033[0m")
        rows.append("")

        if coin_choice == 0:
            rows.append("  \033[1;30;43m ▶ [1] HEADS (SYLVIAN'S GRACE) \033[0m : \033[1;32mBlessing of love, restoration & preservation\033[0m \033[1;33m< [SELECTED]\033[0m")
            rows.append("      [2] TAILS (GRO-GOROTH'S WRATH): \033[90mMight of ancient slaughter, carnage & destruction\033[0m")
        else:
            rows.append("      [1] HEADS (SYLVIAN'S GRACE)   : \033[90mBlessing of love, restoration & preservation\033[0m")
            rows.append("  \033[1;30;43m ▶ [2] TAILS (GRO-GOROTH'S WRATH): \033[1;31mMight of ancient slaughter, carnage & destruction\033[0m \033[1;33m< [SELECTED]\033[0m")

        rows.append("")
        rows.append("\033[1;30m+" + "-" * 98 + "+\033[0m")
        rows.append("  \033[90m[CONTROLS]:\033[0m \033[1;37m[W/S / 1-2]\033[0m Toggle Coin Face  |  \033[1;37m[Enter/Space]\033[0m Flip Coin of Fate")
        rows.append("\033[1;30m+" + "=" * 98 + "+\033[0m")

        clear_screen()
        for r in rows:
            print(r)

        ch = msvcrt.getch()
        if ch in (b'\x00', b'\xe0'):
            ch = msvcrt.getch()
            if ch == b'H':  # Up
                coin_choice = (coin_choice - 1) % 2
            elif ch == b'P':  # Down
                coin_choice = (coin_choice + 1) % 2
        elif ch in (b'w', b'W'):
            coin_choice = (coin_choice - 1) % 2
        elif ch in (b's', b'S'):
            coin_choice = (coin_choice + 1) % 2
        elif ch == b'1':
            coin_choice = 0
            break
        elif ch == b'2':
            coin_choice = 1
            break
        elif ch in (b'\r', b'\n', b' '):
            break

    # 4-frame spinning coin animation
    spin_frames = [
        "     \033[1;33m[  (O) |  ]\033[0m",
        "     \033[1;33m[  (O) /  ]\033[0m",
        "     \033[1;33m[  (O) -  ]\033[0m",
        "     \033[1;33m[  (O) \\  ]\033[0m"
    ]
    clear_screen()
    print("\n  \033[1;33m>> THE COIN SPINS INTO THE DARK AIR...\033[0m")
    for frame in spin_frames:
        print(frame)
        time.sleep(0.08)

    landed = random.choice([0, 1])
    landed_str = "HEADS (SYLVIAN'S GRACE)" if landed == 0 else "TAILS (GRO-GOROTH'S WRATH)"
    is_success = (coin_choice == landed)

    print(f"\n  \033[1;33m>> COIN LANDED ON: [ {landed_str} ] !\033[0m\n")
    if is_success:
        print("\033[1;32m+====================================================================================================+\033[0m")
        print("\033[1;32m|  >>> [SUBLIME PARRY!]: YOU CALLED THE COIN! DEFLECTED LETHAL BLOW AND COUNTER-STRUCK! <<<          |\033[0m")
        print("\033[1;32m+====================================================================================================+\033[0m")
    else:
        print("\033[1;31m+====================================================================================================+\033[0m")
        print("\033[1;31m|  >>> [COIN FLIP FAILED!]: THE LETHAL BLOW SHATTERS FLESH AND DEFENSE WITH CRITICAL CARNAGE! <<<    |\033[0m")
        print("\033[1;31m+====================================================================================================+\033[0m")

    time.sleep(1.2)
    clear_screen()
    return is_success

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
    if "Bleeding (-4 HP/turn)" in hero.setdefault("debuffs", []):
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

    # 7. Check Lethal Coin Flip of Fate (Fear & Hunger Signature Defense)
    is_lethal = False
    lethal_atk_name = "LETHAL CLEAVE"
    if monster.get("archetype") == "ARMORED":
        lethal_atk_name = "CRUSHING CLEAVE"
    elif monster.get("archetype") == "SPECTRAL":
        lethal_atk_name = "SOUL DEVOUR"
    elif monster.get("archetype") == "AMBUSHER":
        lethal_atk_name = "THROAT SLICE"
    elif monster.get("archetype") == "TERROR":
        lethal_atk_name = "TERROR MUTILATION"

    # Bosses 35% chance, normal foes 15% chance if arms intact
    arms_intact = not (monster.get("debuff_arm_r") and monster.get("debuff_arm_l"))
    if arms_intact and ((monster.get("is_boss") and random.random() < 0.35) or (random.random() < 0.15 and not hero.get("is_guarding", False))):
        is_lethal = True

    if is_lethal:
        flip_win = run_coin_flip_interactive("LETHAL CLASH", monster["name"], lethal_atk_name)
        if flip_win:
            counter_dmg = 24
            monster["hp"] = max(0, monster["hp"] - counter_dmg)
            combat_log += f" | \033[1;32m[SUBLIME PARRY!]\033[0m {hero['name']} CALLED THE COIN! Deflected {lethal_atk_name} (+0 DMG) & counter-struck for {counter_dmg} DMG!"
            if monster["hp"] == 0:
                combat_log += " Foe neutralized! VICTORY!"
                combat_outcome = "VICTORY"
            return
        else:
            combat_log += f" | \033[1;31m[COIN FLIP FAILED!]\033[0m {monster['name']}'s {lethal_atk_name} lands with brutal impact!"

    # 8. Incoming Damage calculation with character physical/magic multipliers
    base_atk = monster["atk"]
    if is_lethal:
        base_atk = int(base_atk * 1.5)
    elif monster.get("archetype") == "AMBUSHER" and not hero.get("is_guarding", False):
        base_atk = int(base_atk * 1.5)

    if hero["name"] == "THE GIRL":
        base_atk = int(base_atk * 0.70)
    if "DISTRACTED (-50% ATK)" in monster.get("temp_debuff", ""):
        base_atk = int(base_atk * 0.50)
        monster["temp_debuff"] = ""

    dmg = base_atk - (hero.get("def", 10) // 2)

    # Apply character defense affinity (D'arce -35%, Ragnvaldr -15%, Enki +30% fragile, Nas'hrah +20%)
    phys_mult = hero.get("phys_mult", 1.0)
    dmg = int(dmg * phys_mult)

    if hero.get("is_guarding", False):
        dmg = int(dmg * 0.25)
        hero["is_guarding"] = False

    dmg = max(3, dmg)
    hero["hp"] = max(0, hero["hp"] - dmg)
    ambush_tag = " [LETHAL AMBUSH]" if (monster.get("archetype") == "AMBUSHER" and not hero.get("is_guarding", False)) else ""
    combat_log += f" | Foe strikes{ambush_tag}! {hero['name']} takes {dmg} DMG."

    # Chance foe inflicts bleeding scratch (Nas'hrah immune)
    if random.random() < 0.35 and hero["name"] != "NAS'HRAH" and "Bleeding (-4 HP/turn)" not in hero.setdefault("debuffs", []):
        hero["debuffs"].append("Bleeding (-4 HP/turn)")
        combat_log += " Claws inflict Bleeding (-4 HP/turn)!"

    # Down check
    if hero["hp"] == 0:
        if inventory.get("totem", 0) > 0:
            inventory["totem"] -= 1
            revive_hp = max(1, hero["max_hp"] // 2)
            hero["hp"] = revive_hp
            if "debuffs" in hero:
                hero["debuffs"].clear()
            if "severed_limbs" in hero:
                hero["severed_limbs"] = {"head": 100, "torso": 100, "arm_r": 100, "arm_l": 100, "leg_r": 100, "leg_l": 100}
            combat_log += f" | \033[1;33m★ [TOTEM OF UNDYING DETONATES]! Golden amber aura defies death! Severed limbs restored & {hero['name']} revived to {hero['hp']} HP!\033[0m"
        else:
            combat_log += f" | {hero['name']} has fallen in the dark catacombs! DEFEAT!"
            combat_outcome = "DEFEAT"

# =============================================================================
# MAIN INTERACTIVE LOOP
# =============================================================================
def run_interactive_loop():
    global current_menu, cursor_idx, combat_outcome

    # Clear screen cleanly on entry and hide cursor
    clear_screen()

    while True:
        if combat_outcome is not None:
            render_screen()
            time.sleep(1.0)
            clear_screen()
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
                clear_screen()
                sys.stdout.write("\033[?25h\n[OK] Exited Solo Combat Arena.\n")
                return "QUIT", active_hero, inventory
            elif ch in (b'1', b'2', b'3', b'4', b'5', b'6', b'7', b'8'):
                num = int(ch.decode('ascii')) - 1
                if num < num_options:
                    cursor_idx = num
                    # Number key only navigates cursor; Enter confirms action!
        else:
            raw = sys.stdin.readline()
            if not raw:
                break
            line = raw.strip().lower()
            if line == 'w':
                cursor_idx = (cursor_idx - 1) % num_options
            elif line == 's':
                cursor_idx = (cursor_idx + 1) % num_options
            elif line in ('1', '2', '3', '4', '5', '6', '7', '8'):
                num = int(line) - 1
                if num < num_options:
                    cursor_idx = num
            elif line in ('', 'c', 'enter'):
                handle_selection()
            elif line in ('b', 'q'):
                clear_screen()
                return "QUIT", active_hero, inventory

    clear_screen()
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
