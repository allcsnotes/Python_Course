prices = {"Python": 1499, "SQL": 999, "Docker": 799}
for course in prices:
    if prices[course] < 1000:
        del prices[course]
