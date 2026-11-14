"""File for mazegenerator implementation"""

from src.config import LevelConfig
from mazegenerator import MazeGenerator

WALL_N = 1
WALL_E = 2
WALL_S = 4
WALL_W = 8
SOLID = 15  # all four walls closed for 42 pattern.


class Maze:
    """One level maze built by mazegenerator"""

    def __init__(self, config: LevelConfig) -> None:
        self.config = config
        generator = MazeGenerator(
            size=(config.width, config.height),
            perfect=False,
            seed=config.seed
        )
        self.grid = generator.maze
        self.entry = generator.maze_entry
        self.exit = generator.maze_exit

    def is_open(self, x: int, y: int) -> bool:
        """Return True when the cell is a corridor the player can walk on."""
        return self.grid[y][x] == 0
