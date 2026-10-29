from concurrent.futures import ProcessPoolExecutor

if __name__ == "__main__":
    with ProcessPoolExecutor(2) as pool:
        print(list(pool.map(lambda x: x * 2, [1, 2, 3])))
