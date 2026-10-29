import tracemalloc

tracemalloc.start()

with open("big.log", encoding="utf-8") as f:
    lines = f.readlines()

errors = 0
for line in lines:
    if " ERROR " in line:
        errors += 1

peak = tracemalloc.get_traced_memory()[1]
megabytes = round(peak / 1_000_000, 1)
print(errors, "errors")
print(megabytes, "MB at the peak")
