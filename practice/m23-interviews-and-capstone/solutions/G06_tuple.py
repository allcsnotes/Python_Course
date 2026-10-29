# Gotcha 6 - plus-equals inside a tuple, step by step (the same code as lesson one of this module)
row = (1, [2, 3])
inner = row[1]
inner += [4]
print(row)
row[1] = inner
