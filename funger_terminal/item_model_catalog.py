#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
================================================================================
ITEM MODEL CATALOG (BỘ MÔ HÌNH PIXEL ART VẬT PHẨM TỦ ĐỒ)
Fear & Hunger: Terminal Labyrinth - Solo Explorer Architecture
================================================================================
Tất cả 7 mô hình được xây dựng chuẩn xác từ các ảnh pixel art người dùng cung cấp:
  1. TOTEM OF UNDYING : Thần tượng Minecraft mắt ngọc lục bảo, thân vàng (Ảnh Totem).
  2. POPPY FLOWER     : Hoa anh túc đỏ thẫm có lá và đài hoa (Ảnh Flower).
  3. MARIJUANA HERB   : Lá thảo dược răng cưa 5 cánh xanh biếc (Ảnh Leaf Grid).
  4. MOLDY BREAD      : Ổ Baguette nướng giòn với 3 khía vát vàng sáng (Ảnh Bread).
  5. DRIED MEAT       : Đùi thịt cầm tay rút xương đỏ hồng (Ảnh Meat Drumstick).
  6. ALCHEMICAL VIAL  : Bình thuốc cổ nút bần nhãn chú ấn Hexen (Ảnh Potion Bottle).
  7. RUNIC KEY        : Chìa khóa sắt cổ ngữ Hexen đúc ren ma thuật (Bảng 3).
