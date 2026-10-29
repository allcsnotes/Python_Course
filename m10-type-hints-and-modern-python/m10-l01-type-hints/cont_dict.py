prices: dict[str, int] = {"C101": 499, "C102": 799}


def cheapest(prices: dict[str, int]) -> tuple[str, int]:
    code = min(prices, key=lambda c: prices[c])
    return code, prices[code]


print(cheapest(prices))
