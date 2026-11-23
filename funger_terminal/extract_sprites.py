import subprocess
import json
import re

out_c = subprocess.check_output(["vvp", "sim/show_characters.out"], cwd="d:/NeoProjects/Verilog-lab/retro_game_verilog/funger_terminal").decode("utf-8", errors="ignore")
blocks_c = out_c.split("----------------------------------------------------------------------------------------------------------------")

heroes = {
    "CAHARA": 0,
    "D'ARCE": 1,
    "ENKI": 2,
    "RAGNVALDR": 3,
    "LE'GARDE": 4,
    "MOONLESS": 5,
    "THE GIRL": 6,
    "NAS'HRAH": 7
}

extracted_heroes = {}
for h_name, b_idx in heroes.items():
    raw_lines = [l.split("|")[0].rstrip() for l in blocks_c[b_idx].split("\n") if "|" in l]
    # Filter and format 12 lines
    lines_12 = []
    for r in range(12):
        if r < len(raw_lines):
            lines_12.append(raw_lines[r])
        else:
            lines_12.append("")
    extracted_heroes[h_name] = lines_12

out_m = subprocess.check_output(["vvp", "sim/show_monsters.out"], cwd="d:/NeoProjects/Verilog-lab/retro_game_verilog/funger_terminal").decode("utf-8", errors="ignore")
blocks_m = out_m.split("--------------------------------------------------------------------------------------------------------")

# Monster 8 (Shadow Swordsman) is block 7
m8_raw = [l.split("|")[0].rstrip() for l in blocks_m[7].split("\n") if "|" in l]
m8_lines = []
for r in range(12):
    if r < len(m8_raw):
        m8_lines.append(m8_raw[r])
    else:
        m8_lines.append("")

# Also get a larger monster, e.g. Monster 7 (Beholder Eye) or Monster 4 (Brachio Titan) or Monster 20 (Abyssal Overlord)
m20_raw = [l.split("|")[0].rstrip() for l in blocks_m[19].split("\n") if "|" in l]
m20_lines = []
for r in range(12):
    if r < len(m20_raw):
        m20_lines.append(m20_raw[r])
    else:
        m20_lines.append("")

with open("d:/NeoProjects/Verilog-lab/retro_game_verilog/funger_terminal/extracted_sprites.json", "w", encoding="utf-8") as f:
    json.dump({
        "heroes": extracted_heroes,
        "monster_8": m8_lines,
        "monster_20": m20_lines
    }, f, ensure_ascii=False, indent=2)

print("Extracted sprites saved successfully!")
