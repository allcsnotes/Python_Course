import pytest

from cart import Cart


@pytest.fixture
def cart():
    return Cart()


@pytest.fixture
def full_cart(cart):
    cart.add("Python course", 1500)
    cart.add("SQL course", 500, quantity=2)
    return cart
