"""Game state and logic"""

from src.config import Config
from src.visuals import Pygame
from src.maze import Maze


class Game:
    """Hold the running game state"""

    def __init__(self, config: Config) -> None:
        self.config = config
        self.score = 0
        self.lives = config.lives
        self.level = 0

    def run(self) -> None:
        """Open the visual window"""
        maze = Maze(self.config.levels[self.level])
        Pygame().run(maze)
