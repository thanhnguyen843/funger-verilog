# Git Workflow & Collaboration Guidelines

This document outlines the standard Git workflow for the project. All contributors must follow these guidelines to maintain code stability and prevent merge conflicts.

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
3. **Verify locally with the 5-Gate Suite before pushing.** Run `python funger_terminal/run_comprehensive_verification.py` and ensure all 5 industrial verification gates report `PASS 100%` (0 `$div`, 0 `$mod`, 0 warnings, 100% Golden Model match, 0 FSM deadlocks).
4. **Scope your work.** Avoid editing files outside your assigned module to prevent merge conflicts.
5. **Keep repository clean.** Never commit simulation output binaries (`*.out`, `*.vcd`, `*.csv`) or development rule notes (which reside in the `clone/` folder).

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
Make your RTL or testbench changes, then run the comprehensive industrial verification suite:
```bash
python funger_terminal/run_comprehensive_verification.py
```
Expected result: **5/5 GATES PASSED (100%)**.

Optionally run the interactive gameplay or full-feature checks:
```cmd
PLAY_GAME.bat
```
Do **not** commit if any gate fails, compiler warnings occur, or regressions are introduced.

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
   - **Base:** `develop` $\leftarrow$ **Compare:** `feature/<name>`
4. Add a concise title and description summarizing changes.
5. **Automated CI Execution:** GitHub Actions automatically executes `.github/workflows/hardware_ci.yml`, running `iverilog` linting, the 5-Gate verification suite, and integration testbenches.
6. Ensure the green checkmark appears (`✔ DO-254 / OpenTitan 5-Gate Hardware Verification`) before requesting review from the Team Leader.
4. Add a concise title and description summarizing changes.
5. Request review from the Team Leader.

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
**A:** Check these four criteria before opening a PR:
1. `git status` shows only clean, intended source modifications (no temporary files or simulation outputs).
2. `python funger_terminal/run_comprehensive_verification.py` completes with **ALL 5 GATES PASSED (100%)**.
3. `PLAY_GAME.bat` launches cleanly without compiler warnings or runtime errors.
4. Your branch targets `develop`, not `main`.

