#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
================================================================================
ITEM MODEL CATALOG (BỘ MÔ HÌNH PIXEL ART VẬT PHẨM TỦ ĐỒ)
Fear & Hunger: Terminal Labyrinth - Solo Explorer Architecture
================================================================================
Tất cả 7 mô hình được xây dựng chuẩn xác 100% từ Module Phần Cứng Verilog
`sprite_rom.v` (ID 0..5, kích thước 20x20 bit) và `key_sprite_rom.v`:
  1. TOTEM OF UNDYING (ID 4): Thần tượng Minecraft mắt ngọc lục bảo, thân vàng rực.
  2. POPPY FLOWER     (ID 3): Hoa anh túc đỏ thẫm 8 cánh, đài lá xanh & thân cây.
  3. MARIJUANA HERB   (ID 5): Lá thảo dược răng cưa 5 cánh đa tầng xanh biếc.
  4. MOLDY BREAD      (ID 2): Ổ Baguette nướng giòn với 3 khía vát xiên đặc trưng.
  5. DRIED MEAT       (ID 0): Đùi thịt cầm tay rút xương trắng, thịt nướng xông khói.
  6. ALCHEMICAL VIAL  (ID 1): Bình thuốc nút bần, cổ loe, thân thủy tinh & nhãn Hexen.
  7. RUNIC KEY             : Chìa khóa sắt cổ ngữ Hexen đúc ren ma thuật (Bảng 3).

Kỹ thuật kết xuất Half-Block (▀ / ▄ / █) với ANSI TrueColor (24-bit RGB):
  - Tỷ lệ hiển thị chuẩn xác 1:1 hình vuông trên mỗi điểm ảnh (pixel).
  - Khung nhìn chuẩn xác: Đúng 12 dòng, chiều rộng đúng 29 ký tự (pad 4 trái, 5 phải).
