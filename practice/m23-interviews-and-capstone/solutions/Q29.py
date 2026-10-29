# Q29 - Measuring before optimising
import cProfile
import pstats
import timeit

def concat(n):
    out = ""
    for i in range(n):
        out += str(i)
    return out

def join(n):
    return "".join(str(i) for i in range(n))

print(concat(1000) == join(1000))
for name, fn in (("concat", concat), ("join", join)):
    best = min(timeit.repeat(lambda: fn(20_000), number=20, repeat=5))
    print(f"{name}: best of 5 = {best:.4f}s")

profiler = cProfile.Profile()
profiler.runcall(concat, 200_000)
stats = pstats.Stats(profiler)
stats.sort_stats("cumulative")
rows = sorted(stats.stats.items(), key=lambda kv: -kv[1][3])[:1]
print("profiled calls:", stats.total_calls > 0, "| top entry:", rows[0][0][2])
