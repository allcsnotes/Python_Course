import heapq, random, time

random.seed(7)
nums = [random.random() for _ in range(1_000_000)]

t0 = time.perf_counter()
a = sorted(nums, reverse=True)[:10]
t1 = time.perf_counter()
b = heapq.nlargest(10, nums)
t2 = time.perf_counter()
print(a == b)
print("sorted", round((t1 - t0) * 1000), "ms")
print("nlargest", round((t2 - t1) * 1000), "ms")
