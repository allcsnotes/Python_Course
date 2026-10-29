from discounts import DISCOUNTS, final_price

DISCOUNTS["launch"] = lambda price: price * 75 // 100
print(final_price(1000, "launch"))
