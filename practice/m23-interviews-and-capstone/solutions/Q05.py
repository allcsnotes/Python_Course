# Q05 - Reference counting and the cycle collector
import gc
import sys
import weakref

class Box:
    pass

box = Box()
print(sys.getrefcount(box) - 1)     # minus the temporary reference of the call
other = box
print(sys.getrefcount(box) - 1)
del other
print(sys.getrefcount(box) - 1)

alive = weakref.ref(box)
del box                             # count hits 0: freed at once
print("alive after del:", alive() is not None)

a, b = Box(), Box()
a.other, b.other = b, a             # a cycle: counts can never reach 0
probe = weakref.ref(a)
del a, b
print("alive after del (cycle):", probe() is not None)
gc.collect()
print("alive after gc.collect():", probe() is not None)
