import gc


class Node:
    pass


def make_cycles(n):
    for _ in range(n):
        a = Node()
        b = Node()
        a.other = b
        b.other = a


gc.collect()
make_cycles(10000)
print(gc.collect())
