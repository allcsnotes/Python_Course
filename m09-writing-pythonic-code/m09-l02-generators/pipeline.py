from collections import Counter


def read_lines(path):
    with open(path, encoding="utf-8") as f:
        for line in f:
            yield line.rstrip()


def only_errors(lines):
    for line in lines:
        if " ERROR " in line:
            yield line


def hour_of(lines):
    for line in lines:
        yield line[11:13]


lines = read_lines("server.log")
errors = only_errors(lines)
hours = hour_of(errors)

print(Counter(hours).most_common(3))
