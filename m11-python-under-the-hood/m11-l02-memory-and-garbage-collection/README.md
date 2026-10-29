# M11-L02 · Memory and Garbage Collection

> Video: Module 11, Lesson 2. Watch it first, then follow along here.

## What you'll learn

- What a reference count is, and what counts as a pointer to an object
- Why `del` removes a label, not the object, and when an object is freed
- How objects that point at each other (cycles) are cleaned by the garbage collector (`gc`)
- What a memory leak is, how to find it with `tracemalloc`, and how a limit (`lru_cache`) fixes it
- Weak references: a pointer that does not keep an object alive

## Before you start

- Python 3.14 or newer. Check with `python --version`.
- No Docker needed.
- [M11-L01 · Everything Is an Object](../m11-l01-everything-is-an-object/README.md), and the `lru_cache` from [M09-L05](../../m09-writing-pythonic-code/m09-l05-standard-library-power-tools/README.md).
- Memory sizes and counts depend on your Python build and computer. The numbers in this README are from one real run; yours will differ a little. Read the shape of the numbers, not the exact digits.

## Files in this folder

| File | What it is |
|------|------------|
| `doorbell.py` | The hook: when does `freed Python` appear? |
| `refcount.py` | Reading the reference count with `sys.getrefcount` |
| `scopes.py` | Pointers vanish without `del`: end of a function, moving a label |
| `cycle.py` | Two courses pointing at each other |
| `cycles_on.py` | Ten thousand cycles, collector on |
| `cycles_off.py` | The same with the collector off |
| `gcinfo.py` | Is the collector on? What are its thresholds? |
| `leak.py` | A report cache that only grows, with a memory meter |
| `leak_where.py` | Finding the leaking line with `tracemalloc` |
| `leak_fixed.py` | The fix: `lru_cache(maxsize=100)` |
| `weak_ref.py` | A weak reference does not keep the object alive |
| `weak_cache.py` | `WeakValueDictionary` against a normal dictionary |
| `del_error.py` | Pitfall 1: an error inside `__del__` |
| `none_count.py` | Pitfall 2: the reference count of `None` |
| `weak_list.py` | Pitfall 3: a weak reference to a list |
| `tryit.py` | A model answer to the Try it yourself tasks |

## Follow along

### 1. The hook: where does `freed` appear?

Asha wants to see how Python cleans up. She writes a class `Course` whose `__del__` method prints `freed`. Python calls `__del__` at the moment it throws a course away. We use it only as a doorbell. She makes one course, sticks two labels on it (`a` and `b`), deletes `a`, prints a message, deletes `b`, prints another. Where will the word `freed` appear? Guess.

```python
class Course:
    def __init__(self, title):
        self.title = title

    def __del__(self):
        print("freed", self.title)


a = Course("Python")
b = a
del a
print("after del a")
del b
print("after del b")
```

```bash
python doorbell.py
```

```
after del a
freed Python
after del b
```

Deleting `a` freed nothing. The course was thrown away only when its last label was gone, and at that very moment. But that is not the whole story: some objects are never thrown away this way. By the end of this lesson you will see why.

### 2. Reference counting: the meeting-room counter

Think of a meeting room in an office. People book it: one booking, then two, then three. On the door hangs a counter showing how many bookings the room has right now. When someone cancels, the counter goes down. The moment it shows zero, nobody needs the room any more: the cleaners come, empty it, and it is free for the next meeting.

Python does the same. The room is an object kept in memory. A booking is anything that points at the object: a label, an item in a list, a value in a dictionary. The counter is the **reference count**. When the count drops to zero, Python frees the object at once (gives its memory back so something else can use it). This is **reference counting**, and it cleans up almost everything.

Watch a real counter. `sys.getrefcount` tells us how many pointers an object has. We make a course with label `a`, then add a second label `b`, then put it in a list `team`, then `del b`. With only one label on the course, what will the first number be? Guess all four.

```python
import sys


class Course:
    pass


a = Course()
print(sys.getrefcount(a))
b = a
print(sys.getrefcount(a))
team = [a]
print(sys.getrefcount(a))
del b
print(sys.getrefcount(a))
```

