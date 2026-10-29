import timeit


def with_loop():
    squares = []
    for n in range(1000):
        squares.append(n * n)
    return squares


def with_comprehension():
    return [n * n for n in range(1000)]


for func in (with_loop, with_comprehension):
    runs = timeit.repeat(func, number=2000, repeat=5)
    best = min(runs) / 2000 * 1000000
    print(f"{func.__name__}: {best:.1f} microseconds")
