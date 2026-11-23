#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
================================================================================
CANONICAL SOLO EXPLORER SELECTOR (GIAO DIỆN NGUYÊN BẢN CHUẨN 100 CỘT)
Fear & Hunger: Terminal Labyrinth - Solo Explorer Architecture
================================================================================
Khôi phục nguyên bản 100% bố cục quy hoạch gốc:
  - Chiều ngang: Đúng 100 cột chuẩn (cols=100).
  - Chiều cao: 23 dòng (<= 35 dòng, chống trôi màn hình 100%).
  - Bên trái (34 cột): Khung danh sách 8 nhân vật điều hướng [W/S] + Phím tắt.
  - Bên phải (64 cột): Sân khấu hiển thị mô hình nhân vật 29 cột nguyên vẹn,
    bảng chỉ số đầy đủ (HP, ATK, DEF, Kháng, Trait, Buff, Skill) và Lời đánh giá sinh tồn.
================================================================================
"""

import sys
import os
import re

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import demo_interactive_ui as dui

def main():
    hero, idx = dui.run_solo_select_interactive()
    if hero is None:
        dui.clear_screen()
        print("\033[1;31m[THOÁT]: Bạn đã hủy chọn nhân vật.\033[0m")
        return

    dui.clear_screen()
    print("\033[1;30m+====================================================================================================+\033[0m")
    title = f" [XÁC NHẬN CHỌN EXPLORER]: {hero['name']} [{hero['role']}]"
    print(f"\033[1;30m| \033[1;32m{dui.fit_ansi(title, 96)}\033[1;30m |\033[0m")
    print("\033[1;30m+====================================================================================================+\033[0m")
    print(f"\n  Bạn đã chọn: \033[1;33m{hero['name']}\033[0m ({hero['role']})")
    print(f"  HP: {hero['hp']}/{hero['max_hp']}  |  ATK: {hero['atk']}  |  DEF: {hero['def']}  |  TRAIT: {hero['trait']}")
    print(f"  Đặc tính: {hero['item_buff_str']}")
    print(f"  Kỹ năng : [1] {hero['skills'][0]['label']}  |  [2] {hero['skills'][1]['label']}")
    print("\n\033[1;30m+----------------------------------------------------------------------------------------------------+\033[0m")
    print("  \033[1;37m[1]\033[0m Khởi động chơi game thám hiểm Labyrinth ngay với Hero này")
    print("  \033[1;37m[2]\033[0m Quay lại màn hình chọn nhân vật nguyên bản")
    print("  \033[1;37m[Q]\033[0m Thoát ra ngoài")
    print("\033[1;30m+====================================================================================================+\033[0m")

    if os.name == 'nt' and sys.stdin.isatty():
        choice = input("\nLựa chọn của bạn [1/2/Q]: ").strip().lower()
        if choice == '1':
            dui.clear_screen()
            os.system("python funger_terminal/master_game.py")
        elif choice == '2':
            main()
        else:
            print("[OK] Đã thoát bộ chọn nhân vật.")

if __name__ == "__main__":
    main()
