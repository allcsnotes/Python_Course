# Q19 - Mutable and immutable
name = "Asha"
before = id(name)
name += " Rao"                      # builds a NEW string
print(name, id(name) == before)

team = ["Lukas", "Priya"]
before = id(team)
team += ["Meera"]                   # changes the SAME list
print(team, id(team) == before)

point = (3, 4)
try:
    point[0] = 9
except TypeError as error:
    print("TypeError:", error)

# an immutable tuple can still hold a mutable list
pair = ("Asha", ["python"])
pair[1].append("sql")
print(pair)
