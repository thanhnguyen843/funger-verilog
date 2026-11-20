# Fear & Hunger: Terminal Labyrinth (Verilog Hardware Edition)

> A tactical roguelike RPG simulation engine designed in Verilog RTL hardware and rendered in high-contrast ANSI 24-bit TrueColor in the Windows Terminal.

---

## 🎮 Quick Start (Chạy Game Ngay)

Simply double-click or run from PowerShell/CMD:
```bat
PLAY_GAME.bat
```
The script will automatically detect **Icarus Verilog**, compile the hardware RTL engine in less than a second, and launch the interactive simulation interface.

---

## ⚔️ Key Features & Mechanics

1. **Party & Squad Drafting:**
   - **8 Fear & Hunger Heroes:** Cahara (Mercenary), D'arce (Holy Knight), Enki (Dark Priest), Ragnvaldr (Berserker), Le'garde (Commander), Moonless (Cave Wolf), The Girl, and Nas'hrah (Severed Head).
   - Instant squad drafting presets: `[1] Balanced Vanguard`, `[2] Occult Sorcery`, `[3] Iron Mercenaries`, or `[4] Custom 4-Hero Squad`.
   - 24-bit TrueColor Half-Block Pixel Art portraits rendered for every hero with stats & roles.

2. **Exploration & Survival:**
   - **Tactical Fog of War:** Dynamic lighting radius around player explorer.
   - **Survival Gauges:** Hunger (+1 per 5 steps) and Mind (-1 per 8 steps).
   - **Labyrinth Gate:** Collect 3 Dungeon Keys from chests or elite monsters to unlock the Cyan Exit Gate `G`.
   - **Controls:** `[W/A/S/D]` Move | `[I]` Survival Pouch & Items | `[P]` Squad Roster & Models | `[Q]` Quit.

3. **Unified Tactical Combat & Limb Targeting System:**
   - **50/50 Diagonal Split Screen:** Foe on the top-right, active Explorer on the bottom-left.
   - **Targetable Body Parts:**
     - `[H]` Head (25% base hit - Decapitation Instant Kill, or 100% when crawling)
     - `[T]` Torso (95% hit - Core vital organ strikes)
     - `[R]` Right Arm (80% hit - Disarms foe, reduces attack by 60%)
     - `[L]` Left Arm (80% hit - Destroys foe guard and shields)
     - `[K]` Legs (85% hit - Forces foe to crawl, pin-point head attacks)
   - **Coin Flip of Fate:** High-stakes parry clashes on lethal enemy abilities.
   - **Class Skills & Items:** Hexen Spells (`[1]`, `[2]`), Pouch Herbs & Rations (`[P]`, `[M]`, `[B]`, `[A]`), and Frontline Tag Switch (`[S]`).

---

## 📁 Repository Structure

```
retro_game_verilog/
├── PLAY_GAME.bat               # Single click game launcher
├── GIT_WORKFLOW.md             # Team Git branching, PR & code review workflow
├── .gitignore                  # Git ignore rules for simulation binaries & dumps
├── README.md                   # Project documentation
├── .github/
│   └── workflows/
│       └── hardware_ci.yml     # Automated GitHub Actions 5-Gate Hardware CI Pipeline
└── funger_terminal/
    ├── run_comprehensive_verification.py # Master 5-Gate DO-254 / OpenTitan verification runner
    ├── audit_hardware_linter.py          # Stage 1: Synthesizability & strict compiler linting
    ├── audit_string_overflow.py          # Stage 2: String width & ANSI sequence audit
    ├── audit_damage_accounting.py        # Stage 3: Python golden reference co-simulation
    ├── audit_rng_pity.py                 # Stage 4: 100k-cycle LFSR chi-square & pity proof
    ├── benchmark_hw_vs_sw.py             # Hardware vs. Software (RISC-V) benchmarking tool
    ├── src/                              # 100% Synthesizable Verilog RTL Modules
    │   ├── battle_defs.vh                # Global system definitions & states
    │   ├── battle_top.v                  # Top-level hardware accelerator coordinator
    │   ├── damage_alu.v                  # Combinational 1-cycle combat damage ALU
    │   ├── rng_unit.v                    # 32-bit Galois LFSR pseudo-random generator
    │   ├── collision_unit.v              # Maze collision & boundary detection unit
    │   ├── inventory_ram.v               # Multi-port party HP & survival pouch RAM
    │   ├── map_rom.v                     # 36x20 Labyrinth layout ROM
    │   ├── character_rom.v               # 8 Heroes with dual-profile rebalanced stats
    │   ├── monster_rom.v                 # 36 Monsters & Elite weight database
    │   ├── terminal_ui.v                 # ANSI 24-bit TrueColor display generator
    │   └── *.v                           # Hero & Monster pixel sprite ROMs
    └── tb/                               # Comprehensive Verification Testbenches
        ├── tb_play.v                     # Top-level interactive simulation testbench
        ├── tb_game_check.v               # Full-feature regression check testbench
        ├── tb_battle_auto.v              # Automated combat & sprite regression testbench
        ├── tb_golden_trace.v             # Golden model co-simulation trace generator
        ├── tb_fsm_fuzzer.v               # 50,000-iteration random input FSM fuzzer
        └── tb_waveform_trace.v           # GTKWave VCD architecture waveform testbench
```

---

## 🔬 Hardware Verification & Benchmarking (Kiểm định & Đo kiểm)

To execute the complete industrial quality verification suite:
```bash
python funger_terminal/run_comprehensive_verification.py
```
To run the Hardware vs. Software architectural benchmark:
```bash
python funger_terminal/benchmark_hw_vs_sw.py
```

---

## 🛠️ Requirements

- **OS:** Windows 10 / 11 (PowerShell or Command Prompt with UTF-8 / Virtual Terminal support)
- **Compiler:** [Icarus Verilog](https://bleyer.org/icarus/) (`iverilog` & `vvp`)
- **Python:** Python 3.8+ (for keyboard input streaming)
