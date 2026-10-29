import pytest

from word_stats import longest_word, top_words, words


def test_words_lowercases_and_strips_punctuation():
    assert words("Hello, World! It's 2026.") == ["hello", "world", "it's", "2026"]


def test_top_words_counts_and_ignores_stop_words():
    text = "Python is fun. The fun of Python is learning Python."
    assert top_words(text, 2) == [("python", 3), ("fun", 2)]


def test_ties_are_alphabetical():
    assert top_words("y x z y x z", 3) == [("x", 2), ("y", 2), ("z", 2)]


def test_empty_text_and_zero():
    assert top_words("") == []
    assert top_words("x y", 0) == []


def test_negative_n_is_an_error():
    with pytest.raises(ValueError):
        top_words("x", -1)


def test_longest_word():
    assert longest_word("a bb ccc dd eee") == "ccc"
    assert longest_word("") is None
