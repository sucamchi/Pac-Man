"""Configuration file loading with error handling."""

import json
import sys
from pathlib import Path
from typing import Any

LEVELS = 10
SIZE = 21


class ConfigError(Exception):
    """Raised when the config file has an error."""


class LevelConfig:
    """One level: maze size and seed. A seed of 0 is random."""

    def __init__(
        self, width: int = SIZE, height: int = SIZE, seed: int = 0
    ) -> None:
        self.width = width
        self.height = height
        self.seed = seed


def _default_levels() -> list[LevelConfig]:
    """First level fixed at seed 42, the rest random."""
    return [LevelConfig(seed=42)] + [
        LevelConfig() for _ in range(LEVELS - 1)
    ]


class Config:
    """All game settings, already validated and clamped."""

    def __init__(
        self,
        highscore_filename: str = "highscores.json",
        lives: int = 3,
        points_per_pacgum: int = 10,
        points_per_super_pacgum: int = 50,
        points_per_ghost: int = 200,
        level_max_time: int = 90,
        seed: int = 42,
        levels: list[LevelConfig] | None = None,
    ) -> None:
        self.highscore_filename = highscore_filename
        self.lives = lives
        self.points_per_pacgum = points_per_pacgum
        self.points_per_super_pacgum = points_per_super_pacgum
        self.points_per_ghost = points_per_ghost
        self.level_max_time = level_max_time
        self.seed = seed
        # None beats a list default, which every instance would share.
        self.levels = _default_levels() if levels is None else levels


def load_config(path: str) -> Config:
    """Load a JSON config file, stripping full-line # comments."""
    try:
        text = Path(path).read_text(encoding="utf-8")
    except OSError:
        raise ConfigError(f"cannot read {path}")
    text = "\n".join(
        line for line in text.splitlines()
        if not line.lstrip().startswith("#")
    )
    try:
        data = json.loads(text)
    except json.JSONDecodeError as e:
        raise ConfigError(
            f"{path}: invalid JSON at line {e.lineno}: {e.msg}"
        )
    if not isinstance(data, dict):
        raise ConfigError(f"{path}: top level must be a JSON object")
    return build(data)


def build(data: dict[str, Any]) -> Config:
    """Merge file values with defaults, warning on bad values."""
    seed = _int(data, "seed", 42, 0)
    return Config(
        highscore_filename=text(data, "highscore_filename", "highscores.json"),
        lives=_int(data, "lives", 3, 1),
        points_per_pacgum=_int(data, "points_per_pacgum", 10, 0),
        points_per_super_pacgum=_int(
            data, "points_per_super_pacgum", 50, 0
        ),
        points_per_ghost=_int(data, "points_per_ghost", 200, 0),
        level_max_time=_int(data, "level_max_time", 90, 1),
        seed=seed,
        levels=levels(data.get("levels"), seed),
    )


def levels(raw: Any, seed: int) -> list[LevelConfig]:
    """Build levels from raw data."""
    if not isinstance(raw, list):
        if raw is not None:
            warn("levels must be a list, using defaults")
        raw = []
    levels: list[LevelConfig] = []
    for number, item in enumerate(raw, start=1):
        if not isinstance(item, dict):
            warn(f"level {number} must be an object, skipped")
            continue
        levels.append(LevelConfig(
            width=_int(item, "width", SIZE, 7),
            height=_int(item, "height", SIZE, 7),
            seed=_int(item, "seed", seed if number == 1 else 0, 0),
        ))
    # Pad with random levels so the game always has at least 10.
    if not levels:
        levels.append(LevelConfig(seed=seed))
    levels += [LevelConfig() for _ in range(LEVELS - len(levels))]
    return levels


def _int(
    data: dict[str, Any], key: str, default: int, minimum: int
) -> int:
    """Get an int from data"""
    value = data.get(key, default)
    # bool is a subclass of int, but a JSON true is not a number here.
    if isinstance(value, bool) or not isinstance(value, int):
        warn(f"{key} must be an integer, using {default}")
        return default
    if value < minimum:
        warn(f"{key} must be at least {minimum}, using {minimum}")
        return minimum
    return value


def text(data: dict[str, Any], key: str, default: str) -> str:
    """Get a text value."""
    value = data.get(key, default)
    if not isinstance(value, str) or not value:
        warn(f"{key} must be a non-empty string, using {default}")
        return default
    return value


def warn(message: str) -> None:
    """Print a warning."""
    print(f"config: {message}", file=sys.stderr)
