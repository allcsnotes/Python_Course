# M11-L04 · Measuring and Improving Speed

> Video: Module 11, Lesson 4. Watch it first, then follow along here.

## What you'll learn

- The speed loop: measure, find the slowest part, change only that, measure again
- `timeit` for a small piece of code, `cProfile` for a whole program, and a flame graph (`py-spy`) as a picture
- Why a list lookup was slow and a set fixed it (and how to check the answer stayed the same)
- Why Python is slow (bytecode, everything is an object), and when speed does not matter (I/O-bound)
- How `numpy` changes the game for big piles of numbers, and five pitfalls of measuring

## Before you start

- Python 3.14 or newer. Check with `python --version`.
- `numpy` is needed for one step (`pip install -r requirements.txt` inside a virtual environment, as in module 7). The `py-spy` flame graph step uses Docker with the image `python:3.14-slim`; it is optional, and the finished `flame.svg` files are included, so you can open them in a browser without running it. The reason for Docker: macOS locks the permission that `py-spy` needs.
- [M11-L03 · The GIL and Free-Threaded Python](../m11-l03-the-gil-and-free-threaded-python/README.md): the stopwatch (`perf_counter`) was introduced there.
- **Timings depend on your computer.** Every number of seconds below comes from one real run on one Mac, so yours will differ (and the numbers in the video differ again). The slow-versus-fast gaps will be there. The `v2/` folder is the fixed version of the report.

## Files in this folder

| File | What it is |
|------|------------|
| `data.py` | Builds 60,000 fake enrollment rows (`student,course,price`) |
| `stats.py` | `unique_students` (with a list: the slow part) and `total_revenue` |
| `report.py` | The report script (the hook) |
| `noise.py` | Timing the same line five times: never the same |
| `compare.py` | `timeit.repeat`: list comprehension against a loop |
| `profile_it.py` | `cProfile` and `pstats` from inside code |
| `flame.svg` | Flame graph of `report.py` made with `py-spy` (open in a browser) |
| `dis_loop.py` | The bytecode of a small loop, with `dis` |
| `size.py` | How many bytes is the number 5? |
| `wait.py` | A handler that mostly waits (I/O-bound) |
| `requirements.txt` | `numpy==2.5.4` |
| `numpy_race.py` | A Python loop against `numpy` |
| `setup_mistake.py` | Pitfall 1: timing the setup too |
| `small_test.py` | Pitfall 2: testing with small data |
| `wrong_part.py` | Pitfall 3: speeding up the wrong part |
| `v2/data.py` | Same `data.py` |
| `v2/stats.py` | Fixed: `seen` is a set |
| `v2/report.py` | Same `report.py`, runs against the fixed `stats.py` |
| `v2/flame_run.py` | Runs the work 30 times so the flame graph has enough samples |
| `v2/flame.svg` | Flame graph of the fixed version |
| `v2/overhead.py` | Pitfall 4: the profiler slows the program |
| `tryit.py` | A model answer to the Try it yourself task |

## Follow along

### 1. The hook: where does the time go?

In the last lesson we used a stopwatch to time threads. Today a bigger question: when a program is slow, where does the time go? Asha has a report script for allcsvideos.com. It looks at 60,000 enrollments (rows like `student12,course12,599`, made by `data.py`) and does two things. `unique_students` keeps a list `seen` and for every row asks: is this student already in the list? If not, it adds them. `total_revenue` adds up the price on every row. Both call `split_row` to cut a row apart. A short `report.py` builds the rows, starts a timer, runs both jobs and prints the time. Guess: how long will it take, and which of the two functions is the slow one?

```python
def make_rows(count):
    rows = []
    for i in range(count):
        student = f"student{i % 9000}"
        rows.append(f"{student},course{i % 40},{(i % 7) * 100 + 99}")
    return rows


def split_row(row):
    student, course, price = row.split(",")
    return student, course, int(price)
```

```python
from data import split_row


def unique_students(rows):
    seen = []
    for row in rows:
        student = split_row(row)[0]
        if student not in seen:
            seen.append(student)
    return seen


def total_revenue(rows):
    total = 0
    for row in rows:
        total += split_row(row)[2]
    return total
```

