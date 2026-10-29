import pickle
import time

data = list(range(5_000_000))
start = time.perf_counter()
blob = pickle.dumps(data)
took = time.perf_counter() - start
print(f"packed {len(blob) // 1_000_000} MB: {took:.2f} s")
start = time.perf_counter()
pickle.loads(blob)
took = time.perf_counter() - start
print(f"unpacked: {took:.2f} s")
start = time.perf_counter()
sum(data)
took = time.perf_counter() - start
print(f"added up: {took:.2f} s")
