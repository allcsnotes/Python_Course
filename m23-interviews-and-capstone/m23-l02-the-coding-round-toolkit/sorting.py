people = [("Lukas", 82), ("Priya", 95),
          ("Asha", 82), ("Meera", 95)]
print(sorted(people, key=lambda p: p[1], reverse=True))
print(sorted(people, key=lambda p: (-p[1], p[0])))
