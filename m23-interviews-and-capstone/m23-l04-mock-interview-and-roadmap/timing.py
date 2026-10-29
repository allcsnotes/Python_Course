import random
import timeit

import streak_v1
import streak_v2


def best(func, days, repeat):
    runs = timeit.repeat(lambda: func(days), number=1, repeat=repeat)
    return min(runs)


random.seed(7)
for n in (1_000, 4_000, 16_000):
    days = random.sample(range(n * 3), n)
    t1 = best(streak_v1.longest_streak, days, 3)
    t2 = best(streak_v2.longest_streak, days, 5)
    print(f"{n:>6} days: list {t1 * 1000:8.1f} ms",
          f"| set {t2 * 1000:6.2f} ms")
