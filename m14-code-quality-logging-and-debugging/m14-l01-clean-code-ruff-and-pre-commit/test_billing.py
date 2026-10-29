import pytest

from billing import calc


@pytest.mark.parametrize(
    ("items", "coupon", "expected"),
    [
        ([("Python", 999, 1)], None, 1179),
        ([("Python", 999, 2)], "SAVE10", 2122),
        ([("SQL", 500, 2)], "FLAT200", 944),
    ],
)
def test_calc(items, coupon, expected):
    assert calc(items, coupon) == expected
