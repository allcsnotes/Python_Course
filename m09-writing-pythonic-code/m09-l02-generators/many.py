def read_lines(path):
    with open(path, encoding="utf-8") as f:
        for line in f:
            yield line.rstrip()


def read_many(paths):
    for path in paths:
        yield from read_lines(path)


paths = ["monday.log", "tuesday.log"]
for line in read_many(paths):
    print(line)
