def read_lines(path):
    with open(path, encoding="utf-8") as f:
        for line in f:
            yield line.rstrip()


lines = read_lines("missing.log")
print("made it")
print(next(lines))
