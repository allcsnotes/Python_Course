# Exercise 06 - Predict the output (tuples and unpacking)
point = (3, 4)
print(point, type(point), len(point))
print(point[0], point[-1])
single = (5,)
not_a_tuple = (5)
print(type(single), type(not_a_tuple))
x, y = point
print(x + y)
a, b = 1, 2
a, b = b, a
print(a, b)
first, *middle, last = [10, 20, 30, 40, 50]
print(first, middle, last)
cheapest, *others = (499, 999, 1499)
print(cheapest, others)
empty = ()
print(type(empty), len(empty))
titles = ("Python", "SQL", "Docker")
prices = (1499, 999, 799)
for number, title in enumerate(titles, start=1):
    print(number, title)
for title, price in zip(titles, prices):
    print(title, price)
print(point == (3, 4), point == [3, 4])
