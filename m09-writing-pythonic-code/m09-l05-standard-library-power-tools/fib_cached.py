from functools import cache

calls = 0


@cache
def fib(n):
    global calls
    calls += 1
    if n < 2:
        return n
    return fib(n - 1) + fib(n - 2)


print(fib(20))
print(calls)
print(fib.cache_info())
