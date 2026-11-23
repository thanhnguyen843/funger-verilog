#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
================================================================================
ITEM MODEL CATALOG (BỘ MÔ HÌNH PIXEL ART VẬT PHẨM TỦ ĐỒ)
Fear & Hunger: Terminal Labyrinth - Solo Explorer Architecture
================================================================================
Tất cả 7 mô hình được xây dựng chuẩn xác theo yêu cầu người dùng:
  1. TOTEM OF UNDYING : Thần tượng Minecraft mắt ngọc lục bảo, thân vàng (Đã duyệt).
  2. POPPY FLOWER     : Hoa anh túc đỏ thẫm 8 cánh, đài hoa chalice & nhụy vàng (Làm lại chuẩn).
  3. MARIJUANA HERB   : Lá thảo dược răng cưa 5 nhánh sắc sảo, màu xanh ngọc tươi sáng (Làm lại chuẩn).
  4. MOLDY BREAD      : Ổ Baguette nướng giòn thanh thoát 3 khía vát xiên vàng ươm (Đã duyệt).
  5. DRIED MEAT       : Đùi thịt cầm tay rút xương đỏ hồng, đầu xương trắng ngà (Đã duyệt).
  6. ALCHEMICAL VIAL  : Bình thuốc cổ nút bần nhãn chú ấn Hexen thanh tẩy (Làm lại chuẩn).
  7. RUNIC KEY        : Chìa khóa sắt cổ ngữ Hexen đúc ren ma thuật mở cổng Labyrinth (Đã duyệt).

Quy chuẩn hiển thị:
  - Mỗi mô hình đúng 12 dòng, chiều rộng đúng 29 ký tự (pad cân đối).
  - Phối màu ANSI TrueColor (24-bit RGB) rực rỡ, độ tương phản cao, không vỡ hạt.
