from itertools import accumulate

daily = [3, 5, 2, 4]
print(list(accumulate(daily)))
print(list(accumulate(daily, max)))
