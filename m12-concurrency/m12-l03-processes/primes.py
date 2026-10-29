import time
from concurrent.futures import ProcessPoolExecutor

from primes_lib import count_primes

if __name__ == "__main__":
    starts = list(range(0, 1_000_000, 10_000))
    stops = [s + 10_000 for s in starts]
    begin = time.perf_counter()
    one = sum(map(count_primes, starts, stops))
    took = time.perf_counter() - begin
    print(f"one process:    {one} primes, {took:.2f} s")
    begin = time.perf_counter()
    with ProcessPoolExecutor(4) as pool:
        four = sum(pool.map(count_primes, starts, stops))
    took = time.perf_counter() - begin
    print(f"four processes: {four} primes, {took:.2f} s")
