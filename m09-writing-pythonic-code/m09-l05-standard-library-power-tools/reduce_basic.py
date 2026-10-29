from functools import reduce

prices = [499, 999, 1499]
sizes = [2, 3, 4]
print(reduce(lambda a, b: a + b, prices))
print(sum(prices))
print(reduce(lambda a, b: a * b, sizes))
