#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
================================================================================
HERO SEVERED LIMB MODELS CATALOG (EXPERIMENTAL SHOWCASE ARCHITECTURE)
Fear & Hunger: Terminal Labyrinth - Solo Explorer Architecture
================================================================================
Rules & Specifications:
  1. Golden Joint Rule: Every severed limb socket / stump MUST glow in
     Technical Amber (#FFAA28 -> \033[38;2;255;170;40m▀\033[0m).
  2. Severed right arm deletes wielding weapon / right forearm.
  3. Severed left arm deletes shield / torch / off-hand.
  4. Severed / crippled legs removes lower footing, leaving amber knee stumps.
  5. Moonless (Canine): Severed foreleg / hindleg with amber shoulder/hip joints.
  6. Nas'hrah (Flying Head): Severed arcane skull fractures with amber glowing fissures.
================================================================================
"""

import os
import json
import re

C_AMBER = "\033[38;2;255;170;40m"
C_RESET = "\033[0m"
AMBER_STUMP = f"{C_AMBER}▀{C_RESET}"
AMBER_BOT = f"{C_AMBER}▄{C_RESET}"

# Load intact hero sprites from extracted_sprites.json
INTACT_HEROES = {}
try:
    p = os.path.join(os.path.dirname(__file__), "extracted_sprites.json")
    if os.path.exists(p):
        with open(p, "r", encoding="utf-8") as f:
            data = json.load(f)
            INTACT_HEROES = data.get("heroes", {})
except Exception:
    pass

HERO_SEVERED_MODELS = {}

# -----------------------------------------------------------------------------
# 1. D'ARCE (Holy Paladin)
# -----------------------------------------------------------------------------
d_intact = INTACT_HEROES.get("D'ARCE", [" " * 29] * 12)

d_sev_right = list(d_intact)
# Remove sword & right arm (rows 6..11, right side) and place Amber Stump at row 6, col 12
d_sev_right[6]  = "   ▀▀▀▀▀▀▀▀▀▀▀" + AMBER_STUMP + "             "
d_sev_right[7]  = "   ▀▀▀▀▀▀▀▀▀▀▀▄                 "
d_sev_right[8]  = "   ▀▀ ▀▀▀▀▀▀▀▀▀                 "
d_sev_right[9]  = "      ▀▀▀▀▀▀▀▀▀▀                "
d_sev_right[10] = "      ▀▀▀▀   ▀▀▀▀               "
d_sev_right[11] = "               ▀▀               "

d_sev_left = list(d_intact)
# Remove shield & left arm (rows 4..8, left side) and place Amber Stump at row 4, col 3
d_sev_left[4] = f"   {AMBER_STUMP}▄▀▀▀▀▀▀▀▀▄                "
d_sev_left[5] = "     ▀▀▀▀▀▀▀▀▀▀▀                "
d_sev_left[6] = "     ▀▀▀▀▀▀▀▀▀▀ ▀▀▀             "
d_sev_left[7] = "     ▀▀▀▀▀▀▀▀▀▀▄▀▀▀▀            "
d_sev_left[8] = "      ▀▀▀▀▀▀▀▀▀▄▀▀▀▀▀▀          "

d_sev_both = list(d_sev_right)
d_sev_both[4] = f"   {AMBER_STUMP}▄▀▀▀▀▀▀▀▀▄                "
d_sev_both[5] = "     ▀▀▀▀▀▀▀▀▀▀▀                "
d_sev_both[6] = f"     ▀▀▀▀▀▀▀▀▀▀{AMBER_STUMP}                "
d_sev_both[7] = "     ▀▀▀▀▀▀▀▀▀▀▄                "
d_sev_both[8] = "      ▀▀▀▀▀▀▀▀▀                 "

d_crip_legs = list(d_intact)
# Remove lower legs and replace knees with amber stumps
d_crip_legs[9]  = f"      ▀▀▀▀▀▀▀▀▀▀  ▀▀▀▀▀▄        "
d_crip_legs[10] = f"      {AMBER_STUMP}{AMBER_STUMP}   {AMBER_STUMP}{AMBER_STUMP}     ▀▀▀▄      "
d_crip_legs[11] = "                         ▀▀▀     "

HERO_SEVERED_MODELS["D'ARCE"] = {
    "intact": d_intact,
    "severed_right_arm": d_sev_right,
    "severed_left_arm": d_sev_left,
    "severed_both_arms": d_sev_both,
    "crippled_legs": d_crip_legs,
}

# -----------------------------------------------------------------------------
# 2. CAHARA (Mercenary Rogue)
# -----------------------------------------------------------------------------
c_intact = INTACT_HEROES.get("CAHARA", [" " * 29] * 12)

c_sev_right = list(c_intact)
# Remove twin daggers on right side (rows 3..7) and place Amber Stump at row 5, col 13
c_sev_right[3] = "    ▀▀▀▀▀▀▀▀▀▀▀                 "
c_sev_right[4] = "    ▄▀▀▀▀▀▀▀▀▀▄                 "
c_sev_right[5] = f"  ▄▀▀▀▀▀▀▀▀▀▀▀▀{AMBER_STUMP}                "
c_sev_right[6] = "  ▀▀▀▀▀▀▀▀▀▀▀▀▀                 "
c_sev_right[7] = " ▀▀▀▀▄▀▀▀▀▀▀▀▀▀                 "

c_sev_left = list(c_intact)
# Remove thief cape / left forearm
c_sev_left[5] = f"    {AMBER_STUMP}▀▀▀▀▀▀▀▀▀▀▀▀▄▄▄▄▀▀▀      "
c_sev_left[6] = "     ▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀       "
c_sev_left[7] = f"   {AMBER_STUMP} ▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀        "
c_sev_left[8] = "     ▀▀▀▀▀▀▀▀▀▀                 "

c_sev_both = list(c_sev_right)
c_sev_both[5] = f"    {AMBER_STUMP}▀▀▀▀▀▀▀▀▀▀▀{AMBER_STUMP}                "
c_sev_both[6] = "     ▀▀▀▀▀▀▀▀▀▀▀                "
c_sev_both[7] = "      ▀▀▀▀▀▀▀▀▀▀                "
c_sev_both[8] = "      ▀▀▀▀▀▀▀▀▀▀                "

c_crip_legs = list(c_intact)
c_crip_legs[9]  = "▀▀▀▀▀▀▀▀▀▀▀▀▀▀               "
c_crip_legs[10] = f"  {AMBER_STUMP}{AMBER_STUMP}       {AMBER_STUMP}{AMBER_STUMP}               "
c_crip_legs[11] = "                             "

HERO_SEVERED_MODELS["CAHARA"] = {
    "intact": c_intact,
    "severed_right_arm": c_sev_right,
    "severed_left_arm": c_sev_left,
    "severed_both_arms": c_sev_both,
    "crippled_legs": c_crip_legs,
}

# -----------------------------------------------------------------------------
# 3. RAGNVALDR (Outlander Berserker)
# -----------------------------------------------------------------------------
r_intact = INTACT_HEROES.get("RAGNVALDR", [" " * 29] * 12)

r_sev_right = list(r_intact)
# Remove heavy war axe (rows 4..8 on right)
r_sev_right[4] = " ▀▀▀▀▀▀▀▀▀▀▀▀▀▀                 "
r_sev_right[5] = f" ▀▀▀▀▀▀▀▀▀▀▀▀▀▀{AMBER_STUMP}                "
r_sev_right[6] = " ▀▀▀▀▀▀▀▀▀▀▀▀▀▀                 "
r_sev_right[7] = " ▄▀▀▀▀▀▀▀▀▀▀▀▀▀▄                "
r_sev_right[8] = " ▀▀▀▀▀▀▀▀▀▀▀▀▀                  "

r_sev_left = list(r_intact)
r_sev_left[3] = f"  {AMBER_STUMP}▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀              "
r_sev_left[4] = "    ▀▀▀▀▀▀▀▀▀▀▀▀▀      ▀▄       "
r_sev_left[5] = "    ▀▀▀▀▀▀▀▀▀▀▀▀▀▀   ▄▀▀▀       "

r_crip_legs = list(r_intact)
r_crip_legs[10] = f"   {AMBER_STUMP}{AMBER_STUMP}{AMBER_STUMP}     {AMBER_STUMP}{AMBER_STUMP}{AMBER_STUMP}              "
r_crip_legs[11] = "                             "

HERO_SEVERED_MODELS["RAGNVALDR"] = {
    "intact": r_intact,
    "severed_right_arm": r_sev_right,
    "severed_left_arm": r_sev_left,
    "severed_both_arms": r_sev_right,
    "crippled_legs": r_crip_legs,
}

# -----------------------------------------------------------------------------
# 4. ENKI (Dark Occultist)
# -----------------------------------------------------------------------------
e_intact = INTACT_HEROES.get("ENKI", [" " * 29] * 12)

e_sev_right = list(e_intact)
e_sev_right[5] = f"  ▄▀▀▀▀▀▀▀▀▀▀{AMBER_STUMP}                 "
e_sev_right[6] = " ▄▀▀▀▀▀▀▀▀▀▀▀                   "
e_sev_right[7] = " ▀▀▀▀▀▀▀▀▀▀▀                    "

e_sev_left = list(e_intact)
e_sev_left[5] = f"   {AMBER_STUMP}▀▀▀▀▀▀▀▀▀▀▀▀                "
e_sev_left[6] = "    ▀▀▀▀▀▀▀▀▀▀▀▀▀               "

e_crip_legs = list(e_intact)
e_crip_legs[10] = f"  {AMBER_STUMP}{AMBER_STUMP}{AMBER_STUMP}    {AMBER_STUMP}{AMBER_STUMP}{AMBER_STUMP}                 "
e_crip_legs[11] = "                             "

HERO_SEVERED_MODELS["ENKI"] = {
    "intact": e_intact,
    "severed_right_arm": e_sev_right,
    "severed_left_arm": e_sev_left,
    "severed_both_arms": e_sev_right,
    "crippled_legs": e_crip_legs,
}

# -----------------------------------------------------------------------------
# 5. LE'GARDE (The Strategist)
# -----------------------------------------------------------------------------
l_intact = INTACT_HEROES.get("LE'GARDE", [" " * 29] * 12)

l_sev_right = list(l_intact)
# Remove fencing rapier (rows 2..7)
l_sev_right[2] = "    ▀▀▀▀▀▀▀▀▀▀▀▀                "
l_sev_right[3] = "    ▀▀▀▀▀▀▀▀▀▀▀▀                "
l_sev_right[4] = f"    ▄▀▀▀▀▀▀▀▀▀▀▀{AMBER_STUMP}               "
l_sev_right[5] = "   ▀▀▀▀▀▀▀▀▀▀▀▀▀                "
l_sev_right[6] = "  ▀▀▀▀▀▀▀▀▀▀▀▀▀▀                "
l_sev_right[7] = " ▀▀▀ ▄▀▀▀▀▀▀▀▀▀▄                "

l_sev_left = list(l_intact)
l_sev_left[6] = f"   {AMBER_STUMP}▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀        "
l_sev_left[7] = "     ▄▀▀▀▀▀▀▀▀▀▄ ▀▀▀            "
l_sev_left[8] = "     ▀▀▀▀▀▀▀▀▀▀▀                "

l_crip_legs = list(l_intact)
l_crip_legs[10] = f"   {AMBER_STUMP}{AMBER_STUMP}     {AMBER_STUMP}{AMBER_STUMP}                "
l_crip_legs[11] = "                             "

HERO_SEVERED_MODELS["LE'GARDE"] = {
    "intact": l_intact,
    "severed_right_arm": l_sev_right,
    "severed_left_arm": l_sev_left,
    "severed_both_arms": l_sev_right,
    "crippled_legs": l_crip_legs,
}

# -----------------------------------------------------------------------------
# 6. THE GIRL (Innocent Survivor)
# -----------------------------------------------------------------------------
g_intact = INTACT_HEROES.get("THE GIRL", [" " * 29] * 12)

g_sev_right = list(g_intact)
g_sev_right[5] = f"  ▀▀▀▀▀▀▀▀{AMBER_STUMP}                  "
g_sev_right[6] = "  ▀▀▀▀▀▀▀▀                      "

g_sev_left = list(g_intact)
g_sev_left[5] = f"   {AMBER_STUMP}▀▀▀▀▀▀▀▀▀                  "
g_sev_left[6] = "    ▀▀▀▀▀▀▀▀▀                   "

g_crip_legs = list(g_intact)
g_crip_legs[9] = f"   {AMBER_STUMP}    {AMBER_STUMP}                   "

HERO_SEVERED_MODELS["THE GIRL"] = {
    "intact": g_intact,
    "severed_right_arm": g_sev_right,
    "severed_left_arm": g_sev_left,
    "severed_both_arms": g_sev_right,
    "crippled_legs": g_crip_legs,
}

# -----------------------------------------------------------------------------
# 7. MOONLESS (Ancient Dire Wolf - Quadruped Anatomy)
# -----------------------------------------------------------------------------
m_intact = INTACT_HEROES.get("MOONLESS", [" " * 29] * 12)

# Severed Foreleg (Front paw amputated, front shoulder amber socket)
m_sev_fore = list(m_intact)
m_sev_fore[8]  = f"  {AMBER_STUMP}    ▀▀▀▀▀▀▀▀▀▀▀▀▀▀        "
m_sev_fore[9]  = "       ▀▀▀▀▀▀▀▀ ▀▀▀▀▄        "
m_sev_fore[10] = "                ▀▀▀▀         "

# Severed Hindleg (Back leg amputated, rear hip amber socket)
m_sev_hind = list(m_intact)
m_sev_hind[9]  = f"   ▀▀▀  ▀▀▀▀▀▀▀▀ {AMBER_STUMP}           "
m_sev_hind[10] = "         ▀▀▀                 "
m_sev_hind[11] = "                             "

# Crippled Beast (Both front and hind amputated)
m_sev_both = list(m_intact)
m_sev_both[8]  = f"  {AMBER_STUMP}    ▀▀▀▀▀▀▀▀▀▀▀▀▀▀        "
m_sev_both[9]  = f"        ▀▀▀▀▀▀▀▀ {AMBER_STUMP}           "
m_sev_both[10] = "                             "
m_sev_both[11] = "                             "

HERO_SEVERED_MODELS["MOONLESS"] = {
    "intact": m_intact,
    "severed_foreleg": m_sev_fore,
    "severed_hindleg": m_sev_hind,
    "crippled_beast": m_sev_both,
    "severed_right_arm": m_sev_fore,
    "severed_left_arm": m_sev_fore,
    "crippled_legs": m_sev_hind,
}

# -----------------------------------------------------------------------------
# 8. NAS'HRAH (The Doom Prophet - Floating Severed Cranium)
# -----------------------------------------------------------------------------
# Note: Nas'hrah has NO arms or legs. His trauma manifests as fractured cranium & scorched jaw!
n_intact = INTACT_HEROES.get("NAS'HRAH", [" " * 29] * 12)

n_fractured = list(n_intact)
# Arcane golden amber fissures tearing through skull
n_fractured[1] = f"  ▀▀▀{AMBER_STUMP}▀▀▀▀▀▀                 "
n_fractured[2] = f" ▄▀▀▀▀{AMBER_BOT}▀▀▀▀▀▀                 "
n_fractured[3] = f" ▀▀▀▀▀▀{AMBER_STUMP}▀▀▀▀                  "
n_fractured[4] = f"  ▀▀▀▀▀▀{AMBER_BOT}▀▀▀                  "

n_scorched_jaw = list(n_intact)
# Quai hàm bị vỡ, rực sáng lửa hổ phách Gro-goroth
n_scorched_jaw[7] = f"   ▀▀▀{AMBER_STUMP}{AMBER_STUMP}                     "
n_scorched_jaw[8] = f"   {AMBER_STUMP}  {AMBER_STUMP}▀▀                    "
n_scorched_jaw[9] = f"     {AMBER_BOT}{AMBER_BOT}                      "

HERO_SEVERED_MODELS["NAS'HRAH"] = {
    "intact": n_intact,
    "fractured_cranium": n_fractured,
    "scorched_jaw": n_scorched_jaw,
    "severed_right_arm": n_fractured,
    "severed_left_arm": n_fractured,
    "crippled_legs": n_scorched_jaw,
}

def get_hero_mutilation_sprite(hero_name, mutilation_type="intact"):
    hero_dict = HERO_SEVERED_MODELS.get(hero_name, {})
    return hero_dict.get(mutilation_type, hero_dict.get("intact", INTACT_HEROES.get(hero_name, [])))

if __name__ == "__main__":
    print(f"Loaded {len(HERO_SEVERED_MODELS)} heroes into severed limb catalog.")
    for h, v in HERO_SEVERED_MODELS.items():
        print(f"  - {h:<12}: Variants = {list(v.keys())}")
