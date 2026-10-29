from hypothesis import given
from hypothesis import strategies as st

from pricing import final_price


@given(st.integers(min_value=0, max_value=100_000))
def test_flat_100_copy(price):
    assert final_price(price, "FLAT100") == price - 100
