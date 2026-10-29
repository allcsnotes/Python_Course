# Exercise 19 - Dictionary and set comprehensions
prices = {"python": 1499, "sql": 999, "docker": 799, "go": 699}
names = ["Asha", "Arjun", "Priya", "Mia", "Meera"]

cheap = {c: p for c, p in prices.items() if p < 1000}
discounted = {c: p * 90 // 100 for c, p in prices.items()}
shout = {c.upper(): p for c, p in prices.items()}
inverse = {p: c for c, p in prices.items()}
lengths = {name: len(name) for name in names}
initials = {name[0] for name in names}

print("cheap:", cheap)
print("discounted:", discounted)
print("shout:", shout)
print("inverse:", inverse)
print("lengths:", lengths)
print("initials:", sorted(initials))
print("cheap total:", sum(cheap.values()))
