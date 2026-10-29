import multiprocessing as mp
import os
import time
from concurrent.futures import ProcessPoolExecutor


def whoami(_):
    time.sleep(0.1)
    return os.getpid()


if __name__ == "__main__":
    mine = os.getpid()
    with ProcessPoolExecutor(4) as pool:
        ids = set(pool.map(whoami, range(8)))
    print("workers used:", len(ids))
    print("is one of them me?", mine in ids)
    print("how they start:", mp.get_start_method())
