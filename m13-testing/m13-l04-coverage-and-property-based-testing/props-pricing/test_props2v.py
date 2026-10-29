from hypothesis import Verbosity, given, settings
from hypothesis import strategies as st

from pricing import final_price


@settings(verbosity=Verbosity.verbose)
@given(
    st.integers(min_value=0, max_value=100_000),
    st.sampled_from(["", "HALF", "FLAT100"]),
)
def test_price_never_negative(price, coupon):
    assert 0 <= final_price(price, coupon) <= price
