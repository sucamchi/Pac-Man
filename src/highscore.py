"""Top 10 highscores stored as JSON."""


class Score:
    """One saved score entry."""

    def __init__(self, name: str, score: int) -> None:
        self.name = name
        self.score = score


class Highscores:
    """Load, add, and save the top scores in JSON."""

    def __init__(self, filename: str) -> None:
        self.filename = filename
        self.entries: list[Score] = []

    def load(self) -> None:
        """Read entries"""
        pass

    def add(self, name: str, score: int) -> None:
        """Validate and insert a new score"""
        pass

    def save(self) -> None:
        """Write entries to disk"""
        pass
