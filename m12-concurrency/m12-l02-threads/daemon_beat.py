import threading
import time


def heartbeat():
    while True:
        print("still alive")
        time.sleep(0.5)


threading.Thread(target=heartbeat, daemon=True).start()
time.sleep(1.2)
print("main is done")
