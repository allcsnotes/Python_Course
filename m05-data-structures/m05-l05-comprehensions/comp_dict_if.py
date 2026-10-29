prices = {"python": 1499, "sql": 999, "git": 499}
under = {
    title: price
    for title, price in prices.items()
    if price < 1000
}
print(under)
