row = (1, [2, 3])
try:
    row[1] += [4]
except TypeError as error:
    print("error:", error)
print(row)
