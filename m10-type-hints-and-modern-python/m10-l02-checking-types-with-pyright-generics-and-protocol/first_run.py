def first[T](items: list[T]) -> T:
    return items[0]


titles = ["Python", "SQL Basics"]
prices = [999, 499]
print(first(titles).upper())
print(first(prices) + 1)
