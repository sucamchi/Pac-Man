*This project has been created as part of the 42 curriculum by scamlett, lupalomi.*

# Pac-Man 42

## Description

## Instructions

### Requirements

### Installation

```bash
make install
```

This runs `uv sync`, which installs `pygame` and other dependencies.

### Running

```bash
make run
```

The program takes exactly one argument, a JSON config file (see the Configuration section).


## Configuration

The config is a JSON file. Unknown keys are ignored.
Missing or invalid values are replaced with the defaults below.

| Key | Type | Default | Meaning |
|---|---|---|---|
| `highscore_filename` | string | `highscores.json` | File used to persist scores |
| `lives` | integer | `3` | Starting lives, minimum 1 |
| `points_per_pacgum` | integer | `10` | Points for a small dot, minimum 0 |
| `points_per_super_pacgum` | integer | `50` | Points for a power pellet, minimum 0 |
| `points_per_ghost` | integer | `200` | Points for an edible ghost, minimum 0 |
| `level_max_time` | integer | `90` | Level time limit in seconds, minimum 1 |
| `seed` | integer | `42` | Seed for the first level, minimum 0 |

Example: see `config.json`.

## Controls

## Highscore

## Maze Generation

## Implementation

## General Software Architecture

## Project Management

## Resources

- [42 Pac-Man subject](docs/en.subject.pdf).
- [pygame documentation](https://www.pygame.org/docs/).

### AI Usage
