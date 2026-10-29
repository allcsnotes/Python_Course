from itertools import combinations

team = ["Lukas", "Priya", "Meera"]
for pair in combinations(team, 2):
    print(pair)
