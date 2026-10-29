import time
from functools import cache


@cache
def fib(n):
    if n < 2:
        return n
    return fib(n - 1) + fib(n - 2)


start = time.perf_counter()
print(fib(38))
print(f"{time.perf_counter() - start:.5f} seconds")
