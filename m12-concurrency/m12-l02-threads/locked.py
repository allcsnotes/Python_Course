import threading
import time

total = 0
lock = threading.Lock()


def add_many(count):
    global total
    for _ in range(count):
        with lock:
            current = total
            time.sleep(0)
            total = current + 1


threads = [threading.Thread(target=add_many, args=(50_000,))
           for _ in range(4)]
for t in threads:
    t.start()
for t in threads:
    t.join()
print("expected 200000, got", total)
