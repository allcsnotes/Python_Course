def read_lines(path):
    with open(path, encoding="utf-8") as f:
        for line in f:
            yield line.rstrip()


def read_many(paths):
    for path in paths:
        for line in read_lines(path):
            yield line


paths = ["monday.log", "tuesday.log"]
for line in read_many(paths):
    print(line)