```python
import time
from data import make_rows
from stats import total_revenue, unique_students


def build_report(rows):
    students = unique_students(rows)
    revenue = total_revenue(rows)
    return len(students), revenue


rows = make_rows(60000)
start = time.perf_counter()
print(build_report(rows))
print(f"{time.perf_counter() - start:.3f} seconds")
```

```bash
python report.py
```

```
(9000, 23939400)
1.673 seconds
```

9,000 different students and 23,939,400 in money, but look at the time: far too long for 60,000 rows. Asha's first instinct: adding up the money must be the hard part. Is she right? In this lesson you stop guessing and start measuring.

### 2. Measure first: the kitchen

A restaurant kitchen is slow and the owner wants dinner served faster. One way: shout at every cook to hurry. Another: stand with a stopwatch and see where each dish spends its time. Chopping takes 2 minutes, cooking 3, and then the plate waits 19 minutes at the washing station, because there is one slow dishwasher. Telling the cooks to chop faster changes nothing. You must find the slow station. Your feeling about which line is slow is often wrong, even for experienced developers. So the first rule of speed: **measure first, then change**.

Three tools, from small to big: a stopwatch for one small piece of code (`timeit`), a profiler for a whole program (it lists every function and the time it used), and a flame graph (a picture of the same information). And one loop to follow: measure; find the slowest part; change only that; measure again.

### 3. Tool 1: `timeit`

Time the same line five times: the sum of a range of 100,000 numbers. Will we get the same time five times?

```python
import time

for run in range(5):
    start = time.perf_counter()
    sum(range(100000))
    elapsed = time.perf_counter() - start
    print(f"run {run + 1}: {elapsed * 1000:.3f} ms")
```

```bash
python noise.py
```

```
run 1: 0.378 ms
run 2: 0.378 ms
run 3: 0.377 ms
run 4: 0.642 ms
run 5: 0.377 ms
```

The numbers are close but never the same. Other programs on your computer, and Python warming up, add noise. So the standard way is: run the code many times, repeat that a few times, and keep the best time (the run that was disturbed least). Python ships a tool that does exactly this: `timeit`. From the terminal (`-m` means run a module as a program), here with a smaller sum:

```bash
python -m timeit "sum(range(1000))"
```

```
50000 loops, best of 5: 3.9 usec per loop
```

`timeit` chose the number of loops by itself (e.g. `50000 loops`), repeated five times (`best of 5`) and kept the fastest, in microseconds (millionths of a second). You can choose the numbers yourself: `-n` sets the loops, `-r` sets the repeats.

```bash
python -m timeit -n 1000 -r 3 "sum(range(1000))"
```

```
1000 loops, best of 3: 3.42 usec per loop
```

Close to the first answer, but not equal. That is normal.

Inside a program, use the `timeit` module. Is a list comprehension faster than a loop with `append`? Many people say much faster. Guess how much.

```python
import timeit


def with_loop():
    squares = []
    for n in range(1000):
        squares.append(n * n)
    return squares


def with_comprehension():
    return [n * n for n in range(1000)]


for func in (with_loop, with_comprehension):
    runs = timeit.repeat(func, number=2000, repeat=5)
    best = min(runs) / 2000 * 1000000
    print(f"{func.__name__}: {best:.1f} microseconds")
```

```bash
python compare.py
```

```
with_loop: 20.4 microseconds
with_comprehension: 19.9 microseconds
```

The comprehension wins, but only by around ten percent, not by a mile. Measuring just corrected a popular belief. Use comprehensions because they read well. `timeit` answers "is A faster than B for a small piece of code"; it does not tell you which part of a big program is slow. For that we need the next tool.

### 4. Tool 2: the profiler, `cProfile`

A stopwatch around everything says the report takes about two seconds. It cannot say which function is to blame. A profiler is like a tracker that logs every taxi trip and adds up driving, waiting and traffic: it watches every function call and writes down how often it was called and how long it took. Python ships one, `cProfile`. `-s tottime` means sort by the time spent inside the function itself. Which function will be at the top? (The table is long; only the top rows are shown here.)

