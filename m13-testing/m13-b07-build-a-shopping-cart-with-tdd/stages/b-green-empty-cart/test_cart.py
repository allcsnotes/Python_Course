from cart import Cart


def test_empty_cart_has_subtotal_zero():
    cart = Cart()
    assert cart.subtotal() == 0
