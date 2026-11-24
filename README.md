# Fear & Hunger: Terminal Labyrinth (Verilog Hardware & ANSI Edition)

> A dark fantasy tactical roguelike RPG simulation engine co-designed in Verilog RTL hardware and rendered in high-contrast ANSI 24-bit TrueColor in the Windows Terminal.

---

## 🎮 Quick Start (Khởi Chạy Game Nhanh)

To play immediately, run the **single unified launcher** from Windows Terminal, PowerShell, or CMD:
```bat
PLAY_GAME.bat
```
- **Automatic Configuration:** Sets terminal to `100 cols x 36 lines` and enables Windows 24-bit Virtual Terminal ANSI sequences.
- **Resilient Fallback:** Automatically checks and verifies Verilog RTL hardware synthesis if [Icarus Verilog](https://bleyer.org/icarus/) is installed, and seamlessly launches the full Python game engine (`python funger_terminal/master_game.py`) or hardware simulation binary (`vvp sim/funger_play.out`).

---

## ⚔️ Key Features & Innovations

### 1. 🎒 Dual Split-Box Showcase Satchel UI
- **Left Box (Hero Model Showcase - 46 cols):** Renders the full 24-bit TrueColor pixel-art sprite of the active explorer, updating dynamically between 3 morphologies:
  - `Normal`: Fully armed, battle-ready.
  - `Injured`: Mutilated limb loss, bleeding wounds, Sylvian amber glow.
  - `Dead`: Fallen on blood pool, desaturated monochrome.
- **Right Box (Vitals & Limb Dossier - 47 cols):** Real-time graphical gauge bars and physical status:
  - `HP`: Dynamic color-coded bar (Green $\rightarrow$ Yellow $\rightarrow$ Flashing Red).
  - `MIND`: Indigo sanity meter with Panic/Madness threshold.
  - `HUNGER`: Amber starvation bar.
  - `TOXICITY`: Purple necrosis and poison tracker.
  - `Limb Integrity`: Real-time status for `[HEAD]`, `[TORSO]`, `[ARMS]`, `[LEGS]`.
  - `Class Traits`: Unique passive perks (e.g., *Lockpicking & Dual Daggers*, *Iron Plate Armor*).

### 2. 🌐 Concise English Localization (Zero-Truncation Layout)
- **100% English Survival & Combat Pouch:** Items, categories, and effects translated into clear, concise terminology (`[RELIC]`, `[HERB]`, `[RATION]`, `[TINCTURE]`, `[KEY]`).
- **Strict Budget Invariant:** Descriptions are capped to $\le 45$ characters, guaranteeing **0.0% text truncation** and exact adherence to the `100 cols x <= 35 lines` terminal viewport.

### 3. 👥 8 Fear & Hunger Heroes & 3 Select Layouts
- **Playable Explorers:** Cahara (Mercenary), D'arce (Holy Knight), Enki (Dark Priest), Ragnvaldr (Berserker), Le'garde (Commander), Moonless (Cave Wolf), The Girl, Nas'hrah (Severed Head).
- **Press `[TAB]` to switch layouts:**
  - `Quad Grid (2x2)`: 4 spacious cards with 29-col full hero sprites and stat cards.
  - `Vertical Split`: Vertical roster on the left, full hero stage on the right.
  - `Panorama (3-Col)`: 3 large side-by-side cards with 3-line stacked stat bars.

### 4. 🩸 Tactical Combat & Limb Dismemberment System
- **Diagonal 50/50 Split Arena:** Foe top-right, Hero bottom-left.
- **Targetable Body Parts:**
  - `[H]` Head (25% base hit - Instant Decapitation Kill, 100% when crawling)
  - `[T]` Torso (95% hit - Core vital organ strikes)
  - `[R]` Right Arm (80% hit - Disarms foe, reduces attack by 60%)
  - `[L]` Left Arm (80% hit - Breaks shields and guard stance)
  - `[K]` Legs (85% hit - Forces target to crawl, pinpoints head strikes)
- **Coin Flip of Fate:** High-stakes 50/50 parry clashes against fatal enemy attacks.
- **Totem of Undying:** Sacred relic that auto-revives fallen explorers, restores HP to maximum, and regrows severed limbs.

### 5. 🗺️ Labyrinth Exploration & Guide Book
- **Dynamic Fog of War:** Player-centered visibility cone.
- **Interactive Guide Book (`[G]`):** Instant reference modal for dungeon tiles, hazards, items, and combat mechanics without cluttering map HUD.
- **Survival Bag (`[I]`):** Instant access to healing herbs, dried meat, wine flasks, and keys.

---

## 📁 Repository Structure

```text
retro_game_verilog/
├── PLAY_GAME.bat                         # Single unified click-to-play launcher
├── GIT_WORKFLOW.md                       # Team Git branching, PR & commit standards
├── UI_LAYOUT_MISTAKES_AND_POSTMORTEM_RULES.md # 10 UI bug postmortems & invariants
├── .gitignore                            # Rules ignoring build binaries and caches
├── README.md                             # Master project documentation
├── .github/
│   └── workflows/
│       └── hardware_ci.yml               # Automated GitHub Actions 5-Gate CI Pipeline
└── funger_terminal/
    ├── master_game.py                    # Unified entry point for full game experience
    ├── demo_grid_inventory.py            # Dual Split-Box showcase satchel & English pouch
    ├── demo_grid_hero_select.py          # 3-layout interactive hero drafting screen
    ├── demo_interactive_ui.py            # Diagonal combat arena & limb target engine
    ├── hero_tri_state_catalog.py         # 8 Heroes with 3 morphologies (normal/injured/dead)
    ├── monsters_catalog.py               # 36 Monsters with stats, parts, and movesets
    ├── run_comprehensive_verification.py # Master 5-Gate DO-254 / OpenTitan test runner
    ├── audit_100k_dual_mode_ultimate_suite.py # 100,000-expedition dual-mode fuzzer
    ├── audit_1m_adversarial_footsteps_suite.py# 1,000,000-step single-bit fault injection
    ├── benchmark_hw_vs_sw.py             # Hardware vs. Software (RISC-V) benchmark tool
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

## 🔬 Hardware & Logic Verification Suite

The codebase has undergone exhaustive automated auditing:
- **26/26 Hardware Test Suites:** 100% pass on Icarus Verilog RTL co-simulation (`local_test_matrix.py`).
- **100,000 Dual-Mode Expeditions:** Zero state machine crashes, zero duplicate monster encounters, mathematical proof of 3-key guarantee.
- **1,000,000 Adversarial Footsteps & Fault Injections:** Exhaustive single-bit flips, boundary walking, and memory safety audits (`audit_1m_adversarial_footsteps_suite.py`).

To run the full industrial verification pipeline:
```bash
python funger_terminal/run_comprehensive_verification.py
```

---

## 🛠️ Requirements & Environment

- **Operating System:** Windows 10 / Windows 11 (PowerShell or Command Prompt with UTF-8 / Virtual Terminal support)
- **Runtime:** Python 3.8+ (standard library only; no external pip dependencies needed)
- **Optional Hardware Simulation:** [Icarus Verilog](https://bleyer.org/icarus/) (`iverilog` & `vvp`)
