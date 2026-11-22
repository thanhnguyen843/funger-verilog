# Funger Terminal (Fear & Hunger Verilog HDL Edition)

A complete **Turn-Based Tactical Roguelike Dungeon Crawler** implemented at the Register-Transfer Level (RTL) in **Verilog HDL**, simulated in interactive console terminals using **Icarus Verilog**.

---

## 1. System Architecture & Features

### 1.1 Dual Difficulty Modes (Fear & Hunger vs. Terror & Starvation)
Upon starting an expedition, players choose between two distinct difficulty levels:
1. **Mode 1: "Fear & Hunger" (Normal / Standard Expeditions)**:
   - **Empowered Explorer Combat Stats**: Player character **ATK and DEF are boosted by 1.5x** and **Max HP is boosted by +25%** (`base_hp + (base_hp >> 2)`) (e.g. Cahara: 156 HP, 33 ATK / 21 DEF; D'arce: 181 HP, 30 ATK / 30 DEF; Ragnvaldr: 193 HP, 39 ATK / 18 DEF) while monsters remain at standard stats.
   - **Generous Healing Potencies**: **Poppy Flower** restores **+50 HP**, and **Marijuana Herb** restores **+120 HP**.
   - Ideal for dungeoneers seeking balanced combat and tactical survival.
2. **Mode 2: "Terror & Starvation" (Hardcore / Classic Fear & Hunger Mode)**:
   - **Baseline Explorer Combat Stats**: Player character stats revert to raw **1.0x baseline values** (e.g. Cahara: 22 ATK / 14 DEF, Enki: 30 ATK / 16 DEF, Nas'hrah: 34 ATK / 12 DEF).
   - **Scarce Healing Potencies**: **Poppy Flower** restores only **+30 HP**, and **Marijuana Herb** restores only **+70 HP**.
   - For true hardcore survivors prepared to face despair, severe attrition, and lethal encounters.

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
- **Character Selection**: Players select 4 explorers to form an active party with dynamic stats reflecting their chosen difficulty mode.

### 1.3 Monster Roster & Elite Mechanics
- **36 Total Monsters**:
  - IDs 1 to 20: Built from `monster.v` (Monster pixel-art sheet).
  - IDs 21 to 36: Built from `fantasy_creatures.v` (Fantasy pixel-art creatures).
- **Elite System**:
  - 8 predetermined Elite monsters have reduced spawn weights and **+20% bonus HP, ATK, and DEF**.
- **No-Repeat Rule**: Defeated monsters are tracked in bitmask registers and cannot appear again in subsequent `M` tiles.
- **Drop Rates & Worst-Case Guarantee**:
  - Standard Monster: **20% Key drop**, cannot drop healing items.
  - Elite Monster: **50% Key drop**, **20% Poppy drop**.
  - **Worst-Case 3-Key Safety Net (Pity System)**: Even in the worst possible RNG luck streak, clearing the maze monsters is **100% mathematically guaranteed** to yield all 3 Dungeon Keys!

### 1.4 Chests & Mimics
- **Chest Tile `'C'`** (Brown background, letter `'C'`):
  - **20% encounter probability** to awaken a **Mimic** (dedicated model from Fantasy Creatures, ID 23).
  - **80% safe loot probability**: High chance for **Dungeon Key**, or **Poppy Flower** / **Marijuana Herb**.
  - Mimic is **guaranteed to never be an Elite**.
  - Defeating a Mimic or opening a secure chest permanently clears the tile.
  - **Full-Screen Chest Opening Scene**: Opens an immersive inspection scene rendering the 20x23 chest pixel-art model and boxed bounty notifications.

### 1.4 Endgame Gate Mechanism
- **Dungeon Gates `'G'`** (Cyan background, letter `'G'`):
  - Strictly embedded in the **rightmost outer boundary wall** ($x = 35$).
  - Guarded directly in front ($x = 34$) by a gatekeeper monster `'M'`.
  - Requires **3 Dungeon Keys** collected from monsters or chests to unlock. Keys have no other function.

### 1.5 Medical Pouch & Inventory System
- Initial supply: **10 Poppy Flowers** (+50 HP) and **3 Marijuana Herbs** (+120 HP).
- Usable both during dungeon navigation and inside active combat (**costs 1 combat turn**).
- Full boxed notifications with sender/recipient details and HP restored.
- Inventory HUD displays mini item pixel-art icons, item names, and remaining quantities.

---

## 2. Directory Structure

```text
funger_terminal/
├── run_comprehensive_verification.py # 5-Gate DO-254 / OpenTitan industrial verification suite
├── audit_hardware_linter.py          # Stage 1: Static hardware synthesizability audit
├── audit_string_overflow.py          # Stage 2: String register width & ANSI integrity
├── audit_damage_accounting.py        # Stage 3: Python golden reference co-simulation
├── audit_rng_pity.py                 # Stage 4: 100k-cycle LFSR chi-square & pity proof
├── benchmark_hw_vs_sw.py             # Hardware vs. Software (RISC-V) benchmarking tool
├── src/                              # 100% Synthesizable Verilog RTL Modules
│   ├── battle_defs.vh                # Global system definitions & states
│   ├── character_rom.v               # 8 Fear & Hunger character stats and database
│   ├── monster_rom.v                 # 36 Monster database with Elite weights and stats
│   ├── map_rom.v                     # 20x36 Labyrinth map ROM with rightmost Gates 'G' and guard 'M'
│   ├── collision_unit.v              # Collision detection unit for walls, chests, gates, and foes
│   ├── inventory_ram.v               # RAM managing 4-character squad, Poppy, Marijuana, and 3 Keys
│   ├── chest_sprite_rom.v            # 20x23 pixel-art chest model ROM
│   ├── key_sprite_rom.v              # 11x22 pixel-art key model ROM + compact pouch icon
│   ├── funger_*_rom.v                # 8 Fear & Hunger player character pixel-art ROMs
│   ├── monster.v                     # 20 Monster pixel-art sprite sheet ROM
│   ├── fantasy_creatures.v           # 16 Fantasy creature pixel-art sprite sheet ROM
│   ├── tactical_stance_unit.v        # Hardware Tactical Stance Coprocessor (4 stances)
│   ├── sanity_meter_unit.v           # Hardware Sanity & Hunger Environmental Entropy Coprocessor
│   ├── sprite_router.v               # Color sprite multiplexer for side-by-side battle rendering
│   ├── terminal_ui.v                 # ANSI terminal UI (Map, Bag, Full-Screen Chest, Battle, Boxed Alerts)
│   ├── damage_alu.v                  # Combat damage calculation arithmetic unit
│   ├── rng_unit.v                    # 32-bit LFSR PRNG unit
│   └── battle_top.v                  # Top-level RTL hardware coordinator
└── tb/                               # Comprehensive Testbenches
    ├── tb_play.v                     # Interactive keyboard testbench
    ├── tb_game_check.v               # Comprehensive feature verification testbench
    ├── tb_battle_auto.v              # Automated regression testbench
    ├── tb_damage_alu.v               # ALU combat matrix unit testbench
    ├── tb_golden_trace.v             # Golden model co-simulation trace generator
    ├── tb_fsm_fuzzer.v               # 50,000-iteration random input FSM fuzzer
    └── tb_waveform_trace.v           # GTKWave VCD architecture waveform testbench
```

---

## 3. How to Run and Play

### 3.1 Play the Interactive Game
Double-click or run:
```cmd
play.bat
```
Provides the full playable experience with character drafting, dungeon crawling, chest looting/Mimic encounters, tactical turn-based combat, in-combat character switching, squad viewing, and the 3-key dungeon exit quest!

### 3.2 View All Models & Stats (Encyclopedia Gallery)
Double-click or run:
```cmd
show_models.bat
```
Renders all **44 models** in the game (8 Fear & Hunger Heroes, 20 Retro Monsters, 16 Fantasy Horrors including the Mimic, and Vault Relics/Supplies) in full 24-bit TrueColor ANSI pixel art alongside their complete stats, combat roles, spawn weights, and drop tables!

### 3.3 Run Automated Regression Tests
```cmd
run_game_check.bat
```
All feature checks (Draft screen, Map grid, Pouch UI, Boxed notifications, Full-screen chest, Elite monster weights, In-combat healing turn usage, and 3-Key Gate victory) will be executed and verified in ANSI color.

