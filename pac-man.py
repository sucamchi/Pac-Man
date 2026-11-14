"""Run Pac-Man 42: python3 pac-man.py config.json."""

import sys
from src.config import ConfigError, load_config
from src.game import Game


def main() -> None:
    """Entry point. Run the game with the config file"""
    if len(sys.argv) != 2:
        sys.exit("usage: python3 pac-man.py config.json")
    try:
        Game(load_config(sys.argv[1])).run()
    except ConfigError as e:
        sys.exit(f"error in config file: {e}")
    except KeyboardInterrupt:
        sys.exit("goodbye")


if __name__ == "__main__":
    main()
