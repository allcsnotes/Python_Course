# Q28 - Iterable vs iterator
lessons = ["Variables", "Loops", "Functions"]     # iterable: can give an iterator
it = iter(lessons)                                # iterator: remembers its place
print(next(it), next(it))
print(list(it))                                   # what is left
print(list(it))                                   # exhausted: empty
try:
    next(it)
except StopIteration:
    print("StopIteration")

class Countdown:
    def __init__(self, start):
        self.n = start
    def __iter__(self):
        return self
    def __next__(self):
        if self.n == 0:
            raise StopIteration
        self.n -= 1
        return self.n + 1

print(list(Countdown(3)))
print(iter(it) is it, iter(lessons) is lessons)   # iterators return themselves
