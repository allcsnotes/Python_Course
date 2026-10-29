import threading
import time
from pages import fetch

start = time.perf_counter()
for n in range(1, 9):
    t = threading.Thread(target=fetch, args=(n,))
    t.start()
    t.join()
print(f"{time.perf_counter() - start:.2f} s")
