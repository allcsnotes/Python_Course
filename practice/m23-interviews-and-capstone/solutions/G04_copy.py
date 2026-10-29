# Gotcha 4 - shallow against deep copy (the same code as lesson one of this module)
import copy

batches = [["Lukas", "Priya"], ["Asha"]]
shallow = batches.copy()
deep = copy.deepcopy(batches)
batches[0].append("Meera")
print(shallow[0])
print(deep[0])

grid = [[0] * 3] * 3
grid[0][0] = 1
print(grid)
