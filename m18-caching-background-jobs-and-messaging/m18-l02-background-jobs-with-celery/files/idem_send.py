import sys
import time

from idem_tasks import store, welcome_naive, welcome_safe

task = {"naive": welcome_naive, "safe": welcome_safe}[sys.argv[1]]
task.delay("lukas@example.com")
time.sleep(4)
print("outbox:", store.lrange("outbox", 0, -1))
