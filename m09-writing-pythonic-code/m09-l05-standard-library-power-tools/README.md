# M09-L05 · Standard Library Power Tools

> Video: Module 9, Lesson 5. Watch it first, then follow along here.

## What you'll learn

- Why `@cache` makes a Fibonacci function more than a hundred thousand times faster
- Counters you can add, and the fast two-ended queue `deque` (with `maxlen` to keep only the last few items)
- Six `itertools` tools: `islice`, `groupby`, `accumulate`, `product`, `pairwise`, `batched`
- `functools`: `partial`, `reduce`, `cache` and `lru_cache`, and the two rules for caching
- Using `Counter`, `deque` and `groupby` together on log lines

## Before you start

- Python 3.14 or newer. Check with `python --version` (`itertools.batched` needs 3.12 or newer).
- No Docker needed.
- [M09-L01 · Iterables and Iterators](../m09-l01-iterables-and-iterators/README.md) (walkers) and [M09-L03 · Closures and Decorators](../m09-l03-closures-and-decorators/README.md) (the `remember` notebook this lesson replaces).
- Timings in this lesson depend on your computer. The numbers in the README are from a real run; yours will differ, but the gaps will be there.

## Files in this folder

| File | What it is |
|------|------------|
| `hook_slow.py` | Slow recursive Fibonacci of 38 (the hook) |
| `hook_fast.py` | The same with `@cache` |
| `counter_cb.py` | Adding two Counters, then `update` |
| `deque_basic.py` | A deque with two doors |
| `deque_race.py` | Race: `list.pop(0)` against `deque.popleft()` |
| `deque_max.py` | `maxlen=3` keeps only the last three items |
| `deque_slice.py` | A deque cannot be sliced |
| `islice_next.py` | `islice` cuts a piece out of a walker |
| `groupby_bad.py` | `groupby` on unsorted data |
| `groupby_sorted.py` | `groupby` after sorting |
| `groupby_key.py` | `groupby` with `key=` on course orders |
| `accumulate.py` | Running totals with `accumulate` |
| `product.py` | Every plan in every country with `product` |
| `pairwise.py` | Changes between neighbours with `pairwise` |
| `batched.py` | Batches of two students with `batched` |
| `partial.py` | Fixing the discount with `partial` |
| `reduce_basic.py` | `reduce` against `sum` |
| `reduce_empty.py` | `reduce` on an empty list needs a start value |
| `fib_count.py` | Counting the calls of plain Fibonacci |
| `fib_cached.py` | The same with `@cache` and `cache_info()` |
| `lru.py` | `lru_cache(maxsize=2)` throws out the oldest answer |
| `cache_list.py` | A cached function cannot take a list |
| `cache_tuple.py` | The fix: pass a tuple |
| `cache_stale.py` | A cached function that reads a changing variable gives a stale answer |
| `together.py` | `Counter` and `deque` together on log lines |
| `tryit.py` | A model answer to the Try it yourself task |

## Follow along

### 1. The hook: two lines, 100,000 times faster

Asha tests a function that calls itself (recursion, module 4). It gives the Fibonacci numbers: every number is the two numbers before it, added together (0, 1, 1, 2, 3, 5, 8, ...). She asks for the 38th number and times it. Guess how long it takes.

```python
import time


def fib(n):
    if n < 2:
        return n
    return fib(n - 1) + fib(n - 2)


start = time.perf_counter()
print(fib(38))
print(f"{time.perf_counter() - start:.2f} seconds")
```

```bash
python hook_slow.py
```

```
39088169
2.25 seconds
```

The answer is 39,088,169, but the time is several seconds for one small question (3.39 seconds in the video; yours will differ). The computer is doing something very wasteful. Now add one import line and one line above the function: `@cache`. Nothing else changes.

```python
import time
from functools import cache


@cache
def fib(n):
    if n < 2:
        return n
    return fib(n - 1) + fib(n - 2)


start = time.perf_counter()
print(fib(38))
print(f"{time.perf_counter() - start:.5f} seconds")
```

```bash
python hook_fast.py
```

```
39088169
0.00003 seconds
```

The same answer, in a few hundredths of a millisecond: more than a hundred thousand times faster. Step 5 explains why.

### 2. Drawer 1, collections: Counter and deque

Counters can be added with `+`, and `update` adds more items. Counters print with the biggest count first. Guess the two lines:

```python
from collections import Counter

monday = Counter(["Python", "SQL", "Python"])
tuesday = Counter(["Python", "Docker"])
print(monday + tuesday)
monday.update(["Go", "Go"])
print(monday)
```

```bash
python counter_cb.py
```

```
Counter({'Python': 3, 'SQL': 1, 'Docker': 1})
Counter({'Python': 2, 'Go': 2, 'SQL': 1})
```

