import threading
import time
from pages import fetch


def show(n):
    print(f"course {n}: {fetch(n)}")


start = time.perf_counter()
threads = []
for n in range(1, 9):
    t = threading.Thread(target=show, args=(n,))
    t.start()
    threads.append(t)
for t in threads:
    t.join()
print(f"{time.perf_counter() - start:.2f} s")
