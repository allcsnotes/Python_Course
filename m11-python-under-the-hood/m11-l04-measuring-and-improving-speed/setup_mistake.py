import timeit

setup = "numbers = list(range(1000))"
wrong = timeit.timeit("999 in list(range(1000))", number=2000)
right = timeit.timeit("999 in numbers", setup, number=2000)
print(f"setup inside the timing: {wrong:.4f} seconds")
print(f"setup done once before:  {right:.4f} seconds")
