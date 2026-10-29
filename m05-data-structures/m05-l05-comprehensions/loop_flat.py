table = [[1, 2, 3], [2, 4, 6], [3, 6, 9]]
flat = []
for row in table:
    for number in row:
        flat.append(number)
print(flat)