================================================================================
"""

import re

ANSI_RE = re.compile(r'\x1b\[[0-9;]*m')

def vis_len(s):
    return len(ANSI_RE.sub('', s))

def pad_center(s, width=29):
    w = vis_len(s)
    if w < width:
        l = (width - w) // 2
        r = width - w - l
        return ' ' * l + s + ' ' * r
    return s

def fit_exact_29(s):
    w = vis_len(s)
    if w < 29:
        return s + ' ' * (29 - w)
    elif w > 29:
        lspaces = len(s) - len(s.lstrip(' '))
        cut = w - 29
        if lspaces >= cut:
            s = s[cut:]
            return s + ' ' * (29 - vis_len(s))
    return s

C_RST = "\033[0m"

# -----------------------------------------------------------------------------
# 1. TOTEM OF UNDYING (Minecraft) - ĐÃ DUYỆT
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
# 2. POPPY FLOWER (Hoa anh túc) - LÀM LẠI CHUẨN XÁC THEO ẢNH GỐC
# -----------------------------------------------------------------------------
C_RED  = "\033[38;2;235;45;60m"   # Đỏ cánh hoa anh túc tươi
C_DRD  = "\033[38;2;170;25;38m"   # Đỏ ruby viền cánh
C_GLD  = "\033[38;2;255;215;60m"  # Nhụy vàng kim rực rỡ
C_CORE = "\033[38;2;85;20;25m"    # Lõi nhụy thẫm
C_GRN  = "\033[38;2;45;185;85m"   # Lá đài xanh tươi
C_DGR  = "\033[38;2;20;120;50m"   # Thân cành xanh thẫm

poppy_sprite = [
    pad_center(f"{C_RED}▄▄████▄▄{C_RST}"),
    pad_center(f"{C_DRD}▄██{C_RED}████████{C_DRD}██▄{C_RST}"),
    pad_center(f"{C_RED}▄████{C_RST}  {C_GLD}██████{C_RST}  {C_RED}████▄{C_RST}"),
    pad_center(f"{C_RED}██████{C_RST}  {C_GLD}██{C_CORE}██{C_GLD}██{C_RST}  {C_RED}██████{C_RST}"),
    pad_center(f"{C_RED}▀████{C_RST}  {C_GLD}██████{C_RST}  {C_RED}████▀{C_RST}"),
    pad_center(f"{C_DRD}▀██{C_RED}████████{C_DRD}██▀{C_RST}"),
    pad_center(f"{C_RED}▀▀████▀▀{C_RST}"),
    pad_center(f"{C_DGR}██{C_RST}"),
    pad_center(f"{C_GRN}▄█{C_RST}          {C_DGR}██{C_RST}          {C_GRN}█▄{C_RST}"),
    pad_center(f"{C_GRN}▄████▄{C_RST}      {C_DGR}██{C_RST}      {C_GRN}▄████▄{C_RST}"),
    pad_center(f"{C_DGR}▀██████▄▄{C_RST}  {C_DGR}██{C_RST}  {C_DGR}▄▄██████▀{C_RST}"),
    pad_center(f"{C_DGR}▀▀██████████████▀▀{C_RST}")
]

# -----------------------------------------------------------------------------
# 3. MARIJUANA HERB (Thảo dược an thần) - LÀM LẠI: 5 CÁNH RĂNG CƯA SẮC NÉT
# -----------------------------------------------------------------------------
C_L1 = "\033[38;2;85;240;115m"   # Xanh ngọc lục bảo tươi sáng rực rỡ
C_L2 = "\033[38;2;45;195;80m"    # Xanh thảo dược tươi tự nhiên
C_L3 = "\033[38;2;25;140;55m"    # Xanh lục đậm thân lá
C_L4 = "\033[38;2;12;85;30m"     # Gân & cuống lá sẫm

weed_sprite = [
    pad_center(f"{C_L1}▄█▄{C_RST}"),
    pad_center(f"{C_L1}███{C_RST}"),
    pad_center(f"{C_L1}▄█▄{C_RST}      {C_L2}███{C_RST}      {C_L1}▄█▄{C_RST}"),
    pad_center(f"{C_L1}████▄{C_RST}    {C_L2}███{C_RST}    {C_L1}▄████{C_RST}"),
    pad_center(f"{C_L2}▀████▄  {C_L2}█████{C_RST}  {C_L2}▄████▀{C_RST}"),
    pad_center(f"{C_L1}▄▄{C_L2}████▄{C_RST}  {C_L3}█████{C_RST}  {C_L2}▄████{C_L1}▄▄{C_RST}"),
    pad_center(f"{C_L2}▀▀█████▄{C_L3}███████{C_L2}▄█████▀▀{C_RST}"),
    pad_center(f"{C_L1}▄▄{C_L2}█████{C_RST}  {C_L3}███████{C_RST}  {C_L2}█████{C_L1}▄▄{C_RST}"),
    pad_center(f" {C_L2}▀▀████▄{C_L4}█████████{C_L2}▄████▀▀{C_RST} "),
    pad_center(f"{C_L3}▀███████▀{C_RST}"),
    pad_center(f"{C_L4}███{C_RST}"),
    pad_center(f"{C_L4}██{C_RST}")
]

# -----------------------------------------------------------------------------
# 4. MOLDY BREAD (Ổ Baguette nướng giòn) - ĐÃ DUYỆT
# -----------------------------------------------------------------------------
C_BR1 = "\033[38;2;235;165;60m"   # Vỏ bánh nướng vàng ruộm
C_BR2 = "\033[38;2;185;110;35m"   # Vỏ nâu caramen
C_CUT = "\033[38;2;255;245;190m"  # Ruột khía vát vàng sáng
C_DKB = "\033[38;2;110;55;15m"    # Rãnh nướng giòn đậm nét

bread_sprite = [
    fit_exact_29(f"                   {C_BR1}▄▄████▄▄{C_RST}"),
    fit_exact_29(f"                {C_BR1}▄████████████▄{C_RST}"),
    fit_exact_29(f"             {C_BR1}▄▄████{C_DKB}█{C_CUT}████{C_DKB}█{C_BR1}████▄{C_RST}"),
    fit_exact_29(f"           {C_BR1}▄██████{C_DKB}█{C_CUT}████{C_DKB}█{C_BR1}██████▀{C_RST}"),
    fit_exact_29(f"        {C_BR1}▄▄██{C_DKB}█{C_CUT}████{C_DKB}█{C_BR1}████████████▀{C_RST}"),
    fit_exact_29(f"      {C_BR1}▄████{C_DKB}█{C_CUT}████{C_DKB}█{C_BR1}████████████▀{C_RST}"),
    fit_exact_29(f"    {C_BR2}▄▄██████████{C_DKB}█{C_CUT}████{C_DKB}█{C_BR2}████▀{C_RST}"),
    fit_exact_29(f"   {C_BR2}▄██████████{C_DKB}█{C_CUT}████{C_DKB}█{C_BR2}████▀{C_RST}"),
    fit_exact_29(f"   {C_BR2}▀██████████████████▀{C_RST}"),
    fit_exact_29(f"     {C_DKB}▀██████████████▀{C_RST}"),
    fit_exact_29(f"        {C_DKB}▀▀██████▀▀{C_RST}"),
    fit_exact_29(f"            {C_DKB}▀▀{C_RST}")
]

# -----------------------------------------------------------------------------
# 5. DRIED MEAT (Đùi thịt cầm tay rút xương) - ĐÃ DUYỆT
# -----------------------------------------------------------------------------
C_BONE = "\033[38;2;245;245;235m" # Đầu xương trắng ngà
C_BSHD = "\033[38;2;190;190;180m" # Khớp xương bóng đổ
C_MT1  = "\033[38;2;215;55;55m"   # Thịt nướng xông khói đỏ hồng
C_MT2  = "\033[38;2;160;35;35m"   # Phần thịt nướng đậm
C_FAT  = "\033[38;2;250;185;170m" # Thớ thịt nạc sáng

meat_sprite = [
    fit_exact_29(f"                       {C_BONE}▄▄██{C_RST}"),
    fit_exact_29(f"                      {C_BONE}██████{C_RST}"),
    fit_exact_29(f"                     {C_BSHD}██████{C_RST}"),
    fit_exact_29(f"               {C_MT1}▄▄▄▄{C_BSHD}████{C_RST}"),
    fit_exact_29(f"           {C_MT1}▄▄██████████▄{C_RST}"),
    fit_exact_29(f"     {C_MT1}▄▄████████{C_FAT}████{C_MT1}██████▄{C_RST}"),
    fit_exact_29(f"   {C_MT1}▄██{C_FAT}██{C_MT1}██████{C_FAT}██████{C_MT1}██████{C_RST}"),
    fit_exact_29(f"  {C_MT2}████████████{C_FAT}████{C_MT2}████████{C_RST}"),
    fit_exact_29(f"  {C_MT2}██{C_FAT}██{C_MT2}████████████████████{C_RST}"),
    fit_exact_29(f"  {C_MT2}▀████████████████████▀{C_RST}"),
    fit_exact_29(f"    {C_MT2}▀▀██████████████▀▀{C_RST}"),
    fit_exact_29(f"        {C_MT2}▀▀▀████▀▀▀{C_RST}")
]

# -----------------------------------------------------------------------------
# 6. ALCHEMICAL VIAL (Bình thuốc cổ nút bần) - LÀM LẠI CHUẨN XÁC THEO ẢNH GỐC
# -----------------------------------------------------------------------------
C_CRK  = "\033[38;2;195;130;50m"  # Nút bần gỗ nâu vàng
C_GLS  = "\033[38;2;115;200;240m" # Cổ & miệng chai thủy tinh sáng
C_GLSD = "\033[38;2;55;140;195m"  # Viền thủy tinh xanh pha lê
C_LBL  = "\033[38;2;255;250;235m" # Giấy nhãn da cừu cổ
C_GLY  = "\033[38;2;75;35;95m"    # Chú ấn ma thuật cổ ngữ Hexen
C_POT  = "\033[38;2;225;40;135m"  # Tiên dược ma thuật hồng ngọc sáng
C_POTD = "\033[38;2;165;20;95m"   # Đáy dung dịch huyền bí

bottle_sprite = [
    pad_center(f"{C_CRK}▄▄████▄▄{C_RST}"),
    pad_center(f"{C_CRK}████████{C_RST}"),
    pad_center(f"{C_GLS}████████████{C_RST}"),
    pad_center(f"{C_GLS}████{C_RST}"),
    pad_center(f"{C_GLSD}▄▄██████{C_GLS}████{C_GLSD}██████▄▄{C_RST}"),
    pad_center(f"{C_GLSD}█{C_GLS}█{C_POT}██████████████████{C_GLSD}█{C_GLS}█{C_RST}"),
    pad_center(f"{C_GLSD}█{C_POT}███{C_LBL}████████{C_POT}█████████{C_GLSD}█{C_RST}"),
    pad_center(f"{C_GLSD}█{C_POT}███{C_LBL}██{C_GLY}████{C_LBL}██{C_POT}█████████{C_GLSD}█{C_RST}"),
    pad_center(f"{C_GLSD}█{C_POT}███{C_LBL}████████{C_POT}█████████{C_GLSD}█{C_RST}"),
    pad_center(f"{C_GLSD}█{C_POTD}████████████████████{C_GLSD}█{C_RST}"),
    pad_center(f"{C_GLSD}▀████████████████████▀{C_RST}"),
    pad_center(f"{C_GLSD}▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀{C_RST}")
]

# -----------------------------------------------------------------------------
# 7. RUNIC KEY (Chìa khóa cổ ngữ) - ĐÃ DUYỆT
# -----------------------------------------------------------------------------
C_KEY1 = "\033[38;2;245;195;50m"
C_KEY2 = "\033[38;2;195;135;25m"
C_KEY3 = "\033[38;2;140;90;15m"

key_sprite = [
    fit_exact_29(f"            {C_KEY1}▄▄████▄▄{C_RST}"),
    fit_exact_29(f"           {C_KEY1}████{C_KEY2}▀▀{C_KEY1}████{C_RST}"),
    fit_exact_29(f"           {C_KEY1}███{C_RST}    {C_KEY1}███{C_RST}"),
    fit_exact_29(f"           {C_KEY1}████{C_KEY2}▄▄{C_KEY1}████{C_RST}"),
    fit_exact_29(f"            {C_KEY2}▀▀████▀▀{C_RST}"),
    fit_exact_29(f"              {C_KEY2}██{C_RST}"),
    fit_exact_29(f"              {C_KEY2}██{C_RST}"),
    fit_exact_29(f"              {C_KEY2}██{C_RST} {C_KEY1}▄▄█{C_RST}"),
    fit_exact_29(f"              {C_KEY2}██{C_RST} {C_KEY2}▀▀█{C_RST}"),
    fit_exact_29(f"              {C_KEY2}██{C_RST} {C_KEY1}▄▄█{C_RST}"),
    fit_exact_29(f"              {C_KEY2}██{C_RST} {C_KEY2}▀▀█{C_RST}"),
    fit_exact_29(f"              {C_KEY3}▀▀{C_RST}")
]

# -----------------------------------------------------------------------------
# 8. BẢNG MỤC LỤC TỦ ĐỒ HOÀN CHỈNH (CANONICAL ITEM CATALOG)
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
