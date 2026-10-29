from bfs import shortest

grid = ["S..#....",
        ".#.#.##.",
        ".#...#..",
        ".####.#.",
        "......#G"]
print(shortest(grid, (0, 0), (4, 7)))
print(shortest(grid, (0, 0), (0, 0)))
print(shortest(["S#G"], (0, 0), (0, 2)))
