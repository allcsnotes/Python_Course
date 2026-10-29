import random, time
from topk import top_k
from topk_slow import top_k_sorted

random.seed(1)
N, M = 1_000_000, 200_000
words = [f"w{random.randrange(M)}" for _ in range(N)]
for f in (top_k_sorted, top_k):
    t0 = time.perf_counter()
    f(words, 10)
    print(f.__name__, round((time.perf_counter() - t0) * 1000), "ms")
