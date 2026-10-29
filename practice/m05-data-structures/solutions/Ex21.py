# Exercise 21 - Predict the output (two names, one list?)
a = [1, 2, 3]
b = a
b.append(4)
print(a, b)
print(a is b, a == b)
c = a.copy()
c.append(5)
print(a, c)
print(a is c, a == c[:4])
d = a[:]
d[0] = 99
print(a, d)
x = 10
y = x
y += 1
print(x, y)
s = "abc"
t = s.upper()
print(s, t)
e = [1]
f = e
f = f + [2]
print(e, f)
g = (1, [2])
g[1].append(3)
print(g)