```bash
python refcount.py
```

```
2
3
4
3
```

One label, and the answer says 2. Is Python wrong? No. To count, the function has to hold the course for a moment, so its own argument is one extra, temporary pointer. The number is always one more than the pointers you made. Subtract one and read the story: `a` is one pointer; `b` makes two; the list `team` holds the course too (an item in a list is a pointer) so three; `del b` lets go of one, back to two.

So what counts as a pointer? A label, an item in a list, a value in a dictionary, an attribute of another object, and an argument while the function runs. Every one of them keeps the object alive.

### 3. The hook in slow motion

Python builds the course; the label `a` is stuck on it: count 1. `b = a`: count 2. `del a` removes the label and the count falls to 1: the course is still alive, so the doorbell stays silent. `del b`: the count falls to zero, and at that very instant Python rings the doorbell (`__del__`) and `freed Python` appears; then the memory is released. So `del` does not delete an object, it removes one pointer. Python deletes the object itself when nobody points to it any more.

Pointers also vanish without `del`. In this file `make` creates a temporary course. After calling it we make a course with label `x`, then move `x` onto a second course, then delete `x`. In what order do the messages and the `freed` words appear?

```python
class Course:
    def __init__(self, title):
        self.title = title

    def __del__(self):
        print("freed", self.title)


def make():
    temp = Course("Temp")
    print("made", temp.title)


make()
print("after the call")
x = Course("Python")
x = Course("SQL")
print("moved the label")
del x
print("done")
```

```bash
python scopes.py
```

```
made Temp
freed Temp
after the call
freed Python
moved the label
freed SQL
done
```

`freed Temp` appears before the message after the call: when the function ended, its label `temp` vanished and the count hit zero. `freed Python` appears when `x` moves onto SQL, because the first course lost its last label. So in everyday code you almost never write `del`. Labels disappear by themselves: when a function ends, when a label moves, when a list is emptied. And in the Python you installed, the object is freed right then, not later.

### 4. Cycles and the garbage collector

Now a strange office: room 1 is booked only by room 2, room 2 only by room 1. Nobody else has a booking. Both counters show 1, so neither room is ever cleaned, yet nobody in the company can reach them. For that case Python has a second helper: the **garbage collector**, an inspector who starts at the places people really use, follows every booking, and notices the rooms nobody can reach.

In code: two courses `x` and `y`; `x.partner` points at `y` and `y.partner` points back at `x`. We delete both labels. `gc.collect()` (from the `gc` module that ships with Python) means "inspector, do a round now" and returns how many unreachable objects it found. The first `collect` near the top only tidies leftovers. After both labels are deleted, does `freed` appear right away, later, or never? Guess.

```python
import gc


class Course:
    def __init__(self, title):
        self.title = title

    def __del__(self):
        print("freed", self.title)


gc.collect()
x = Course("Python")
y = Course("SQL")
x.partner = y
y.partner = x
del x
del y
print("both labels deleted")
print("collecting")
print(gc.collect())
```

```bash
python cycle.py
```

```
both labels deleted
collecting
freed Python
freed SQL
2
```

Deleting the labels freed nothing, because each course still had one pointer, from the other. The inspector found the two and freed them. The collector ignores counts: it starts from the names your program really uses, follows every arrow and marks everything it reaches; anything unmarked is garbage.

Do you have to call `collect` yourself? `make_cycles` builds ten thousand pairs of nodes pointing at each other (twenty thousand objects) and drops them all, then asks `collect` how many it finds. First with the collector on:

```python
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
```

```bash
python cycles_on.py
```

```
2026
```

Then with the collector switched off first:

```python
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
gc.disable()
make_cycles(10000)
print(gc.collect())
```

```bash
python cycles_off.py
```

```
20000
```

With the collector on, most of the cycles were already cleaned in the background before our own `collect`; with it off, our `collect` found exactly 20,000. (The first number can differ a little on your computer.) How does it decide when to run?

