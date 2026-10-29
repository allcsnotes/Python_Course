import queue
import threading
from pages import fetch

jobs = queue.Queue()
for n in range(1, 9):
    jobs.put(n)


def worker():
    name = threading.current_thread().name
    while True:
        try:
            n = jobs.get_nowait()
        except queue.Empty:
            return
        print(f"{name} took course {n}: {fetch(n)}")


team = [threading.Thread(target=worker) for _ in range(3)]
for t in team:
    t.start()
for t in team:
    t.join()
