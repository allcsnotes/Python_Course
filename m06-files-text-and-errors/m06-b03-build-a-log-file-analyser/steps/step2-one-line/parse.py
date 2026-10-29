from datetime import datetime

FORMAT = "%Y-%m-%d %H:%M:%S"


def parse_line(line):
    day, clock, level, message = line.rstrip().split(" ", 3)
    when = datetime.strptime(f"{day} {clock}", FORMAT)
    return when, level, message


line = "2026-03-12 14:05:09 ERROR Database connection timeout"
when, level, message = parse_line(line)
print(when)
print(when.hour, level)
print(message)
