import re
from collections import Counter

import lines


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
                when, level, message = lines.parse_line(line)
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
