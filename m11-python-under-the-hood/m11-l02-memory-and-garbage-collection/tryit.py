import gc
import sys
import weakref
from functools import lru_cache


class Course:
    def __init__(self, title):
        self.title = title


course = Course("Python")
team = [course]
print(sys.getrefcount(course) - 1)
gc.collect()
a = Course("A")
b = Course("B")
a.other = b
b.other = a
del a, b
print(gc.collect())


@lru_cache(maxsize=3)
def build(n):
    return [n] * 10


for n in range(10):
    build(n)
print(build.cache_info().currsize)
cache = weakref.WeakValueDictionary()
cache["py"] = course
del course
print(len(cache))
team.clear()
print(len(cache))
