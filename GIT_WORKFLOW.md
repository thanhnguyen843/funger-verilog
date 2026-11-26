# Git Workflow & Collaboration Guidelines

This document outlines the standard Git workflow, RTL hygiene invariants, and verification gates for the **Fear & Hunger: Terminal Labyrinth (100% Pure Verilog Solo Explorer Edition)** repository. All contributors must follow these guidelines to maintain code stability and prevent merge conflicts.

---

## 1. Branch Strategy

| Branch | Purpose | Permissions |
| :--- | :--- | :--- |
| `main` | Production & release builds. Stable, verified code only. | **Protected**. Direct pushes forbidden. Merges only via PR from `develop`. |
| `develop` | Primary integration branch. Staging area for current sprint. | **Protected**. Direct pushes forbidden. Merges only via PR. |
| `feature/<name>` | New features or gameplay mechanics. | Created from `develop`. Pushed by author. |
| `fix/<name>` | Bug fixes or balance adjustments. | Created from `develop`. Pushed by author. |

---

## 2. Core Rules

1. **Never commit directly to `main` or `develop`.** All changes must go through a working branch and a Pull Request (PR).
2. **Always pull latest changes** from `develop` before starting work.
3. **Preserve 100% Pure Verilog Runtime & Single Launcher Discipline:**
   - Keep [`PLAY_GAME.bat`](PLAY_GAME.bat) as the **only `.bat` file** in the repository (zero Python at runtime; uses `iverilog -Wall -g2012` + `vvp sim/funger_play.out` + PowerShell raw-key/atomic frame blitter).
   - Python (`*.py` in `funger_terminal/`) must remain strictly offline verification, auditing, linting, or reference helpers.
4. **Enforce Strict RTL & Solo UI Invariants:**
   - Across all **27** `funger_terminal/src/*.v` modules and **19** `funger_terminal/tb/*.v` testbenches: `0` `$random` calls in `src/*.v`, `0` non-power-of-2 `/` or `%`, `0` hierarchical probes in RTL, and `0` `iverilog -Wall -g2012` warnings.
   - Across all Solo Explorer screens: `<= 44` visible rows x exact `100` columns, `0` mid-game `\x1b[2J` clear-screen flashes (allowed only on init/exit), `0` yellow `\033[43m` menu glare, and `0` string truncations.
5. **Verify locally before pushing.** Pass the full **7-Stage Comprehensive Verification Suite** and Solo/Audit checks (see Step 3).
6. **Scope your work & keep the repository clean.** Never commit simulation outputs (`*.out`, `*.vcd`, `*.csv`) or scratch/development rule notes (stored outside git in `clone/`).

---

## 3. Daily Development Workflow

### Step 1: Update Local Repository
Before starting any new task, switch to `develop` and sync with the remote repository:
```bash
git checkout develop
git pull origin develop
```

### Step 2: Create a Working Branch
Branch names must follow `feature/<name>` or `fix/<name>`:
```bash
# Example for a new mechanic
git checkout -b feature/chiptune-apu

# Example for a bug fix
git checkout -b fix/rebalance-stats
```

### Step 3: Implement & Verify Locally (Mandatory Quality Gates)
Make your RTL, testbench, or documentation changes, then execute the verification gates:

```bash
# 1. Master 7-Stage Hardware Verification Suite (from repo root)
#    Stages 1-7: Linter, String/ANSI Guard, Golden Trace, 100k LFSR, 50k FSM Fuzzer, Deep Logic, Chaos
python funger_terminal/run_comprehensive_verification.py

# 2. Pure Verilog Solo Explorer & Hardware Integration Suites (from funger_terminal/)
python local_test_matrix.py                  # 26 Solo Explorer & RTL suites + UI invariants
python test_matrix.py                        # 7 fast Solo & RTL CI integration suites
python audit_visual_screen_inspector.py      # 108/108 monster tri-state visual audit
python audit_5000_deep_adversarial_matrix.py # 5,000/5,000 combinatorial & adversarial matrix
```

Also verify the interactive Pure Verilog launcher compiles cleanly with `iverilog -Wall -g2012` (0 warnings) and runs `vvp sim/funger_play.out`:
```bat
PLAY_GAME.bat
```
Do **not** commit if any gate fails, `iverilog -Wall -g2012` warnings occur, or regressions are introduced.

