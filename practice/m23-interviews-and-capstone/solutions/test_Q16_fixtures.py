# Q16 (fixtures) - Fixtures and parametrize
import pytest


def final_price(price, percent):
    if not 0 <= percent <= 100:
        raise ValueError("percent must be 0..100")
    return price - price * percent // 100


@pytest.fixture
def catalogue():
    # built fresh for every test that asks for it
    return {"Python": 499, "SQL": 399}


@pytest.mark.parametrize(
    "price, percent, expected",
    [(500, 0, 500), (500, 10, 450), (500, 100, 0), (399, 50, 200)],
)
def test_final_price(price, percent, expected):
    assert final_price(price, percent) == expected


@pytest.mark.parametrize("percent", [-1, 101])
def test_bad_percent(percent):
    with pytest.raises(ValueError, match="0..100"):
        final_price(500, percent)


def test_fixture_is_fresh(catalogue):
    catalogue["Rust"] = 999
    assert len(catalogue) == 3


def test_fixture_is_fresh_again(catalogue):
    assert len(catalogue) == 2      # the Rust course from the test above is gone
