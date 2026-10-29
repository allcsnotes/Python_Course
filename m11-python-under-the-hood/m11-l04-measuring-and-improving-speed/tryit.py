import timeit

words = [f"word{i}" for i in range(1000)]
as_set = set(words)
for name, group in (("list", words), ("set", as_set)):
    runs = timeit.repeat(lambda: "word999" in group, number=2000, repeat=3)
    print(f"{name}: {min(runs):.4f} seconds")


def with_loop():
    total = 0
    for n in range(1000):
        total += n
    return total


for func in (with_loop, lambda: sum(range(1000))):
    runs = timeit.repeat(func, number=2000, repeat=3)
    print(f"{min(runs) / 2000 * 1000000:.1f} microseconds")
