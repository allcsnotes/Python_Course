import multiprocessing as mp

from counters import add_safe, add_unsafe


def run(target):
    counter = mp.Value("i", 0)
    procs = [mp.Process(target=target, args=(counter,))
             for _ in range(4)]
    for p in procs:
        p.start()
    for p in procs:
        p.join()
    return counter.value


if __name__ == "__main__":
    print("without a lock:", run(add_unsafe))
    print("with a lock:   ", run(add_safe))
