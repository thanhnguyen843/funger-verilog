# Funger Terminal (Fear & Hunger Verilog HDL & Terminal Edition)

A complete **Turn-Based Tactical Roguelike Dungeon Crawler** co-designed at the Register-Transfer Level (RTL) in **Verilog HDL** and rendered in 24-bit TrueColor ANSI in the Windows Terminal.

---

## 1. System Architecture & Features

### 1.1 Dual Difficulty Modes (Fear & Hunger vs. Terror & Starvation)
Upon starting an expedition, players choose between two distinct difficulty levels:
1. **Mode 1: "Fear & Hunger" (Normal / Standard Expeditions)**:
   - **Empowered Explorer Combat Stats**: Player character **ATK and DEF are boosted by 1.5x** and **Max HP is boosted by +25%** (`base_hp + (base_hp >> 2)`).
   - **Generous Healing Potencies**: **Poppy Flower** restores **+50 HP**, and **Marijuana Herb** restores **+120 HP**.
2. **Mode 2: "Terror & Starvation" (Hardcore Mode)**:
   - **Baseline Explorer Combat Stats**: Player character stats revert to raw **1.0x baseline values**.
   - **Scarce Healing Potencies**: **Poppy Flower** restores only **+30 HP**, and **Marijuana Herb** restores only **+70 HP**.

### 1.2 Playable Explorers (Fear & Hunger Roster)
- **8 Distinct Characters** loaded with dedicated pixel-art ROMs:
  - Cahara (Mercenary / Swift Rogue)
  - D'arce (Holy Knight / Guardian)
  - Enki (Dark Priest / Occult Mage)
  - Ragnvaldr (Outlander / Berserker Tank)
  - Le'garde (The Commander / Tactician)
  - Moonless (Cavehound / Swift Beast)
  - The Girl (Innocent Ward / Evasive)
  - Nas'hrah (Doom Lord / Arch-Mage)
- **3 Dynamic Roster Selection Layouts (`[TAB]` toggled):**
  - **Quad Grid (2x2):** 4 spacious cards per page with 29-col full hero sprites and stat cards.
  - **Vertical Split:** Scrolling 30-col vertical roster on the left, 67-col main stage on the right.
  - **Panorama (3-Col):** 3 wide cards with 3-line stacked stat bars.

### 1.3 Dual Split-Box Showcase Satchel UI
- **Left Box (Hero Model Showcase - 46 cols):** Renders the active hero's full pixel sprite in real-time (`normal`, `injured` limb loss, or `dead`).
- **Right Box (Vitals & Limb Dossier - 47 cols):** Graphical gauge bars for HP, Mind, Hunger, and Toxicity, alongside physical limb integrity (`[HEAD]`, `[TORSO]`, `[ARMS]`, `[LEGS]`) and passive traits.
- **English Localization:** 100% concise English item and category descriptions (`[RELIC]`, `[HERB]`, `[RATION]`, `[TINCTURE]`, `[KEY]`) guaranteed $\le 45$ characters to prevent text truncation.

### 1.4 Monster Roster & Elite Mechanics
- **36 Total Monsters** across Retro Monsters (`monster.v`) and Fantasy Horrors (`fantasy_creatures.v`).
- **Elite System:** 8 predetermined Elite monsters have reduced spawn weights and **+20% bonus HP, ATK, and DEF**.
- **No-Repeat Guarantee:** Defeated monsters are tracked in bitmask registers and cannot appear again in subsequent `M` tiles.
- **Worst-Case 3-Key Guarantee (Pity System):** Clearing the maze monsters is mathematically proven to yield all 3 Dungeon Keys required to unlock the exit Gate `G`.

### 1.5 Chests & Mimics
- **Chest Tile `'C'`:** 20% chance to awaken a Mimic (ID 23); 80% safe loot probability for Dungeon Keys or healing items.
- Mimics are guaranteed to never be Elites.

---

## 2. Directory Structure

