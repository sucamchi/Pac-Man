# Pac-Man 42: step-by-step plan

- **scamlett (presentation):** pygame (visuals, menus, HUD...) config loading,
  highscores, README, packaging.
- **lupalomi (simulation):** player movement, pacgums, level flow, ghosts, cheat mode, test suite.

Why this split: A owns everything the player sees and every file that talks to
pygame or the disk. B owns everything that advances the game state. The two sets
of files barely overlap, so merges stay small.

## Timeline at a glance

| Phase | Days | Goal | Main owner |
|---|---|---|---|
| 0. Setup | 1 | Toolchain works, interfaces agreed | Both |
| 1. Vertical slice | 2 to 4 | Maze on screen, player moves | Both |
| 2. Rules | 5 to 7 | Pacgums, score, lives, menus | Both |
| 3. Ghosts | 8 to 10 | Chase, flee, eat, respawn | B, A for visuals |
| 4. Robustness | 11 to 12 | Bad config, cheat mode, tests | Both |
| 5. Docs and packaging | 13 to 14 | README, build, upload | A, B for project docs |
| 6. Defence | 15 | Demo and recode practice | Both |


---

## Phase 0: Setup (day 1)

### 0.1 Check the machine

- Linux with a graphical session. pygame needs a display to open a window.
- Python 3.10 or later: `python3 --version`.
- `uv`: `uv --version`.

Done when: both commands print a usable version.

### 0.2 Install the Python project

From the repository root:

```bash
make install
uv run flake8 .
uv run mypy . --warn-return-any --warn-unused-ignores \
  --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs
```

The skeleton should pass both. `make install` runs `uv sync`, and `pygame` is
declared in `pyproject.toml`.

Done when: lint is clean and `.venv/` exists.

### 0.3 Check pygame

`make install` already installed it from PyPI. Confirm with:

```bash
uv run python -c "import pygame; print(pygame.version.ver)"
```

Verify with a real window, not just the import: `make run` should open the
window. `docs/PYGAME.md` has the minimum program. Both members should do this
on their own machine.

Done when: a window opens and closes cleanly.

Troubleshooting: `DISPLAY` must be set and you must be in a graphical session.
pygame bundles SDL2, so no extra system package is needed.

### 0.4 Study the assigned maze package

Read `mazegenerator/mazegenerator.py` together. It is used as-is: no edits,
no vendored copy. Key facts:

- `MazeGenerator(size=(w, h), perfect=False, entry_cell=(x, y),
  exit_cell=(x, y), seed=n)`.
- `maze` is a grid of wall bitmasks: `1` north, `2` east, `4` south, `8` west.
  A set bit means a wall is there.
- Value `15` marks both "all four walls" and the isolated cells of the `42`
  art. Treat `15` as solid, never as a corridor.
- The border is made of wall cells. Entry and exit such as `(0, 0)` sit inside
  the border. Prefer safe interior cells such as `(1, 1)` and `(w - 2, h - 2)`
  and verify them.
- `seed=0` means random. The first level must use a fixed seed (42 by
  default), later levels use random seeds.
- The package prints its own warnings. Do not let those prints become your
  error handling.

Spike, with your own eyes:

```bash
uv run python - <<'EOF'
from mazegenerator import MazeGenerator
m = MazeGenerator(size=(21, 21), perfect=False,
                  entry_cell=(1, 1), exit_cell=(19, 19), seed=42)
print(m.maze_entry, m.maze_exit, len(m.shortest_path))
for row in m.maze:
    print("".join("0123456789ABCDEF"[cell & 0xF] for cell in row))
EOF
```

Each hex digit is the cell's wall bits (`1` north, `2` east, `4` south,
`8` west). The point is to see that `perfect=False` produces loops and that
the `42` cells are blocked.

Done when: both members can explain the bitmask and have printed a maze.

### 0.5 Freeze the interfaces

Agree in writing before coding:

- Config keys and defaults (see `config.json` and the README Configuration
  section).
- Module boundaries: `config.py`, `highscore.py`, `maze.py`, `game.py`,
  `ui.py`. See the README architecture table.
- Coordinate system: grid coordinates for logic, pixels only in `ui.py`.
- Timing: `game.update(dt)` takes seconds, never frame counts.
- Naming: snake_case files, one class per module where possible.

Done when: both members can point to the file they own for each feature.

### 0.6 Start the project management evidence

Open `docs/PROJECT_MANAGEMENT.md`. Move phase 0 cards to In progress,
then to Done as they finish. Add the date on every move. This file is graded as
evidence, so update it weekly, not at the end.

