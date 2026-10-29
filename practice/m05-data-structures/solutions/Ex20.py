# Exercise 20 - Know when to stop
grid = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
flat = [n for row in grid for n in row]
column_sums = [grid[0][i] + grid[1][i] + grid[2][i] for i in range(3)]
print("flat:", flat)
print("column sums:", column_sums)

messy = [n * n if n % 2 == 0 else -n for n in range(10) if n != 5 and (n % 3 != 0 or n == 0)]


def transform(n):
    if n % 2 == 0:
        return n * n
    return -n


def keep(n):
    return n != 5 and (n % 3 != 0 or n == 0)


clean = [transform(n) for n in range(10) if keep(n)]
print("messy:", messy)
print("clean:", clean)
print("same:", clean == messy)

for name in ["Asha", "Lukas", "Priya"]:
    print(name)
