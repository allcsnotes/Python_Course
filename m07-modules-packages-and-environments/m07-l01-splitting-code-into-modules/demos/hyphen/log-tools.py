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


if __name__ == "__main__":
    sample = "2026-03-12 14:05:09 ERROR Payment failed for order 512"
    print(parse_line(sample))