### Step 4: Commit and Push
Commit with concise, conventional commit messages (`feat:`, `fix:`, `refactor:`, `docs:`, `ci:`):
```bash
git add .
git commit -m "feat: rebalance character vitality and integrate hardware CI/CD"
git push -u origin feature/<name>
```

### Step 5: Open a Pull Request (PR) & Automated CI Check
1. Go to the GitHub repository page.
2. Click **Compare & pull request**.
3. Set base branch:
   - **Base:** `develop` <- **Compare:** `feature/<name>`
4. Add a concise title and description summarizing changes.
5. **Automated CI Execution:** GitHub Actions automatically executes [`.github/workflows/hardware_ci.yml`](.github/workflows/hardware_ci.yml), running:
   - `python funger_terminal/run_comprehensive_verification.py` (7-Stage verification suite)
   - Strict `iverilog -Wall -g2012` + `vvp` integration runs (`tb_game_check.v`, `tb_battle_auto.v`, `tb_damage_alu.v`, `tb_play.v`)
   - `python local_test_matrix.py` (26 Solo Explorer & RTL suites)
   - `python audit_visual_screen_inspector.py` (108/108 visual render checks)
6. Ensure the green checkmark appears (`DO-254 / OpenTitan 5-Gate Hardware Verification`) before requesting review from the Team Leader.

---

## 4. Code Review & Merging

- PRs require at least **1 approval** from the team leader or designated reviewer.
- After approval, merge into `develop` using **Squash and merge** (or standard merge if requested).
- Delete the remote feature branch after merge:
  ```bash
  git branch -d feature/<name>
  ```

---

## 5. Conflict Resolution & Troubleshooting

### Handling Merge Conflicts
If your branch is behind `develop` or has conflicts:
```bash
# 1. Fetch latest changes
git checkout develop
git pull origin develop

# 2. Rebase or merge develop into your feature branch
git checkout feature/<name>
git merge develop

# 3. Resolve conflicts in files marked with conflict markers (<<<<<<<, =======, >>>>>>>)
# 4. Mark resolved and complete merge
git add <resolved-file>
git commit -m "chore: resolve merge conflicts with develop"
git push origin feature/<name>
```

### Discarding Local Uncommitted Changes
If you made unwanted local modifications and need a clean slate:
```bash
git restore .
git clean -fd
```

---

## 6. Frequently Asked Questions (FAQ)

#### Q1: Why did GitHub reject my `git push` with `protected branch hook declined`?
**A:** `main` and `develop` branches are protected by rulesets. Direct pushes are blocked. You must push your changes to a `feature/<name>` branch and open a Pull Request into `develop`.

#### Q2: I wrote code directly on `develop` without creating a branch first. How do I move it?
**A:** If you have **not** committed yet, simply create and switch to a new branch now. Git will automatically bring your uncommitted changes along:
```bash
git checkout -b feature/<new-feature-name>
git add .
git commit -m "feat: description of changes"
```

#### Q3: How do I update my existing feature branch with newer code from `develop`?
**A:** Pull the latest `develop` into your local branch before opening or updating a PR:
```bash
git checkout feature/<your-branch>
git pull origin develop
# Test the build, resolve conflicts if any, then push:
git push origin feature/<your-branch>
```

#### Q4: How do I know if my code is ready for a Pull Request?
**A:** Check these criteria before opening a PR:
1. `git status` shows only clean, intended source modifications (no temporary files, extra `.bat` launchers, or simulation binaries).
2. `python funger_terminal/run_comprehensive_verification.py` completes with all **7 Stages** passing `100%`.
3. `python local_test_matrix.py` (`26/26`), `python audit_visual_screen_inspector.py` (`108/108`), and `python audit_5000_deep_adversarial_matrix.py` (`5,000/5,000`) pass with zero warnings or UI invariant violations.
4. `PLAY_GAME.bat` compiles with `iverilog -Wall -g2012` (`0` warnings) and launches `vvp sim/funger_play.out` cleanly with zero Python at runtime.
5. Your branch targets `develop`, not `main`.