```bash
python -m cProfile -s tottime report.py
```

```
(9000, 23939400)
1.802 seconds
         309360 function calls (309358 primitive calls) in 1.823 seconds

   Ordered by: internal time

   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
        1    1.760    1.760    1.785    1.785 stats.py:4(unique_students)
   120000    0.024    0.000    0.037    0.000 data.py:9(split_row)
        1    0.017    0.017    0.020    0.020 data.py:1(make_rows)
   120000    0.013    0.000    0.013    0.000 {method 'split' of 'str' objects}
        1    0.005    0.005    0.018    0.018 stats.py:13(total_revenue)
    69004    0.004    0.000    0.004    0.000 {method 'append' of 'list' objects}
        2    0.000    0.000    0.000    0.000 {built-in method builtins.compile}
        1    0.000    0.000    1.823    1.823 report.py:1(<module>)
        4    0.000    0.000    0.000    0.000 {built-in method _io.open_code}
```

At the top: `unique_students`, almost the whole time. Not `total_revenue`. Asha's instinct was wrong. The columns: `ncalls` is how many times the function was called; `tottime` is the time inside the function itself; `cumtime` is the time including everything it called; `percall` is the time divided by the number of calls.

You can also start the profiler from inside code and choose what to show:

```python
import cProfile
import pstats

import data
import stats

rows = data.make_rows(60000)
with cProfile.Profile() as profiler:
    stats.unique_students(rows)
    stats.total_revenue(rows)
report = pstats.Stats(profiler)
report.sort_stats("cumulative")
report.print_stats(3)
```

```bash
python profile_it.py
```

```
         249004 function calls in 1.983 seconds

   Ordered by: cumulative time
   List reduced from 7 to 3 due to restriction <3>

   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
        1    1.925    1.925    1.956    1.956 stats.py:4(unique_students)
   120000    0.031    0.000    0.048    0.000 data.py:9(split_row)
        1    0.008    0.008    0.027    0.027 stats.py:13(total_revenue)
```

The same story: `unique_students` on top. Look at `split_row`: its own time is small, but its cumulative time includes the `split` it calls. So the profiler answers the question the stopwatch could not: which function.

### 5. Tool 3: the flame graph

A table is fine for seven functions. For a program with hundreds we want a picture. A **flame graph** draws the profile as stacked boxes. The tool is `py-spy`, a *sampling* profiler: instead of watching every call, it looks at your program 500 times a second and writes down which function is running. A function that shows up in many looks, uses a lot of time. A Mac keeps the permission `py-spy` needs locked, so the video ran it inside Docker on Linux with Python 3.14. This step needs Docker and is optional; `flame.svg` is already in this folder.

```bash
py-spy record -r 500 -F -f flamegraph -o flame.svg -- python report.py
```

```
py-spy 0.4.2
py-spy> Sampling process 500 times a second. Press Control-C to exit.

(9000, 23939400)
2.047 seconds

py-spy> Stopped sampling because process exited
py-spy> Wrote flamegraph data to 'flame.svg'. Samples: 1086 Errors: 0
```

It ran the report, took roughly a thousand samples and wrote `flame.svg` (the exact number of samples will differ). Open it in a browser. How to look at it: the top box, `all`, is the whole program; each row below is the functions called by the box above; the **width of a box is its share of the time**. Look for the widest box that has nothing wide below it. That box is where the time goes. The name "flame" comes from the tongues of boxes that real programs make.

### 6. Find, change, measure again

Now we know where. But why is `unique_students` slow? Look at the line `if student not in seen`. Here `seen` is a list, and a list checks the items one by one from the front. With 9,000 different students a check can look at thousands of items, 60,000 times. In module 5 you met the better tool: a **set**. A set does not search: it jumps straight to the right spot using the hash of the item. The fix is two small changes in `v2/stats.py`: `seen` is a set instead of a list, and `add` instead of `append`. Change one thing, then measure again. Guess how long the report takes now. (Run it from the `v2` folder.)

`v2/stats.py`:

```python
from data import split_row


def unique_students(rows):
    seen = set()
    for row in rows:
        student = split_row(row)[0]
        if student not in seen:
            seen.add(student)
    return seen


def total_revenue(rows):
    total = 0
    for row in rows:
        total += split_row(row)[2]
    return total
```