`Python` is 3 because two orders came from Monday and one from Tuesday. The `update` changed Monday's own counter.

A **deque** (say "deck", short for double-ended queue) is a line with two fast doors. Taking a name off the front of a list with `pop(0)` makes every other name move up one place; a deque moves nothing.

```python
from collections import deque

line = deque(["Lukas", "Priya"])
line.append("Asha")
line.appendleft("Meera")
print(line)
print(line.popleft())
print(line)
```

```bash
python deque_basic.py
```

```
deque(['Meera', 'Lukas', 'Priya', 'Asha'])
Meera
deque(['Lukas', 'Priya', 'Asha'])
```

`appendleft` put Meera at the front, `popleft` handed her back. On the right end you use `append` and `pop`; on the left end `appendleft` and `popleft`. Is it really faster? Race a list of 100,000 numbers emptied with `pop(0)` against a deque emptied with `popleft()`:

```python
import time
from collections import deque

items = list(range(100000))
start = time.perf_counter()
while items:
    items.pop(0)
list_time = time.perf_counter() - start

line = deque(range(100000))
start = time.perf_counter()
while line:
    line.popleft()
deque_time = time.perf_counter() - start

print(f"list pop(0): {list_time * 1000:.1f} ms")
print(f"deque popleft: {deque_time * 1000:.1f} ms")
```

```bash
python deque_race.py
```

```
list pop(0): 754.2 ms
deque popleft: 2.3 ms
```

A list is a row of boxes in memory, and taking the first box moves all the others. The gap grows with the size. (Your numbers will differ; the deque wins by a factor of hundreds.)

The most famous use is to keep only the last few items: give it `maxlen`. When a fourth item arrives, the oldest falls out of the other end, like a shelf with room for three books. This is the tail of a log file in four lines:

```python
from collections import deque

recent = deque(maxlen=3)
for number in range(1, 6):
    recent.append(f"line {number}")
    print(list(recent))
```

```bash
python deque_max.py
```

```
['line 1']
['line 1', 'line 2']
['line 1', 'line 2', 'line 3']
['line 2', 'line 3', 'line 4']
['line 3', 'line 4', 'line 5']
```

One limit: a deque is not a list. Position 0 works, a slice does not. Turn it into a list first if you need a slice.

```python
from collections import deque

recent = deque(["a", "b", "c"])
print(recent[0])
print(recent[0:2])
```

```bash
python deque_slice.py
```

```
a
Traceback (most recent call last):
  File "deque_slice.py", line 5, in <module>
    print(recent[0:2])
          ~~~~~~^^^^^
TypeError: sequence index must be integer, not 'slice'
```

### 3. Drawer 2, itertools: six tools for streams

`itertools` means iterator tools: they take a walker and give a walker back, so they never build a big list.

**islice** (iterator slice) cuts a piece out of a walker. `count(101)` never ends, so `islice` takes three. The second `islice` carries on where the first stopped, because a walker remembers its place. The third line starts at place 2 and stops before place 5, just like a slice.

```python
from itertools import count, islice

ids = count(101)
print(list(islice(ids, 3)))
print(list(islice(ids, 3)))
print(list(islice("ABCDEFG", 2, 5)))
```

```bash
python islice_next.py
```

```
[101, 102, 103]
[104, 105, 106]
['C', 'D', 'E']
```

**groupby** gathers neighbours with the same value into a group. Watch an unsorted list: it only joins equal items that sit next to each other.

```python
from itertools import groupby

levels = ["INFO", "ERROR", "INFO", "ERROR", "INFO"]
for level, group in groupby(levels):
    print(level, len(list(group)))
```

```bash
python groupby_bad.py
```

```
INFO 1
ERROR 1
INFO 1
ERROR 1
INFO 1
```

Five groups of size one. The fix is to sort first, so equal items sit side by side:

```python
from itertools import groupby

levels = ["INFO", "ERROR", "INFO", "ERROR", "INFO"]
for level, group in groupby(sorted(levels)):
    print(level, len(list(group)))
```

```bash
python groupby_sorted.py
```

```
ERROR 2
INFO 3
```

The rule: groupby needs sorted input. (The `defaultdict` of module 6 collects from anywhere; `groupby` does not look further along.) With real records you group by one part of each item with `key=`, the same key idea as in `sort` and `max`:

```python
from itertools import groupby

orders = [
    ("Python", "Lukas"),
    ("SQL", "Priya"),
    ("Python", "Asha"),
    ("SQL", "Rahul"),
]
orders.sort()
for course, rows in groupby(orders, key=lambda o: o[0]):
    names = [o[1] for o in rows]
    print(course, names)
```

