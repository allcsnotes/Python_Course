print(divmod(17, 5))

a, b = 1, 2
a, b = b, a
print(a, b)

def show(*prices):
    print(prices)
show(1499, 999, 1999)