```bash
python report.py
```

```
(9000, 23939400)
0.017 seconds
```

The same answer (9,000 students and the same money). That matters: a faster version must give the same result. And the time: a small fraction of what it was. Now profile again, because the picture has changed:

```bash
python -m cProfile -s tottime report.py
```

```
(9000, 23939400)
0.065 seconds
         309360 function calls (309358 primitive calls) in 0.090 seconds

   Ordered by: internal time

   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
   120000    0.027    0.000    0.040    0.000 data.py:9(split_row)
        1    0.021    0.021    0.025    0.025 data.py:1(make_rows)
        1    0.014    0.014    0.036    0.036 stats.py:4(unique_students)
   120000    0.013    0.000    0.013    0.000 {method 'split' of 'str' objects}
        1    0.009    0.009    0.028    0.028 stats.py:13(total_revenue)
    60004    0.004    0.000    0.004    0.000 {method 'append' of 'list' objects}
     9000    0.001    0.000    0.001    0.000 {method 'add' of 'set' objects}
```

`unique_students` dropped out of the top. Now `split_row` is first, called 120,000 times, and the whole report is a few hundredths of a second. The flame graph tells the same story (for this one the work is repeated 30 times, so the tool collects enough samples):

```bash
py-spy record -r 500 -F -f flamegraph -o flame.svg -- python flame_run.py
```

```
py-spy 0.4.2
py-spy> Sampling process 500 times a second. Press Control-C to exit.


py-spy> Stopped sampling because process exited
py-spy> Wrote flamegraph data to 'flame.svg'. Samples: 277 Errors: 0
```

There is no giant box now: `unique_students` and `total_revenue` are about the same width. Should we keep going? We could call `split_row` once per row and save a few milliseconds, but the code gets harder to read. The rule: stop when it is fast enough. Speed always costs something. The loop worked: measure, find (`unique_students`), change (list into set), measure again.

### 7. Why is Python slow?

People say Python is slow. Compared with C, the same loop usually takes longer in Python. There are two main reasons.

**Reason 1: Python runs bytecode, one instruction at a time.** In module 1, lesson 4 you saw that Python turns your file into bytecode (a to-do list) and the virtual machine carries the list out. Here is a tiny function that adds up numbers, shown with `dis`:

```python
import dis


def add_all(numbers):
    total = 0
    for n in numbers:
        total += n
    return total


dis.dis(add_all)
```

```bash
python dis_loop.py
```

```
  4           RESUME                   0

  5           LOAD_SMALL_INT           0
              STORE_FAST               1 (total)

  6           LOAD_FAST_BORROW         0 (numbers)
              GET_ITER
      L1:     FOR_ITER                11 (to L2)
              STORE_FAST               2 (n)

  7           LOAD_FAST_BORROW_LOAD_FAST_BORROW 18 (total, n)
              BINARY_OP               13 (+=)
              STORE_FAST               1 (total)
              JUMP_BACKWARD           13 (to L1)

  6   L2:     END_FOR
              POP_ITER

  8           LOAD_FAST_BORROW         1 (total)
              RETURN_VALUE
```

Look between `FOR_ITER` and `JUMP_BACKWARD`: about six instructions for every number: get the next number, store it in `n`, load `total` and `n`, add them, store the answer in `total`, jump back to the top. For a million numbers that is six million instructions, each looked up and carried out by the virtual machine. A loop in C does the same job with a handful of instructions straight on the processor. (The exact instruction names depend on your Python version.)

**Reason 2: everything is an object** (lesson 1 of this module). `sys.getsizeof` tells how many bytes an object takes:

```python
import sys

print(sys.getsizeof(5), "bytes for the number 5")
```

```bash
python size.py
```

```
28 bytes for the number 5
```

28 bytes for the number 5, where C would use 4 or 8. A Python list of numbers is a row of arrows, each pointing to a separate number object somewhere in memory. A `numpy` array is different: the raw numbers sit side by side in one block, with no objects between. This is the price of flexibility: the same line works for whole numbers, decimals, text and your own classes. Python is built to save the programmer's time.

