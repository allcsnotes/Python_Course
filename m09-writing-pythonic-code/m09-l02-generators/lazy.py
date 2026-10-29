import tracemalloc


def read_lines(path):
    with open(path, encoding="utf-8") as f:
        for line in f:
            yield line


tracemalloc.start()

errors = 0
for line in read_lines("big.log"):
    if " ERROR " in line:
        errors += 1

peak = tracemalloc.get_traced_memory()[1]
megabytes = round(peak / 1_000_000, 1)
print(errors, "errors")
print(megabytes, "MB at the peak")
