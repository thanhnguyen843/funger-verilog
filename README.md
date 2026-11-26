# Fear & Hunger: Terminal Labyrinth (100% Pure Verilog Solo Explorer Edition)

> A **100% Synthesizable Verilog HDL** turn-based tactical roguelike RPG engine simulated in Icarus Verilog (`iverilog` / `vvp`) with 24-bit TrueColor ANSI terminal graphics, hardware combat arithmetic ([`damage_alu.v`](funger_terminal/src/damage_alu.v)), 32-bit Galois LFSR PRNG ([`rng_unit.v`](funger_terminal/src/rng_unit.v)), maze collision ([`collision_unit.v`](funger_terminal/src/collision_unit.v)), tri-state monster morphology ([`monster_state_model.v`](funger_terminal/src/monster_state_model.v)), and hardware tactical/sanity coprocessors.

---

## 🎮 Quick Start — 100% Pure Verilog Launch (Zero Python at Runtime)

Double-click or run the **sole `.bat` launcher** in the repository from Command Prompt, PowerShell, or Windows Terminal:

```bat
PLAY_GAME.bat
```

- **Zero Python at Runtime:** [`PLAY_GAME.bat`](PLAY_GAME.bat) configures UTF-8 (`chcp 65001`), console size (`mode con: cols=100 lines=46`), and Windows Virtual Terminal ANSI (`VirtualTerminalLevel`), compiles the Solo Explorer RTL/ROM modules and [`tb_play.v`](funger_terminal/tb/tb_play.v) with `iverilog -Wall -g2012 -I src` (0 errors, 0 warnings), and runs **`vvp sim/funger_play.out`** directly. All `.py` files in the repository are strictly offline verification/audit/benchmark utilities (or legacy reference prototypes) and are **never executed at runtime**.
- **Built-in PowerShell Raw Key & Atomic Frame Blitter:** [`PLAY_GAME.bat`](PLAY_GAME.bat) embeds an inline Windows PowerShell host (`__PS_HOST_BEGIN__`) around `vvp sim/funger_play.out`:
  - **Zero-Enter Raw Keys (`[Console]::ReadKey($true)`):** `W`/`A/S/D`, Arrow keys (`↑`/`↓`/`←`/`→`), `Enter`/`Space`, `Esc`/`Backspace` (`x`/`b`), `1..8`, `G`, `I`, `Z`, and `Q` respond immediately with repeat-key drain — while automatically falling back to plain `vvp sim/funger_play.out` when stdin is piped (CI/automated test mode).
  - **Atomic Zero-Flicker Rendering:** Buffers each Verilog frame from `\033[H` through `\033[K\033[J` (or `\033[?25h` on exit) and emits a single atomic `$stdout.Write` call per frame. `\x1b[2J` is issued strictly at initial startup and clean exit (**0 mid-game clear-screen flashes**), enforcing **`<= 44` rows x exact `100` columns** and zero yellow `\033[43m` menu glare.

### Manual Compile & Run (Linux / CLI Evaluation)

```bash
cd funger_terminal
mkdir -p sim

# Compile and run Pure Verilog Solo Explorer (tb_play.v)
iverilog -Wall -g2012 -I src -o sim/funger_play.out tb/tb_play.v src/*.v
vvp sim/funger_play.out
```

*(Note on Windows PowerShell: expand `src/*.v` via `$srcs = (Get-ChildItem src/*.v).FullName; iverilog -Wall -g2012 -Isrc -o sim/funger_play.out tb/tb_play.v $srcs`.)*

---

## 🧭 Solo Explorer Gameplay UX (100% Pure Verilog RTL)

All onboarding, labyrinth exploration, survival inventory, and combat screens are rendered directly by [`terminal_ui.v`](funger_terminal/src/terminal_ui.v) and driven by [`tb_play.v`](funger_terminal/tb/tb_play.v):