```bash
python groupby_key.py
```

```
Python ['Asha', 'Lukas']
SQL ['Priya', 'Rahul']
```

**accumulate** gives running totals (sign-ups per day: 3, 5, 2, 4), like a bank balance. Give it a function without brackets to use instead of adding: `max` gives the best day so far.

```python
from itertools import accumulate

daily = [3, 5, 2, 4]
print(list(accumulate(daily)))
print(list(accumulate(daily, max)))
```

```bash
python accumulate.py
```

```
[3, 8, 10, 14]
[3, 5, 5, 5]
```

**product** is a nested loop in one line: every plan with every country (2 times 3 is 6).

```python
from itertools import product

plans = ["monthly", "yearly"]
countries = ["India", "Germany", "Brazil"]
for plan, country in product(plans, countries):
    print(plan, country)
print(len(list(product(plans, countries))))
```

```bash
python product.py
```

```
monthly India
monthly Germany
monthly Brazil
yearly India
yearly Germany
yearly Brazil
6
```

**pairwise** hands out overlapping neighbours, perfect for changes. Four numbers make three pairs:

```python
from itertools import pairwise

signups = [10, 14, 13, 20]
for before, after in pairwise(signups):
    print(after - before)
```

```bash
python pairwise.py
```

```
4
-1
7
```

**batched** cuts a stream into batches of a fixed size (Python 3.12 or newer). Asha emails five students but the mail server accepts two at a time. The last batch has a comma after `Rahul`: that is how Python writes a tuple with one value.

```python
from itertools import batched

students = ["Lukas", "Priya", "Asha", "Meera", "Rahul"]
for group in batched(students, 2):
    print(group)
```

```bash
python batched.py
```

```
('Lukas', 'Priya')
('Asha', 'Meera')
('Rahul',)
```

### 4. Drawer 3, functools: partial and reduce

**partial** makes a new function with some inputs already filled in. During the festive sale the discount is always 20, and typing it every time invites typos. We hand the function over without brackets:

```python
from functools import partial


def price_after(price, discount):
    return price - price * discount / 100


festive = partial(price_after, discount=20)
print(price_after(2000, 20))
print(festive(2000))
print(festive(500))
```

```bash
python partial.py
```

```
1600.0
1600.0
400.0
```

**reduce** squeezes a list into one value: it combines the first two items, then that result with the third, like a snowball rolling along. Honest advice: reach for `sum`, `max`, `min` or a plain loop first. Use `reduce` for a job `sum` cannot do, like multiplying.

```python
from functools import reduce

prices = [499, 999, 1499]
sizes = [2, 3, 4]
print(reduce(lambda a, b: a + b, prices))
print(sum(prices))
print(reduce(lambda a, b: a * b, sizes))
```

```bash
python reduce_basic.py
```

```
2997
2997
24
```

One trap: what does `reduce` do with an empty list? A third input gives it a start value. Guess the two lines:

```python
from functools import reduce

print(reduce(lambda a, b: a + b, [], 0))
print(reduce(lambda a, b: a + b, []))
```

```bash
python reduce_empty.py
```

```
0
Traceback (most recent call last):
  File "reduce_empty.py", line 4, in <module>
    print(reduce(lambda a, b: a + b, []))
          ~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^
TypeError: reduce() of empty iterable with no initial value
```

With a start value you get `0`; without one, a `TypeError`. When the list could be empty, give a start value.

### 5. `cache`: why the hook was slow, and the fix

In lesson 3 you built `remember`, a decorator with a notebook. `functools.cache` is the careful, ready-made version. Why was Asha's function so slow? `fib(5)` needs `fib(4)` and `fib(3)`, but `fib(4)` also needs `fib(3)`, so the same questions are asked again and again. Count the calls for `fib(20)` with a global counter:

```python
calls = 0


def fib(n):
    global calls
    calls += 1
    if n < 2:
        return n
    return fib(n - 1) + fib(n - 2)


print(fib(20))
print(calls)
```

```bash
python fib_count.py
```

```
6765
21891
```

21,891 calls just for the 20th number. Now the cache: `from functools import cache` and `@cache` on its own line above the `def`. It also understands values passed by name, which `remember` did not.

```python
from functools import cache

calls = 0


@cache
def fib(n):
    global calls
    calls += 1
    if n < 2:
        return n
    return fib(n - 1) + fib(n - 2)


print(fib(20))
print(calls)
print(fib.cache_info())
```

```bash
python fib_cached.py
```

```
6765
21
CacheInfo(hits=18, misses=21, maxsize=None, currsize=21)
```

Same answer, but the function ran only 21 times: once for every number from 0 to 20. `cache_info()` says there were 18 hits (questions answered from the notebook) and 21 misses (questions the notebook could not answer, so the function ran).

