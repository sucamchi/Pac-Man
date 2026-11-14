"""Pygame window and event loop."""

import os
from src.maze import Maze, WALL_N, WALL_E, WALL_S, WALL_W

TITLE = "Pac-Man"
WIDTH = 960
HEIGHT = 720
FPS = 60
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLUE = (40, 40, 255)


class Pygame:
    """Pygame window."""

    def run(self, maze: Maze) -> None:
        """Open the window and block until it closes."""
        os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"  # Skip pygame banner
        try:
            import pygame as pg
        except ImportError:
            raise SystemExit("error: pygame is not installed")

        pg.init()
        try:
            screen = pg.display.set_mode((WIDTH, HEIGHT))
        except pg.error:
            raise SystemExit("error: cannot open a display")
        pg.display.set_caption(TITLE)
        clock = pg.time.Clock()
        font = pg.font.Font(None, 32)
        rows = len(maze.grid)
        columns = len(maze.grid[0])
        cell_size = min((WIDTH - 48) / columns, (HEIGHT - 120) / rows)
        left = (WIDTH - columns * cell_size) / 2
        top = 96 + (HEIGHT - 120 - rows * cell_size) / 2
        wall = max(1, round(cell_size * 0.1))

        while True:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    return
                elif event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        return

            screen.fill(BLACK)
            for y, row in enumerate(maze.grid):
                for x, walls in enumerate(row):
                    x0 = round(left + x * cell_size)
                    x1 = round(left + (x + 1) * cell_size)
                    y0 = round(top + y * cell_size)
                    y1 = round(top + (y + 1) * cell_size)

                    if walls & WALL_N:
                        pg.draw.line(screen, BLUE, (x0, y0), (x1, y0), wall)
                    if walls & WALL_E:
                        pg.draw.line(screen, BLUE, (x1, y0), (x1, y1), wall)
                    if walls & WALL_S:
                        pg.draw.line(screen, BLUE, (x0, y1), (x1, y1), wall)
                    if walls & WALL_W:
                        pg.draw.line(screen, BLUE, (x0, y0), (x0, y1), wall)

            screen.blit(font.render(TITLE, True, YELLOW), (24, 24))
            pg.display.flip()
            clock.tick(FPS)
