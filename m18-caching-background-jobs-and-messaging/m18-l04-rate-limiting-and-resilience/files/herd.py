import random
import threading
import time
from collections import Counter

CLIENTS = 50
times = []


def client(jitter):
    for attempt in range(4):
        delay = 0.5 * 2**attempt
        if jitter:
            delay = random.uniform(0, delay)
        time.sleep(delay)
        times.append(time.perf_counter())


def run(jitter):
    times.clear()
    start = time.perf_counter()
    crowd = [threading.Thread(target=client, args=(jitter,))
             for _ in range(CLIENTS)]
    for t in crowd:
        t.start()
    for t in crowd:
        t.join()
    busy = Counter(int((t - start) / 0.1) for t in times)
    peak = max(busy.values())
    label = "jitter" if jitter else "no jitter"
    print(f"{label:9}: busiest 0.1 s had {peak} retries")


run(False)
run(True)
