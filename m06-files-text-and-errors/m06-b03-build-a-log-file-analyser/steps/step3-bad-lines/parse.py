from datetime import datetime

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


samples = [
    "2026-03-12 14:05:09 ERROR Database connection timeout",
    "",
    "2026-03-12 09:30",
    "2026-03-12 25:61:07 INFO GET /courses 200 31ms",
    "#### log rotated ####",
    "2026-03-12 20:02:37 ERORR Disk full",
]
bad = 0
for line in samples:
    try:
        when, level, message = parse_line(line)
    except ValueError as err:
        bad += 1
        print("skip:", err)
    else:
        print("ok:", when.hour, level)
print(bad, "bad lines")
