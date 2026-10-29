from hypothesis import example, given
from hypothesis import strategies as st

from pricing import final_price


@example(price=0, coupon="FLAT100")
@given(
    st.integers(min_value=0, max_value=100_000),
    st.sampled_from(["", "HALF", "FLAT100"]),
)
def test_price_never_negative(price, coupon):
    assert 0 <= final_price(price, coupon) <= price
