from cart import Cart


def test_empty_cart_has_subtotal_zero():
    cart = Cart()
    assert cart.subtotal() == 0


def test_adding_an_item_adds_its_price():
    cart = Cart()
    cart.add("Python course", 1500)
    assert cart.subtotal() == 1500
