team = ["Lukas", "Priya"]
a = list(team)
b = team.copy()
c = team[:]
a.append("Asha")
print(team)
print(a)
print(b == c, b is c)
