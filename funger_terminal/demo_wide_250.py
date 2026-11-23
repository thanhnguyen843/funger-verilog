#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
================================================================================
PANOPTIC 250-COLUMN TERMINAL ENGINE (BẢN SIÊU RỘNG 250 CỘT KHÔNG GIỚI HẠN)
Fear & Hunger: Terminal Labyrinth - Solo Explorer Architecture
================================================================================
Key Innovations of the 250-Column Architecture:
  1. Panoptic 8-Hero Grand Roster:
     - ALL 8 HEROES (Cahara, D'Arce, Enki, Ragnvaldr, Le'Garde, Moonless, The Girl, Nas'hrah)
       are displayed SIMULTANEOUSLY on a SINGLE ROW at 100% native 29-col uncropped resolution!
     - Zero pagination, zero page switching needed!
  2. 4 Colossus Columns (60 Cols/Hero):
     - 4 massive cards with full sprite + complete 30-column lore & combat dossier.
  3. 3-Pane Ultra Battlefield (Combat Arena):
     - Left Pane (78 cols): Explorer Hero & 4 Limb Integrity
     - Center Pane (88 cols): Foe Horror, Anatomical Targeting & Monster Sprite
     - Right Pane (78 cols): Tactical Commands, Hexen Spellbook & Live Combat Log
  4. 8-Slot Tactical Inventory & Anatomical Paperdoll (250 Cols)
================================================================================
"""

import sys
import os
import re
import copy
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import demo_interactive_ui as dui
from hero_tri_state_catalog import HERO_TRI_STATES

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

HEROES = dui.ALL_HEROES
TOTAL_W = 250

# =============================================================================
# 1. 8-HERO PANOPTIC GRAND ROSTER (TẤT CẢ 8 NHÂN VẬT TRÊN CÙNG 1 HÀNG)
# =============================================================================
def render_wide_hero_select_8panoptic(sel_idx):
    """
    250 columns / 8 cards:
    Border: 9 chars (+ or |). Remaining: 241 cols.
    Card widths: [30, 30, 30, 30, 30, 30, 30, 31]. Total = 241 + 9 = 250!
    All 8 heroes visible side-by-side without any page flips!
    """
    c_widths = [30, 30, 30, 30, 30, 30, 30, 31]
    active_h = HEROES[sel_idx]

    lines = []
    lines.append("\033[1;30m+" + "=" * 248 + "+\033[0m")
    title = "FEAR & HUNGER: PANOPTIC GRAND ROSTER (250-COL ULTRA WIDE) - [TẤT CẢ 8 NHÂN VẬT ĐỒNG THỜI TRÊN 1 HÀNG NGANG]"
    hint = "[TAB: ĐỔI MÀN HÌNH  |  M: ĐỔI BỐ CỤC 250  |  1-8: CHỌN TRỰC TIẾP]"
    hdr = f" \033[1;37m{title:<180}\033[1;33m{hint:>65} "
    lines.append(f"\033[1;30m|{fit_exact(hdr, 248)}\033[1;30m|\033[0m")

    div_8 = "\033[1;30m+" + "+".join(["-" * w for w in c_widths]) + "+\033[0m"
    lines.append(div_8)

    # 8 Badges
    b_cells = []
    for i, w in enumerate(c_widths):
        h = HEROES[i]
        is_cur = (i == sel_idx)
        tag = f"[{h['id']}] {h['name'].upper()} ({h['role'].split()[0]})"
        txt = f"\033[1;32m▶ {tag}\033[0m" if is_cur else f"\033[90m  {tag}\033[0m"
        b_cells.append(fit_exact(txt, w))
    lines.append(f"\033[1;30m|{'|'.join(b_cells)}|\033[0m")
    lines.append(div_8)

    # 12 Sprite Rows (29 cols wide each)
    for r in range(12):
        row_cells = []
        for i, w in enumerate(c_widths):
            h = HEROES[i]
            spr = HERO_TRI_STATES[h["name"]]["normal"]
            sp_line = spr[r] if r < len(spr) else " " * 29
            # 30 cols: sprite (29) + 1 space
            # 31 cols: 1 space + sprite (29) + 1 space
            pad_left = 1 if w == 31 else 0
            pad_right = w - pad_left - 29
            cell_str = " " * pad_left + sp_line + " " * pad_right
            row_cells.append(fit_exact(cell_str, w))
        lines.append(f"\033[1;30m|{'|'.join(row_cells)}|\033[0m")

    lines.append(div_8)

    # Stats Row 1: HP & ATK
    s1_cells = []
    for i, w in enumerate(c_widths):
        h = HEROES[i]
        txt = f" \033[1;32mHP:{h['hp']:3d}\033[0m | \033[1;31mATK:{h['atk']:2d} DMG\033[0m"
        s1_cells.append(fit_exact(txt, w))
    lines.append(f"\033[1;30m|{'|'.join(s1_cells)}|\033[0m")

    # Stats Row 2: DEF & DODGE
    s2_cells = []
    for i, w in enumerate(c_widths):
        h = HEROES[i]
        txt = f" \033[1;36mDEF:{h['def']:2d}\033[0m  | \033[1;35mNÉ:{int(h['dodge_rate']*100):2d}%\033[0m"
        s2_cells.append(fit_exact(txt, w))
    lines.append(f"\033[1;30m|{'|'.join(s2_cells)}|\033[0m")

    # Stats Row 3: TRAIT
    s3_cells = []
    for i, w in enumerate(c_widths):
        h = HEROES[i]
        txt = f" \033[1;33m{h['trait'][:w-2]}\033[0m"
        s3_cells.append(fit_exact(txt, w))
    lines.append(f"\033[1;30m|{'|'.join(s3_cells)}|\033[0m")

    # Stats Row 4: SKILL
    s4_cells = []
    for i, w in enumerate(c_widths):
        h = HEROES[i]
        txt = f" \033[1;36m{h['skills'][0]['label'][:w-2]}\033[0m"
        s4_cells.append(fit_exact(txt, w))
    lines.append(f"\033[1;30m|{'|'.join(s4_cells)}|\033[0m")

    lines.append("\033[1;30m+" + "=" * 248 + "+\033[0m")

    # ACTIVE EXPLORER GRAND DOSSIER (248 COLUMNS OF GLORIOUS LORE & DATA!)
    ah = active_h
    d1 = f" \033[1;33mĐANG KHẢO SÁT:\033[1;37m #{ah['id']} {ah['name']} [{ah['role']}]\033[0m  |  \033[1;32mSINH MỆNH: {ah['hp']}/{ah['max_hp']}\033[0m  |  \033[1;31mSỨC TẤN CÔNG: {ah['atk']} DMG\033[0m  |  \033[1;36mGIÁP TRỤ: {ah['def']}\033[0m  |  \033[1;35mNÉ TRÁNH: {int(ah['dodge_rate']*100)}%\033[0m  |  \033[1;33mKHÁNG VẬT LÝ: {ah['phys_resist_str']}\033[0m  |  \033[1;36mKHÁNG MA THUẬT: {ah['magic_resist_str']}\033[0m"
    lines.append(f"\033[1;30m|{fit_exact(d1, 248)}\033[1;30m|\033[0m")

    d2 = f" \033[1;37mĐẶC TÍNH BẨM SINH:\033[0;37m {ah['trait']:<35} \033[1;32mCƯỜNG HÓA VẬT PHẨM: {ah['item_buff_str']:<35} \033[1;36mBỘ KỸ NĂNG: [1] {ah['skills'][0]['label']}  |  [2] {ah['skills'][1]['label']}\033[0m"
    lines.append(f"\033[1;30m|{fit_exact(d2, 248)}\033[1;30m|\033[0m")

    assess = " ".join(ah["assessment"][:3])
    d3 = f" \033[1;33mĐÁNH GIÁ CHIẾN THUẬT SINH TỒN SOLO:\033[0;37m {assess[:205]}"
    lines.append(f"\033[1;30m|{fit_exact(d3, 248)}\033[1;30m|\033[0m")

    lines.append("\033[1;30m+" + "-" * 248 + "+\033[0m")
    ctrls = " \033[90m[ĐIỀU KHIỂN]:\033[0m \033[1;37m[A/D / Mũi tên Trái/Phải]\033[0m Chọn Hero  |  \033[1;33m[1-8]\033[0m Chọn Trực Tiếp  |  \033[1;33m[M]\033[0m Đổi Bố Cục 250  |  \033[1;33m[TAB]\033[0m Đổi Màn Hình (Combat/Túi Đồ)  |  \033[1;32m[Enter]\033[0m Xác Nhận  |  \033[1;31m[Q]\033[0m Thoát"
    lines.append(f"\033[1;30m|{fit_exact(ctrls, 248)}\033[1;30m|\033[0m")
    lines.append("\033[1;30m+" + "=" * 248 + "+\033[0m")

    return lines

# =============================================================================
# 2. 4 COLOSSUS COLUMNS (4 CỘT KHỔ ĐẠI - 61 CỘT MỖI THẺ)
# =============================================================================
def render_wide_hero_select_4colossus(sel_idx):
    """
    250 columns / 4 cards:
    Border: 5 chars. Remaining: 245 cols.
    Card widths: [61, 61, 61, 62].
    Inside each 61-column card:
    Left: 29-column sprite.
    Right: 30 columns of rich dossier!
    """
    page = sel_idx // 4
    start = page * 4
    p_heroes = [HEROES[start + i] if start + i < len(HEROES) else None for i in range(4)]
    active_h = HEROES[sel_idx]
    c_widths = [61, 61, 61, 62]

    lines = []
    lines.append("\033[1;30m+" + "=" * 248 + "+\033[0m")
    title = f"FEAR & HUNGER: 4 COLOSSUS COLUMNS (250-COL ULTRA WIDE) - [CHẾ ĐỘ 2: 4 THẺ KHỔ ĐẠI 61 CỘT]  (TRANG {page+1}/2)"
    hint = "[TAB: ĐỔI MÀN HÌNH  |  M: ĐỔI BỐ CỤC 250  |  W/S: LẬT TRANG]"
    hdr = f" \033[1;37m{title:<180}\033[1;33m{hint:>65} "
    lines.append(f"\033[1;30m|{fit_exact(hdr, 248)}\033[1;30m|\033[0m")

    div_4 = "\033[1;30m+" + "+".join(["-" * w for w in c_widths]) + "+\033[0m"
    lines.append(div_4)

    # Badges
    b_cells = []
    for i, w in enumerate(c_widths):
        h = p_heroes[i]
        if h:
            real_idx = HEROES.index(h)
            is_cur = (real_idx == sel_idx)
            tag = f"[{h['id']}] {h['name']} ({h['role']})"
            txt = f"\033[1;32m ▶ {tag}\033[0m" if is_cur else f"\033[90m   {tag}\033[0m"
        else:
            txt = "   \033[90m-- TRỐNG --\033[0m"
        b_cells.append(fit_exact(txt, w))
    lines.append(f"\033[1;30m|{'|'.join(b_cells)}|\033[0m")
    lines.append(div_4)

    def get_colossus_dossier(h):
        if not h: return [""] * 12
        return [
            f"\033[1;32mSINH MỆNH : {h['hp']:3d}/{h['max_hp']:3d}\033[0m",
            f"\033[1;31mSỨC ĐÁNH  : {h['atk']:2d} DMG\033[0m",
            f"\033[1;36mGIÁP TRỤ  : {h['def']:2d}\033[0m",
            f"\033[1;35mNÉ TRÁNH  : {int(h['dodge_rate']*100)}%\033[0m",
            f"\033[1;37mKHÁNG V.LÝ: {h['phys_resist_str'][:16]}\033[0m",
            f"\033[1;33mĐẶC TÍNH  : {h['trait'][:16]}\033[0m",
            f"\033[1;32mCƯỜNG HÓA : {h['item_buff_str'][:16]}\033[0m",
            f"\033[1;36mKỸ NĂNG 1 : {h['skills'][0]['label'][:16]}\033[0m",
            f"\033[1;36mKỸ NĂNG 2 : {h['skills'][1]['label'][:16]}\033[0m",
            f"\033[90mĐÁNH GIÁ  : {h['assessment'][0][:16]}..\033[0m",
            "",
            ""
        ]

    # 12 Rows of Sprite on left + Stats on right
    for r in range(12):
        row_cells = []
        for i, w in enumerate(c_widths):
            h = p_heroes[i]
            if h:
                spr = HERO_TRI_STATES[h["name"]]["normal"]
                sp_line = spr[r] if r < len(spr) else " " * 29
                st_list = get_colossus_dossier(h)
                st_line = st_list[r] if r < len(st_list) else ""
                cell_str = f" {sp_line} {st_line}"
            else:
                cell_str = " " * w
            row_cells.append(fit_exact(cell_str, w))
        lines.append(f"\033[1;30m|{'|'.join(row_cells)}|\033[0m")

    lines.append("\033[1;30m+" + "=" * 248 + "+\033[0m")
    ah = active_h
    d1 = f" \033[1;33mCHỌN HIỆN TẠI:\033[1;37m {ah['name']} [{ah['role']}]\033[0m  |  \033[1;32mHP: {ah['hp']}/{ah['max_hp']}\033[0m  |  \033[1;31mATK: {ah['atk']} DMG\033[0m  |  \033[1;36mDEF: {ah['def']}\033[0m  |  \033[1;35mNÉ TRÁNH: {int(ah['dodge_rate']*100)}%\033[0m  |  \033[1;33mKHÁNG VẬT LÝ: {ah['phys_resist_str']}\033[0m"
    lines.append(f"\033[1;30m|{fit_exact(d1, 248)}\033[1;30m|\033[0m")

    assess = " ".join(ah["assessment"][:3])
    d2 = f" \033[1;33mCHI TIẾT SINH TỒN:\033[0;37m {assess[:220]}"
    lines.append(f"\033[1;30m|{fit_exact(d2, 248)}\033[1;30m|\033[0m")

    lines.append("\033[1;30m+" + "-" * 248 + "+\033[0m")
    ctrls = " \033[90m[ĐIỀU KHIỂN]:\033[0m \033[1;37m[A/D]\033[0m Chọn Hero  |  \033[1;37m[W/S]\033[0m Đổi Trang (1-4 / 5-8)  |  \033[1;33m[1-8]\033[0m Chọn Trực Tiếp  |  \033[1;33m[M]\033[0m Đổi Bố Cục  |  \033[1;32m[Enter]\033[0m Xác Nhận  |  \033[1;31m[Q]\033[0m Thoát"
    lines.append(f"\033[1;30m|{fit_exact(ctrls, 248)}\033[1;30m|\033[0m")
    lines.append("\033[1;30m+" + "=" * 248 + "+\033[0m")
    return lines

# =============================================================================
# 3. 3-PANE ULTRA BATTLEFIELD (ĐẤU TRƯỜNG COMBAT 3 PHÂN VÙNG 250 CỘT)
# =============================================================================
def render_wide_combat_3pane(sel_hero_idx=0, foe_id="13", action_idx=0):
    """
    250-Column 3-Pane Battlefield:
    Pane 1 (Left - 78 cols): Explorer Hero (Sprite + 4 Limb Integrity Status + Health Bars)
    Pane 2 (Center - 88 cols): Foe Horror (Anatomical Weaknesses + Monster Sprite + Intent Telegraph)
    Pane 3 (Right - 80 cols): Tactical Intel & Hexen Magic Library (Commands + Spellbook + Live Combat Log)
    """
    hero = HEROES[sel_hero_idx]
    foe_data = dui.ALL_MONSTER_SPRITES.get(foe_id, dui.ALL_MONSTER_SPRITES["13"])
    foe_name = foe_data["name"]
    foe_spr = foe_data["normal"]

    w1, w2, w3 = 78, 88, 80
    lines = []
    lines.append("\033[1;30m+" + "=" * 248 + "+\033[0m")
    title = f"FEAR & HUNGER: 3-PANE ULTRA COMBAT THEATER (250-COL ARENA)"
    hint = "[TAB: ĐỔI MÀN HÌNH  |  1-5: LỆNH CHIẾN ĐẤU  |  Q: RÚT CHẠY]"
    hdr = f" \033[1;31m⚔  \033[1;37m{title:<180}\033[1;33m{hint:>62} "
    lines.append(f"\033[1;30m|{fit_exact(hdr, 248)}\033[1;30m|\033[0m")

    div_3 = f"\033[1;30m+{'-'*w1}+{'-'*w2}+{'-'*w3}+\033[0m"
    lines.append(div_3)

    # Headers for 3 Panes
    p1_hdr = f" \033[1;32m[EXPLORER HERO]:\033[1;37m {hero['name']} [{hero['role']}]\033[0m"
    p2_hdr = f" \033[1;31m[ADVERSARY FOE]:\033[1;37m #{foe_id} {foe_name.upper()} [SUBTERRANEAN]\033[0m"
    p3_hdr = f" \033[1;35m[TACTICAL INTEL & HEXEN GRIMOIRE]\033[0m"
    lines.append(f"\033[1;30m|{fit_exact(p1_hdr, w1)}|{fit_exact(p2_hdr, w2)}|{fit_exact(p3_hdr, w3)}|\033[0m")
    lines.append(div_3)

    # 12 Combat Rows
    h_spr = HERO_TRI_STATES[hero["name"]]["normal"]

    p1_stats = [
        f"\033[1;32mHP   :\033[0m \033[1;32m[████████████████] {hero['hp']}/{hero['max_hp']}\033[0m",
        f"\033[1;36mMIND :\033[0m \033[1;36m[██████████░░░░░░] 70/100 (Minh Mẫn)\033[0m",
        f"\033[1;33mHUNGR:\033[0m \033[1;33m[████████████░░░░] 75/100 (No Nê)\033[0m",
        f"\033[1;35mTOXIC:\033[0m \033[0;37m[░░░░░░░░░░░░░░░░]  0% [AN TOÀN]\033[0m",
        "",
        f"\033[1;33m[TÌNH TRẠNG 4 TỨ CHI]:\033[0m",
        f" \033[1;32m● Tay Phải: Lành Lặn\033[0m (Cầm vũ khí 100% DMG)",
        f" \033[1;32m● Tay Trái: Lành Lặn\033[0m (Cầm khiên thủ -70% DMG)",
        f" \033[1;32m● Chân Trái: Lành Lặn\033[0m (Né tránh 25% Evasion)",
        f" \033[1;32m● Chân Phải: Lành Lặn\033[0m (Tốc độ rút lui 100%)",
        f"\033[1;33mĐẶC TÍNH: {hero['trait'][:32]}\033[0m",
        ""
    ]

    p2_stats = [
        f"\033[1;31mSINH MỆNH:\033[0m \033[1;31m[████████████████] 90/90 (100%)\033[0m",
        f"\033[1;33mÝ ĐỒ     :\033[1;37m Chuẩn bị vồ xé rách cơ bắp đứt chi!\033[0m",
        "",
        f"\033[1;33m[CÁC BỘ PHẬN CÓ THỂ NHẮM BẮN (TARGETING)]:\033[0m",
        f"  \033[1;31m[1] ĐẦU (HEAD)   :\033[0m 25 HP | 60% Hit | Chí Mạng",
        f"  \033[1;37m[2] THÂN (TORSO) :\033[0m 50 HP | 95% Hit | Cố Định",
        f"  \033[1;33m[3] VUỐT PHẢI    :\033[0m 20 HP | 80% Hit | Tước Vũ Khí",
        f"  \033[1;33m[4] VUỐT TRÁI    :\033[0m 20 HP | 80% Hit | Giảm 50% DMG",
        f"  \033[1;36m[5] CHÂN SAU     :\033[0m 25 HP | 85% Hit | Triệt Hạ Né",
        "",
        f"\033[1;35mTRẠNG THÁI: Tứ chi hung tợn, chưa gãy đổ!\033[0m",
        ""
    ]

    p3_stats = [
        f"\033[1;35m[BỘ MA THUẬT HEXEN CỔ XƯA]:\033[0m",
        f" \033[1;36m◆ Black Orb\033[0m (15 Mind): Cầu bóng tối xuyên giáp",
        f" \033[1;32m◆ Healing Whispers\033[0m (10 Mind): Hồi phục 80 HP",
        f" \033[1;31m◆ Blood Sacrifice\033[0m (-20 HP): Tăng 100% ATK 3 lượt",
        "",
        f"\033[1;33m[VẬT PHẨM KHẨN CẤP TRONG TÚI]:\033[0m",
        f" \033[38;2;255;170;40m★ TOTEM OF FLESH (x1):\033[0m Tái sinh toàn bộ chi đứt",
        f" \033[1;32m★ Poppy Flower (x3)  :\033[0m Cầm máu & +50 HP",
        f" \033[1;36m★ Vintage Ale (x2)   :\033[0m Giảm nỗi sợ & +35 Mind",
        "",
        f"\033[1;33m[TỈ LỆ RÚT CHẠY]:\033[1;32m 50% Cơ hội thành công\033[0m",
        ""
    ]

    for r in range(12):
        # Pane 1: Hero sprite (29) + stats (46) = 75 cols
        sp_l = h_spr[r] if r < len(h_spr) else " " * 29
        st_l = p1_stats[r] if r < len(p1_stats) else ""
        c1 = fit_exact(f" {sp_l}  {st_l}", w1)

        # Pane 2: Stats (50) + Monster sprite (25) = 75 cols
        sp_r = foe_spr[r] if r < len(foe_spr) else " " * 14
        st_mid = p2_stats[r] if r < len(p2_stats) else ""
        c2 = fit_exact(f" {st_mid:<50}  {sp_r}", w2)

        # Pane 3: Tactical info (78 cols)
        st_right = p3_stats[r] if r < len(p3_stats) else ""
        c3 = fit_exact(f" {st_right}", w3)

        lines.append(f"\033[1;30m|{c1}|{c2}|{c3}|\033[0m")

    lines.append("\033[1;30m+" + "=" * 248 + "+\033[0m")

    # Full 248-col Live Combat Log
    c_log = f" \033[1;33m[NHẬT KÝ CHIẾN TRƯỜNG]:\033[1;37m {hero['name']} rút vũ khí đối mặt {foe_name}! Bóng tối dày đặc rung chuyển trước tiếng gầm gừ đói khát của quái vật hầm ngục!\033[0m"
    lines.append(f"\033[1;30m|{fit_exact(c_log, 248)}\033[1;30m|\033[0m")

    lines.append("\033[1;30m+" + "-" * 248 + "+\033[0m")

    # 5 Tactical Action Buttons Across 248 Columns
    actions = [
        "[1] TẤN CÔNG ĐIỂM YẾU (CHI ĐỐI THỦ)",
        "[2] PHÒNG THỦ (-70% SÁT THƯƠNG)",
        "[3] MA THUẬT & KỸ NĂNG HEXEN",
        "[4] DÙNG VẬT PHẨM TÚI ĐỒ (TOTEM)",
        "[5] RÚT CHẠY VỀ HÀNH LANG (50%)"
    ]
    act_row = "       "
    for i, a in enumerate(actions):
        if i == action_idx:
            act_row += f"\033[1;42;30m ▶ {a} \033[0m      "
        else:
            act_row += f"\033[1;37m {a} \033[0m      "
    lines.append(f"\033[1;30m|{fit_exact(act_row, 248)}\033[1;30m|\033[0m")

    lines.append("\033[1;30m+" + "-" * 248 + "+\033[0m")
    ctrls = " \033[90m[ĐIỀU KHIỂN]:\033[0m \033[1;37m[A/D / 1-5]\033[0m Chọn Hành Động  |  \033[1;32m[Enter/Space]\033[0m Thực Thi  |  \033[1;33m[TAB]\033[0m Đổi Màn Hình (Hero Select / Túi Đồ)  |  \033[1;31m[Q]\033[0m Thoát"
    lines.append(f"\033[1;30m|{fit_exact(ctrls, 248)}\033[1;30m|\033[0m")
    lines.append("\033[1;30m+" + "=" * 248 + "+\033[0m")
    return lines

# =============================================================================
# MAIN INTERACTIVE LOOP
# =============================================================================
def run_wide_250_engine():
    screen_idx = 0  # 0: Hero Select, 1: Combat 3-Pane
    hero_mode = 0   # 0: 8-Hero Panoptic, 1: 4 Colossus
    sel_hero_idx = 0
    sel_combat_act = 0

    dui.clear_screen()
    print("\033[?25l", end="", flush=True)

    try:
        while True:
            if screen_idx == 0:
                if hero_mode == 0:
                    frame = render_wide_hero_select_8panoptic(sel_hero_idx)
                else:
                    frame = render_wide_hero_select_4colossus(sel_hero_idx)
            else:
                frame = render_wide_combat_3pane(sel_hero_idx, "13", sel_combat_act)

            dui.atomic_blit(frame)

            if not (os.name == 'nt' and sys.stdin.isatty()):
                break

            ch = msvcrt.getch()
            while msvcrt.kbhit():
                msvcrt.getch()

            if ch in (b'\x00', b'\xe0'):
                ext = msvcrt.getch()
                if screen_idx == 0:
                    if ext in (b'K',): sel_hero_idx = (sel_hero_idx - 1) % len(HEROES)
                    elif ext in (b'M',): sel_hero_idx = (sel_hero_idx + 1) % len(HEROES)
                    elif ext in (b'H',): sel_hero_idx = (sel_hero_idx - 4) % len(HEROES)
                    elif ext in (b'P',): sel_hero_idx = (sel_hero_idx + 4) % len(HEROES)
                else:
                    if ext in (b'K', b'H'): sel_combat_act = (sel_combat_act - 1) % 5
                    elif ext in (b'M', b'P'): sel_combat_act = (sel_combat_act + 1) % 5

            elif ch in (b'\t',):
                screen_idx = (screen_idx + 1) % 2

            elif ch in (b'm', b'M'):
                if screen_idx == 0:
                    hero_mode = (hero_mode + 1) % 2

            elif ch in (b'1', b'2', b'3', b'4', b'5', b'6', b'7', b'8'):
                val = int(ch.decode('ascii')) - 1
                if screen_idx == 0 and val < len(HEROES):
                    sel_hero_idx = val
                elif screen_idx == 1 and val < 5:
                    sel_combat_act = val

            elif ch in (b'a', b'A'):
                if screen_idx == 0: sel_hero_idx = (sel_hero_idx - 1) % len(HEROES)
                else: sel_combat_act = (sel_combat_act - 1) % 5
            elif ch in (b'd', b'D'):
                if screen_idx == 0: sel_hero_idx = (sel_hero_idx + 1) % len(HEROES)
                else: sel_combat_act = (sel_combat_act + 1) % 5
            elif ch in (b'w', b'W'):
                if screen_idx == 0: sel_hero_idx = (sel_hero_idx - 4) % len(HEROES)
            elif ch in (b's', b'S'):
                if screen_idx == 0: sel_hero_idx = (sel_hero_idx + 4) % len(HEROES)

            elif ch in (b'q', b'Q', b'\x1b'):
                break

    finally:
        print("\033[?25h", end="", flush=True)

def print_samples():
    print("\n" + "=" * 250)
    print(" SAMPLE 1: 8-HERO PANOPTIC GRAND ROSTER (250 COLS - TẤT CẢ 8 HERO TRÊN CÙNG 1 HÀNG)")
    print("=" * 250)
    f1 = render_wide_hero_select_8panoptic(0)
    for l in f1: print(l)

    print("\n" + "=" * 250)
    print(" SAMPLE 2: 4 COLOSSUS COLUMNS (250 COLS - 4 CỘT KHỔ ĐẠI 61 CỘT)")
    print("=" * 250)
    f2 = render_wide_hero_select_4colossus(0)
    for l in f2: print(l)

    print("\n" + "=" * 250)
    print(" SAMPLE 3: 3-PANE ULTRA BATTLEFIELD (250 COLS - ĐẤU TRƯỜNG 3 PHÂN VÙNG)")
    print("=" * 250)
    f3 = render_wide_combat_3pane(0, "13", 0)
    for l in f3: print(l)

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--print-samples":
        print_samples()
    else:
        run_wide_250_engine()
