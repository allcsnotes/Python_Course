import multiprocessing as mp


def worker(name, queue):
    queue.put((name, len(name)))


if __name__ == "__main__":
    queue = mp.Queue()
    people = ["Asha", "Lukas", "Priya", "Meera"]
    procs = [mp.Process(target=worker, args=(p, queue))
             for p in people]
    for p in procs:
        p.start()
    results = sorted(queue.get() for _ in procs)
    for p in procs:
        p.join()
    print(results)
