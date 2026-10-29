import time


def average(work, times):
    start = time.perf_counter()
    for _ in range(times):
        work()
    return (time.perf_counter() - start) / times
