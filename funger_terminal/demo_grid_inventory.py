#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
================================================================================
MULTI-SLOT GRID INVENTORY (TÚI ĐỒ Ô LƯỚI CHIẾN THUẬT) WITH TOTEM OF RESTORATION
Fear & Hunger: Terminal Labyrinth - Solo Explorer Architecture
================================================================================
Key Innovations:
  1. Multi-Slot 3x2 Grid Layout:
     - 6 dedicated slot boxes with pixel icons, item tags, and quantity counters.
     - 2D Navigation (W/A/S/D / Arrow keys) with direct jump keys [1-6].
  2. The Unique Mythic Item: TOTEM OF FLESH RESTORATION (Totem Cổ Thần):
     - Rarity: 1 unique totem granted per expedition (cannot be looted elsewhere).
     - Effect: Shatters into golden amber ash to reattach all amputated limbs,
       mend bone fractures, and purge bleeding & gangrene back to 100% pristine form!
  3. Survival Trauma Cures:
     - Bleeding (Poppy Flower)
     - Agony & Terror (Marijuana / Vintage Ale)
     - Fractures (Wood Splint)
     - Starvation (Moldy Bread)
================================================================================
"""

import sys
import os
import re
import copy
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import demo_interactive_ui as dui

if os.name == 'nt':
    import msvcrt

ANSI_RE = re.compile(r'\x1b\[[0-9;]*m')

def vis_len(s):
    return len(ANSI_RE.sub('', s))

def fit_exact(s, width):
    cur = vis_len(s)
    if cur > width:
        clean = ""
        idx = 0
        w = 0
        while idx < len(s) and w < width:
            if s[idx] == '\x1b':
                m = ANSI_RE.match(s[idx:])
                if m:
                    clean += m.group(0)
                    idx += len(m.group(0))
                    continue
            clean += s[idx]
            w += 1
            idx += 1
        return clean + "\033[0m" + " " * (width - w)
    return s + " " * (width - cur)

INITIAL_INVENTORY = [
    {
        "id": "totem",
        "name": "TOTEM OF FLESH",
        "type": "CỔ THẦN BẢO VẬT (ARTIFACT)",
        "qty": 1,
        "max_qty": 1,
        "color": "\033[38;2;255;170;40m",
        "icon": [
            "      ▄▄▄▀(O)▀▄▄▄       ",
            "     ██ ▀█▀█▀ █▄        ",
            "     ▀▄▄ ▀█▀ ▄▄▀        ",
            "       ▀▀▀█▀▀▀          "
        ],
        "summary": "Tái sinh toàn bộ tứ chi bị đứt",
        "cure": "Gãy xương, Đứt chi, Xuất huyết, Hoại tử",
        "lore": "Bảo vật cổ xưa chứa tinh thể Hổ Phách của Sylvian. Khi kích hoạt, nó vỡ vụn thành bụi vàng tái tạo lại da thịt, gắn liền xương tủy và nối lại toàn bộ tứ chi đã mất!"
    },
    {
        "id": "poppy",
        "name": "POPPY FLOWER",
        "type": "DƯỢC LIỆU CẦM MÁU (HERB)",
        "qty": 2,
        "max_qty": 5,
        "color": "\033[38;2;230;40;40m",
        "icon": [
            "        ▄▄▄▄▄▄          ",
            "       ████████         ",
            "        ▀████▀          ",
            "          ││            "
        ],
        "summary": "Hồi +50 HP & Cầm máu xuất huyết",
        "cure": "Chảy máu (Bleeding), Vết chém hở",
        "lore": "Loài hoa đỏ thẫm sinh trưởng từ máu những kẻ tử nạn trong ngục tối. Nhựa hoa làm đông máu vết thương hở trong tích tắc và xoa dịu cơn đau thể xác."
    },
    {
        "id": "weed",
        "name": "MARIJUANA HERB",
        "type": "DƯỢC THẢO GIẢM ĐAU (HERB)",
        "qty": 1,
        "max_qty": 5,
        "color": "\033[38;2;40;200;60m",
        "icon": [
            "         ▄▀█▀▄          ",
            "       ▄▀ █ █ ▀▄        ",
            "      ▀▄▄█████▄▄▀       ",
            "          ││            "
        ],
        "summary": "Hồi +120 HP & Giảm đau cực mạnh",
        "cure": "Cơn đau thấu xương, Giảm tụt Mind",
        "lore": "Lá thảo dược xanh thẫm mang dược tính gây tê liệt hệ thần kinh. Đốt lên hít khói giúp hồi phục 120 HP và làm dịu cơn co thắt do chấn thương nặng."
    },
    {
        "id": "bread",
        "name": "MOLDY BREAD",
        "type": "LƯƠNG KHÔ KHẨN CẤP (FOOD)",
        "qty": 3,
        "max_qty": 5,
        "color": "\033[38;2;180;130;70m",
        "icon": [
            "       ▄▄▄▄▄▄▄▄▄        ",
            "      ███████████       ",
            "      ██▓▓██▓▓███       ",
            "       ▀▀▀▀▀▀▀▀▀        "
        ],
        "summary": "Giảm 40 Đói (Hunger Relief)",
        "cure": "Đói lả, Suy nhược cơ bắp",
        "lore": "Mẩu bánh mì thô cứng mọc đầy nấm mốc xanh. Dù mùi vị chua chát kinh tởm nhưng chứa đủ calo để giữ cho đôi chân người sống sót không ngã quỵ."
    },
    {
        "id": "ale",
        "name": "VINTAGE ALE",
        "type": "RƯỢU CỔ KHỬ TRÙNG (DRINK)",
        "qty": 1,
        "max_qty": 3,
        "color": "\033[38;2;220;170;50m",
        "icon": [
            "          ▄▄▄           ",
            "         │   │          ",
            "        █▀▀▀▀▀█         ",
            "        ▀▄▄▄▄▄▀         "
        ],
        "summary": "Hồi +35 Mind & Khử trùng vết thương",
        "cure": "Hoảng loạn (Panic), Nhiễm trùng (Gangrene)",
        "lore": "Bình rượu mạnh cổ xưa được ủ trong hầm mộ. Một hớp rượu cay nồng dập tắt nỗi sợ hãi điên loạn (Mind +35), dùng rửa vết thương hở để ngăn hoại tử."
    },
    {
        "id": "splint",
        "name": "WOOD SPLINT",
        "type": "Y TẾ DÃ CHIẾN (SURGERY)",
        "qty": 1,
        "max_qty": 2,
        "color": "\033[38;2;160;110;60m",
        "icon": [
            "        ││   ││         ",
            "        ├───┼──┤        ",
            "        ││   ││         ",
            "        ├───┼──┤        "
        ],
        "summary": "Cố định & Chữa lành xương rạn nứt",
        "cure": "Rạn nứt tay chân (Fractured Limb)",
        "lore": "Hai thanh gỗ sồi buộc chặt bằng dây gai thô. Dùng nẹp cố định cánh tay hoặc cẳng chân bị rạn nứt, khôi phục lại 100% sức mạnh tấn công và tốc độ né đòn."
    }
]

def render_grid_inventory_screen(items, cur_slot, status_msg=""):
    lines = []
    lines.append("\033[1;30m+" + "=" * 98 + "+\033[0m")
    title_str = "FEAR & HUNGER: SURVIVAL POUCH - MULTI-SLOT GRID INVENTORY"
    sub_title = "[TÚI ĐỒ Ô LƯỚI CHIẾN THUẬT]"
    hdr = f" \033[1;37m{title_str:<68}\033[1;33m{sub_title:>27} "
    lines.append(f"\033[1;30m|{fit_exact(hdr, 98)}\033[1;30m|\033[0m")

    # Divider: 3 columns: 32 + 32 + 32 = 96 + 4 borders = 100
    div_slots = "\033[1;30m+" + "-" * 32 + "+" + "-" * 32 + "+" + "-" * 32 + "+\033[0m"
    lines.append(div_slots)

    # ROW 1 OF SLOTS (Slots 0, 1, 2)
    row1_tags = []
    for c in range(3):
        item = items[c]
        is_cur = (c == cur_slot)
        tag = f"[{c+1}] {item['name']}"
        qty_str = f"x{item['qty']}"
        inner = f"{tag:<22}{qty_str:>6}"
        if is_cur:
            txt = f"\033[1;32m▶ {inner}\033[0m"
        else:
            txt = f"\033[90m  {inner}\033[0m"
        row1_tags.append(fit_exact(txt, 32))
    lines.append(f"\033[1;30m|{row1_tags[0]}|{row1_tags[1]}|{row1_tags[2]}|\033[0m")

    for r in range(4):
        cells = []
        for c in range(3):
            item = items[c]
            is_cur = (c == cur_slot)
            icon_line = item["icon"][r]
            colored_icon = f"   {item['color']}{icon_line}\033[0m  "
            cells.append(fit_exact(colored_icon, 32))
        lines.append(f"\033[1;30m|{cells[0]}|{cells[1]}|{cells[2]}|\033[0m")

    row1_effs = []
    for c in range(3):
        item = items[c]
        eff_str = f" \033[0;37m{item['summary'][:30]}\033[0m"
        row1_effs.append(fit_exact(eff_str, 32))
    lines.append(f"\033[1;30m|{row1_effs[0]}|{row1_effs[1]}|{row1_effs[2]}|\033[0m")
    lines.append(div_slots)

    # ROW 2 OF SLOTS (Slots 3, 4, 5)
    row2_tags = []
    for c in range(3):
        item = items[3 + c]
        is_cur = (3 + c == cur_slot)
        tag = f"[{4+c}] {item['name']}"
        qty_str = f"x{item['qty']}"
        inner = f"{tag:<22}{qty_str:>6}"
        if is_cur:
            txt = f"\033[1;32m▶ {inner}\033[0m"
        else:
            txt = f"\033[90m  {inner}\033[0m"
        row2_tags.append(fit_exact(txt, 32))
    lines.append(f"\033[1;30m|{row2_tags[0]}|{row2_tags[1]}|{row2_tags[2]}|\033[0m")

    for r in range(4):
        cells = []
        for c in range(3):
            item = items[3 + c]
            icon_line = item["icon"][r]
            colored_icon = f"   {item['color']}{icon_line}\033[0m  "
            cells.append(fit_exact(colored_icon, 32))
        lines.append(f"\033[1;30m|{cells[0]}|{cells[1]}|{cells[2]}|\033[0m")

    row2_effs = []
    for c in range(3):
        item = items[3 + c]
        eff_str = f" \033[0;37m{item['summary'][:30]}\033[0m"
        row2_effs.append(fit_exact(eff_str, 32))
    lines.append(f"\033[1;30m|{row2_effs[0]}|{row2_effs[1]}|{row2_effs[2]}|\033[0m")

    div_wide = "\033[1;30m+" + "=" * 98 + "+\033[0m"
    lines.append(div_wide)

    # INSPECTION PANE OF ACTIVE HIGHLIGHTED ITEM (5 rows)
    act = items[cur_slot]
    p1 = f" \033[1;33mVẬT PHẨM:\033[1;37m {act['name']} \033[1;30m[{act['type']}]\033[0m  |  \033[1;32mSỐ LƯỢNG: {act['qty']}/{act['max_qty']}\033[0m  |  \033[1;36mHIỆU QUẢ: {act['summary']}\033[0m"
    lines.append(f"\033[1;30m|{fit_exact(p1, 98)}\033[1;30m|\033[0m")

    p2 = f" \033[1;31mĐIỀU TRỊ CHẤN THƯƠNG:\033[0;37m {act['cure']}"
    lines.append(f"\033[1;30m|{fit_exact(p2, 98)}\033[1;30m|\033[0m")

    lines.append("\033[1;30m+" + "-" * 98 + "+\033[0m")
    p3 = f" \033[1;33mCỐT TRUYỆN:\033[0;37m {act['lore']}"
    lines.append(f"\033[1;30m|{fit_exact(p3, 98)}\033[1;30m|\033[0m")

    # Status / Feedback log if any
    if status_msg:
        lines.append("\033[1;30m+" + "-" * 98 + "+\033[0m")
        lines.append(f"\033[1;30m| \033[1;33m{fit_exact(status_msg, 96)}\033[1;30m |\033[0m")

    # Controls footer (2 rows)
    lines.append("\033[1;30m+" + "-" * 98 + "+\033[0m")
    ctrls = " \033[90m[ĐIỀU KHIỂN]:\033[0m \033[1;37m[W/A/S/D / Mũi tên]\033[0m Di chuyển ô  |  \033[1;33m[1-6]\033[0m Chọn nhanh  |  \033[1;32m[Enter]\033[0m Sử dụng  |  \033[1;31m[Q/Esc]\033[0m Đóng"
    lines.append(f"\033[1;30m|{fit_exact(ctrls, 98)}\033[1;30m|\033[0m")
    lines.append(div_wide)
    return lines

def run_grid_inventory_interactive():
    items = copy.deepcopy(INITIAL_INVENTORY)
    cur_slot = 0
    status_msg = "[THÔNG BÁO]: Túi đồ đã mở. Hãy chọn một vật phẩm để kiểm tra hoặc sử dụng."

    dui.clear_screen()

    while True:
        frame = render_grid_inventory_screen(items, cur_slot, status_msg)
        dui.atomic_blit(frame)

        if not (os.name == 'nt' and sys.stdin.isatty()):
            break

        ch = msvcrt.getch()
        while msvcrt.kbhit():
            msvcrt.getch()

        if ch in (b'\x00', b'\xe0'):
            ext = msvcrt.getch()
            r = cur_slot // 3
            c = cur_slot % 3
            if ext == b'H': r = (r - 1) % 2
            elif ext == b'P': r = (r + 1) % 2
            elif ext == b'K': c = (c - 1) % 3
            elif ext == b'M': c = (c + 1) % 3
            cur_slot = r * 3 + c
            status_msg = ""

        elif ch in (b'w', b'W'):
            r = cur_slot // 3
            c = cur_slot % 3
            r = (r - 1) % 2
            cur_slot = r * 3 + c
            status_msg = ""
        elif ch in (b's', b'S'):
            r = cur_slot // 3
            c = cur_slot % 3
            r = (r + 1) % 2
            cur_slot = r * 3 + c
            status_msg = ""
        elif ch in (b'a', b'A'):
            r = cur_slot // 3
            c = cur_slot % 3
            c = (c - 1) % 3
            cur_slot = r * 3 + c
            status_msg = ""
        elif ch in (b'd', b'D'):
            r = cur_slot // 3
            c = cur_slot % 3
            c = (c + 1) % 3
            cur_slot = r * 3 + c
            status_msg = ""
        elif ch in (b'1', b'2', b'3', b'4', b'5', b'6'):
            cur_slot = int(ch.decode('ascii')) - 1
            status_msg = ""
        elif ch in (b'\r', b'\n', b' '):
            it = items[cur_slot]
            if it["qty"] > 0:
                it["qty"] -= 1
                if it["id"] == "totem":
                    status_msg = "\033[1;33m[TOTEM KÍCH HOẠT]: Bụi vàng Hổ phách bao bọc thể xác! Toàn bộ tứ chi đã được nối liền vẹn nguyên!\033[0m"
                elif it["id"] == "poppy":
                    status_msg = "\033[1;32m[HOA ANH TÚC]: Hồi phục +50 HP. Máu đông lại, vết thương hở đã được cầm máu!\033[0m"
                elif it["id"] == "weed":
                    status_msg = "\033[1;32m[CỎ DƯỢC LIỆU]: Hít khói thuốc (+120 HP). Thể xác thư giãn, cơn đau thấu xương biến mất!\033[0m"
                elif it["id"] == "bread":
                    status_msg = "\033[1;33m[BÁNH MÌ]: Ăn bánh mì mốc (-40 Đói). Khôi phục sinh lực, chống kiệt sức đói lả!\033[0m"
                elif it["id"] == "ale":
                    status_msg = "\033[1;36m[RƯỢU CỔ]: Uống một hớp lớn (+35 Mind). Rửa vết thương hở, triệt tiêu nguy cơ hoại tử!\033[0m"
                elif it["id"] == "splint":
                    status_msg = "\033[1;32m[NẸP GỖ]: Cố định xương gãy. Khôi phục lại 100% lực đánh và phản xạ né đòn!\033[0m"
            else:
                status_msg = f"\033[1;31m[HẾT VẬT PHẨM]: Bạn không còn {it['name']} trong túi đồ!\033[0m"

        elif ch in (b'q', b'Q', b'\x1b'):
            break

def main():
    run_grid_inventory_interactive()
    dui.clear_screen()
    print("[OK] Đã đóng giao diện túi đồ ô lưới.")

if __name__ == "__main__":
    main()
