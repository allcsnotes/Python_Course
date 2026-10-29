from concurrent.futures import ProcessPoolExecutor

names = []


def add(name):
    names.append(name)
    return len(names)


if __name__ == "__main__":
    with ProcessPoolExecutor(1) as pool:
        print(list(pool.map(add, ["Asha", "Lukas", "Priya"])))
    print(names)
