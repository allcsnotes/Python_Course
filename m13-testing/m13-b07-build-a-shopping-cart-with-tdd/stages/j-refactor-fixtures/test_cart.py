import pytest

from cart import Cart, InvalidPrice, InvalidQuantity, UnknownItem


def test_empty_cart_has_subtotal_zero(cart):
    assert cart.subtotal() == 0


def test_adding_an_item_adds_its_price(cart):
    cart.add("Python course", 1500)
    assert cart.subtotal() == 1500


def test_quantity_multiplies_the_price(cart):
    cart.add("SQL course", 500, quantity=2)
    assert cart.subtotal() == 1000


def test_adding_the_same_item_twice_adds_quantities(cart):
    cart.add("SQL course", 500)
    cart.add("SQL course", 500)
    assert cart.subtotal() == 1000


@pytest.mark.parametrize(
    "quantity",
    [0, -1, 11],
    ids=["zero", "negative", "too-many"],
)
def test_bad_quantity_is_refused(cart, quantity):
    with pytest.raises(InvalidQuantity):
        cart.add("SQL course", 500, quantity=quantity)


def test_ten_in_total_is_the_limit(cart):
    cart.add("SQL course", 500, quantity=6)
    with pytest.raises(InvalidQuantity, match="at most 10"):
        cart.add("SQL course", 500, quantity=5)


@pytest.mark.parametrize(
    "price",
    [0, -50, 99.5],
    ids=["zero", "negative", "has-a-fraction"],
)
def test_price_must_be_whole_rupees_above_zero(cart, price):
    with pytest.raises(InvalidPrice):
        cart.add("SQL course", price)


def test_remove_takes_the_item_out(cart):
    cart.add("SQL course", 500)
    cart.remove("SQL course")
    assert cart.subtotal() == 0


def test_remove_of_an_item_not_in_the_cart(cart):
    with pytest.raises(UnknownItem, match="SQL course"):
        cart.remove("SQL course")
