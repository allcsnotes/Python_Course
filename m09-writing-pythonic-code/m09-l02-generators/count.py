def read_lines(path):
    with open(path, encoding="utf-8") as f:
        for line in f:
            yield line.rstrip()


errors = sum(
    1
    for line in read_lines("server.log")
    if " ERROR " in line
)
print(errors)
