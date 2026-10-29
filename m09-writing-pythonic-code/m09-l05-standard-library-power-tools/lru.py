from functools import lru_cache


@lru_cache(maxsize=2)
def square(n):
    print("working on", n)
    return n * n


print(square(2))
print(square(3))
print(square(2))
print(square(4))
print(square(3))
