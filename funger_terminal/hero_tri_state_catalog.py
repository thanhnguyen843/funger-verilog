#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
================================================================================
HERO TRI-STATE MORPHOLOGY CATALOG (NORMAL vs INJURED vs DEAD)
Fear & Hunger: Terminal Labyrinth - Solo Explorer Architecture
================================================================================
Design Principles & Specifications:
  1. NORMAL (State 0 / Thường):
     - Full vitality, intact limbs, active weapons, and vibrant RGB truecolor palette.
  2. INJURED (State 1 / Chấn thương):
     - Preserves the hero's rich RGB truecolor palette for face, hair, and armor.
     - Severed limb / weapon pixels are cleared away.
     - Technical Amber (#FFAA28 -> \\033[38;2;255;170;40m▀\\033[0m) stumps placed at
       the exact anatomical joint socket, with coagulated crimson drips.
     - Special anatomy:
       * Moonless: Quadruped canine front leg amputation with amber shoulder joint.
       * Nas'hrah: Arcane cranial fractures glowing with radiant amber fissures.
  3. DEAD (State 2 / Tử vong):
     - Collapsed horizontal corpse lying prone on the cold stone floor (rows 6..11).
     - Color shifted into Deactivated Ash Gray (#6E7378), Charcoal (#464A4E),
       and dark dried crimson blood (#551212) pooling on the dungeon stones.
     - Upper rows (0..5) rendered as silent dark dungeon air.
  4. DEAD STANDING / GHOST (State 2b / Chuyển màu tro tàn đứng):
     - Complete RGB color-drain of the upright silhouette into ghostly Ash Gray.
================================================================================
"""

import os
import json
import re

# Color Constants
C_RESET = "\033[0m"
C_AMBER = "\033[38;2;255;170;40m"
C_BLOOD = "\033[38;2;160;25;25m"
C_GRAY  = "\033[38;2;110;115;120m"
C_DARK  = "\033[38;2;60;65;70m"
C_POOL  = "\033[38;2;85;18;18m"

AMBER_TOP = f"{C_AMBER}▀{C_RESET}"
AMBER_BOT = f"{C_AMBER}▄{C_RESET}"

# Load intact models from extracted_sprites.json
INTACT_HEROES = {}
try:
    p = os.path.join(os.path.dirname(__file__), "extracted_sprites.json")
    if os.path.exists(p):
        with open(p, "r", encoding="utf-8") as f:
            INTACT_HEROES = json.load(f).get("heroes", {})
except Exception:
    pass

def parse_line(line, target_width=29):
    """Parses an ANSI truecolor string into an array of (char, fg_code, bg_code)."""
    cells = []
    fg, bg = None, None
    i = 0
    while i < len(line):
        if line[i] == '\x1b':
            m = re.match(r'\x1b\[([0-9;]*)m', line[i:])
            if m:
                code = m.group(1)
                i += len(m.group(0))
                if code in ('0', ''):
                    fg, bg = None, None
                elif code.startswith('38;2;'):
                    fg = code
                elif code.startswith('48;2;'):
                    bg = code
                elif code == '39':
                    fg = None
                elif code == '49':
                    bg = None
                continue
        cells.append((line[i], fg, bg))
        i += 1
    while len(cells) < target_width:
        cells.append((' ', None, None))
    return cells[:target_width]

def serialize_line(cells):
    """Rebuilds a list of (char, fg_code, bg_code) into an optimal ANSI string."""
    res = []
    last_fg, last_bg = None, None
    for ch, fg, bg in cells:
        if fg != last_fg or bg != last_bg:
            code = ''
            if fg is None and bg is None:
                code = '\x1b[0m'
            else:
                if fg != last_fg:
                    code += f'\x1b[{fg}m' if fg else '\x1b[39m'
                if bg != last_bg:
                    code += f'\x1b[{bg}m' if bg else '\x1b[49m'
            res.append(code)
            last_fg, last_bg = fg, bg
        res.append(ch)
    res.append('\x1b[0m')
    return ''.join(res)

def shift_code_to_ash(code):
    """Converts a 38;2;R;G;B or 48;2;R;G;B string into a desaturated Ash Gray shade."""
    if not code or ";2;" not in code:
        return code
    prefix, _, rgb = code.partition(";2;")
    try:
        r, g, b = map(int, rgb.split(";"))
        lum = int(0.299 * r + 0.587 * g + 0.114 * b)
        gr = max(15, int(lum * 0.65))
        gg = max(15, int(lum * 0.68))
        gb = max(18, int(lum * 0.74))
        return f"{prefix};2;{gr};{gg};{gb}"
    except Exception:
        return code

def create_dead_standing(intact_rows):
    """Returns an upright sprite shifted entirely into pale Deactivated Ash Gray."""
    out = []
    for r in intact_rows:
        cells = parse_line(r)
        ash_cells = [(ch, shift_code_to_ash(fg), shift_code_to_ash(bg)) for ch, fg, bg in cells]
        out.append(serialize_line(ash_cells))
    return out

# -----------------------------------------------------------------------------
# HERO TRI-STATES DEFINITIONS
# -----------------------------------------------------------------------------
HERO_TRI_STATES = {}

HERO_METADATA = {
    "D'ARCE": {
        "role": "Holy Paladin",
        "desc_normal": "Vũ khí nguyên vẹn, giáp sáng bóng, thể lực sung mãn",
        "desc_injured": "Cụt cánh tay phải, mất kiếm, khớp hổ phách #FFAA28 rực sáng",
        "desc_dead": "Gục ngã trên sàn đá, giáp sắt hoen xám tro tàn & vũng máu sẫm",
        "lore": "Thánh kỵ sĩ kiêu hãnh gục ngã trước bóng tối hầm ngục, máu thánh nhuộm đá lạnh."
    },
    "CAHARA": {
        "role": "Mercenary Rogue",
        "desc_normal": "Song đao linh hoạt, áo da gọn gàng, phản xạ nhạy bén",
        "desc_injured": "Đứt cổ tay, rơi song đao, khớp hổ phách #FFAA28 rực sáng",
        "desc_dead": "Co quắp bất động trên nền đá, sắc xám tro tàn & máu đông",
        "lore": "Tên lính đánh thuê ranh mãnh không thể trốn chạy khỏi số mệnh đoạt mạng."
    },
    "RAGNVALDR": {
        "role": "Outlander Berserker",
        "desc_normal": "Rìu chiến khổng lồ, lông thú hoang dã, cuồng nộ ngút trời",
        "desc_injured": "Chém đứt bắp tay phải, rơi rìu tạ, khớp hổ phách #FFAA28",
        "desc_dead": "Thân hình hộ pháp đổ sụp, tóc hung đỏ hóa tro xám, biển máu loang",
        "lore": "Chiến binh cuồng nộ ngã xuống, lời thề báo thù vĩnh viễn chìm vào bóng tối."
    },
    "ENKI": {
        "role": "Dark Occultist",
        "desc_normal": "Pháp y huyền bí, bàn tay thi triển tà thuật Gro-goroth",
        "desc_injured": "Bàn tay niệm chú bị phản phệ nát vụn, khớp hổ phách rực lửa",
        "desc_dead": "Áo choàng đen trải dài như vải liệm, mắt rỗng vô hồn, huyết đen",
        "lore": "Kẻ tìm kiếm tri thức cấm kỵ bị chính vực thẳm nuốt chửng linh hồn."
    },
    "LE'GARDE": {
        "role": "The Strategist",
        "desc_normal": "Kiếm liễu quý tộc, giáp bạc mạ vàng, tóc vàng vương giả",
        "desc_injured": "Cụt cổ tay cầm kiếm, kiếm gãy, khớp hổ phách #FFAA28",
        "desc_dead": "Kẻ định mệnh ngã sấp mặt, tóc vàng vấy bụi tro xám, máu quý tộc",
        "lore": "Giấc mộng trở thành vị thần mới tan vỡ thành mảnh vụn trên sàn ngục tối."
    },
    "THE GIRL": {
        "role": "Innocent Survivor",
        "desc_normal": "Thân hình nhỏ bé, đôi mắt sợ hãi nhưng kiên cường",
        "desc_injured": "Cánh tay nhỏ bị thương đứt đoạn, vết cắt hổ phách rỉ máu",
        "desc_dead": "Thể xác co ro trong tư thế bào thai, váy nâu bạc phếch, máu tươi",
        "lore": "Đứa trẻ vô tội vĩnh viễn ngủ say nơi đáy sâu tăm tối nhất của hầm ngục."
    },
    "MOONLESS": {
        "role": "Ancient Dire Wolf",
        "desc_normal": "Sói hắc ám 4 chân, nanh nhọn hoắt, đuôi vểnh oai phong",
        "desc_injured": "Cụt chân trước bên trái, khớp vai hổ phách, đứng 3 chân",
        "desc_dead": "Sói khổng lồ nằm nghiêng bất động, mắt khép, lông xám tro tàn",
        "lore": "Dã thú trung thành gục ngã bảo vệ chủ nhân, hơi thở cuối cùng hòa vào hư không."
    },
    "NAS'HRAH": {
        "role": "The Doom Prophet",
        "desc_normal": "Đầu lâu bay lơ lửng, vương miện lửa Gro-goroth rực cháy",
        "desc_injured": "Hộp sọ rạn vỡ, vết nứt hổ phách phóng tia ma thuật, lửa suy tàn",
        "desc_dead": "Đầu lâu rơi va vỡ trên sàn, lửa ma thuật tắt ngấm, quai hàm lệch",
        "lore": "Nhà tiên tri bất tử rớt khỏi không trung, lời nguyền rủa nghẹn lại trong tro bụi."
    }
}

# -----------------------------------------------------------------------------
# COLLAPSED DEAD BODIES ON DUNGEON FLOOR (Exact 12 rows, width 29)
# -----------------------------------------------------------------------------
FALLEN_CORPSES = {
    "D'ARCE": [
        "                             ",
        "                             ",
        "                             ",
        "                             ",
        "                             ",
        "                             ",
        f"{C_GRAY}        ▄▄▄▄▄▄▄              {C_RESET}",
        f"{C_GRAY}    ▄▀▀▀▀▀▀▀▀▀▀▀▀▀▄          {C_RESET}",
        f"{C_GRAY}   ▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▄ ▄▀     {C_RESET}",
        f"{C_GRAY}  ▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀    {C_RESET}",
        f"{C_DARK}   ▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀  ▀▄   {C_RESET}",
        f"{C_POOL}    ▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀          {C_RESET}"
    ],
    "CAHARA": [
        "                             ",
        "                             ",
        "                             ",
        "                             ",
        "                             ",
        "                             ",
        f"{C_GRAY}       ▄▄▄▀▀▀▀▄▄             {C_RESET}",
        f"{C_GRAY}    ▄▀▀▀▀▀▀▀▀▀▀▀▀▄           {C_RESET}",
        f"{C_GRAY}   ▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▄  ▄▀    {C_RESET}",
        f"{C_GRAY}  ▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀      {C_RESET}",
        f"{C_DARK}    ▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀         {C_RESET}",
        f"{C_POOL}     ▀▀▀▀▀▀▀▀▀▀▀▀            {C_RESET}"
    ],
    "RAGNVALDR": [
        "                             ",
        "                             ",
        "                             ",
        "                             ",
        "                             ",
        f"{C_GRAY}        ▄▄▄▄▄▄▄▄▄▄           {C_RESET}",
        f"{C_GRAY}     ▄▀▀▀▀▀▀▀▀▀▀▀▀▀▀▄        {C_RESET}",
        f"{C_GRAY}   ▄▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▄ ▄▀▄  {C_RESET}",
        f"{C_GRAY}  ▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀ {C_RESET}",
        f"{C_DARK}   ▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀    {C_RESET}",
        f"{C_DARK}     ▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀       {C_RESET}",
        f"{C_POOL}      ▀▀▀▀▀▀▀▀▀▀▀▀▀          {C_RESET}"
    ],
    "ENKI": [
        "                             ",
        "                             ",
        "                             ",
        "                             ",
        "                             ",
        "                             ",
        f"{C_GRAY}       ▄▄▀▀▀▀▄▄              {C_RESET}",
        f"{C_GRAY}    ▄▀▀▀▀▀▀▀▀▀▀▀▄            {C_RESET}",
        f"{C_GRAY}   ▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▄▄        {C_RESET}",
        f"{C_GRAY}  ▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▄     {C_RESET}",
        f"{C_DARK}   ▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀     {C_RESET}",
        f"{C_POOL}     ▀▀▀▀▀▀▀▀▀▀▀▀▀▀          {C_RESET}"
    ],
    "LE'GARDE": [
        "                             ",
        "                             ",
        "                             ",
        "                             ",
        "                             ",
        "                             ",
        f"{C_GRAY}        ▄▄▄▄▄▄▄▄             {C_RESET}",
        f"{C_GRAY}     ▄▀▀▀▀▀▀▀▀▀▀▀▀▄          {C_RESET}",
        f"{C_GRAY}   ▄▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▄   ▄   {C_RESET}",
        f"{C_GRAY}  ▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀    {C_RESET}",
        f"{C_DARK}    ▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀       {C_RESET}",
        f"{C_POOL}     ▀▀▀▀▀▀▀▀▀▀▀▀▀           {C_RESET}"
    ],
    "THE GIRL": [
        "                             ",
        "                             ",
        "                             ",
        "                             ",
        "                             ",
        "                             ",
        "                             ",
        f"{C_GRAY}       ▄▄▄▄▄▄                {C_RESET}",
        f"{C_GRAY}    ▄▀▀▀▀▀▀▀▀▀▀▄             {C_RESET}",
        f"{C_GRAY}   ▀▀▀▀▀▀▀▀▀▀▀▀▀▀▄           {C_RESET}",
        f"{C_DARK}    ▀▀▀▀▀▀▀▀▀▀▀▀▀▀           {C_RESET}",
        f"{C_POOL}      ▀▀▀▀▀▀▀                {C_RESET}"
    ],
    "MOONLESS": [
        "                             ",
        "                             ",
        "                             ",
        "                             ",
        "                             ",
        "                             ",
        f"{C_GRAY}   ▄▄▀▄                      {C_RESET}",
        f"{C_GRAY}  ▀▀▀▀▀▀▀▄▄▄▀▀▀▀▀▀▀▀▄▄▄      {C_RESET}",
        f"{C_GRAY}   ▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▄▄   {C_RESET}",
        f"{C_DARK}     ▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀  {C_RESET}",
        f"{C_DARK}       ▀▀▀▀▀▀▀▀ ▀▀▀▀▀ ▀▀▀▀   {C_RESET}",
        f"{C_POOL}        ▀▀▀▀▀▀▀▀▀▀           {C_RESET}"
    ],
    "NAS'HRAH": [
        "                             ",
        "                             ",
        "                             ",
        "                             ",
        "                             ",
        "                             ",
        "                             ",
        f"{C_GRAY}        ▄▀▀▀▀▀▀▀▄            {C_RESET}",
        f"{C_GRAY}       ▀▀▀▀▀▀▀▀▀▀▀           {C_RESET}",
        f"{C_DARK}      ▄▀▀▀▀▀▀▀▀▀▀▀           {C_RESET}",
        f"{C_DARK}      ▀▀▀▀▀▀▀▀▀▀▀            {C_RESET}",
        f"{C_POOL}       ▀▀▀▀▀▀▀▀▀▀            {C_RESET}"
    ]
}

# -----------------------------------------------------------------------------
# BUILD INJURED MODELS (Truecolor + Amber Stumps + Blood Drips)
# -----------------------------------------------------------------------------
CODE_AMBER = "38;2;255;170;40"
CODE_BLOOD = "38;2;160;25;25"

def build_injured_sprite(name):
    raw_rows = INTACT_HEROES.get(name, [" " * 29] * 12)
    rows = [parse_line(r) for r in raw_rows]
    
    if name == "D'ARCE":
        # Sever right sword & arm (rows 6..11, col >= 12)
        rows[6][12] = ('▀', CODE_AMBER, None)
        for c in range(13, 29): rows[6][c] = (' ', None, None)
        for r in range(7, 12):
            for c in range(12, 29): rows[r][c] = (' ', None, None)
        rows[7][12] = ('▄', CODE_BLOOD, None)
        # Left shield damage at row 4 col 0..3
        for c in range(0, 3): rows[4][c] = (' ', None, None)
        rows[4][3] = ('▀', CODE_AMBER, None)

    elif name == "CAHARA":
        # Sever twin daggers on right (rows 3..7, col >= 15)
        for r in range(3, 8):
            for c in range(15, 29): rows[r][c] = (' ', None, None)
        rows[5][15] = ('▀', CODE_AMBER, None)
        rows[6][15] = ('▄', CODE_BLOOD, None)
        # Sever off-hand at left row 5 col 0..2
        rows[5][2] = ('▀', CODE_AMBER, None)

    elif name == "RAGNVALDR":
        # Sever massive waraxe on right (rows 4..8, col >= 15)
        for r in range(4, 9):
            for c in range(15, 29): rows[r][c] = (' ', None, None)
        rows[5][15] = ('▀', CODE_AMBER, None)
        rows[6][15] = ('▄', CODE_BLOOD, None)

    elif name == "ENKI":
        # Sever right casting arm (rows 5..8, col >= 12)
        for r in range(5, 9):
            for c in range(12, 29): rows[r][c] = (' ', None, None)
        rows[5][12] = ('▀', CODE_AMBER, None)
        rows[6][12] = ('▄', CODE_BLOOD, None)

    elif name == "LE'GARDE":
        # Sever rapier sword (rows 2..7, col >= 13)
        for r in range(2, 8):
            for c in range(13, 29): rows[r][c] = (' ', None, None)
        rows[4][13] = ('▀', CODE_AMBER, None)
        rows[5][13] = ('▄', CODE_BLOOD, None)

    elif name == "THE GIRL":
        # Sever small arm (rows 5..7, col >= 10)
        for r in range(5, 8):
            for c in range(10, 29): rows[r][c] = (' ', None, None)
        rows[5][10] = ('▀', CODE_AMBER, None)
        rows[6][10] = ('▄', CODE_BLOOD, None)

    elif name == "MOONLESS":
        # Quadruped dire wolf: sever front paw (row 8..9, col 0..5)
        for c in range(0, 5):
            rows[8][c] = (' ', None, None)
        rows[8][2] = ('▀', CODE_AMBER, None)
        rows[9][2] = ('▄', CODE_BLOOD, None)

    elif name == "NAS'HRAH":
        # Floating skull: arcane amber fractures cutting through bone
        rows[1][5] = ('▀', CODE_AMBER, None)
        rows[2][6] = ('▄', CODE_AMBER, None)
        rows[3][7] = ('▀', CODE_AMBER, None)
        rows[7][4] = ('▀', CODE_AMBER, None)

    return [serialize_line(r) for r in rows]

# Assemble the catalog
HERO_ORDER = ["D'ARCE", "CAHARA", "RAGNVALDR", "ENKI", "LE'GARDE", "THE GIRL", "MOONLESS", "NAS'HRAH"]

for h in HERO_ORDER:
    intact = INTACT_HEROES.get(h, [" " * 29] * 12)
    inj = build_injured_sprite(h)
    dead = FALLEN_CORPSES.get(h, [" " * 29] * 12)
    dead_standing = create_dead_standing(intact)
    meta = HERO_METADATA.get(h, {})

    HERO_TRI_STATES[h] = {
        "name": h,
        "role": meta.get("role", "Survivor"),
        "normal": intact,
        "injured": inj,
        "dead": dead,
        "dead_standing": dead_standing,
        "desc_normal": meta.get("desc_normal", "Normal"),
        "desc_injured": meta.get("desc_injured", "Injured"),
        "desc_dead": meta.get("desc_dead", "Dead"),
        "lore": meta.get("lore", "")
    }

if __name__ == "__main__":
    print(f"Hero Tri-State Catalog Loaded: {len(HERO_TRI_STATES)} heroes.")
    for name in HERO_ORDER:
        d = HERO_TRI_STATES[name]
        print(f"  - {name:<12} ({d['role']}): norm={len(d['normal'])}, inj={len(d['injured'])}, dead={len(d['dead'])}")
