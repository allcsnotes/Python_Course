from functools import reduce

print(reduce(lambda a, b: a + b, [], 0))
print(reduce(lambda a, b: a + b, []))
