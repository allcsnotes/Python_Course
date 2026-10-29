import re
from collections import Counter
from datetime import datetime
from pathlib import Path

LOG_FILE = Path("server.log")
FORMAT = "%Y-%m-%d %H:%M:%S"
LEVELS = {"INFO", "WARNING", "ERROR"}


def parse_line(line):
    parts = line.rstrip().split(" ", 3)
    if len(parts) < 4:
        raise ValueError(f"need 4 parts, got {len(parts)}")
    day, clock, level, message = parts
    if level not in LEVELS:
        raise ValueError(f"unknown level {level}")
    when = datetime.strptime(f"{day} {clock}", FORMAT)
    return when, level, message


def analyse(path):
    levels = Counter()
    errors_by_hour = Counter()
    kinds = Counter()
    bad = []
    total = 0
    with path.open(encoding="utf-8") as f:
        for number, line in enumerate(f, start=1):
            total += 1
            try:
                when, level, message = parse_line(line)
            except ValueError as err:
                bad.append((number, str(err)))
                continue
            levels[level] += 1
            if level == "ERROR":
                errors_by_hour[when.hour] += 1
                kind = re.sub(r"\d+", "#", message)
                kinds[kind] += 1
    return {
        "total": total,
        "bad": bad,
        "levels": levels,
        "errors_by_hour": errors_by_hour,
        "kinds": kinds,
    }


result = analyse(LOG_FILE)
print(result["total"], len(result["bad"]))
print(result["levels"])
print(result["errors_by_hour"].most_common(3))
print(result["kinds"].most_common(2))
