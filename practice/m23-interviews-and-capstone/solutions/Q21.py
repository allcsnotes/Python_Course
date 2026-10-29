# Q21 - sorted, sort and stability
students = [("Priya", 85), ("Lukas", 72), ("Asha", 85), ("Meera", 72)]
print(sorted(students, key=lambda s: s[1]))          # ties keep original order
print(sorted(students, key=lambda s: (-s[1], s[0])))  # score high-to-low, then name

names = ["lukas", "Asha", "priya", "Meera"]
print(sorted(names), sorted(names, key=str.lower))

result = names.sort()
print(result, names)                # .sort() changes the list and returns None
