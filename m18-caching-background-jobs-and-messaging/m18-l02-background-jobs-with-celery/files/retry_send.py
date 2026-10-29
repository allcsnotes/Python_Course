import time

from retry_tasks import send_flaky

start = time.time()
result = send_flaky.delay("lukas@example.com")
print("answer:", result.get(timeout=30))
print("took", round(time.time() - start), "seconds")
