"""Tests for the config loader."""

import json
from pathlib import Path

from src.config import load_config


def test_missing_keys_get_defaults(tmp_path: Path) -> None:
    path = tmp_path / "config.json"
    path.write_text("{}", encoding="utf-8")
    config = load_config(str(path))
    assert config.lives == 3
    assert config.level_max_time == 90
    assert len(config.levels) == 10
    assert config.levels[0].seed == 42


def test_comments_are_ignored(tmp_path: Path) -> None:
    path = tmp_path / "config.json"
    path.write_text('# note\n{"lives": 5}\n', encoding="utf-8")
    assert load_config(str(path)).lives == 5


def test_bad_values_are_clamped(tmp_path: Path) -> None:
    """Invalid values are pushed to the nearest valid value."""
    path = tmp_path / "config.json"
    path.write_text(
        json.dumps({"lives": 0, "level_max_time": 0, "seed": -1,
                    "unknown": True}),
        encoding="utf-8",
    )
    config = load_config(str(path))
    assert config.lives == 1
    assert config.level_max_time == 1
    assert config.seed == 0