1. **Onboarding FSM (`Title <-> Difficulty <-> Solo Hero Select`):**
   - **Title Screen:** Dark gothic boxed menu (`[1] START EXPEDITION (EMBARK SOLO)` / `[2] ABANDON HOPE (QUIT)`).
   - **Difficulty Screen:** Choose between *Fear & Hunger* (Normal: `1.25x` Max HP, `1.5x` ATK/DEF boost, Poppy `+50 HP`, Medicinal Herb `+120 HP`) and *Terror & Starvation* (Hardcore: `1.0x` baseline stats, Poppy `+30 HP`, Medicinal Herb `+75 HP`).
   - **Solo Hero Select (1 of 8 Heroes):** Dual Split-Box selector with **Live 24-bit TrueColor Sprite Preview** and complete **Solo Hero Dossier** (HP, ATK, DEF, PHYS-R, MAG-R, DODGE, Bag Cap / MaxTox, Trait, Buff, 4 unique skills, and Survival Assessment) for **Cahara**, **D'arce**, **Enki**, **Ragnvaldr**, **Le'garde**, **Moonless**, **The Girl**, and **Nas'hrah**.
   - **Full Navigation Controls:** `W`/`S` or `↑`/`↓` cursor movement, `1..8` quick jump, `Enter`/`Space` confirm, `Esc`/`Backspace` (`x`/`b`) Back navigation (`Solo Select -> Difficulty -> Title`), and `Q` Quit.

2. **`36x20` Labyrinth Map (`map_rom.v`, `collision_unit.v`):**
   - **2-Tier Torchlight & Persistent Exploration:** Full-brightness Euclidean torch radius `R = 4` (`dx^2 + dy^2 <= 16`) with dimmed TrueColor memory across the `720`-bit `explored_mask`.
   - **`[G]` On-Demand Expedition Survivor Guide Book Modal:** Cleanly separates tile legend, hazards, supplies/relics, and controls from the map viewport (`<= 26` rows).
   - **`[I]` Persistent Dual-Box Survival Pouch & Dossier:** Displays the live TrueColor Hero sprite alongside 4 visual meter bars (`HP`, `MIND`, `HUNGER`, `TOXIC`), combat stats, `0/3` Runic Keys, limb status (`H/T/RA/LA/LG`), trait/status, and **8 unified pouch slots** (`[1] Totem of Undying` auto-revive relic, `[2] Poppy Flower`, `[3] Medicinal Herb`, `[4] Moldy Bread`, `[5] Dried Meat`, `[6] Alchemical Vial`, `[7] Runic Key`, `[8] [ CLOSE POUCH ]`), including Herbal Toxicity / Overdose and hero-specific asymmetries.
   - **Obstacles, Traps & 3-Key Victory:** Features `#` Barricades, `§` Hexen Seals (Occultists dispel safely; mortals take `-10 HP`), `=` Crawlspaces (small frames slip through effortlessly), 3 Spring-Needle Key Vaults (`Cahara` & `Le'garde` disarm safely; others `-20 HP`), `25%` Mimic (`ID 23`) chest ambushes via `rng_unit`, Gatekeeper Bosses at `(34,6)` and `(34,14)`, a deterministic 3-Key Pity Safety Net, and Eastern Exit Gates `G` requiring `3/3` Runic Keys.

3. **Pokémon-Style Solo Combat Arena (`render_solo_combat_screen`):**
   - **Tri-State Monster Morphology ([`monster_state_model.v`](funger_terminal/src/monster_state_model.v)):** All 36 monsters render in `NORMAL` (full-color upright), `INJURED` (Technical Amber `#FFAA28` crouched posture & fractured joints), and `DEAD` (Ash Gray `#6E7378` neutralized/decapitated).
   - **Clean 5-Option Hierarchical Menu (`▶` Cursor, Zero Yellow Glare):**
     - `ATTACK` -> Limb Submenu (`HEAD` `30%` / `100%` if crawling, `TORSO` `95%`, `RIGHT ARM` `80%` disarms ATK, `LEFT ARM` `80%` shatters DEF, `LEGS` `85%` forces crawling, `BACK`)
     - `GUARD` (`-70%` incoming DMG; `Nas'hrah` refuses)
     - `SKILL` (`4` unique skills per hero + `BACK`)
     - `ITEM` (opens Survival Pouch; consumes a turn only if an item is used)
     - `FLEE` (`100%` for `Cahara` or against crawling enemies; stance-scaled otherwise)
   - **`[Z]` Tactical Stance Coprocessor ([`tactical_stance_unit.v`](funger_terminal/src/tactical_stance_unit.v)):** Cycles `BALANCED` -> `BERSERK` -> `IRON GUARD` -> `AGILE` mid-combat without spending a turn.
   - **Coin Flip of Fate & Game Over:** Interactive Heads/Tails parry clash (`W/S` + `Enter`) on lethal enemy cleaves and dedicated `SURVIVOR DEMISE` Game Over screen (after any *Totem of Undying* auto-revive is consumed).

