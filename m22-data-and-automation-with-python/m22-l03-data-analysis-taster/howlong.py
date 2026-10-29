import time

start = time.perf_counter()
import pandas
seconds = time.perf_counter() - start
print(f"import pandas took {seconds:.2f} seconds")
