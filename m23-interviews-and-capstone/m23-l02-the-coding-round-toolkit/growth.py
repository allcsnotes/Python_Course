import time

def slow(nums):
    for i in range(len(nums)):
        for j in range(i + 1, len(nums)):
            if nums[i] == nums[j]:
                return True
    return False

def fast(nums):
    return len(set(nums)) != len(nums)

def best(f, nums):
    times = []
    for _ in range(3):
        t0 = time.perf_counter()
        f(nums)
        times.append(time.perf_counter() - t0)
    return min(times) * 1000

for n in (1000, 2000, 4000):
    nums = list(range(n))
    print(n, round(best(slow, nums), 1), round(best(fast, nums), 3))
