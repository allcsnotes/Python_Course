# Gotcha 2 - late binding in closures (the same code as lesson one of this module)
names = ["Lukas", "Priya", "Meera"]

late = []
for name in names:
    late.append(lambda: "Hello, " + name)

fixed = []
for name in names:
    fixed.append(lambda name=name: "Hello, " + name)

print([f() for f in late])
print([f() for f in fixed])
