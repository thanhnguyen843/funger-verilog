# Funger Terminal (100% Pure Verilog Solo Explorer Edition)

A complete **Turn-Based Tactical Roguelike Dungeon Crawler** implemented in **synthesizable Verilog HDL** (`src/*.v` — **27** modules + `battle_defs.vh`) and played interactively via Icarus Verilog ([`tb/tb_play.v`](tb/tb_play.v) + `vvp`), featuring 24-bit TrueColor ANSI graphics rendered directly from hardware sprite ROMs with **zero Python at runtime**.

---

## 1. Core System Architecture (100% Pure Verilog)

### 1.1 Onboarding FSM & Dual Difficulty Modes (`character_rom.v`, `terminal_ui.v`, `tb_play.v`)
The onboarding FSM (`onboard_state`) cycles cleanly between **Title <-> Difficulty <-> Solo Hero Select** using `W/S` (`↑/↓`), `1..8`, `Enter`/`Space`, `Esc`/`Backspace` (`x`/`b`) Back navigation, and `Q` Quit:

1. **Mode 1 — "Fear & Hunger" (Normal Mode):**
   - **Empowered Explorer Stats:** Explorer **ATK and DEF are boosted by 1.5x** (`base + (base >> 1)`) and **Max HP increases by +25%** (`base_hp + (base_hp >> 2)`).
   - **Standard Solo Healing:** **Poppy Flower** restores **+50 HP** (`+65 HP` for Cahara), and **Medicinal Herb** restores **+120 HP** (`+150 HP` for Cahara).
2. **Mode 2 — "Terror & Starvation" (Hardcore Mode):**
   - **Baseline 1.0x Stats:** Raw character vitality, attack, and defense.
   - **Scarce Solo Healing:** **Poppy Flower** restores **+30 HP** (`+37 HP` for Cahara), and **Medicinal Herb** restores **+75 HP** (`+95 HP` for Cahara).

### 1.2 8 Solo Explorers, Unique 4-Skill Decks & Asymmetries
Using the Dual Split-Box **Solo Hero Selector** (`render_solo_select_screen`), pick **1 of 8 Explorers** with a live 24-bit TrueColor sprite preview and full dossier:

| ID | Explorer | Role | Unique 4-Skill Deck (`get_solo_skill_info`) | Key Solo Asymmetry |
| :---: | :--- | :--- | :--- | :--- |
| `1` | **Cahara** | Mercenary Rogue | `Twin Daggers`, `Poison Dart`, `Steal Item`, `Smoke Bomb` | `10`-slot bag (`2x` starter stock), `+25%` food/herb heal, `100%` Trap Disarm & `100%` Flee |
| `2` | **D'arce** | Holy Paladin | `Defense Stance`, `Healing Prayer`, `Holy Smite`, `Knight Charge` | Iron Armor (`-37.5%` physical damage taken); `0%` Toxicity Healing Prayer |
| `3` | **Enki** | Dark Occultist | `Black Orb`, `Ritual Dagger`, `Blood Sacrifice`, `Hexen Bind` | `130` Max Mind, `+5 Mind/turn`, dispels Hexen Seals (`0` dmg), `+25%` physical fragility |
| `4` | **Ragnvaldr** | Outlander Berserker | `War Axe`, `Spirit Totem`, `Feral Roar`, `Devour Flesh` | `150%` MaxTox tolerance, Bloodlust (`+50% ATK` below `35%` HP), Meat heals `+40 HP` (Bread `-20 Hng`) |
| `5` | **Le'garde** | Tactician Commander | `Fencing Thrust`, `Legion Light`, `Tactical Focus`, `War Cry` | Disarms Spring-Needle Chest traps (`0` dmg); Alchemical Vial grants `+50% ATK` Rush (`3` turns) |
| `6` | **Moonless** | Ancient Direhound | `Feral Bite`, `Moon Howl`, `Shadow Pounce`, `Scent Danger` | `30%` base Dodge, `0%` Herb Toxicity gain, Meat `+40 HP`, slips through `=` Crawlspaces |
| `7` | **The Girl** | Innocent Ward | `Nimble Dodge`, `Loving Embrace`, `Pure Light`, `Distract Foe` | `35%` base Dodge, Dread Aura immune, `-10% Tox/turn` auto-detox, slips through `=` Crawlspaces |
| `8` | **Nas'hrah** | Doom Wizard Head | `Combustion`, `Curse of Decay`, `Head Gnaw`, `Mock Foe` | `150` Max Mind, `0` Hunger / `0%` Tox, Seal dispel, refuses Guard & mortal herbs/food; Vial heals `+15 HP` |

