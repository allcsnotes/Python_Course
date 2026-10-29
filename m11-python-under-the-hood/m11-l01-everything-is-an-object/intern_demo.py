import sys

first = "python"
second = "".join(["p", "y", "t", "h", "o", "n"])
print(first == second)
print(first is second)
third = sys.intern(second)
print(first is third)
