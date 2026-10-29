prices = {"Python": 1499, "SQL": 999, "Docker": 799}
cheap = []
for course in prices:
    if prices[course] < 1000:
        cheap.append(course)
for course in cheap:
    del prices[course]
print(prices)
