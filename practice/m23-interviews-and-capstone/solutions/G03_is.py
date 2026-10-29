# Gotcha 3 - is against == (the same code as lesson one of this module)
a = int("100")
b = int("100")
c = int("1000")
d = int("1000")
print(a == b, a is b)
print(c == d, c is d)

x = [1, 2]
y = [1, 2]
print(x == y, x is y)
