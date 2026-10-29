prices = [1499, 999, 1999, 499, 2499]
off = [price - 100 for price in prices]
above = [price for price in prices if price > 1000]
titles = ["python", "sql", "git"]
sizes = {title: len(title) for title in titles}
print(off)
print(above)
print(sizes)
