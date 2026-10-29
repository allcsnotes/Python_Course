import threading

lock = threading.Lock()


def record():
    with lock:
        print("writing the record")


def update():
    with lock:
        print("got the lock")
        record()


update()
