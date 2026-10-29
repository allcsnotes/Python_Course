import threading
import time


def wait():
    time.sleep(1)


start = time.perf_counter()
for _ in range(4):
    wait()
print(f"one by one:   {time.perf_counter() - start:.2f} s")

start = time.perf_counter()
workers = [threading.Thread(target=wait) for _ in range(4)]
for w in workers:
    w.start()
for w in workers:
    w.join()
print(f"four threads: {time.perf_counter() - start:.2f} s")
