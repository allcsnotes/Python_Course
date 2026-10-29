# Exercise 07 - Priya's shopping cart
cart = 0
print("Start:", cart)

cart += 1999        # Python course
print("After Python course:", cart)

cart += 1499        # Spring Boot course
print("After Spring Boot course:", cart)

cart -= 300         # coupon
print("After coupon:", cart)

cart *= 2           # a friend buys the same cart
print("After doubling:", cart)

print("Cheapest:", min(1999, 1499, 2999))
print("Priciest:", max(1999, 1499, 2999))
print("Refund size:", abs(-250))