### 1.3 `36x20` Labyrinth, Torchlight, Guide Modal & Obstacles
- **2-Tier Torchlight (`render_solo_map_screen`):** Full ANSI brightness within Euclidean torch radius `R = 4` (`dx^2 + dy^2 <= 16`) and dimmed TrueColor memory across the persistent `720`-bit `explored_mask`.
- **`[G]` Expedition Survivor Guide Book (`render_guide_modal_screen`):** On-demand 26-row modal keeping map legends, hazards, supplies, and controls out of the exploration viewport.
- **Role-Aware Obstacles & Vaults:**
  - `#` **Barricade** `(6,7), (20,11)`: Smashed open on contact.
  - `§` **Hexen Seal** `(16,3), (24,15)`: Arcane ward dispelled safely by `Enki`/`Nas'hrah`; burns mortals for `-10 HP`.
  - `=` **Crawlspace / Crevice** `(10,2), (28,16)`: Small frames (`Moonless`, `The Girl`) slip effortlessly through; others wedge carefully.
  - `C` **Chests (7 Vaults):** 3 **Spring-Needle Key Vaults** at `(6,11)`, `(12,17)`, `(26,17)` guarantee Runic Keys (`Cahara` & `Le'garde` disarm; others take `-20 HP`). Remaining chests roll `25%` **Chest Mimic (`ID 23`)** via `rng_unit` (`hw_rand_pct < 25`) or open the 24-bit TrueColor supply/key vault screen.
  - `G` **Eastern Exit Gates** `(35,6), (35,14)`: Guarded by Gatekeeper Bosses at `(34,6)` **Abyssal Overlord (`ID 20`)** and `(34,14)` **Cthulhu Titan (`ID 36`)**. Collecting `3/3` Runic Keys (backed by a deterministic Pity Safety Net) unlocks the gate for the **Solo Victory Screen**.

### 1.4 Persistent Dual-Box Survival Pouch (`[I]`) — 8 Unified Items
`render_solo_pouch_screen` displays the live hero sprite (left), 4 color meter bars (`HP`, `MIND`, `HUNGER`, `TOXIC`), limb status (`H/T/RA/LA/LG`), trait/status (right), and 8 selectable slots:
1. `[1]` **Totem of Undying** (`x1` unique relic): Restores full HP, clears toxicity/bleeding/poison & mends limbs manually, or **auto-revives on fatal collapse** (combat, Spring Needle trap, or starvation).
2. `[2]` **Poppy Flower**: Restores `+50`/`+30 HP` & stops bleeding (`+35%` Tox; Ragnvaldr `+15%`, Moonless `0%`).
3. `[3]` **Medicinal Herb**: Restores `+120`/`+75 HP` & `+15 Mind` (`+50%` Tox; Ragnvaldr `+25%`, Moonless `0%`). Herbs at `>= MaxTox` trigger **Overdose** (`-5 HP`, `0` heal).
4. `[4]` **Moldy Bread**: Relieves `-40 Hunger` (`-50` Cahara, `-20` Ragnvaldr).
5. `[5]` **Dried Meat**: Relieves `-60 Hunger` & restores `+20 HP` (`+40 HP` Ragnvaldr/Moonless).
6. `[6]` **Alchemical Vial**: `+35 Mind`, `-25% Tox`, purges bleeding & necrotic poison (`+15 HP` for Nas'hrah; `+50% ATK` Rush for Le'garde).
7. `[7]` **Runic Key**: Reports `0/3` Eastern Gate key progress.
8. `[8]` **[ CLOSE POUCH ]** (or `[I]` / `[Esc]` / `[B]` / `[Q]`).

