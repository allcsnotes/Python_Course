from datetime import datetime

FORMAT = "%Y-%m-%d %H:%M:%S"


def parse_line(line):
    day, clock, level, message = line.rstrip().split(" ", 3)
    when = datetime.strptime(f"{day} {clock}", FORMAT)
    return when, level, message


print(parse_line("2026-03-12 09:30"))
