prices = {"Python": 1499, "SQL": 999, "Docker": 799}
total = 0
for course, price in prices.items():
    print(f"{course} costs Rs {price}")
    total += price
print(total)
