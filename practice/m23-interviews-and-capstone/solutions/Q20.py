# Q20 - Truthiness and None
falsy = [0, 0.0, "", [], {}, set(), (), None, False]
print([bool(x) for x in falsy])

def final_price(price, discount=None):
    if not discount:                # BUG: treats 0 like "no discount given"
        discount = 10
    return price - price * discount // 100

def final_price_fixed(price, discount=None):
    if discount is None:            # only None means "not given"
        discount = 10
    return price - price * discount // 100

print(final_price(500, 0), final_price_fixed(500, 0))
print(final_price(500), final_price_fixed(500))
