import bisect, time

nums = list(range(0, 2_000_000, 2))
target = 1_999_998

t0 = time.perf_counter()
i = nums.index(target)
t1 = time.perf_counter()
j = bisect.bisect_left(nums, target)
t2 = time.perf_counter()
print(i == j)
print("index", round((t1 - t0) * 1e6), "microseconds")
print("bisect", round((t2 - t1) * 1e6), "microseconds")