The good news: the slow part is the loop that Python itself runs. Work that runs inside C is fast. The built-in tools, like `sum`, `sorted` and the set lookup we just used, are written in C, and so are libraries like `numpy`.

### 8. When speed does not matter: waiting

A parcel takes three days to arrive. Making the packing clerk twice as fast saves a few seconds out of three days. Nobody notices. Many programs spend most of their time waiting for a database, a web request or a file. Here `fetch_course` stands in for a slow database call: it sleeps for 0.3 seconds, and the handler runs three times. Where will the time go?

```python
import time


def fetch_course():
    time.sleep(0.3)
    return {"title": "Python"}


def handle_request():
    course = fetch_course()
    return course["title"].upper()


for _ in range(3):
    handle_request()
```

```bash
python wait.py
```

(no output)

```bash
python -m cProfile -s tottime wait.py
```

```
         15 function calls in 0.915 seconds

   Ordered by: internal time

   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
        3    0.914    0.305    0.914    0.305 {built-in method time.sleep}
        1    0.000    0.000    0.000    0.000 {method 'disable' of '_lsprof.Profiler' objects}
        3    0.000    0.000    0.915    0.305 wait.py:9(handle_request)
        3    0.000    0.000    0.915    0.305 wait.py:4(fetch_course)
```

Three calls, about 0.9 seconds in total, almost all of it inside `time.sleep`. Our own Python code takes less than a thousandth of a second. Making our Python ten times faster would change nothing. A program like this is **I/O-bound**: limited by waiting for input and output. Asha's report was the opposite, **CPU-bound**: limited by computing. Which kind you have decides what helps (the next module, lesson 1, is all about it).

### 9. `numpy` for big piles of numbers

For big piles of numbers the answer is `numpy`, a package you install (module 7). It is a C extension: a Python package whose heavy work is written in C and which stores numbers in one block. Create a virtual environment and install it from `requirements.txt` (pinned to the version the video used):

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

```
Collecting numpy==2.5.4 (from -r requirements.txt (line 1))
  Using cached numpy-2.5.4-cp314-cp314-macosx_14_0_arm64.whl.metadata (6.6 kB)
Using cached numpy-2.5.4-cp314-cp314-macosx_14_0_arm64.whl (5.5 MB)
Installing collected packages: numpy
Successfully installed numpy-2.5.4

```

We add up the squares of the numbers up to one million, first with a Python loop, then with `numpy`: the array times itself, and `.sum()`. How many times faster is `numpy`? Twice? Ten? A hundred?

```python
import time

import numpy as np

numbers = list(range(1000000))
array = np.arange(1000000)

start = time.perf_counter()
loop_total = 0
for n in numbers:
    loop_total += n * n
loop_ms = (time.perf_counter() - start) * 1000

start = time.perf_counter()
numpy_total = (array * array).sum()
numpy_ms = (time.perf_counter() - start) * 1000

print(loop_total, numpy_total)
print(f"Python loop: {loop_ms:.1f} ms")
print(f"NumPy:       {numpy_ms:.1f} ms")
print(f"NumPy is {loop_ms / numpy_ms:.0f} times faster")
```

```bash
python numpy_race.py
```

```
333332833333500000 333332833333500000
Python loop: 77.4 ms
NumPy:       1.2 ms
NumPy is 65 times faster
```

Both lines give the same answer. `numpy` is many times faster (19 times in the video, more or fewer on your computer). Why? There is no Python instruction per number and no object per number: it is one tight loop in C over raw numbers. The rule: before you write a loop over many numbers, look for a built-in tool or a `numpy` operation that does the whole job.

### 10. Five pitfalls

**1. Timing the setup too.** Both lines ask whether 999 is in a list. The first builds the list inside the timed code; the second builds it once, in the `setup` argument. Do they give the same time?

```python
import timeit

setup = "numbers = list(range(1000))"
wrong = timeit.timeit("999 in list(range(1000))", number=2000)
right = timeit.timeit("999 in numbers", setup, number=2000)
print(f"setup inside the timing: {wrong:.4f} seconds")
print(f"setup done once before:  {right:.4f} seconds")
```

