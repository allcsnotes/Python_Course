import threading

total = 0


def add_many():
    global total
    for _ in range(1_000_000):
        total += 1


workers = [threading.Thread(target=add_many) for _ in range(4)]
for w in workers:
    w.start()
for w in workers:
    w.join()
print("expected 4000000, got", total)
