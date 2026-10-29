import time
from pages import fetch


def show(n):
    print(f"course {n}: {fetch(n)}")


start = time.perf_counter()
for n in range(1, 9):
    show(n)
print(f"{time.perf_counter() - start:.2f} s")
