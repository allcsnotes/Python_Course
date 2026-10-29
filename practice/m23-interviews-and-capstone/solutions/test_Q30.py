# Q30 - What makes a good test (edge cases, one behaviour per test, properties)
from hypothesis import given, strategies as st


def normalize(text):
    return " ".join(text.split())


def test_collapses_spaces():
    assert normalize("  hello   world ") == "hello world"


def test_empty_and_blank():
    assert normalize("") == ""
    assert normalize("   \t\n ") == ""


@given(st.text())
def test_idempotent(text):
    once = normalize(text)
    assert normalize(once) == once          # a property: doing it twice changes nothing


@given(st.text())
def test_no_double_spaces(text):
    assert "  " not in normalize(text)
