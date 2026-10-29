total = 0
price = int(input("Course price (0 to finish): "))
while price != 0:
    total += price
    price = int(input("Course price (0 to finish): "))
print("Cart total:", total)