Mỗi mô hình chuẩn xác 12 dòng, chiều rộng 29 ký tự, phối màu ANSI TrueColor rực rỡ.
================================================================================
"""

import re

ANSI_RE = re.compile(r'\x1b\[[0-9;]*m')

def fit_exact_29(s):
    w = len(ANSI_RE.sub('', s))
    if w < 29:
        return s + ' ' * (29 - w)
    elif w > 29:
        lspaces = len(s) - len(s.lstrip(' '))
        cut = w - 29
        if lspaces >= cut:
            s = s[cut:]
            return s + ' ' * (29 - len(ANSI_RE.sub('', s)))
    return s

C_RST = "\033[0m"

# -----------------------------------------------------------------------------
# 1. TOTEM OF UNDYING (Minecraft)
# -----------------------------------------------------------------------------
C_OUT = "\033[38;2;160;70;15m"    # Viền nâu đậm
C_ARM = "\033[38;2;182;90;23m"    # Cánh tay nâu
C_GLD = "\033[38;2;220;140;40m"   # Thân vàng gold
C_YEL = "\033[38;2;252;225;130m"  # Vàng sáng trán & sống mũi
C_EYE = "\033[38;2;0;235;140m"    # Mắt ngọc lục bảo Emerald
C_WHT = "\033[1;37m"              # Điểm sáng mắt

totem_sprite = [
    fit_exact_29(f"        {C_OUT}▄▄▄▄▄▄▄▄▄▄▄▄{C_RST}"),
    fit_exact_29(f"      {C_OUT}▄█{C_YEL}████████████{C_OUT}█▄{C_RST}"),
    fit_exact_29(f"       {C_OUT}█{C_GLD}██{C_YEL}████████{C_GLD}██{C_OUT}█{C_RST}"),
    fit_exact_29(f"       {C_OUT}█{C_GLD}██{C_WHT}█{C_EYE}█{C_YEL}████{C_WHT}█{C_EYE}█{C_GLD}██{C_OUT}█{C_RST}"),
    fit_exact_29(f"       {C_OUT}█{C_GLD}██{C_EYE}██{C_YEL}████{C_EYE}██{C_GLD}██{C_OUT}█{C_RST}"),
    fit_exact_29(f"       {C_OUT}█{C_GLD}████{C_YEL}████{C_GLD}████{C_OUT}█{C_RST}"),
    fit_exact_29(f"   {C_OUT}▄▄▄▄▄{C_OUT}██{C_GLD}██{C_YEL}████{C_GLD}██{C_OUT}██{C_OUT}▄▄▄▄▄{C_RST}"),
    fit_exact_29(f"  {C_OUT}█{C_ARM}██████{C_OUT}█{C_GLD}████████{C_OUT}█{C_ARM}██████{C_OUT}█{C_RST}"),
    fit_exact_29(f"   {C_OUT}▀▀▀▀▀{C_OUT}██{C_YEL}████████{C_OUT}██{C_OUT}▀▀▀▀▀{C_RST}"),
    fit_exact_29(f"       {C_OUT}█{C_GLD}████████████{C_OUT}█{C_RST}"),
    fit_exact_29(f"       {C_OUT}█{C_ARM}████████████{C_OUT}█{C_RST}"),
    fit_exact_29(f"        {C_OUT}▀▀▀▀▀▀▀▀▀▀▀▀{C_RST}")
]

# -----------------------------------------------------------------------------
# 2. POPPY FLOWER (Hoa anh túc)
# -----------------------------------------------------------------------------
C_RED1 = "\033[38;2;235;45;45m"
C_RED2 = "\033[38;2;180;25;25m"
C_CORE = "\033[38;2;70;20;20m"
C_PLN  = "\033[38;2;250;210;50m"
C_GRN1 = "\033[38;2;55;185;65m"
C_GRN2 = "\033[38;2;30;125;40m"

poppy_sprite = [
    fit_exact_29(f"          {C_RED1}▄▄▄████▄▄▄{C_RST}"),
    fit_exact_29(f"       {C_RED1}▄██████████████▄{C_RST}"),
    fit_exact_29(f"      {C_RED1}████{C_RED2}██████████{C_RED1}████{C_RST}"),
    fit_exact_29(f"      {C_RED1}████{C_CORE}██{C_PLN}████{C_CORE}██{C_RED1}████{C_RST}"),
    fit_exact_29(f"      {C_RED1}████{C_PLN}██{C_CORE}████{C_PLN}██{C_RED1}████{C_RST}"),
    fit_exact_29(f"      {C_RED2}████{C_CORE}██{C_PLN}████{C_CORE}██{C_RED2}████{C_RST}"),
    fit_exact_29(f"       {C_RED2}▀██████████████▀{C_RST}"),
    fit_exact_29(f"          {C_RED2}▀▀▀████▀▀▀{C_RST}"),
    fit_exact_29(f"   {C_GRN1}▄▄▄▄{C_RST}       {C_GRN2}██{C_RST}       {C_GRN1}▄▄▄▄{C_RST}"),
    fit_exact_29(f"  {C_GRN1}██████▄▄{C_RST}    {C_GRN2}██{C_RST}    {C_GRN1}▄▄██████{C_RST}"),
    fit_exact_29(f"   {C_GRN1}▀███████▄{C_RST}  {C_GRN2}██{C_RST}  {C_GRN1}▄███████▀{C_RST}"),
    fit_exact_29(f"      {C_GRN1}▀▀███{C_RST}   {C_GRN2}██{C_RST}   {C_GRN1}███▀▀{C_RST}")
]

# -----------------------------------------------------------------------------
# 3. MARIJUANA HERB (Lá thảo mộc răng cưa)
# -----------------------------------------------------------------------------
C_LF1 = "\033[38;2;90;210;85m"
C_LF2 = "\033[38;2;45;155;50m"
C_LF3 = "\033[38;2;25;105;30m"

weed_sprite = [
    fit_exact_29(f"             {C_LF1}▄██▄{C_RST}"),
    fit_exact_29(f"           {C_LF1}▄██████▄{C_RST}"),
    fit_exact_29(f"   {C_LF1}▄██▄{C_RST}    {C_LF2}████████{C_RST}    {C_LF1}▄██▄{C_RST}"),
    fit_exact_29(f"   {C_LF1}██████▄{C_RST} {C_LF2}████████{C_RST} {C_LF1}▄██████{C_RST}"),
    fit_exact_29(f"   {C_LF2}▀████████████████████▀{C_RST}"),
    fit_exact_29(f"     {C_LF2}▀████████████████▀{C_RST}"),
    fit_exact_29(f"  {C_LF1}▄██████{C_RST}  {C_LF2}████████{C_RST}  {C_LF1}▄██████▄{C_RST}"),
    fit_exact_29(f"  {C_LF2}▀██████▄▄████████▄▄██████▀{C_RST}"),
    fit_exact_29(f"    {C_LF2}▀▀████████████████▀▀{C_RST}"),
    fit_exact_29(f"       {C_LF3}▀████████████▀{C_RST}"),
    fit_exact_29(f"           {C_LF3}████████{C_RST}"),
    fit_exact_29(f"             {C_LF3}████{C_RST}")
]

# -----------------------------------------------------------------------------
# 4. MOLDY BREAD (Ổ Baguette nướng giòn khía xẻ)
# -----------------------------------------------------------------------------
C_BR1 = "\033[38;2;230;160;60m"
C_BR2 = "\033[38;2;180;110;40m"
C_CUT = "\033[38;2;255;235;150m"
C_DKB = "\033[38;2;130;70;20m"

bread_sprite = [
    fit_exact_29(f"                 {C_BR1}▄▄████▄▄{C_RST}"),
    fit_exact_29(f"             {C_BR1}▄▄████████████▄{C_RST}"),
    fit_exact_29(f"           {C_BR1}▄██{C_CUT}████{C_BR1}████{C_CUT}████{C_BR1}██▄{C_RST}"),
    fit_exact_29(f"       {C_BR1}▄▄██████{C_CUT}██{C_BR1}██████{C_CUT}██{C_BR1}████▄{C_RST}"),
    fit_exact_29(f"     {C_BR1}▄██████████{C_CUT}██{C_BR1}██████{C_CUT}██{C_BR1}████▀{C_RST}"),
    fit_exact_29(f"   {C_BR1}▄██████{C_CUT}████{C_BR1}██████{C_CUT}██{C_BR1}██████▀{C_RST}"),
    fit_exact_29(f" {C_BR2}▄████████{C_CUT}██{C_BR2}██████{C_CUT}██{C_BR2}██████▀{C_RST}"),
    fit_exact_29(f" {C_BR2}▀██████████{C_CUT}██{C_BR2}████████████▀{C_RST}"),
    fit_exact_29(f"  {C_DKB}▀██████████████████████▀{C_RST}"),
    fit_exact_29(f"    {C_DKB}▀▀████████████████▀▀{C_RST}"),
    fit_exact_29(f"        {C_DKB}▀▀████████▀▀{C_RST}"),
    fit_exact_29(f"            {C_DKB}▀▀▀▀{C_RST}")
]

# -----------------------------------------------------------------------------
# 5. DRIED MEAT (Đùi thịt cầm tay rút xương)
# -----------------------------------------------------------------------------
C_BONE = "\033[38;2;245;245;235m"
C_BSHD = "\033[38;2;190;190;180m"
C_MT1  = "\033[38;2;215;55;55m"
C_MT2  = "\033[38;2;160;35;35m"
C_FAT  = "\033[38;2;250;185;170m"

meat_sprite = [
    fit_exact_29(f"                       {C_BONE}▄▄██{C_RST}"),
    fit_exact_29(f"                      {C_BONE}██████{C_RST}"),
    fit_exact_29(f"                     {C_BSHD}██████{C_RST}"),
    fit_exact_29(f"               {C_MT1}▄▄▄▄{C_BSHD}████{C_RST}"),
    fit_exact_29(f"           {C_MT1}▄▄██████████▄{C_RST}"),
    fit_exact_29(f"     {C_MT1}▄▄████████{C_FAT}████{C_MT1}██████▄{C_RST}"),
    fit_exact_29(f"   {C_MT1}▄██{C_FAT}░░{C_MT1}██████{C_FAT}██████{C_MT1}██████{C_RST}"),
    fit_exact_29(f"  {C_MT2}████████████{C_FAT}████{C_MT2}████████{C_RST}"),
    fit_exact_29(f"  {C_MT2}██{C_FAT}░░{C_MT2}████████████████████{C_RST}"),
    fit_exact_29(f"  {C_MT2}▀████████████████████▀{C_RST}"),
    fit_exact_29(f"    {C_MT2}▀▀██████████████▀▀{C_RST}"),
    fit_exact_29(f"        {C_MT2}▀▀▀████▀▀▀{C_RST}")
]

# -----------------------------------------------------------------------------
# 6. ALCHEMICAL VIAL (Bình thuốc nút bần nhãn Hexen)
# -----------------------------------------------------------------------------
C_CRK = "\033[38;2;190;140;80m"
C_GLS = "\033[1;37m"
C_LBL = "\033[38;2;230;215;180m"
C_LBLS = "\033[1;30m"
C_ELX1 = "\033[38;2;60;185;245m"
C_ELX2 = "\033[38;2;25;120;195m"

bottle_sprite = [
    fit_exact_29(f"           {C_CRK}▄▄▄▄▄▄▄▄{C_RST}"),
    fit_exact_29(f"           {C_CRK}████████{C_RST}"),
    fit_exact_29(f"             {C_GLS}████{C_RST}"),
    fit_exact_29(f"           {C_GLS}▄▄████▄▄{C_RST}"),
    fit_exact_29(f"   {C_GLS}▄▄██████████████████▄▄{C_RST}"),
    fit_exact_29(f"  {C_GLS}█{C_LBL}░░░░░░░░░░{C_ELX1}████████████{C_GLS}█{C_RST}"),
    fit_exact_29(f"  {C_GLS}█{C_LBL}░░{C_LBLS}[HEX]{C_LBL}░░{C_ELX1}████████████{C_GLS}█{C_RST}"),
    fit_exact_29(f"  {C_GLS}█{C_LBL}░░{C_LBLS} RUNE{C_LBL}░░{C_ELX1}████████████{C_GLS}█{C_RST}"),
    fit_exact_29(f"  {C_GLS}█{C_LBL}░░░░░░░░░░{C_ELX2}████████████{C_GLS}█{C_RST}"),
    fit_exact_29(f"  {C_GLS}█{C_ELX2}██████████████████████{C_GLS}█{C_RST}"),
    fit_exact_29(f"  {C_GLS}▀██████████████████████▀{C_RST}"),
    fit_exact_29(f"     {C_GLS}▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀{C_RST}")
]

# -----------------------------------------------------------------------------
# 7. RUNIC KEY (Chìa khóa cổ ngữ Hexen)
# -----------------------------------------------------------------------------
C_K1 = "\033[38;2;190;200;225m"
C_K2 = "\033[38;2;135;145;165m"
C_K3 = "\033[38;2;90;100;120m"

key_sprite = [
    fit_exact_29(f"            {C_K1}▄▄████▄▄{C_RST}"),
    fit_exact_29(f"           {C_K1}████▀▀████{C_RST}"),
    fit_exact_29(f"           {C_K2}███    ███{C_RST}"),
    fit_exact_29(f"           {C_K2}████▄▄████{C_RST}"),
    fit_exact_29(f"            {C_K2}▀▀████▀▀{C_RST}"),
    fit_exact_29(f"              {C_K2}██{C_RST}"),
    fit_exact_29(f"              {C_K3}██{C_RST}"),
    fit_exact_29(f"              {C_K3}██ ▄▄█{C_RST}"),
    fit_exact_29(f"              {C_K3}██ ▀▀█{C_RST}"),
    fit_exact_29(f"              {C_K3}██ ▄▄█{C_RST}"),
    fit_exact_29(f"              {C_K3}██ ▀▀█{C_RST}"),
    fit_exact_29(f"              {C_K3}▀▀{C_RST}")
]

# =============================================================================
# ITEM CATALOG EXPORT
# =============================================================================
ITEM_CATALOG = [
    {
        "id": "totem",
        "name": "TOTEM OF UNDYING",
        "type": "CỔ THẦN (ARTIFACT)",
        "qty": 1,
        "max_qty": 1,
        "effect": "Tái sinh toàn bộ chi đứt",
        "cure": "Đứt chi, Gãy xương, Hoại tử",
        "target": "Solo Explorer",
        "usage": "Khẩn cấp (Map & Combat)",
        "rarity": "Độc Bản Cổ Xưa (Mythic)",
        "lore": [
            "Bảo vật thần bí tạc hình người tí hon với đôi mắt ngọc lục bảo rực sáng.",
            "Khi kích hoạt, thần vật vỡ vụn thành luồng bụi vàng ấm áp che chở sinh mạng,",
            "nối lại toàn bộ tứ chi bị đứt và đưa cơ thể về trạng thái nguyên bản!"
        ],
        "sprite": totem_sprite
    },
    {
        "id": "poppy",
        "name": "POPPY FLOWER",
        "type": "THẢO DƯỢC Y TẾ",
        "qty": 3,
        "max_qty": 10,
        "effect": "+50 HP (+65 với Cahara)",
        "cure": "Cầm Máu (Bleeding)",
        "target": "Vết Thương Hở",
        "usage": "Map & Trong Trận Đánh",
        "rarity": "Dược Liệu Hầm Ngục",
        "lore": [
            "Bông hoa anh túc đỏ thẫm sinh trưởng từ những vũng máu trong ngục tối.",
            "Cánh hoa nghiền nát tạo thành lớp cao dán đông máu tức thì,",
            "chặn đứng cơn xuất huyết hiểm nghèo đang đe dọa sinh mạng."
        ],
        "sprite": poppy_sprite
    },
    {
        "id": "weed",
        "name": "MARIJUANA HERB",
        "type": "DƯỢC LIỆU GIẢM ĐAU",
        "qty": 2,
        "max_qty": 10,
        "effect": "+120 HP (+75 Hardcore)",
        "cure": "Cơn Đau Dữ Dội, Sốc Sức",
        "target": "Hệ Thần Kinh",
        "usage": "Map & Trong Trận Đánh",
        "rarity": "Thảo Mộc Quý",
        "lore": [
            "Bó lá thảo dược khô với cấu trúc răng cưa và hương nồng đặc trưng.",
            "Khi đốt lên hít sâu, khói thuốc lập tức làm dịu hệ thần kinh,",
            "xua tan các cơn đau quằn quại và hồi phục thể lực dồi dào."
        ],
        "sprite": weed_sprite
    },
    {
        "id": "bread",
        "name": "MOLDY BREAD",
        "type": "LƯƠNG THỰC SINH TỒN",
        "qty": 4,
        "max_qty": 10,
        "effect": "Giảm 40 Cơn Đói Khát",
        "cure": "Đói Cồn Cào, Suy Dinh Dưỡng",
        "target": "Dạ Dày",
        "usage": "Khám Phá Bản Đồ (Map)",
        "rarity": "Lương Khô Phổ Thông",
        "lore": [
            "Ổ bánh mì Baguette nướng dài với các khía vát giòn tan tìm thấy trong hòm rương.",
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
