# Gotcha 6 - plus-equals inside a tuple (the hook) (the same code as lesson one of this module)
row = (1, [2, 3])
try:
    row[1] += [4]
except TypeError as error:
    print("error:", error)
print(row)
