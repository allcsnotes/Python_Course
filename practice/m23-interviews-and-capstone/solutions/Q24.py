# Q24 - Recursion, the limit and functools.cache
import functools
import sys

calls = 0
def fib(n):
    global calls
    calls += 1
    return n if n < 2 else fib(n - 1) + fib(n - 2)

fib(20)
print("plain calls:", calls)

cached_calls = 0
@functools.cache
def fib_fast(n):
    global cached_calls
    cached_calls += 1
    return n if n < 2 else fib_fast(n - 1) + fib_fast(n - 2)

print(fib_fast(80), "cached calls:", cached_calls)
print(fib_fast.cache_info())

print("limit:", sys.getrecursionlimit())
def forever(n):
    return forever(n + 1)
try:
    forever(0)
except RecursionError as error:
    print("RecursionError:", error)