---

## ⚙️ Core Synthesizable Verilog Hardware Architecture

- **Top-Level Hardware Core ([`battle_top.v`](funger_terminal/src/battle_top.v)) & FSM ([`battle_fsm.v`](funger_terminal/src/battle_fsm.v)):** Coordinates game states using synchronous non-blocking transitions.
- **1-Cycle Combinational Combat ALU ([`damage_alu.v`](funger_terminal/src/damage_alu.v)):** Computes limb-targeted multipliers, guard mitigation, disarm scaling, flee penalties (`5/16` via shift-add), and underflow clamping (`>= 2 DMG`) with zero non-power-of-2 `/` or `%`.
- **32-bit Galois LFSR PRNG ([`rng_unit.v`](funger_terminal/src/rng_unit.v)):** Generates `rand_pct` (`0..99`), `rand_bit_50`, and monster IDs using shift/mask logic (`0` `$random` in RTL).
- **Labyrinth ROM & Collision Unit ([`map_rom.v`](funger_terminal/src/map_rom.v), [`collision_unit.v`](funger_terminal/src/collision_unit.v)):** Combinational coordinate & tile evaluation across the `36x20` dungeon grid.
- **Multi-Port Inventory RAM ([`inventory_ram.v`](funger_terminal/src/inventory_ram.v)):** Tracks explorer HP, pouch supplies, and the `3`-Key Escape Gate counter.
- **Hardware Coprocessors:** [`tactical_stance_unit.v`](funger_terminal/src/tactical_stance_unit.v) and [`sanity_meter_unit.v`](funger_terminal/src/sanity_meter_unit.v) (Mind, Hunger, Panic ATK penalty, and Starvation pulses).

---

## 📁 Repository Structure

```text
retro_game_verilog/
├── PLAY_GAME.bat                                # Sole .bat launcher (iverilog + vvp + PS raw-key blitter; 0% Python)
├── README.md                                    # Master project documentation
├── GIT_WORKFLOW.md                              # Team branching & verification rules
├── UI_LAYOUT_MISTAKES_AND_POSTMORTEM_RULES.md   # Terminal UI invariants & layout postmortems
├── .github/workflows/hardware_ci.yml            # GitHub Actions automated RTL & Solo CI workflow
└── funger_terminal/
    ├── README.md                                # Detailed RTL module, hero & testbench reference
    ├── src/                                     # 27 Synthesizable Verilog modules + battle_defs.vh
    │   ├── battle_defs.vh                       # Global opcodes, item IDs, map & stance constants
    │   ├── battle_top.v / battle_fsm.v          # Top-level hardware core & state machine
    │   ├── damage_alu.v / rng_unit.v            # Combinational combat ALU & 32-bit Galois LFSR
    │   ├── collision_unit.v / inventory_ram.v   # Maze boundary unit & party/supply RAM
    │   ├── tactical_stance_unit.v               # Dynamic stance multiplier coprocessor
    │   ├── sanity_meter_unit.v                  # Sanity / hunger / starvation coprocessor
    │   ├── map_rom.v, character_rom.v, monster_rom.v
    │   ├── monster_state_model.v                # Tri-state posture & Amber/Ash morphology transform
    │   ├── sprite_rom.v, chest_sprite_rom.v, key_sprite_rom.v, sprite_router.v
    │   ├── funger_*_rom.v, monster.v, fantasy_creatures.v
    │   └── terminal_ui.v                        # ANSI 24-bit TrueColor Solo & hardware renderer
    ├── tb/                                      # 19 Pure Verilog testbenches (0 -Wall warnings)
    │   ├── tb_play.v                            # Main playable Pure Verilog Solo Explorer simulator
    │   ├── tb_full_map_victory.v                # battle_top.v full-map 3-key victory campaign
    │   ├── tb_damage_alu.v, tb_game_check.v, tb_battle_auto.v, tb_battle_top.v
    │   ├── tb_deep_logic_suite.v, tb_adversarial_chaos.v, tb_fsm_fuzzer.v
    │   ├── tb_golden_trace.v, tb_dual_mode_top.v, tb_waveform_trace.v
    │   └── tb_show_*.v / tb_showcase_all.v      # ANSI TrueColor hero, monster & event galleries
    └── *.py                                     # Strictly offline verification, audit & benchmark helpers
```

