#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Robust Hardware Sprite Extractor for 36 Monsters x 3 States (Normal, Injured, Dead)
Using atomic cell tokenization to ensure 100% ANSI escape sequence integrity.
"""
import subprocess
import json
import re
import os

def extract():
    cwd = os.path.dirname(os.path.abspath(__file__))
    sim_out = os.path.join(cwd, "sim", "show_monster_states.out")
    if not os.path.exists(sim_out):
        print("Compiling tb_show_monster_states.v...")
        subprocess.check_call([
            "iverilog", "-I", "src", "-o", "sim/show_monster_states.out",
            "src/monster.v", "src/fantasy_creatures.v", "src/monster_rom.v",
            "src/monster_state_model.v", "tb/tb_show_monster_states.v"
        ], cwd=cwd)

    print("[*] Running Verilog Tri-State simulation...")
    raw_output = subprocess.check_output(["vvp", "sim/show_monster_states.out"], cwd=cwd).decode("utf-8", errors="ignore")
    blocks = raw_output.split(">>> FOE #")

    cell_re = re.compile(r'((?:\x1b\[[0-9;]*[a-zA-Z])+[▀▄]\x1b\[0m| )')
    monsters_db = {}

    for b in blocks[1:]:
        lines = b.split("\n")
        header = lines[0]
        m_id = int(header.split(":")[0])
        m_name = header.split(":")[1].split("(")[0].strip()

        start_idx = -1
        for idx, l in enumerate(lines):
            if "+---------------------------+" in l:
                start_idx = idx + 4
                break

        s0, s1, s2 = [], [], []
        for l in lines[start_idx:]:
            if "----------------------------------------------------------------------------------------------------" in l:
                break
            cells = cell_re.findall(l)
            if len(cells) != 88:
                continue

            # Cell mapping:
            # 0..1: 2 spaces
            # 2..25: 24 cells for State 0 (Normal)
            # 26..32: 7 spaces
            # 33..56: 24 cells for State 1 (Injured)
            # 57..63: 7 spaces
            # 64..87: 24 cells for State 2 (Dead)

            c_s0 = "".join(cells[2:26]).rstrip()
            c_s1 = "".join(cells[33:57]).rstrip()
            c_s2 = "".join(cells[64:88]).rstrip()

            s0.append(c_s0)
            s1.append(c_s1)
            s2.append(c_s2)

        # Sanity check: Ensure no leaked ANSI fragments like '38;2;' or ';255;' in visible text!
        for st_name, st_arr in [("normal", s0), ("injured", s1), ("dead", s2)]:
            for row_idx, r in enumerate(st_arr):
                visible = re.sub(r'\x1b\[[0-9;]*[a-zA-Z]', '', r)
                if re.search(r'[0-9]{1,3};[0-9]{1,3}', visible) or re.search(r';[0-9]{2,3}m', visible):
                    raise ValueError(f"CORRUPTED ANSI LEAK in Monster #{m_id} ({m_name}) {st_name} row {row_idx}: '{visible}'")

        monsters_db[m_id] = {
            "id": m_id,
            "name": m_name,
            "normal": s0,
            "injured": s1,
            "dead": s2
        }

    json_path = os.path.join(cwd, "all_monster_sprites.json")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(monsters_db, f, indent=2, ensure_ascii=False)

    print(f"[SUCCESS] Extracted all {len(monsters_db)} monsters with 100% verified clean sprites to {json_path}!")

if __name__ == "__main__":
    extract()
