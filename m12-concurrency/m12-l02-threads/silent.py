from concurrent.futures import ThreadPoolExecutor
from pages import fetch

with ThreadPoolExecutor() as pool:
    pool.submit(fetch, 13)
print("finished, and no error was shown")
