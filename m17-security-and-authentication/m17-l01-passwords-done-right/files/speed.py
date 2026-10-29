import hashlib
import time

start = time.perf_counter()
for i in range(1_000_000):
    hashlib.sha256(f"guess{i}".encode()).hexdigest()
seconds = time.perf_counter() - start
print(f"one million guesses: {seconds:.2f} seconds")
print(f"guesses per second: {1_000_000 / seconds:,.0f}")
