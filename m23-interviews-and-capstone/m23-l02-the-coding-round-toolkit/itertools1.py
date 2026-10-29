from itertools import accumulate
from itertools import combinations, permutations

team = ["Asha", "Lukas", "Priya"]
print(list(combinations(team, 2)))
print(list(permutations(team, 2)))
print(len(list(permutations(range(8)))))
print(list(accumulate([3, 1, 4, 1, 5])))