```text
funger_terminal/
├── master_game.py                    # Master game engine & interactive loop
├── demo_grid_inventory.py            # Dual Split-Box satchel showcase & English pouch
├── demo_grid_hero_select.py          # 3-layout interactive hero drafting screen
├── demo_interactive_ui.py            # Diagonal combat arena & limb target engine
├── hero_tri_state_catalog.py         # 8 Heroes with 3 morphologies (normal/injured/dead)
├── monsters_catalog.py               # 36 Monsters database with stats and movesets
├── item_model_catalog.py             # Item definitions, icons, and localized descriptions
├── run_comprehensive_verification.py # Master 5-Gate DO-254 / OpenTitan test runner
├── audit_100k_dual_mode_ultimate_suite.py # 100,000-expedition dual-mode fuzzer
├── audit_1m_adversarial_footsteps_suite.py# 1,000,000-step single-bit fault injection
├── benchmark_hw_vs_sw.py             # Hardware vs. Software (RISC-V) benchmarking tool
├── src/                              # 100% Synthesizable Verilog RTL Modules
│   ├── battle_defs.vh                # Global system definitions & states
│   ├── character_rom.v               # 8 Fear & Hunger character stats and database
│   ├── monster_rom.v                 # 36 Monster database with Elite weights and stats
│   ├── map_rom.v                     # 20x36 Labyrinth map ROM with rightmost Gates 'G' and guard 'M'
│   ├── collision_unit.v              # Collision detection unit for walls, chests, gates, and foes
│   ├── inventory_ram.v               # RAM managing party HP, items, and 3 Keys
│   ├── chest_sprite_rom.v            # 20x23 pixel-art chest model ROM
│   ├── key_sprite_rom.v              # 11x22 pixel-art key model ROM
│   ├── funger_*_rom.v                # 8 Fear & Hunger player character pixel-art ROMs
│   ├── monster.v                     # 20 Monster pixel-art sprite sheet ROM
│   ├── fantasy_creatures.v           # 16 Fantasy creature pixel-art sprite sheet ROM
│   ├── tactical_stance_unit.v        # Hardware Tactical Stance Coprocessor
│   ├── sanity_meter_unit.v           # Hardware Sanity & Hunger Environmental Entropy Coprocessor
│   ├── sprite_router.v               # Color sprite multiplexer for side-by-side battle rendering
│   ├── terminal_ui.v                 # ANSI terminal UI generator
│   ├── damage_alu.v                  # Combat damage calculation arithmetic unit
│   ├── rng_unit.v                    # 32-bit LFSR PRNG unit
│   └── battle_top.v                  # Top-level RTL hardware coordinator
└── tb/                               # Comprehensive Testbenches
    ├── tb_play.v                     # Interactive keyboard testbench
    ├── tb_game_check.v               # Comprehensive feature verification testbench
    ├── tb_battle_auto.v              # Automated regression testbench
    ├── tb_damage_alu.v               # ALU combat matrix unit testbench
    ├── tb_golden_trace.v             # Golden model co-simulation trace generator
    └── tb_waveform_trace.v           # GTKWave VCD architecture waveform testbench
```

---

## 3. How to Run and Play

### 3.1 Quick Start (Single Unified Launcher)
From the repository root:
```bat
PLAY_GAME.bat
```
Or directly within `funger_terminal/`:
```bash
python master_game.py
```

### 3.2 Running Verification Audits
- **Industrial 5-Gate Hardware CI Suite:**
  ```bash
  python run_comprehensive_verification.py
  ```
- **100k Dual-Mode Fuzzing & Balance Audit:**
  ```bash
  python audit_100k_dual_mode_ultimate_suite.py
  ```
- **1,000,000 Adversarial Footsteps & Single-Bit Fault Injection:**
  ```bash
  python audit_1m_adversarial_footsteps_suite.py
  ```
- **Hardware vs. Software Architectural Benchmark:**
  ```bash
  python benchmark_hw_vs_sw.py
  ```
