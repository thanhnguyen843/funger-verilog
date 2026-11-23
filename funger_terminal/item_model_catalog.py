#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
================================================================================
ITEM MODEL CATALOG (BỘ MÔ HÌNH PIXEL ART VẬT PHẨM TỦ ĐỒ)
Fear & Hunger: Terminal Labyrinth - Solo Explorer Architecture
================================================================================
Các mô hình pixel art được chọn lọc chuẩn xác từ các bảng sprite người dùng cung cấp:
  - Totem: Nguyên mẫu Totem of Undying từ ảnh người dùng (mắt ngọc lục bảo, thân vàng, viền nâu).
  - Bánh mì: Ổ Baguette nướng giòn có khía xẻ vàng óng (Bảng 1).
  - Thịt: Đùi thịt cầm tay rút xương kinh điển (Bảng 1).
  - Rượu: Vại bia gỗ sồi sủi bọt trắng xóa có quai cầm (Bảng 2).
  - Hóa chất: Lọ cầu tròn nút bần phát sáng dung dịch giả kim (Bảng 2).
  - Chìa khóa: Chìa khóa sắt cổ ngữ Hexen đúc ren ma thuật (Bảng 3).
Mỗi mô hình chuẩn xác 12 dòng, chiều rộng 29 ký tự, phối màu ANSI TrueColor rực rỡ.
================================================================================
"""

# Bảng màu cho Totem of Undying
C_OUT = "\033[38;2;160;70;15m"    # Viền nâu đậm
C_ARM = "\033[38;2;182;90;23m"    # Cánh tay nâu
C_GLD = "\033[38;2;220;140;40m"   # Thân vàng gold
C_YEL = "\033[38;2;252;225;130m"  # Vàng sáng trán & sống mũi
C_EYE = "\033[38;2;0;235;140m"    # Mắt ngọc lục bảo Emerald
C_WHT = "\033[1;37m"              # Điểm sáng mắt
C_RST = "\033[0m"

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
            "Bảo vật tạc hình người tí hon với đôi mắt ngọc lục bảo rực sáng.",
            "Khi kích hoạt, thần vật vỡ vụn thành luồng bụi vàng ấm áp",
            "tái tạo lại da thịt, gắn liền xương tủy và nối lại toàn bộ",
            "tứ chi đã mất trở về trạng thái lành lặn nguyên bản!"
        ],
        "sprite": [
            f"        {C_OUT}▄▄▄▄▄▄▄▄▄▄▄▄{C_RST}         ",
            f"      {C_OUT}▄█{C_YEL}████████████{C_OUT}█▄{C_RST}       ",
            f"       {C_OUT}█{C_GLD}██{C_YEL}████████{C_GLD}██{C_OUT}█{C_RST}        ",
            f"       {C_OUT}█{C_GLD}██{C_WHT}█{C_EYE}█{C_YEL}████{C_WHT}█{C_EYE}█{C_GLD}██{C_OUT}█{C_RST}        ",
            f"       {C_OUT}█{C_GLD}██{C_EYE}██{C_YEL}████{C_EYE}██{C_GLD}██{C_OUT}█{C_RST}        ",
            f"       {C_OUT}█{C_GLD}████{C_YEL}████{C_GLD}████{C_OUT}█{C_RST}        ",
            f"   {C_OUT}▄▄▄▄▄{C_OUT}██{C_GLD}██{C_YEL}████{C_GLD}██{C_OUT}██{C_OUT}▄▄▄▄▄{C_RST}    ",
            f"  {C_OUT}█{C_ARM}██████{C_OUT}█{C_GLD}████████{C_OUT}█{C_ARM}██████{C_OUT}█{C_RST}   ",
            f"   {C_OUT}▀▀▀▀▀{C_OUT}██{C_YEL}████████{C_OUT}██{C_OUT}▀▀▀▀▀{C_RST}    ",
            f"       {C_OUT}█{C_GLD}████████████{C_OUT}█{C_RST}        ",
            f"       {C_OUT}█{C_ARM}████████████{C_OUT}█{C_RST}        ",
            f"        {C_OUT}▀▀▀▀▀▀▀▀▀▀▀▀{C_RST}         "
        ]
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
            "Ổ bánh mì lúa mạch nướng giòn tìm thấy trong các hòm gỗ bỏ hoang.",
            "Dù lớp vỏ ngoài đã ngả màu xám với vết mốc rải rác nhưng phần",
            "ruột bên trong vẫn cứu sống bạn khỏi cơn đói lả nguy kịch."
        ],
        "sprite": [
            "         \033[38;2;210;150;70m▄▄▄▄████████▄▄▄▄\033[0m    ",
            "       \033[38;2;210;150;70m▄██████████████████▄\033[0m  ",
            "      \033[38;2;190;130;60m████\033[38;2;250;220;140m██\033[38;2;190;130;60m████\033[38;2;250;220;140m██\033[38;2;190;130;60m████\033[38;2;250;220;140m██\033[38;2;190;130;60m████\033[0m ",
            "     \033[38;2;190;130;60m██████\033[38;2;250;220;140m██\033[38;2;190;130;60m████\033[38;2;250;220;140m██\033[38;2;190;130;60m████\033[38;2;250;220;140m██\033[38;2;190;130;60m████\033[0m ",
            "     \033[38;2;170;110;50m████████\033[38;2;250;220;140m██\033[38;2;170;110;50m████\033[38;2;250;220;140m██\033[38;2;170;110;50m████████\033[0m ",
            "     \033[38;2;170;110;50m██████████\033[38;2;250;220;140m██\033[38;2;170;110;50m████\033[38;2;250;220;140m██\033[38;2;170;110;50m██████\033[0m ",
            "      \033[38;2;150;90;40m██████████\033[38;2;250;220;140m██\033[38;2;150;90;40m██████████\033[0m  ",
            "      \033[38;2;150;90;40m▀██████████████████▀\033[0m  ",
            "       \033[38;2;130;80;35m▀████████████████▀\033[0m   ",
            "         \033[38;2;110;70;30m▀▀▀▀▀▀▀▀▀▀▀▀▀▀\033[0m     ",
            "                             ",
            "                             "
        ]
    },
    {
        "id": "meat",
        "name": "DRIED MEAT",
        "type": "LƯƠNG THỰC CAO CẤP",
        "qty": 2,
        "max_qty": 10,
        "effect": "-60 Đói Khát & +20 HP",
        "cure": "Đói Lả, Kiệt Quệ",
        "target": "Dạ Dày & Cơ Bắp",
        "usage": "Khám Phá Bản Đồ (Map)",
        "rarity": "Lương Khô Quý",
        "lore": [
            "Khúc đùi thịt động vật săn bắn được sấy khô bằng muối biển và khói.",
            "Lớp mỡ giòn dai cung cấp nguồn calo dồi dào, giúp hồi phục thể lực",
            "nhanh chóng sau những cuộc giao tranh ác liệt chống lại quái thú."
        ],
        "sprite": [
            "            \033[38;2;180;50;50m▄▄████▄\033[0m          ",
            "          \033[38;2;180;50;50m▄████████▄\033[0m         ",
            "        \033[38;2;160;40;40m▄████████████\033[0m        ",
            "       \033[38;2;160;40;40m████\033[38;2;240;180;160m████\033[38;2;160;40;40m██████\033[0m       ",
            "       \033[38;2;140;30;30m███\033[38;2;240;180;160m██████\033[38;2;140;30;30m█████\033[0m       ",
            "       \033[38;2;140;30;30m████\033[38;2;240;180;160m████\033[38;2;140;30;30m██████\033[0m       ",
            "        \033[38;2;120;25;25m▀███████████▀\033[0m        ",
            "          \033[38;2;120;25;25m▀███████▀\033[0m          ",
            "            \033[38;2;230;230;220m████\033[0m             ",
            "            \033[38;2;230;230;220m████\033[0m             ",
            "          \033[38;2;230;230;220m▄█▀  ▀█▄\033[0m           ",
            "          \033[38;2;230;230;220m▀▀    ▀▀\033[0m           "
        ]
    },
    {
        "id": "ale",
        "name": "VINTAGE ALE",
        "type": "RƯỢU THẦN KHÍ",
        "qty": 2,
        "max_qty": 10,
        "effect": "+35 Mind (Thần Trí)",
        "cure": "Kinh Hoàng, Hoảng Loạn",
        "target": "Tâm Trí & Tinh Thần",
        "usage": "Map & Trong Trận Đánh",
        "rarity": "Rượu Ủ Cổ Xưa",
        "lore": [
            "Chiếc vại bia gỗ sồi ủ men vàng óng với lớp bọt trắng sủi bông.",
            "Vị cồn nồng ấm làm tê liệt nỗi sợ hãi, ngăn chặn tâm trí rơi vào",
            "hố sâu điên loạn và ảo giác ma quái trong bóng tối vô tận."
        ],
        "sprite": [
            "          \033[1;37m▄▄▄▄▄▄▄▄▄\033[0m          ",
            "         \033[1;37m███████████\033[0m         ",
            "        \033[1;37m▀▀▀███████▀▀▀\033[0m        ",
            "        \033[38;2;220;170;50m███████████\033[38;2;160;100;40m▄▄\033[0m        ",
            "        \033[38;2;220;170;50m███████████\033[38;2;160;100;40m██\033[0m        ",
            "        \033[38;2;200;150;40m███████████\033[38;2;160;100;40m██\033[0m        ",
            "        \033[38;2;200;150;40m███████████\033[38;2;160;100;40m██\033[0m        ",
            "        \033[38;2;180;130;30m███████████\033[38;2;160;100;40m▀▀\033[0m        ",
            "        \033[38;2;180;130;30m███████████\033[0m          ",
            "        \033[38;2;150;100;20m▀█████████▀\033[0m          ",
            "         \033[38;2;120;80;20m▀▀▀▀▀▀▀▀▀\033[0m           ",
            "                             "
        ]
    },
    {
        "id": "vial",
        "name": "ALCHEMICAL VIAL",
        "type": "CỒN SÁT TRÙNG",
        "qty": 2,
        "max_qty": 5,
        "effect": "Xóa Bỏ Nhiễm Trùng & Độc Tố",
        "cure": "Hoại Tử, Nhiễm Trùng Máu",
        "target": "Vết Cắt & Khớp Xương",
        "usage": "Khám Phá & Combat",
        "rarity": "Dung Dịch Thuật Giả Kim",
        "lore": [
            "Bình thủy tinh tròn có nút bần chứa dung dịch thanh tẩy phát sáng.",
            "Rót trực tiếp vào vết thương để thiêu đốt sạch sẽ vi khuẩn",
            "hoại thư, ngăn ngừa vết cắt chuyển sang màu xanh độc địa."
        ],
        "sprite": [
            "            \033[38;2;180;140;80m▄▄▄▄\033[0m             ",
            "            \033[38;2;180;140;80m████\033[0m             ",
            "             \033[38;2;100;200;255m██\033[0m              ",
            "           \033[38;2;100;200;255m▄▄████▄▄\033[0m          ",
            "         \033[38;2;100;200;255m▄██████████▄\033[0m        ",
            "        \033[38;2;80;180;240m████\033[1;37m░░\033[38;2;80;180;240m████████\033[0m       ",
            "       \033[38;2;60;160;220m██████\033[1;37m░░\033[38;2;60;160;220m████████\033[0m      ",
            "       \033[38;2;40;140;200m████████████████\033[0m      ",
            "       \033[38;2;30;120;180m████████████████\033[0m      ",
            "        \033[38;2;20;100;160m▀████████████▀\033[0m       ",
            "          \033[38;2;15;80;140m▀▀██████▀▀\033[0m         ",
            "                             "
        ]
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
        "sprite": [
            "            \033[38;2;180;190;210m▄▄████▄▄\033[0m         ",
            "           \033[38;2;180;190;210m████▀▀████\033[0m        ",
            "           \033[38;2;150;160;180m███    ███\033[0m        ",
            "           \033[38;2;150;160;180m████▄▄████\033[0m        ",
            "            \033[38;2;130;140;160m▀▀████▀▀\033[0m         ",
            "              \033[38;2;130;140;160m██\033[0m             ",
            "              \033[38;2;110;120;140m██\033[0m             ",
            "              \033[38;2;110;120;140m██ ▄▄█\033[0m         ",
            "              \033[38;2;90;100;120m██ ▀▀█\033[0m         ",
            "              \033[38;2;90;100;120m██ ▄▄█\033[0m         ",
            "              \033[38;2;70;80;100m██ ▀▀█\033[0m         ",
            "              \033[38;2;70;80;100m▀▀\033[0m             "
        ]
    }
]