```python
import gc

print(gc.isenabled())
print(gc.get_threshold())
```

```bash
python gcinfo.py
```

```
True
(2000, 10, 10)
```

The collector is enabled, and its thresholds are 2000, 10, 10: roughly, "when about 2000 more objects have been created than freed, take a look". Only objects that can hold other objects can be part of a cycle (lists, dictionaries, your own classes). Numbers and text cannot, so the collector ignores them. The rule: leave the collector switched on and do not call `collect` in everyday code. Reference counting does the daily cleaning and the collector catches the cycles.

### 5. A memory leak, found with `tracemalloc`

The problem people really meet: Asha's server answers requests all day. At first it works, but after some days its memory keeps growing until the machine runs out and the server is killed. That is a **memory leak**. But Python cleans up automatically, so how can it leak? Counting and collecting free only objects that nobody points to. A leak is an object that something still points to for no good reason. Python cannot guess that you will never need it again.

The classic leak is a cache that only grows. `report_cache` is a dictionary at the top of the file. `build_report` makes a list of 1000 items, saves it in the cache under the request number and returns its length. A memory meter prints the memory in use after every 1000 requests. Flat or growing? Guess.

```python
import tracemalloc

report_cache = {}


def build_report(request_id):
    report = [request_id] * 1000
    report_cache[request_id] = report
    return len(report)


tracemalloc.start()
for request_id in range(1, 3001):
    build_report(request_id)
    if request_id % 1000 == 0:
        used, peak = tracemalloc.get_traced_memory()
        print(request_id, round(used / 1_000_000, 1), "MB")
```

```bash
python leak.py
```

```
1000 8.1 MB
2000 16.2 MB
3000 24.4 MB
```

A straight line up: about 8 MB for every thousand requests. A million requests would need about 8 GB. Where is the leak? `tracemalloc` can point at the line: `take_snapshot()` takes a photo of memory and `statistics("lineno")` sorts the lines by how much memory they created, biggest first:

```python
import tracemalloc

report_cache = {}


def build_report(request_id):
    report = [request_id] * 1000
    report_cache[request_id] = report
    return len(report)


tracemalloc.start()
for request_id in range(1, 3001):
    build_report(request_id)
snapshot = tracemalloc.take_snapshot()
top = snapshot.statistics("lineno")[0]
print("line", top.traceback[0].lineno)
print(round(top.size / 1_000_000, 1), "MB")
```

```bash
python leak_where.py
```

```
line 7
24.2 MB
```

The line that builds each report. The question to ask next is: who still points at those lists? Here the answer is the report cache, which never lets go. The fix is a limit. In module 9 you met the LRU cache: with `maxsize=100` it keeps only the hundred most recently used answers and throws the rest away. Same loop, same meter:

```python
import tracemalloc
from functools import lru_cache


@lru_cache(maxsize=100)
def build_report(request_id):
    return [request_id] * 1000


tracemalloc.start()
for request_id in range(1, 3001):
    build_report(request_id)
    if request_id % 1000 == 0:
        used, peak = tracemalloc.get_traced_memory()
        print(request_id, round(used / 1_000_000, 1), "MB")
```

```bash
python leak_fixed.py
```

```
1000 0.8 MB
2000 0.8 MB
3000 0.8 MB
```

Flat: the old reports are freed as the cache lets go of them. Other classic leaks look the same: a global list that you only append to, a cache with no limit, a log of every request kept in memory, and callbacks you register and never remove. The pattern is always: something keeps a pointer for ever.

### 6. Weak references: a pointer that does not count

Sometimes you want a cache that helps while an object is in use but never keeps it alive by itself. Think of a sticky note on your desk saying "ask Meera about the course": the note does not make Meera stay in the office. The `weakref` module makes one. `weakref.ref(course)` gives a weak reference; calling it with round brackets gives the object back if it is still alive. We print the title, delete the course label, and call the reference again:

```python
import weakref


class Course:
    def __init__(self, title):
        self.title = title


course = Course("Python")
ref = weakref.ref(course)
print(ref().title)
del course
print(ref())
```

