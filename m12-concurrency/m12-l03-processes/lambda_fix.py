from concurrent.futures import ProcessPoolExecutor


def double(x):
    return x * 2


if __name__ == "__main__":
    with ProcessPoolExecutor(2) as pool:
        print(list(pool.map(double, [1, 2, 3])))
