import time
from concurrent.futures import ProcessPoolExecutor


def square(x):
    return x * x


if __name__ == "__main__":
    numbers = range(20_000)
    start = time.perf_counter()
    [square(x) for x in numbers]
    print(f"one by one:    {time.perf_counter() - start:.3f} s")
    start = time.perf_counter()
    with ProcessPoolExecutor(4) as pool:
        list(pool.map(square, numbers))
    print(f"4 processes:   {time.perf_counter() - start:.3f} s")
    start = time.perf_counter()
    with ProcessPoolExecutor(4) as pool:
        list(pool.map(square, numbers, chunksize=2_500))
    print(f"in big chunks: {time.perf_counter() - start:.3f} s")
