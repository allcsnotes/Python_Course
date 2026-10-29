def first[T](items: list[T]) -> T:
    return items[0]


titles = ["Python", "SQL Basics"]
prices = [999, 499]
reveal_type(first(titles))
reveal_type(first(prices))
print(first(prices).upper())
