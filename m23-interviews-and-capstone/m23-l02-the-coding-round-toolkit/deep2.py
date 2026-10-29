import sys
from functools import cache

sys.setrecursionlimit(20000)

@cache
def stairs(n):
    if n <= 2:
        return n
    return stairs(n - 1) + stairs(n - 2)

def stairs_loop(n):
    a, b = 1, 2
    for _ in range(n - 2):
        a, b = b, a + b
    return b

print(len(str(stairs(5000))), "digits")
print(stairs_loop(5000) == stairs(5000))
