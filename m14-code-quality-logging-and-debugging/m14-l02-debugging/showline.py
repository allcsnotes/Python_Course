import sys

lines = open(sys.argv[1]).read().splitlines()
print(repr(lines[int(sys.argv[2]) - 1]))
