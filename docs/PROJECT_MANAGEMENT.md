# Project management

This file is the project management evidence required by the subject.

Related documents:

- `plan.md`: the ordered technical plan, step by step.
- `../README.md`: the user documentation.

## 1. Team and ownership

| Member | Login | Role | Owns |
|---|---|---|---|
| Member A | `scamlett` | Presentation and data | `visuals.py`, `config.py`, `highscore.py`, README, packaging |
| Member B | `lupalomi` | Simulation | `maze.py`, `game.py`, level flow, ghosts, cheat mode, testing |

Both members review each other's pull requests and can explain the other's code.

Working agreement:

- One branch per card, named `feat/...` or `fix/...`.
- Small pull requests, reviewed by the other member before merge.
- No direct pushes to `main` after setup.

## 2. Kanban board

Columns follow the flow of a card. Keep at most three cards per person in
In progress. A card is there because work started, not because it exists.

Format: `[owner] [phase] description (started YYYY-MM-DD)`.

### Backlog

- [ ] [A] P2 Ghost sprite art and edible flashing
- [ ] [A] P2 Pause menu (resume, main menu)
- [ ] [A] P2 Game over and victory screens with name entry
- [ ] [A] P4 Faulty config test matrix
- [ ] [A] P5 PyInstaller spec and Linux build
- [ ] [A] P5 itch.io unlisted build and link
- [ ] [B] P2 Level timer and timeout rule
- [ ] [B] P3 Four ghosts with distinct chase behavior
- [ ] [B] P3 Edible mode, flee, eat, respawn
- [ ] [B] P4 Cheat mode (5 toggles, visible indicator)
- [ ] [B] P5 Acceptance test log and demo script
- [ ] [Both] P5 Clean clone install test
- [ ] [Both] P6 Recode practice and cross walkthrough

### Ready

Cards with no blockers left. Pick from the top.

- [ ] [A] P1 Config loader with comments and defaults
- [ ] [A] P1 pygame window shell, scene state, dirty flag
- [ ] [B] P1 Maze adapter around the assigned package
- [ ] [B] P1 Player grid movement and wall collision
- [ ] [B] P2 Pacgums, super-pacgums, score, lives, respawn
- [ ] [A] P2 Highscore storage and menu screen
- [ ] [A] P2 HUD (score, lives, level, time)
- [ ] [B] P4 pytest suite for config, scores, maze, scoring

### In progress

- [ ] [Both] P0 Install pygame, verify window (started YYYY-MM-DD)
- [ ] [Both] P0 Read the assigned maze package, agree interfaces
      (started YYYY-MM-DD)

### Review

A card enters Review only when it passes lint and the manual check.

- [ ] (empty)

### Done

Move finished cards here with the finish date. Do not delete them.

- [x] P0 Repository skeleton and docs (YYYY-MM-DD)

## 3. Gantt (15 working days)

Replace `Day 1` with a real date in the header row, for example
`Mon 16 Nov`. The bars show planned work, not actual. Record actuals in
section 6.

Legend: `####` = planned, `....` = buffer or part time.

| Work item | Owner | D1 | D2 | D3 | D4 | D5 | D6 | D7 | D8 | D9 | D10 | D11 | D12 | D13 | D14 | D15 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Setup, pygame install, maze spike | Both | #### | | | | | | | | | | | | | | |
| Config loader | A | | #### | #### | | | | | | | | | | | | |
| Pygame shell, scenes, draw helpers | A | | #### | #### | #### | | | | | | | | | | | |
| Maze adapter, level list | B | | #### | #### | #### | | | | | | | | | | | |
| Player movement and collision | B | | | | #### | #### | | | | | | | | | | |
| Pacgums, score, lives, timer | B | | | | | | #### | #### | | | | | | | | |
| HUD and main menu | A | | | | | | #### | #### | #### | | | | | | | |
| Highscores and name entry | A | | | | | | | #### | #### | | | | | | | |
| Ghosts, chase, edible, respawn | B | | | | | | | | #### | #### | #### | | | | | |
| Ghost visuals and power feedback | A | | | | | | | | | #### | #### | | | | | |
| Robustness and fault matrix | A | | | | | | | | | | | #### | #### | | | |
| Cheat mode and error handling | B | | | | | | | | | | | #### | #### | | | |
| Tests and manual acceptance | Both | | | | | | | | | | | | #### | #### | | |
| README and pygame docs | A | | | | | | | | | | | | | #### | #### | |
| Packaging and clean-machine test | A | | | | | | | | | | | | | | #### | |
| Project management and demo prep | B | | | | | | | | | | | | | #### | #### | #### |
| Buffer and bug fixing | Both | | | | | | | | | | | | | | .... | #### |

## Defence checklist

- Demo script rehearsed: menu, play, cheat mode, highscore, packaged build.
- Live config edit tested: change lives, points, time limit, and start again.
- Recode practice: points per pacgum, ghost speed, cheat key, timeout rule.
- Each member explains the other member's modules.
- Repository clean: no caches, no venv, no wheel, no personal paths.
- README first line exact, all required sections present.
