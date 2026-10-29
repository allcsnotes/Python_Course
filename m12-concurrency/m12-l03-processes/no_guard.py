from concurrent.futures import ProcessPoolExecutor


def double(x):
    return x * 2


with ProcessPoolExecutor(2) as pool:
    print(list(pool.map(double, [1, 2, 3])))
