import pytest

from cart import (
    Cart,
    InvalidCoupon,
    InvalidPrice,
    InvalidQuantity,
    UnknownItem,
)


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


def test_percent_coupon_takes_a_share_off(full_cart):
    full_cart.apply_coupon("SAVE10")
    assert full_cart.discount() == 250


@pytest.mark.parametrize(
    "price, expected",
    [(999, 99), (1000, 100), (5, 0)],
    ids=["rounds-down", "exact", "tiny"],
)
def test_percent_discount_rounds_down(cart, price, expected):
    cart.add("Course", price)
    cart.apply_coupon("SAVE10")
    assert cart.discount() == expected


def test_without_a_coupon_there_is_no_discount(full_cart):
    assert full_cart.discount() == 0


def test_flat_coupon_takes_a_fixed_amount(full_cart):
    full_cart.apply_coupon("FLAT200")
    assert full_cart.discount() == 200


def test_flat_coupon_needs_a_minimum_cart(cart):
    cart.add("Course", 900)
    cart.apply_coupon("FLAT200")
    assert cart.discount() == 0


def test_discount_never_goes_above_the_cart(cart):
    cart.add("Course", 300)
    cart.apply_coupon("WELCOME500")
    assert cart.discount() == 300


def test_unknown_coupon_is_refused(cart):
    with pytest.raises(InvalidCoupon, match="NOPE"):
        cart.apply_coupon("NOPE")