---

## Phase 1: Vertical slice (days 2 to 4)

Goal: config loads, maze draws, player moves, ESC exits. No ghosts, no score.

### Member A

1. **Config loader** (`pacman/config.py`), subject V.2 and V.3.
   - Strip full-line `#` comments before parsing.
   - Merge defaults, clamp bad values, warn, continue.
   - Ignore unknown keys.
   - Never raise a traceback at the command line.
   - Write tests for: missing file, broken JSON, wrong types, negative
     numbers, too few levels.
2. **Pygame shell** (`pacman/ui.py`), subject VI.8.
   - Open one window, handle the close button and ESC, run a 60 FPS loop.
   - Convert `time.monotonic()` into a `dt` in seconds.
   - Add a scene enum: menu, playing, paused, highscores, instructions, game
     over, victory.
   - Redraw only when a dirty flag is set.
3. **Draw helpers**.
   - Text with `font.render`.
   - A board background image built once per level, then sprites on top.
   - Pixel and tile conversions in one place.

### Member B

1. **Maze adapter** (`pacman/maze.py`), subject V.4.
   - Wrap `MazeGenerator` with `perfect=False`.
   - Expose a simple grid plus entry and exit.
   - Validate width, height, and seed from the config.
   - Catch generator failures and show a clean error, not a traceback.
   - Test at least three seeds, including 42 and a random one.
2. **Level list** (`Game` or a small level builder).
   - Build the configured levels. Every level after the first gets a random
     seed.
   - Keep at least 10 levels even if the config lists fewer.
3. **Player movement** (`pacman/game.py`), subject VI.2.
   - Spawn in the middle of the maze.
   - Grid position, current direction, buffered next direction.
   - Arrow keys and WASD.
   - Wall collision using the adapter's grid.
   - Movement speed in tiles per second, not pixels per frame.

### Integration

- `pac-man.py` already parses exactly one argument and loads the config.
- Wire `Game.run()` to the UI shell.
- Both members play the slice and file bugs as Kanban cards.

Done when: the maze is visible, the player cannot cross a wall, the window
closes with ESC and the close button, and a broken config prints one clear
line.

---

## Phase 2: Game rules and menus (days 5 to 7)

### Member B

1. Pacgums on most corridor cells, never on walls or the `42` blocks.
2. Super-pacgums in the four corners of the maze, on reachable corridor cells.
3. Eating pacgums and super-pacgums, score, level clear when no pacgum is
   left.
4. Lives, death, respawn in the middle, game over at zero lives.
5. Level timer with a documented timeout rule (lose a life and restart, or
   restart the level). Pick one and write it in the README.
6. Pause state that freezes the timer and movement.

### Member A

1. HUD: score, lives, level number, remaining time (subject VI.8).
2. Main menu with Start Game, View Highscores, Instructions, Exit. Keyboard
   navigation is enough; add mouse only if time allows.
3. Highscore module (`pacman/highscore.py`), subject V.5.
   - JSON file named by the config.
   - Top 10, names up to 10 characters, alphanumeric and spaces only.
   - Non-negative integer scores.
   - Missing or corrupt file means an empty list, never a crash.
   - Save at game end, load at startup, show in the menu.
4. Name entry after win or lose, with validation feedback and a length cap.
5. Return to the main menu after saving.

Done when: the full loop works: menu, play, win or lose, name entry, saved
score visible in the menu, back to menu.

---

## Phase 3: Ghosts (days 8 to 10)

### Member B

1. Four ghosts, one starting near each corner.
2. Grid movement along corridors, with a sensible rule for reversing.
3. Chase behavior when not edible. Simple distance-based chase is enough.
   Give each ghost a small variation so they do not stack: direct chase,
   ambush one tile ahead, random turn, patrol.
4. Edible mode after a super-pacgum: flee from the player.
5. Eating an edible ghost scores points and sends it back to its corner after
   a short delay.
6. Collision rules: edible ghost is eaten, normal ghost costs a life, and the
   player is briefly invulnerable after respawning.

### Member A

1. Ghost sprites, or simple colored shapes if art is not ready.
2. Edible flashing and a visible timer.
3. Power-up feedback in the HUD.

Done when: ghosts chase, flee, can be eaten, respawn, and cost a life when
they touch the player.

---

## Phase 4: Robustness and cheat mode (days 11 to 12)

### Member A

1. Faulty config matrix, subject V.3: missing key, wrong type, null, negative,
   huge value, broken JSON, comment lines, unknown keys. Each case must warn
   and continue, or exit with one clear line.
