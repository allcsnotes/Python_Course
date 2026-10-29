from cart import Cart

cart = Cart()
cart.add("Python course", 1500)
cart.add("SQL course", 500, quantity=2)
cart.apply_coupon("SAVE10")
print(f"subtotal {cart.subtotal():>6}")
print(f"discount {cart.discount():>6}")
print(f"tax      {cart.tax():>6}")
print(f"total    {cart.total():>6}")