### 1.5 Pokémon-Style Solo Combat Arena & Tri-State Monster Morphology
- **36 Monsters & Tri-State Shader (`monster_rom.v`, `monster.v`, `fantasy_creatures.v`, `monster_state_model.v`):** `NORMAL` (`2'b00`, full-color upright), `INJURED` (`2'b01`, Technical Amber `#FFAA28` crouched posture & fracture joints), and `DEAD` (`2'b10`, Ash Gray `#6E7378` decapitated/neutralized). Includes Grave Spider (`ID 10`) horizontal orientation handling and 8 Elite horrors (`+20%` stats).
- **Clean 5-Option Hierarchical Menu (`▶` Cursor, Zero Yellow Glare):**
  - `ATTACK` -> `HEAD` (`30%` / `100%` crawling instant decapitate), `TORSO` (`95%`), `RIGHT ARM` (`80%` disarm), `LEFT ARM` (`80%` guard break), `LEGS` (`85%` crawling -> `100%` Head Hit & `100%` Flee), `BACK`.
  - `GUARD` (`-70%` incoming DMG; `Nas'hrah` refuses).
  - `SKILL` (`4` unique hero skills + `BACK`).
  - `ITEM` (opens Survival Pouch; spends turn only when an item is used).
  - `FLEE` (`100%` for Cahara or crawling enemies; `hw_stance_flee_pct` otherwise).
- **Hardware Coprocessors (`battle_top.v`, `battle_fsm.v`, `damage_alu.v`, `rng_unit.v`, `tactical_stance_unit.v`, `sanity_meter_unit.v`):** Single-cycle combinational `damage_alu.v`, 32-bit Galois LFSR (`rng_unit.v`, 0 `$random`), `[Z]` mid-combat 4-stance toggle (`BALANCED`, `BERSERK`, `IRON GUARD`, `AGILE`), synchronous Mind/Hunger/Panic/Starvation pulses, and Coin Flip of Fate lethal-cleave parry.

---

## 2. Directory Layout (`27` RTL/ROM Modules + `19` Testbenches)

```text
funger_terminal/
├── src/                                    # 27 Synthesizable Verilog Modules + battle_defs.vh
│   ├── battle_defs.vh                      # Shared constants, opcodes, item IDs & map tiles
│   ├── battle_top.v / battle_fsm.v         # Top-level hardware coordinator & state machine
│   ├── damage_alu.v / rng_unit.v           # Combinational combat ALU & 32-bit Galois LFSR
│   ├── collision_unit.v / inventory_ram.v  # Maze wall/tile detector & party/supply RAM
│   ├── tactical_stance_unit.v              # 4-Stance multiplier coprocessor ([Z])
│   ├── sanity_meter_unit.v                 # Mind / hunger / panic / starvation coprocessor
│   ├── map_rom.v / character_rom.v / monster_rom.v
│   ├── monster_state_model.v               # Tri-state posture & Amber/Ash color morphology
│   ├── sprite_rom.v / chest_sprite_rom.v / key_sprite_rom.v / sprite_router.v
│   ├── funger_cahara_rom.v / funger_darce_rom.v / funger_enki_rom.v / funger_ragnvaldr_rom.v
│   ├── funger_legarde_rom.v / funger_moonless_rom.v / funger_thegirl_rom.v / funger_nashrah_rom.v
│   ├── monster.v / fantasy_creatures.v
│   ├── terminal_ui.v                       # 24-bit TrueColor ANSI renderer (simulation display)
│   └── gen_chest_key_roms.py               # Offline pixel-art ROM codegen utility
├── tb/                                     # 19 Pure Verilog Verification & Gallery Testbenches
│   ├── tb_play.v                           # Main interactive Solo Explorer simulation
│   ├── tb_full_map_victory.v               # battle_top.v full-map 3-key campaign TB
│   ├── tb_battle_top.v / tb_dual_mode_top.v / tb_battle_auto.v / tb_game_check.v
│   ├── tb_damage_alu.v / tb_golden_trace.v / tb_fsm_fuzzer.v
│   ├── tb_deep_logic_suite.v / tb_adversarial_chaos.v / tb_waveform_trace.v
│   └── tb_show_characters.v / tb_show_monsters.v / tb_show_monster_states.v / tb_show_events.v / tb_show_models.v / tb_showcase_all.v / tb_show_victory_lose.v
└── *.py                                    # Strictly offline verification, audit & benchmark scripts
```

