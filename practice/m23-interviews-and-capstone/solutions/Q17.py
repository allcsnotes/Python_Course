# Q17 - A race condition and a Lock
import threading
import time

balance = 0
lock = threading.Lock()

def deposit_unsafe():
    global balance
    current = balance               # read
    time.sleep(0)                   # another thread may run here
    balance = current + 1           # write: may overwrite someone else's update

def deposit_safe():
    global balance
    with lock:                      # only one thread inside at a time
        current = balance
        time.sleep(0)
        balance = current + 1

def run(worker):
    global balance
    balance = 0
    threads = [threading.Thread(target=worker) for _ in range(200)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    return balance

print("unsafe, expected 200:", run(deposit_unsafe))
print("safe,   expected 200:", run(deposit_safe))
