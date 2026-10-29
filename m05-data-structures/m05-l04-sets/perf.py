import time
numbers_list = list(range(1000000))
numbers_set = set(numbers_list)

start = time.perf_counter()
print(999999 in numbers_list)
list_time = time.perf_counter() - start

start = time.perf_counter()
print(999999 in numbers_set)
set_time = time.perf_counter() - start
print(f"list: {list_time * 1000:.4f} ms")
print(f"set:  {set_time * 1000:.4f} ms")