================================================================================
"""

import os
import re

ANSI_RE = re.compile(r'\x1b\[[0-9;]*m')

def vis_len(s):
    return len(ANSI_RE.sub('', s))

def fit_exact_29(s):
    w = vis_len(s)
    if w < 29:
        return s + ' ' * (29 - w)
    elif w > 29:
        # Cắt bớt khoảng trắng thừa nếu có
        lspaces = len(s) - len(s.lstrip(' '))
        cut = w - 29
        if lspaces >= cut:
            s = s[cut:]
            return s + ' ' * (29 - vis_len(s))
    return s

def _color_fg_bg(fg_rgb, bg_rgb, char):
    fg_s = f"\033[38;2;{fg_rgb[0]};{fg_rgb[1]};{fg_rgb[2]}m" if fg_rgb else ""
    bg_s = f"\033[48;2;{bg_rgb[0]};{bg_rgb[1]};{bg_rgb[2]}m" if bg_rgb else ""
    rst = "\033[0m"
    return f"{fg_s}{bg_s}{char}{rst}"

def _render_halfblock_grid(pixel_map, width=20, height=20, pad_left=4, pad_right=5):
    """
    Kết xuất lưới điểm ảnh thành danh sách 12 dòng văn bản (mỗi dòng 29 ký tự hiển thị).
      Dòng 0 : 29 dấu cách trống.
      Dòng 1..10: pad_left + 20 ký tự half-block + pad_right (quét 2 pixel dọc y, y+1 mỗi dòng).
      Dòng 11: 29 dấu cách trống.
    """
    lines = [" " * 29]
    for r in range(10):
        y_top = r * 2
        y_bot = r * 2 + 1
        row_str = " " * pad_left
        for x in range(width):
            c_top = pixel_map.get((x, y_top))
            c_bot = pixel_map.get((x, y_bot))
            if c_top and c_bot:
                if c_top == c_bot:
                    row_str += _color_fg_bg(c_top, None, "█")
                else:
                    row_str += _color_fg_bg(c_top, c_bot, "▀")
            elif c_top and not c_bot:
                row_str += _color_fg_bg(c_top, None, "▀")
            elif not c_top and c_bot:
                row_str += _color_fg_bg(c_bot, None, "▄")
            else:
                row_str += " "
        row_str += " " * pad_right
        assert vis_len(row_str) == 29, f"Row {r} width {vis_len(row_str)} != 29"
        lines.append(row_str)
    lines.append(" " * 29)
    assert len(lines) == 12
    return lines

# -----------------------------------------------------------------------------
# DỮ LIỆU BITMAP TỪ SPRITE_ROM VERILOG (20x20 BITS CHO 6 MÔ HÌNH)
# -----------------------------------------------------------------------------
_RAW_ROM = {
    # --- ID 0: Đùi gà (Meat Drumstick) ---
    0:  "00000000000000010110",
    1:  "00000000000000111111",
    2:  "00000000000000011110",
    3:  "00000000000000111000",
    4:  "00000000000001100000",
    5:  "00000000000111000000",
    6:  "00000000011111100000",
    7:  "00000001111111110000",
    8:  "00000111111111111000",
    9:  "00001100111111111100",
    10: "00011001111111111100",
    11: "00110101111111111000",
    12: "00101011111111110000",
    13: "00100101111111100000",
    14: "00110101011111000000",
    15: "00011010101110000000",
    16: "00001111011100000000",
    17: "00000111111000000000",
    18: "00000000000000000000",
    19: "00000000000000000000",

    # --- ID 1: Lọ thuốc (Potion Bottle) ---
    20: "00000000000000000000",
    21: "00000000111100000000",
    22: "00000001111110000000",
    23: "00000000000000000000",
    24: "00000001111110000000",
    25: "00000000111100000000",
    26: "00000000100100000000",
    27: "00000111100111100000",
    28: "00001000000000010000",
    29: "00010011111111001000",
    30: "00010100011111101000",
    31: "00010100111111101000",
    32: "00010100011111101000",
    33: "00010100000111101000",
    34: "00010011111111001000",
    35: "00001000000000010000",
    36: "00000111111111100000",
    37: "00000000000000000000",
    38: "00000000000000000000",
    39: "00000000000000000000",

    # --- ID 2: Bánh mì Baguette (Bread) ---
    40: "00000000000000000000",
    41: "00000000000000000000",
    42: "00000000000000000000",
    43: "00000000001111000000",
    44: "00000000011111100000",
    45: "00000000100001100000",
    46: "00000001101110100000",
    47: "00000011100001100000",
    48: "00000111111111000000",
    49: "00000100000110000000",
    50: "00001101111010000000",
    51: "00001100000100000000",
    52: "00001111111000000000",
    53: "00011000010000000000",
    54: "00010111100000000000",
    55: "00010000100000000000",
    56: "00011111000000000000",
    57: "00001110000000000000",
    58: "00000000000000000000",
    59: "00000000000000000000",

    # --- ID 3: Hoa anh túc (Poppy Flower) ---
    60: "00000000000000000000",
    61: "00000000000000000000",
    62: "00000000000000000000",
    63: "00000000011000000000",
    64: "00000001111110000000",
    65: "00000011100111000000",
    66: "00000011011011000000",
    67: "00000011011011000000",
    68: "00000011100111000000",
    69: "00000001111110000000",
    70: "00000000011000000000",
    71: "00000000000000000000",
    72: "00000111011011100000",
    73: "00001011111111010000",
    74: "00000010111101000000",
    75: "00000001111110000000",
    76: "00000000011000000000",
    77: "00000000011000000000",
    78: "00000000000000000000",
    79: "00000000000000000000",

    # --- ID 4: Thần tượng bất tử (Totem of Undying) ---
    80: "00000000000000000000",
    81: "00000000000000000000",
    82: "00000001111110000000",
    83: "00000011111111000000",
    84: "00000011111111000000",
    85: "00000011111111000000",
    86: "00000011001100100000",
    87: "00000011001100100000",
    88: "00000011111111000000",
    89: "00011111111111111000",
    90: "00011111111111111000",
    91: "00001111111111110000",
    92: "00000011111111000000",
    93: "00000011111111000000",
    94: "00000001111110000000",
    95: "00000001111110000000",
    96: "00000000111100000000",
    97: "00000000000000000000",
    98: "00000000000000000000",
    99: "00000000000000000000",

    # --- ID 5: Chiếc lá thảo dược (Marijuana Leaf) ---
    100: "00000000011000000000",
    101: "00000000111100000000",
    102: "00000000111100000000",
    103: "00010000111100001000",
    104: "00111001111110011100",
    105: "00111101111110111100",
    106: "00111111111111111100",
    107: "00111111111111111100",
    108: "00011111111111111000",
    109: "00011111111111111000",
    110: "00001111111111110000",
    111: "01111111111111111110",
    112: "11111111111111111111",
    113: "11111111111111111111",
    114: "01111111111111111110",
    115: "00111111111111111100",
    116: "00001111111111110000",
    117: "00000111111111100000",
    118: "00000011100111000000",
    119: "00000000011000000000"
}

# -----------------------------------------------------------------------------
# 1. TẠO MÃ MÀU PIXEL ART CHO TỪNG VẬT PHẨM
# -----------------------------------------------------------------------------
def _build_totem_sprite():
    m = {}
    for y in range(20):
        b = _RAW_ROM[4 * 20 + y]
        for x in range(20):
            if b[x] == '1':
                if 6 <= y <= 7 and (x in (8, 9) or x in (12, 13)):
                    m[(x, y)] = (0, 245, 140)  # Mắt ngọc lục bảo Emerald
                elif 2 <= y <= 5 and 8 <= x <= 11:
                    m[(x, y)] = (255, 235, 145)  # Trán và sống mũi vàng sáng
                elif 9 <= y <= 11 and (x <= 6 or x >= 13):
                    m[(x, y)] = (185, 105, 25)   # Cánh tay nâu đồng
                elif y in (2, 8, 16):
                    m[(x, y)] = (170, 90, 20)    # Viền tối
                else:
                    m[(x, y)] = (230, 160, 45)   # Thân vàng gold
    return _render_halfblock_grid(m)

def _build_poppy_sprite():
    m = {}
    for y in range(20):
        b = _RAW_ROM[3 * 20 + y]
        for x in range(20):
            if b[x] == '1':
                if y <= 10:
                    if 6 <= y <= 7 and 9 <= x <= 10:
                        m[(x, y)] = (255, 220, 60) # Nhụy vàng kim
                    else:
                        m[(x, y)] = (235, 45, 60) if (x + y) % 2 == 0 else (205, 25, 40) # Cánh đỏ rực
                elif y <= 15:
                    m[(x, y)] = (50, 195, 95) if y <= 13 else (35, 160, 75) # Lá xanh tươi
                else:
                    m[(x, y)] = (25, 115, 50) # Thân cây xanh thẫm
    return _render_halfblock_grid(m)

def _build_weed_sprite():
    m = {}
    for y in range(20):
        b = _RAW_ROM[5 * 20 + y]
        for x in range(20):
            if b[x] == '1':
                if y <= 3:
                    m[(x, y)] = (110, 230, 65) # Đỉnh lá xanh non
                elif y >= 17:
                    m[(x, y)] = (20, 100, 35)  # Cuống lá
                elif 4 <= y <= 10:
                    m[(x, y)] = (65, 195, 50) if (x + y) % 2 == 0 else (45, 165, 40) # Răng cưa
                else:
                    m[(x, y)] = (35, 140, 35)  # Tán lá trung tâm
    return _render_halfblock_grid(m)

def _build_bread_sprite():
    m = {}
    for y in range(20):
        b = _RAW_ROM[2 * 20 + y]
        for x in range(20):
            if b[x] == '1':
                if y in (3, 4, 16, 17) or x in (3, 4, 14, 15):
                    m[(x, y)] = (195, 115, 35) # Vỏ bánh nướng caramen
                elif (x + y) % 3 == 0:
                    m[(x, y)] = (255, 215, 115) # Khía nướng xẻ vàng sáng
                else:
                    m[(x, y)] = (235, 170, 65)  # Ruột bánh vàng ươm
    return _render_halfblock_grid(m)

def _build_meat_sprite():
    m = {}
    for y in range(20):
        b = _RAW_ROM[0 * 20 + y]
        for x in range(20):
            if b[x] == '1':
                if y <= 5 or (x >= 14 and y <= 8):
                    m[(x, y)] = (245, 240, 225) if (x >= 16 or y <= 2) else (210, 200, 185) # Đầu xương trắng ngà
                elif y >= 15:
                    m[(x, y)] = (150, 40, 25) # Đế thịt nướng đậm
                elif x <= 7:
                    m[(x, y)] = (220, 80, 50) # Thớ thịt nướng đỏ hồng
                else:
                    m[(x, y)] = (195, 60, 35) # Nạc thịt xông khói
    return _render_halfblock_grid(m)

def _build_potion_sprite():
    m = {}
    for y in range(20):
        b = _RAW_ROM[1 * 20 + y]
        for x in range(20):
            if b[x] == '1':
                if y <= 3:
                    m[(x, y)] = (205, 135, 65) # Nút bần gỗ
                elif y <= 6:
                    m[(x, y)] = (140, 210, 250) # Cổ chai thủy tinh
                elif y in (7, 8, 15, 16) or x in (3, 4, 15, 16):
                    m[(x, y)] = (85, 175, 230)  # Thân thủy tinh xanh trong suốt
                elif y in (10, 11, 12) and x in (5, 6, 7, 8):
                    m[(x, y)] = (250, 245, 235) # Nhãn giấy chú ấn trắng
                else:
                    m[(x, y)] = (215, 45, 130)  # Dung dịch tiên dược hồng ngọc
    return _render_halfblock_grid(m)

def _build_key_sprite():
    # Chìa khóa Runic Key lấy trực tiếp từ key_sprite_rom.v (11 cột x 22 hàng)
    src_path = os.path.join(os.path.dirname(__file__), "src", "key_sprite_rom.v")
    key_map = {}
    if os.path.exists(src_path):
        with open(src_path, "r", encoding="utf-8") as f:
            v_text = f.read()
        for m in re.finditer(r"6\'d(\d+):\s*begin\s*case\s*\(col\)(.*?)endcase", v_text, re.DOTALL):
            row = int(m.group(1))
            body = m.group(2)
            for mc in re.finditer(r"6\'d(\d+):\s*begin\s*is_transparent\s*=\s*1\'b0;\s*color_rgb\s*=\s*24\'h([0-9a-fA-F]{6});", body):
                col = int(mc.group(1))
                hex_c = mc.group(2)
                r = int(hex_c[0:2], 16)
                g = int(hex_c[2:4], 16)
                b = int(hex_c[4:6], 16)
                key_map[(col, row)] = (r, g, b)
    else:
        # Fallback tọa độ chìa khóa cổ nếu file v chưa nạp
        for r in range(22):
            for c in range(11):
                if 2 <= r <= 9 or (10 <= r <= 20 and 4 <= c <= 6):
                    key_map[(c, r)] = (245, 185, 30)

    lines = [" " * 29]
    for r in range(11):
        y_top = r * 2
        y_bot = r * 2 + 1
        row_str = " " * 9
        for x in range(11):
            c_top = key_map.get((x, y_top))
            c_bot = key_map.get((x, y_bot))
            if c_top and c_bot:
                if c_top == c_bot:
                    row_str += f"\033[38;2;{c_top[0]};{c_top[1]};{c_top[2]}m█\033[0m"
                else:
                    row_str += f"\033[38;2;{c_top[0]};{c_top[1]};{c_top[2]}m\033[48;2;{c_bot[0]};{c_bot[1]};{c_bot[2]}m▀\033[0m"
            elif c_top:
                row_str += f"\033[38;2;{c_top[0]};{c_top[1]};{c_top[2]}m▀\033[0m"
            elif c_bot:
                row_str += f"\033[38;2;{c_bot[0]};{c_bot[1]};{c_bot[2]}m▄\033[0m"
            else:
                row_str += " "
        row_str += " " * 9
        assert vis_len(row_str) == 29
        lines.append(row_str)
    assert len(lines) == 12
    return lines

totem_sprite  = _build_totem_sprite()
poppy_sprite  = _build_poppy_sprite()
weed_sprite   = _build_weed_sprite()
bread_sprite  = _build_bread_sprite()
meat_sprite   = _build_meat_sprite()
bottle_sprite = _build_potion_sprite()
key_sprite    = _build_key_sprite()

# -----------------------------------------------------------------------------
# 2. BẢNG MỤC LỤC TỦ ĐỒ HOÀN CHỈNH (CANONICAL ITEM CATALOG)
# -----------------------------------------------------------------------------
ITEM_CATALOG = [
    {
        "id": "totem",
        "name": "TOTEM OF UNDYING",
        "type": "CỔ VẬT BẢO MỆNH",
        "qty": 1,
        "max_qty": 2,
        "effect": "Hồi Sinh Tức Thì Khi Tử Vong",
        "cure": "Cứu Nguy 1 Lần Khi HP Về 0",
        "target": "Toàn Bộ Cơ Thể",
        "usage": "Tự Động Khi HP Chạm 0",
        "rarity": "Cổ Vật Thần Thoại",
        "lore": [
            "Thần tượng cổ xưa tạc hình linh hồn hộ mệnh với đôi mắt ngọc lục bảo.",
            "Khi chủ nhân nhận đòn chí tử, thần tượng sẽ vỡ nát để giải phóng",
            "nguồn sinh lực thần thánh, hồi sinh và ban tặng hào quang hộ thể."
        ],
        "sprite": totem_sprite
    },
    {
        "id": "poppy",
        "name": "POPPY FLOWER",
        "type": "DƯỢC LIỆU CẦM MÁU",
        "qty": 4,
        "max_qty": 10,
        "effect": "Hồi 30 HP & Chặn Chảy Máu",
        "cure": "Chảy Máu Cấp Tính, Trầy Xước",
        "target": "Tứ Chi & Da Thịt",
        "usage": "Khám Phá & Combat",
        "rarity": "Thảo Dược Phổ Thông",
        "lore": [
            "Hoa anh túc đỏ thẫm sinh trưởng nơi kẽ đá ẩm ướt của hầm ngục.",
            "Nhựa hoa có đặc tính giảm đau cực mạnh và làm đông máu tức thì,",
            "giúp ngăn chặn tử vong do mất máu ồ ạt trong bóng tối."
        ],
        "sprite": poppy_sprite
    },
    {
        "id": "weed",
        "name": "MARIJUANA HERB",
        "type": "THẢO DƯỢC AN THẦN",
        "qty": 2,
        "max_qty": 5,
        "effect": "Hồi 70 HP & +25 Tỉnh Táo",
        "cure": "Chấn Thương Nặng & Hoảng Loạn",
        "target": "Hệ Thần Kinh & Tâm Trí",
        "usage": "Khám Phá & Combat",
        "rarity": "Thảo Dược Quý Hiếm",
        "lore": [
            "Lá thảo dược xanh thẫm tỏa hương thơm nồng nàn xoa dịu thần kinh.",
            "Khói đốt từ lá khô giúp người thám hiểm lấy lại sự bình tĩnh,",
            "xua tan ảo giác điên loạn và phục hồi cơ bắp rách nát."
        ],
        "sprite": weed_sprite
    },
    {
        "id": "bread",
        "name": "MOLDY BREAD",
        "type": "LƯƠNG THỰC SINH TỒN",
        "qty": 3,
        "max_qty": 10,
        "effect": "-40 Đói Khát & Cứu Đói",
        "cure": "Cơn Đói Cồn Cào, Hoa Mắt",
        "target": "Dạ Dày & Thể Lực",
        "usage": "Khám Phá Bản Đồ (Map)",
        "rarity": "Lương Khô Phổ Thông",
        "lore": [
            "Ổ bánh mì Baguette nướng giòn với ba đường rạch vát vàng ươm.",
            "Dù có chút vết mốc bên ngoài nhưng vẫn là nguồn lương thực quý giá",
            "giúp bạn sống sót qua những ngày dài đói lả trong ngục tối."
        ],
        "sprite": bread_sprite
    },
    {
        "id": "meat",
        "name": "DRIED MEAT",
        "type": "LƯƠNG THỰC CAO CẤP",
        "qty": 2,
        "max_qty": 10,
        "effect": "-60 Đói Khát & +20 HP",
        "cure": "Đói Lả, Kiệt Quệ Thể Lực",
        "target": "Dạ Dày & Cơ Bắp",
        "usage": "Khám Phá Bản Đồ (Map)",
        "rarity": "Lương Khô Quý",
        "lore": [
            "Khúc đùi thịt sấy muối xông khói với thớ thịt săn chắc và đầu xương trắng.",
            "Lớp mỡ giòn dai cung cấp nguồn năng lượng khổng lồ, hồi phục",
            "sinh lực và thể lực sau những trận huyết chiến ác liệt."
        ],
        "sprite": meat_sprite
    },
    {
        "id": "vial",
        "name": "ALCHEMICAL VIAL",
        "type": "CỒN SÁT TRÙNG",
        "qty": 2,
        "max_qty": 5,
        "effect": "Xóa Nhiễm Trùng & Độc Tố",
        "cure": "Hoại Tử, Nhiễm Trùng Máu",
        "target": "Vết Cắt & Khớp Xương",
        "usage": "Khám Phá & Combat",
        "rarity": "Dung Dịch Thuật Giả Kim",
        "lore": [
            "Bình thủy tinh có nút bần và nhãn chú ấn Hexen chứa dung dịch thanh tẩy.",
            "Rót trực tiếp vào vết thương để thiêu đốt sạch sẽ vi khuẩn",
            "hoại thư, ngăn ngừa vết cắt chuyển sang màu xanh độc địa."
        ],
        "sprite": bottle_sprite
    },
    {
        "id": "key",
        "name": "RUNIC KEY",
        "type": "CHÌA KHÓA CỔ NGỮ",
        "qty": 2,
        "max_qty": 3,
        "effect": "Mở Cổng Thoát Hiểm Đông",
        "cure": "Cần 3 Chìa Mở Cổng",
        "target": "Cổng Đá Ma Thuật",
        "usage": "Cổng Labyrinth",
        "rarity": "Vật Phẩm Nhiệm Vụ",
        "lore": [
            "Chiếc chìa khóa sắt đúc cổ xưa có gắn ấn chú Hexen kỳ bí.",
            "Thu thập đủ 3 chiếc chìa khóa này từ quái vật tinh anh và hòm rương",
            "để mở toang Cánh Cổng Phía Đông và trốn thoát khỏi Labyrinth."
        ],
        "sprite": key_sprite
    }
]

if __name__ == "__main__":
    print(f"Loaded {len(ITEM_CATALOG)} items from Item Model Catalog.")
    for it in ITEM_CATALOG:
        print(f"Item: {it['name']} ({it['id']}) - Sprite rows: {len(it['sprite'])}")
        assert len(it['sprite']) == 12
        for line in it['sprite']:
            assert vis_len(line) == 29
    print("All item sprites validated with 100% exact dimensions (12 rows x 29 cols)!")
