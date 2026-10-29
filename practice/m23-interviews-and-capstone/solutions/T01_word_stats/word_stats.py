"""Task 1 - word statistics for a block of text."""
import re
from collections import Counter

STOP_WORDS = frozenset({"a", "an", "and", "the", "is", "of", "to", "in", "it", "for", "on"})

_WORD = re.compile(r"[a-z0-9']+")


def words(text: str) -> list[str]:
    """Lower-case words with punctuation removed."""
    return _WORD.findall(text.lower())


def top_words(text: str, n: int = 3, stop_words=STOP_WORDS) -> list[tuple[str, int]]:
    """The n most common words, ignoring stop words.

    Ties are broken alphabetically so the result is always the same.
    """
    if n < 0:
        raise ValueError("n must not be negative")
    counts = Counter(w for w in words(text) if w not in stop_words)
    return sorted(counts.items(), key=lambda item: (-item[1], item[0]))[:n]


def longest_word(text: str) -> str | None:
    found = words(text)
    return max(found, key=len, default=None)   # first of the longest wins
