import sys
from functools import cache

@cache
def stairs(n):
    if n <= 2:
        return n
    return stairs(n - 1) + stairs(n - 2)

print(sys.getrecursionlimit())
print(len(str(stairs(500))), "digits")
print(len(str(stairs(5000))), "digits")
