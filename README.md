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
├── PLAY_GAME.bat               # Single click launcher
├── .gitignore                  # Git ignore rules for simulation binaries
├── README.md                   # Project documentation
└── funger_terminal/
    ├── launch_game.py          # Windows UTF-8 streaming & input resilience handler
    ├── test_matrix.py          # Automated 7-suite verification testbench
    ├── src/                    # Verilog RTL Modules
    │   ├── character_rom.v     # 8 Character stats & archetype database
    │   ├── collision_unit.v    # Maze collision and boundary logic
    │   ├── inventory_ram.v     # Pouch RAM storage unit
    │   ├── map_rom.v           # 36x20 Labyrinth layout ROM
    │   ├── monster.v           # Monster database & scaling
    │   ├── sprite_router.v     # 24-bit TrueColor pixel art ROM router
    │   ├── terminal_ui.v       # ANSI rendering, half-block graphics, and HUDs
    │   └── *.v                 # Hero & Monster pixel sprite ROMs
    └── tb/
        └── tb_play.v           # Top-level interactive simulation testbench
```

---

## 🛠️ Requirements

- **OS:** Windows 10 / 11 (PowerShell or Command Prompt with UTF-8 / Virtual Terminal support)
- **Compiler:** [Icarus Verilog](https://bleyer.org/icarus/) (`iverilog` & `vvp`)
- **Python:** Python 3.8+ (for keyboard input streaming)
