from cart import Cart


def test_empty_cart_has_subtotal_zero():
    cart = Cart()
    assert cart.subtotal() == 0


def test_adding_an_item_adds_its_price():
    cart = Cart()
    cart.add("Python course", 1500)
    assert cart.subtotal() == 1500


def test_quantity_multiplies_the_price():
    cart = Cart()
    cart.add("SQL course", 500, quantity=2)
    assert cart.subtotal() == 1000


def test_adding_the_same_item_twice_adds_quantities():
    cart = Cart()
    cart.add("SQL course", 500)
    cart.add("SQL course", 500)
    assert cart.subtotal() == 1000
