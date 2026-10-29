import tracemalloc
from dataclasses import dataclass


@dataclass
class Plain:
    title: str
    price: int


@dataclass(slots=True)
class Slim:
    title: str
    price: int


def megabytes(kind):
    tracemalloc.start()
    items = [kind("Python", 1499) for _ in range(100000)]
    used = tracemalloc.get_traced_memory()[0]
    tracemalloc.stop()
    return used / 1_000_000


print(f"plain: {megabytes(Plain):.1f} MB")
print(f"slots: {megabytes(Slim):.1f} MB")
