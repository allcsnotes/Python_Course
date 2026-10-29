from itertools import count, islice

ids = count(101)
print(list(islice(ids, 3)))
print(list(islice(ids, 3)))
print(list(islice("ABCDEFG", 2, 5)))
