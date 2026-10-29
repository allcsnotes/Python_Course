from collections.abc import Iterable


def count_titles(titles: Iterable[str]) -> int:
    return sum(1 for _ in titles)


print(count_titles(["Python", "SQL"]))
print(count_titles(("Python", "SQL", "Git")))
print(count_titles(t.title() for t in ["a", "b"]))
print(count_titles(42))
