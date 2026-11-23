#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Unified 36-Monster Hardware Catalog matching monster_rom.v exactly.
"""

ALL_MONSTERS_CATALOG = {
    1:  {"id": 1,  "name": "MAGE GHOST",         "archetype": "SPECTRAL", "hp": 85,  "atk": 21, "def": 12},
    2:  {"id": 2,  "name": "CLASSIC GHOST",      "archetype": "SPECTRAL", "hp": 80,  "atk": 19, "def": 10},
    3:  {"id": 3,  "name": "MAW SLIME",          "archetype": "NORMAL",   "hp": 110, "atk": 16, "def": 18},
    4:  {"id": 4,  "name": "BRACHIO TITAN",      "archetype": "ARMORED",  "hp": 150, "atk": 24, "def": 22, "is_boss": True},
    5:  {"id": 5,  "name": "ANTLER TOTEM",       "archetype": "NORMAL",   "hp": 100, "atk": 20, "def": 16},
    6:  {"id": 6,  "name": "KRAKEN OCTOPUS",     "archetype": "NORMAL",   "hp": 115, "atk": 22, "def": 14},
    7:  {"id": 7,  "name": "BEHOLDER EYE",       "archetype": "TERROR",   "hp": 90,  "atk": 25, "def": 10},
    8:  {"id": 8,  "name": "SHADOW SWORDSMAN",   "archetype": "ARMORED",  "hp": 95,  "atk": 24, "def": 14},
    9:  {"id": 9,  "name": "GIANT SNAIL",        "archetype": "ARMORED",  "hp": 120, "atk": 14, "def": 24},
    10: {"id": 10, "name": "GRAVE SPIDER",       "archetype": "NORMAL",   "hp": 90,  "atk": 23, "def": 12},
    11: {"id": 11, "name": "DUNGEON ANT",        "archetype": "NORMAL",   "hp": 85,  "atk": 20, "def": 14},
    12: {"id": 12, "name": "BATTLE LLAMA",       "archetype": "NORMAL",   "hp": 105, "atk": 18, "def": 16},
    13: {"id": 13, "name": "SHADOW HOUND",       "archetype": "NORMAL",   "hp": 85,  "atk": 24, "def": 8},
    14: {"id": 14, "name": "FOREST STAG",        "archetype": "NORMAL",   "hp": 95,  "atk": 19, "def": 14},
    15: {"id": 15, "name": "CAVE GNOME",         "archetype": "NORMAL",   "hp": 80,  "atk": 18, "def": 12},
    16: {"id": 16, "name": "MINI KNIGHT",        "archetype": "ARMORED",  "hp": 100, "atk": 21, "def": 18},
    17: {"id": 17, "name": "LITTLE DRAKE",       "archetype": "NORMAL",   "hp": 105, "atk": 23, "def": 12},
    18: {"id": 18, "name": "SHADOW SLUG",        "archetype": "NORMAL",   "hp": 95,  "atk": 15, "def": 20},
    19: {"id": 19, "name": "DARK CONSTRUCT",     "archetype": "ARMORED",  "hp": 140, "atk": 22, "def": 24, "is_boss": True},
    20: {"id": 20, "name": "ABYSSAL OVERLORD",   "archetype": "TERROR",   "hp": 160, "atk": 28, "def": 20, "is_boss": True},
    21: {"id": 21, "name": "WYVERN",             "archetype": "NORMAL",   "hp": 115, "atk": 24, "def": 14},
    22: {"id": 22, "name": "GARGOYLE",           "archetype": "ARMORED",  "hp": 110, "atk": 20, "def": 20},
    23: {"id": 23, "name": "CHEST MIMIC",        "archetype": "NORMAL",   "hp": 95,  "atk": 22, "def": 12, "is_mimic": True},
    24: {"id": 24, "name": "HYDRA SERPENT",      "archetype": "TERROR",   "hp": 145, "atk": 26, "def": 16, "is_boss": True},
    25: {"id": 25, "name": "IMP DEMON",          "archetype": "NORMAL",   "hp": 85,  "atk": 23, "def": 10},
    26: {"id": 26, "name": "SPECTRAL BEAST",     "archetype": "SPECTRAL", "hp": 95,  "atk": 22, "def": 12},
    27: {"id": 27, "name": "ANCIENT TREANT",     "archetype": "NORMAL",   "hp": 130, "atk": 18, "def": 22},
    28: {"id": 28, "name": "ABYSS BEHOLDER",     "archetype": "TERROR",   "hp": 100, "atk": 25, "def": 12},
    29: {"id": 29, "name": "DUNGEON BASILISK",   "archetype": "ARMORED",  "hp": 155, "atk": 22, "def": 25, "is_boss": True},
    30: {"id": 30, "name": "CHIMERA HORROR",     "archetype": "TERROR",   "hp": 135, "atk": 27, "def": 18, "is_boss": True},
    31: {"id": 31, "name": "CAVE MANTICORE",     "archetype": "NORMAL",   "hp": 100, "atk": 21, "def": 15},
    32: {"id": 32, "name": "CATHEDRAL GARGOYLE", "archetype": "ARMORED",  "hp": 110, "atk": 20, "def": 18},
    33: {"id": 33, "name": "TROLL BERSERKER",    "archetype": "NORMAL",   "hp": 150, "atk": 25, "def": 20, "is_boss": True},
    34: {"id": 34, "name": "CRYPT VAMPIRE",      "archetype": "NORMAL",   "hp": 115, "atk": 24, "def": 15},
    35: {"id": 35, "name": "LICH NECROMANCER",   "archetype": "SPECTRAL", "hp": 125, "atk": 29, "def": 14, "is_boss": True},
    36: {"id": 36, "name": "DARK DRAGON",        "archetype": "ARMORED",  "hp": 170, "atk": 30, "def": 22, "is_boss": True},
}

# Sub-pools for guaranteed unique selection without replacement per run:
REGULAR_MONSTER_IDS = [
    1, 2, 3, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18,
    21, 22, 25, 26, 27, 28, 31, 32, 34
]

BOSS_MONSTER_IDS = [4, 19, 20, 24, 29, 30, 33, 35, 36]

MIMIC_ID = 23
