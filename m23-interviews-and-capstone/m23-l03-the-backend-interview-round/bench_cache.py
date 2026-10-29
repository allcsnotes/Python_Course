import statistics
import time

import httpx

import cache

url = "http://localhost:8233/courses/popular"
client = httpx.Client()


def avg_ms(clear, rounds=20):
    times = []
    for _ in range(rounds):
        if clear:
            cache.forget("popular")
        start = time.perf_counter()
        client.get(url)
        times.append((time.perf_counter() - start) * 1000)
    return statistics.mean(times)


print(f"without the cache: {avg_ms(True):.0f} ms")
print(f"with the cache:    {avg_ms(False):.0f} ms")