```bash
python weak_ref.py
```

```
Python
None
```

The weak reference pointed at the course without adding to the count, so when the last real label went the course was freed and the weak reference answers `None`.

A cache would use a `WeakValueDictionary`: a dictionary whose values are held by weak references. Here are a normal dictionary `strong` and a weak one. The Python course goes into the strong one and the SQL course into the weak one, then both labels are deleted:

```python
import weakref


class Course:
    def __init__(self, title):
        self.title = title


strong = {}
weak = weakref.WeakValueDictionary()
python = Course("Python")
sql = Course("SQL")
strong["py"] = python
weak["sql"] = sql
del python
del sql
print(len(strong), len(weak))
print(strong["py"].title)
print(weak.get("sql"))
```

```bash
python weak_cache.py
```

```
1 0
Python
None
```

The strong dictionary kept Python alive, so its entry is still there. The weak dictionary lost its entry on its own, the moment the SQL course was freed, and `get` gives `None`. That is the use: a cache of objects that someone else owns. While any real label holds an object the cache can hand it out; when nobody does, the entry disappears by itself, so the cache can never leak.

### 7. Four pitfalls

**1. Trusting `__del__`.** What if it breaks? Here it raises a `ValueError`. We make a course, delete it and print `done`.

```python
class Course:
    def __del__(self):
        raise ValueError("oops")


c = Course()
del c
print("done")
```

```bash
python del_error.py
```

```
Exception ignored while calling deallocator <function Course.__del__ at 0x104a371c0>:
Traceback (most recent call last):
  File "del_error.py", line 3, in __del__
    raise ValueError("oops")
ValueError: oops
done
```

Python prints `Exception ignored while calling deallocator` with the traceback, then the program carries on and prints `done`. The error was swallowed. Also, exactly when `__del__` runs can differ between Python versions and builds. Use it for a doorbell in a lesson, never for something that must happen (use a context manager, module 9).

**2. The count of an object that never dies.** Print the reference count of `None`:

```python
import sys

print(sys.getrefcount(None))
```

```bash
python none_count.py
```

```
3221225472
```

A huge number (about three billion). `None`, `True` and small numbers are *immortal* in modern Python: they are never freed, so Python marks them with a giant count. (The exact number can differ by build.)

**3. A weak reference to a list.**

```python
import weakref

ref = weakref.ref([1, 2, 3])
```

```bash
python weak_list.py
```

```
Traceback (most recent call last):
  File "weak_list.py", line 3, in <module>
    ref = weakref.ref([1, 2, 3])
TypeError: cannot create weak reference to 'list' object
```

`TypeError: cannot create weak reference to 'list' object`. Plain lists, dictionaries, numbers and text cannot have weak references; instances of your own classes can. Wrap the data in a small class.

**4. Calling `collect` to fix a leak** (no code). A leak is an object that something still points to. The collector only removes objects that nobody can reach, so it cannot free it. Find the pointer instead.

### 8. Try it yourself: model answer

Make a class, put one object in a list and print its reference count minus one. Make two objects point at each other, delete them and free them with `collect`. Cache build results with a max size and read the cache info. Make a weak reference and watch it turn into `None`. One answer:

```python
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
```

```bash
python tryit.py
```

```
2
2
3
1
0
```

## Common mistakes

1. Thinking `del x` deletes the object. It only removes one pointer.

2. Calling `gc.collect()` to fix a leak. The collector cannot free an object that something still points to.

3. Putting must-happen work in `__del__`: errors in it are swallowed and its timing is not guaranteed.

4. A cache with no limit (a plain dictionary at the top of the file): it grows for ever. Use `lru_cache(maxsize=...)` or a weak dictionary.

5. Making a weak reference to a list or dictionary: wrap the data in a class.

## Clean up

Nothing to clean up. Delete the folder if you want it gone.

## Next

Next lesson: [M11-L03 · The GIL and Free-Threaded Python](../m11-l03-the-gil-and-free-threaded-python/README.md). You will meet the one pen in the office that only one worker can hold, and see why it keeps these reference counts safe.