The notebook of `remember` never forgot anything. A real notebook has a limited number of pages. `lru_cache` keeps at most `maxsize` answers; LRU means least recently used: when the notebook is full, the answer used longest ago is thrown out.

```python
from functools import lru_cache


@lru_cache(maxsize=2)
def square(n):
    print("working on", n)
    return n * n


print(square(2))
print(square(3))
print(square(2))
print(square(4))
print(square(3))
```

```bash
python lru.py
```

```
working on 2
4
working on 3
9
4
working on 4
16
working on 3
9
```

`2` and `3` are cached; asking `2` again prints no `working on` line. `4` is new, the notebook is full, so it throws out `3`, the answer used longest ago, and asking `3` again works it out again.

### 6. The two rules for caching

**Rule 1: the inputs must be hashable**, like the items of a set. A list is not.

```python
from functools import cache


@cache
def total(prices):
    return sum(prices)


print(total([499, 999]))
```

```bash
python cache_list.py
```

```
Traceback (most recent call last):
  File "cache_list.py", line 9, in <module>
    print(total([499, 999]))
          ~~~~~^^^^^^^^^^^^
TypeError: unhashable type: 'list'
```

The notebook cannot file a list under a page number, because a list can change. The fix is to pass a tuple, which cannot change:

```python
from functools import cache


@cache
def total(prices):
    return sum(prices)


print(total((499, 999)))
```

```bash
python cache_tuple.py
```

```
1498
```

**Rule 2: cache only functions whose answer depends on the inputs alone.** This one also reads `rate` (tax) from outside. We ask for the tax price of 2000, change the rate, and ask again. Guess the second line.

```python
from functools import cache

rate = 1.18


@cache
def with_tax(price):
    return price * rate


print(with_tax(2000))
rate = 1.05
print(with_tax(2000))
```

```bash
python cache_stale.py
```

```
2360.0
2360.0
```

`2360.0` twice. The second call never ran the function: the notebook still held the old, stale answer. A cached function must give the same answer for the same input, always: no clock, no files, no changing variables.

### 7. Using the tools together

Six log lines. A `Counter` counts the levels, and a `deque` with `maxlen=2` keeps the last two errors. The level is the second word of each line.

```python
from collections import Counter, deque

lines = [
    "10:01 INFO login",
    "10:02 ERROR payment failed",
    "10:03 INFO login",
    "10:04 ERROR video missing",
    "10:05 INFO logout",
    "10:06 ERROR payment failed",
]
counts = Counter()
last = deque(maxlen=2)
for line in lines:
    level = line.split()[1]
    counts[level] += 1
    if level == "ERROR":
        last.append(line)
print(counts)
print(list(last))
```

```bash
python together.py
```

```
Counter({'INFO': 3, 'ERROR': 3})
['10:04 ERROR video missing', '10:06 ERROR payment failed']
```

Three of each, and only the last two errors: the first one fell out of the deque by itself. Counting and remembering the tail in a handful of lines.

### 8. Try it yourself: model answer

Take a list of words. Count them with `Counter` and print the most common. Keep the last two in a `deque`. Group them after sorting. Cut them into batches of four. And cache a function that squares a number. One answer:

```python
from collections import Counter, deque
from functools import cache
from itertools import batched, groupby

words = ["go", "sql", "go", "rust", "sql", "go"]
print(Counter(words).most_common(1))
last = deque(words, maxlen=2)
print(list(last))
for key, grp in groupby(sorted(words)):
    print(key, len(list(grp)))
print(list(batched(words, 4)))


@cache
def square(n):
    return n * n


print(square(12))
```

```bash
python tryit.py
```

```
[('go', 3)]
['sql', 'go']
go 3
rust 1
sql 2
[('go', 'sql', 'go', 'rust'), ('sql', 'go')]
144
```

## Common mistakes

1. Taking from the front of a long list with `pop(0)` many times. Use a `deque` and `popleft()`.

2. Using `groupby` without sorting first: you get many small groups. Sort with the same key.

3. Reusing a walker: a second `islice` on the same walker carries on where the first stopped. Make a new walker to start again.

4. Caching a function that takes a list (unhashable), or that reads a clock, a file or a changing variable (stale answers).

5. Treating a `deque` as a list: no slices. And reaching for `reduce` when `sum`, `max`, `min` or a loop is clearer.

6. Calling `reduce` on a list that might be empty without a start value.

## Clean up

Nothing to clean up. Delete the folder if you want it gone.

## Next

Next: the build video, [M09-B05 · Build a Decorator Toolkit](../m09-b05-build-a-decorator-toolkit/README.md). You will write your own decorators: a timer, a retry, a cache with an expiry time, and a login check.