```bash
python setup_mistake.py
```

```
setup inside the timing: 0.0360 seconds
setup done once before:  0.0161 seconds
```

The first also timed the building of the list, 2000 times. Put the preparation in the `setup` argument: it runs once, outside the clock.

**2. Testing with small data.** Asha tests the slow report with 200 rows and then with 60,000 (this runs against the slow `stats.py` in this folder). What does the small test show?

```python
import time

from data import make_rows
from stats import unique_students

for count in (200, 60000):
    rows = make_rows(count)
    start = time.perf_counter()
    unique_students(rows)
    seconds = time.perf_counter() - start
    print(f"{count} rows: {seconds:.3f} seconds")
```

```bash
python small_test.py
```

```
200 rows: 0.000 seconds
60000 rows: 2.424 seconds
```

200 rows: it looks instant. 60,000 rows: seconds. A slow idea can hide in small data. Test with realistic sizes.

**3. Speeding up the wrong part.** Asha, still sure about the money, writes a faster `total` with `sum`. How much faster does the whole report get?

```python
import timeit

from data import make_rows, split_row
from stats import total_revenue, unique_students


def total_sum(rows):
    return sum(split_row(row)[2] for row in rows)


def report(total):
    unique_students(rows)
    total(rows)


rows = make_rows(60000)
for total in (total_revenue, total_sum):
    runs = timeit.repeat(lambda: report(total), number=1, repeat=3)
    print(f"{total.__name__}: {min(runs):.2f} seconds")
```

```bash
python wrong_part.py
```

```
total_revenue: 2.89 seconds
total_sum: 1.94 seconds
```

No gain at all. That function was less than one percent of the time, and the small difference is just noise. Profile first, then change the biggest part.

**4. Believing the profiler's seconds.** The profiler slows the program while it watches. Here is the fixed report run normally, then under the profiler (run from the `v2` folder):

```bash
python overhead.py
```

```
normal:   0.024 seconds
profiled: 0.047 seconds
```

More than three times slower under the profiler in the video. Use the profiler to find the culprit; use `timeit` or `perf_counter` for the real numbers.

**5. Optimising too early.** First make it work. Then make it clear. Then, only if it is too slow, measure and make it fast. Fast code that nobody can read, and that did not need to be fast, is a bad trade.

### 11. Try it yourself: model answer

Time two ways of checking a word, in a list and in a set. Race a loop against `sum`. Profile one of your own scripts from the command line, read its table, and fix its slowest function. One answer for the first task:

```python
import timeit

words = [f"word{i}" for i in range(1000)]
as_set = set(words)
for name, group in (("list", words), ("set", as_set)):
    runs = timeit.repeat(lambda: "word999" in group, number=2000, repeat=3)
    print(f"{name}: {min(runs):.4f} seconds")


def with_loop():
    total = 0
    for n in range(1000):
        total += n
    return total


for func in (with_loop, lambda: sum(range(1000))):
    runs = timeit.repeat(func, number=2000, repeat=3)
    print(f"{min(runs) / 2000 * 1000000:.1f} microseconds")
```

```bash
python tryit.py
```

```
list: 0.0146 seconds
set: 0.0000 seconds
13.7 microseconds
4.3 microseconds
```

## Common mistakes

1. Guessing which part is slow instead of measuring.

2. Timing the setup together with the code (put it in `setup=`).

3. Testing a slow idea with tiny data.

4. Optimising a function that is a tiny share of the profile.

5. Quoting the profiler's seconds as real timings.

6. Making code hard to read for speed it did not need.

7. Using a list for membership checks on big data. Use a set.

## Clean up

The `.venv` folder you made for numpy lives where you ran the commands; delete it when you are done (`rm -rf .venv`). Nothing else to clean up.

## Next

Next: module 12, [M12-L01 · CPU-Bound vs IO-Bound](../../m12-concurrency/m12-l01-cpu-bound-vs-io-bound/README.md). Is your program computing, or waiting? The answer decides how to make it faster.

Your turn first: time two ways of checking a word (list and set), race a loop against `sum`, profile one of your own scripts and fix its slowest function.
