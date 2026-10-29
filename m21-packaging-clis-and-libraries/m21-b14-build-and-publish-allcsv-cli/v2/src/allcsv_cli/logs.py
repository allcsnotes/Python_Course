"""Count the levels in a server log."""

from collections import Counter
from pathlib import Path


def count_levels(path: Path) -> Counter[str]:
    levels: Counter[str] = Counter()
    for line in path.read_text().splitlines():
        parts = line.split(maxsplit=3)
        if len(parts) == 4:
            levels[parts[2]] += 1
    return levels


def lines_of_level(path: Path, level: str) -> list[str]:
    lines = path.read_text().splitlines()
    return [x for x in lines if f" {level} " in x]
