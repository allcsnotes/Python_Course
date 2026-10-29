import sys

squares = [n * n for n in range(1_000_000)]
lazy = (n * n for n in range(1_000_000))

print(sys.getsizeof(squares))
print(sys.getsizeof(lazy))
print(sum(squares) == sum(lazy))
