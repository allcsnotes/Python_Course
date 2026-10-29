# Exercise 14 - Predict the output (sets)
a = {1, 2, 3, 3, 2}
print(a, len(a))
b = {3, 4, 5}
print(a | b, a & b, a - b, b - a, a ^ b)
print(a.union(b), a.intersection(b), a.difference(b), a.symmetric_difference(b))
print(2 in a, 9 in a, 9 not in a)
a.add(10)
a.add(1)
print(sorted(a))
a.discard(99)
a.remove(10)
print(sorted(a))
print(type({}), type(set()), type({1}))
log = ["Lukas", "Priya", "Lukas", "Asha", "Priya"]
print(len(log), len(set(log)), sorted(set(log)))
print(len(set([1, 1, 1, 2])))
print(sorted({"Mia", "Chen"} | {"Sofia"}))