---

## 🔬 Verification, Hardware Hygiene & Audit Suite

### Pure Verilog RTL Verification (Zero Python Required)

All **27** modules in `funger_terminal/src/` maintain `0` `$random` calls, `0` non-power-of-2 `/` or `%` operators, `0` hierarchical probes, and `0` `iverilog -Wall -g2012` warnings across all **19** testbenches:

```bash
# Run from funger_terminal/ (tb_full_map_victory reads funger_terminal/sim/tour_moves.txt from repo root)
iverilog -Wall -g2012 -I src -o sim/tb_damage_alu.out tb/tb_damage_alu.v src/damage_alu.v && vvp sim/tb_damage_alu.out
iverilog -Wall -g2012 -I src -o sim/tb_game_check.out tb/tb_game_check.v src/*.v && vvp sim/tb_game_check.out
iverilog -Wall -g2012 -I src -o sim/tb_battle_auto.out tb/tb_battle_auto.v src/*.v && vvp sim/tb_battle_auto.out
iverilog -Wall -g2012 -I src -o sim/tb_waveform_trace.out tb/tb_waveform_trace.v src/*.v && vvp sim/tb_waveform_trace.out
```

From the repository root (`retro_game_verilog/`), verify top-level full-map victory on `battle_top.v`:
```bash
iverilog -Wall -g2012 -I funger_terminal/src -o funger_terminal/sim/tb_full_map_victory.out funger_terminal/tb/tb_full_map_victory.v funger_terminal/src/*.v
vvp funger_terminal/sim/tb_full_map_victory.out
```

### Offline Python Verification & Audit Suites

All `.py` scripts are **strictly offline verification, fuzzing, linting, visual-audit, and benchmark tools** and are never required to build or play the Verilog game:

```bash
# Run from repository root (retro_game_verilog/)
python funger_terminal/run_comprehensive_verification.py     # 7 Stages: Linter, String/ANSI Guard, Golden Trace, 100k LFSR, 50k FSM Fuzzer, Deep Logic, Chaos
python funger_terminal/audit_hardware_linter.py              # Static synthesizability & strict iverilog -Wall -g2012 linter
python funger_terminal/audit_string_overflow.py              # ROM register string-width & ANSI reset guard

# Run from funger_terminal/
python local_test_matrix.py                                  # 26 Solo Explorer & RTL verification suites (<=44 rows x 100 cols, 0 warnings, 0 mid-game 2J)
python test_matrix.py                                        # 7 fast Solo & RTL CI integration suites
python audit_visual_screen_inspector.py                      # 108/108 visual render checks (36 monsters x 3 states)
python audit_5000_deep_adversarial_matrix.py                 # 5,000/5,000 combinatorial & adversarial verification matrix
```

---

## 🛠️ Requirements

- **Required (Verilog RTL Compilation & Simulation):** [Icarus Verilog](https://bleyer.org/icarus/) (`iverilog` & `vvp` in `PATH`) on Windows 10/11 (PowerShell/CMD/Windows Terminal with UTF-8 + Virtual Terminal support) or Linux.
- **Optional:** [GTKWave](https://gtkwave.sourceforge.net/) for inspecting `.vcd` waveforms from `tb_waveform_trace.v`, and Python 3.8+ (standard library only) for running the offline audit/verification suites.
