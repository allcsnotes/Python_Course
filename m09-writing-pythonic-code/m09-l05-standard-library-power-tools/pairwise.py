from itertools import pairwise

signups = [10, 14, 13, 20]
for before, after in pairwise(signups):
    print(after - before)
