prices = {"python": 1499, "sql": 999, "git": 499}
sale = {
    title: price - 200
    for title, price in prices.items()
}
print(sale)