2. Highscore fault matrix: missing file, unreadable file, invalid JSON, wrong
   shape, more than 10 entries, invalid names.
3. Document every default in the README.

### Member B

1. Cheat mode, subject VI.5. Suggested set:
   - invincibility,
   - level skip,
   - ghost freeze,
   - extra life,
   - player speed boost.
2. Make each cheat reachable by a single key, with a visible on-screen
   indicator, so a reviewer can test everything in a few minutes.
3. Error handling sweep: generator failure, missing assets, display failure.
   No traceback anywhere.

### Both

1. `pytest` suite for config, highscores, maze adapter, scoring, and name
   validation. Tests are not graded but save time at defence.
2. Manual acceptance log in the project management file with date and result.

Done when: every faulty input in the matrix behaves as documented, and cheat
mode demonstrates every feature.

---

## Phase 5: Documentation and packaging (days 13 to 14)

### Member A

1. Fill every README section. The headings are already there.
2. Keep the pygame notes and README links accurate.
3. Package the game for Linux. PyInstaller is the simplest route. The spec
   file belongs at the repository root and must include:
   - the assets,
   - the XPM assets,
   - the default config.
4. Test the packaged build on a clean machine or a fresh user account.
5. Upload an unlisted or private build to itch.io or Steam, and put the link
   in the README.

### Member B

1. Finish the project management file: planned versus actual, risks that
   happened, decisions, acceptance results.
2. Write the demo script: one pass through menu, play, cheat mode, highscores,
   packaging.
3. Clean-clone test: fresh clone, `make install`, `make run`.

### Both

1. `make lint` and fix everything reasonable.
2. Play all 10 levels once, with a short time limit, and log bugs.
3. Check the README first line and the required section list.

---

## Phase 6: Defence preparation (day 15)

- Rehearse a five minute demo, including cheat mode and a live config edit.
- Practise small recode requests, for example: change points per pacgum, add a
  cheat key, change ghost speed, add a highscore field, change the timeout
  rule.
- Each member must be able to explain every file, including the parts the
  other wrote. Swap a walkthrough.
- Know the failure paths: bad config, missing file, generator error, missing
  display.

---

## Division at a glance

| Area | Member A | Member B |
|---|---|---|
| Pygame window, drawing, scenes | Owner | Review |
| Config loading and defaults | Owner | Review |
| Highscores and name entry | Owner | Review |
| Menus, HUD, game over screens | Owner | Review |
| Maze adapter | Review | Owner |
| Player movement, collision | Review | Owner |
| Pacgums, scoring, lives, timer | Review | Owner |
| Ghosts and AI | Visuals | Owner |
| Cheat mode | Indicator | Owner |
| Tests | Config and highscores | Gameplay and maze |
| README, pygame notes | Owner | Review |
| Project management, demo | Review | Owner |
| Packaging | Owner | Clean-machine test |

Rule for conflicts: the listed owner makes the call. The other member reviews
the pull request before merge.

## Definition of done for every task

- Code passes `flake8` and the subject's `mypy` command.
- Type hints on every function.
- One-line docstring on every public class and function.
- Behaviour tested by hand, and by a test when the logic is not trivial.
- README or config docs updated if the task changes them.
- Kanban card moved to Done with the date.

## Acceptance checklist (use before submission)

- [ ] `python3 pac-man.py config.json` works, and only one argument is
      accepted.
- [ ] Missing file, broken JSON, and bad values produce clear messages and no
      traceback.
- [ ] Config accepts full-line `#` comments and ignores unknown keys.
- [ ] Mazes come from the assigned `mazegenerator`, unmodified, with
      `perfect=False`.
- [ ] Generator failure is handled cleanly.
- [ ] First level uses a fixed seed; later levels are random.
- [ ] At least 10 levels, each with a time limit, keeping score and lives.
- [ ] Player moves with arrows and WASD, cannot cross walls, respawns in the
      middle, and loses lives to ghosts.
- [ ] Four ghosts with distinct chase behavior, edible mode, flee behavior,
      and respawn.
- [ ] Pacgums and four super-pacgums, with documented points.
- [ ] Main menu, HUD, pause menu, game over screen, victory screen.
- [ ] Name entry, validation, top 10 highscores shown in the menu, stored
      persistently.
- [ ] Cheat mode helps a reviewer test everything quickly.
- [ ] Linux package runs on a clean machine, link in the README.
- [ ] README has every required section and the exact first line.
- [ ] `make install`, `run`, `debug`, `clean`, `lint` work.
- [ ] `flake8 .` and the subject's `mypy` command pass.
