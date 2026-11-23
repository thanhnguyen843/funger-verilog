#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import subprocess
import json
import re
import os

def extract():
    cwd = os.path.dirname(os.path.abspath(__file__))
    sim_out = os.path.join(cwd, "sim", "test_states.out")
    if not os.path.exists(sim_out):
        print("Compiling tb_show_monster_states.v...")
        subprocess.check_call([
            "iverilog", "-I", "src", "-o", "sim/test_states.out",
            "src/monster.v", "src/fantasy_creatures.v", "src/monster_rom.v",
            "src/monster_state_model.v", "tb/tb_show_monster_states.v"
        ], cwd=cwd)

    raw_output = subprocess.check_output(["vvp", "sim/test_states.out"], cwd=cwd).decode("utf-8", errors="ignore")
    blocks = raw_output.split(">>> FOE #")

    ANSI_REGEX = re.compile(r'\x1b\[[0-9;]*[a-zA-Z]')
    def vlen(s):
        return len(ANSI_REGEX.sub('', s))

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
            # Split by 7 spaces delimiter:
            # Note: the testbench writes: "  ", 24 chars, "       ", 24 chars, "       ", 24 chars
            # But inside 24 chars, trailing spaces might exist.
            # To be 100% exact, let's extract characters by visible columns!
            # Each character is either an ANSI sequence ending with ▀/▄ followed by \033[0m, or a single space ' '.
            # Let's parse tokens!
            tokens = []
            curr_pos = 0
            while curr_pos < len(l):
                if l[curr_pos] == '\x1b':
                    # Parse ANSI sequence until m
                    m_end = l.find('m', curr_pos)
                    if m_end != -1:
                        # Character after m is the block char, then closing \033[0m
                        if m_end + 1 < len(l):
                            char_val = l[m_end + 1]
                            if l.startswith('\x1b[0m', m_end + 2):
                                token = l[curr_pos : m_end + 6]
                                tokens.append(token)
                                curr_pos = m_end + 6
                                continue
                            else:
                                token = l[curr_pos : m_end + 2]
                                tokens.append(token)
                                curr_pos = m_end + 2
                                continue
                tokens.append(l[curr_pos])
                curr_pos += 1

            # tokens now has individual visible cells!
            # Strip initial 2 spaces
            if len(tokens) >= 2 and tokens[0] == ' ' and tokens[1] == ' ':
                tokens = tokens[2:]

            # State 0 is 24 cells
            cell_s0 = "".join(tokens[0:24]).rstrip() if len(tokens) >= 24 else "".join(tokens).rstrip()
            # Delimiter is 7 spaces (24..31)
            # State 1 is 24 cells (31..55)
            cell_s1 = "".join(tokens[31:55]).rstrip() if len(tokens) >= 55 else ""
            # Delimiter is 7 spaces (55..62)
            # State 2 is 24 cells (62..86)
            cell_s2 = "".join(tokens[62:86]).rstrip() if len(tokens) >= 86 else ""

            s0.append(cell_s0)
            s1.append(cell_s1)
            s2.append(cell_s2)

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

    print(f"Successfully extracted {len(monsters_db)} monsters to {json_path}!")

if __name__ == "__main__":
    extract()
