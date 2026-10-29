import time

calls = 0

def stairs(n):
    global calls
    calls += 1
    if n <= 2:
        return n
    return stairs(n - 1) + stairs(n - 2)

t0 = time.perf_counter()
print(stairs(35), calls, "calls")
print(round(time.perf_counter() - t0, 2), "seconds")
