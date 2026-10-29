from hypothesis import given
from hypothesis import strategies as st


@given(st.lists(st.integers()))
def test_reversing_twice(items):
    print(items)
    assert items[::-1][::-1] == items
