import re
from collections import Counter
from datetime import datetime
from enum import Enum

FORMAT = "%Y-%m-%d %H:%M:%S"


class Level(Enum):
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"


LEVELS = {item.value for item in Level}


def read_line(line):
    parts = line.rstrip().split(" ", 3)
    if len(parts) < 4:
        raise ValueError(f"need 4 parts, got {len(parts)}")
    day, clock, level, message = parts
    if level not in LEVELS:
        raise ValueError(f"unknown level {level}")
    when = datetime.strptime(f"{day} {clock}", FORMAT)
    return when, level, message


def analyse(lines, level="ERROR"):
    levels = Counter()
    kinds = Counter()
    total = bad = 0
    for line in lines:
        total += 1
        try:
            when, found, message = read_line(line)
        except ValueError:
            bad += 1
            continue
        levels[found] += 1
        if found == level:
            kinds[re.sub(r"\d+", "#", message)] += 1
    return {"total": total, "bad": bad, "levels": levels, "kinds": kinds}