*(Note: All `.py` files inside `funger_terminal/` — including `run_comprehensive_verification.py`, `local_test_matrix.py`, `test_matrix.py`, `audit_*.py`, `benchmark_hw_vs_sw.py`, and legacy/reference TUI scripts such as `master_game.py` and `demo_*.py` — are strictly offline tools and are never invoked by [`PLAY_GAME.bat`](../PLAY_GAME.bat).)*

---

## 3. Running & Inspecting the Pure Verilog Project

### 3.1 Launch Playable Solo Explorer Simulation (Zero Python Required)
From the repository root (sole `.bat` launcher — configures `cols=100 lines=46`, compiles with `iverilog -Wall -g2012`, and runs `vvp sim/funger_play.out` via an inline PowerShell raw-key & atomic `\033[H...\033[K\033[J` frame blitter with `<= 44` rows and `0` mid-game `\x1b[2J` flashes):
```bat
PLAY_GAME.bat
```
Or manually inside `funger_terminal/`:
```bash
mkdir -p sim
iverilog -Wall -g2012 -I src -o sim/funger_play.out tb/tb_play.v src/*.v
vvp sim/funger_play.out
```

### 3.2 Run Hardware Testbenches & Gallery Viewers
```bash
# Functional & Integration TBs (inside funger_terminal/)
iverilog -Wall -g2012 -I src -o sim/tb_damage_alu.out tb/tb_damage_alu.v src/damage_alu.v && vvp sim/tb_damage_alu.out
iverilog -Wall -g2012 -I src -o sim/tb_game_check.out tb/tb_game_check.v src/*.v && vvp sim/tb_game_check.out
iverilog -Wall -g2012 -I src -o sim/tb_battle_auto.out tb/tb_battle_auto.v src/*.v && vvp sim/tb_battle_auto.out
iverilog -Wall -g2012 -I src -o sim/tb_dual_mode_top.out tb/tb_dual_mode_top.v src/*.v && vvp sim/tb_dual_mode_top.out

# TrueColor ANSI Hardware ROM Galleries (36 monsters tri-state, heroes, items)
iverilog -Wall -g2012 -I src -o sim/tb_show_monster_states.out tb/tb_show_monster_states.v src/*.v && vvp sim/tb_show_monster_states.out
iverilog -Wall -g2012 -I src -o sim/tb_show_models.out tb/tb_show_models.v src/*.v && vvp sim/tb_show_models.out

# Waveform Trace (.vcd) for GTKWave
iverilog -Wall -g2012 -I src -o sim/tb_waveform_trace.out tb/tb_waveform_trace.v src/*.v && vvp sim/tb_waveform_trace.out
```

### 3.3 Offline Python Verification & Audit Suites
```bash
# From repository root (retro_game_verilog/)
python funger_terminal/run_comprehensive_verification.py   # 7-Stage Master Verification Suite
python funger_terminal/audit_hardware_linter.py            # Static RTL synthesizability & -Wall lint audit
python funger_terminal/audit_string_overflow.py            # ROM string width & ANSI escape integrity guard

# From funger_terminal/
python local_test_matrix.py                                # 26 Solo Explorer & RTL E2E test suites
python test_matrix.py                                      # 7 fast Solo & RTL CI integration suites
python audit_visual_screen_inspector.py                    # 108/108 visual checks (36 monsters x 3 states)
python audit_5000_deep_adversarial_matrix.py               # 5,000/5,000 combinatorial & adversarial matrix
python benchmark_hw_vs_sw.py                               # Hardware RTL vs. RISC-V software benchmark
```
