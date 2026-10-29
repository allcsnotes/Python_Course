# M12-L03 · Processes

> Video: Module 12, Lesson 3. Watch it first, then follow along here.

## What you'll learn

- What a process is (a whole separate Python with its own memory and its own GIL) and how `ProcessPoolExecutor` runs jobs on several cores
- Why `if __name__ == "__main__":` is required (spawn runs your file again in every worker)
- What moving data costs: tiny jobs lose, `chunksize`, and pickling (why a lambda cannot travel)
- Why processes share nothing, and three safe ways to get results back: return values, a queue, a shared value with a lock
- Four pitfalls

## Before you start

- Python 3.14 or newer. Check with `python --version`.
- No Docker and no packages needed (only the standard library).
- [M12-L02 · Threads](../m12-l02-threads/README.md) (pools and locks) and [M11-L03 · The GIL](../../m11-python-under-the-hood/m11-l03-the-gil-and-free-threaded-python/README.md).
- **Timings depend on your computer, especially here, because the speed-up depends on how many fast cores you have and what else is running.** The seconds below are from one real run on one Mac, so yours will differ (and the video's numbers differ again). The pattern will be the same: several processes beat one for big computing jobs, and lose for tiny jobs. Process ids and shared-counter totals change on every run.

## Files in this folder

| File | What it is |
|------|------------|
| `speed_proc.py` | The hook: one process counts 300 million, then four processes count a quarter each |
| `speed8_proc.py` | The same with eight processes |
| `cpu_count.py` | How many cores do I have? |
| `who.py` | Proof that the workers are separate processes |
| `own_memory.py` | Each process has its own memory |
| `no_guard.py` | Pitfall: no `if __name__ == "__main__":` guard |
| `tiny.py` | Twenty thousand tiny jobs: processes lose |
| `big_data.py` | What packing five million numbers costs |
| `lambda_fail.py` | A lambda cannot be packed |
| `lambda_fix.py` | The fix: a named function |
| `primes_lib.py` | `is_prime` and `count_primes` for one slice of numbers |
| `primes.py` | Counting primes below one million: one process against four |
| `queue_demo.py` | Results through a `multiprocessing.Queue` |
| `counters.py` | Two worker functions that add to a shared counter |
| `shared_value.py` | A shared `mp.Value`, without and with a lock |

## Follow along

### 1. The hook: more than one pen

Last lesson ended with a promise: more than one pen at a time. Remember Asha's counting job from module 11, lesson 3? One thread counted 300 million, and four threads took the same time. `count` is the same as before: it counts down to zero, pure computing. The function `run` is new: it starts some workers, gives each one a share of the counting and waits for them. The workers are not threads this time. They are **processes**: a process is a whole separate copy of Python, running at the same moment as yours. A pool is a team of such workers, as in the last lesson. `pool.map` calls `count` once for each number in the list and hands every call to a free worker (the list is the number `n`, repeated once per worker; the `list(...)` around it makes us wait until every worker is done). The last two lines are the guard from module 7: `if __name__ == "__main__":`. It looks like decoration here; you will see why it is required. At the bottom, two timings: one process counts all 300 million, then four processes each do a quarter, 75 million.

```python
import time
from concurrent.futures import ProcessPoolExecutor


def count(n):
    while n > 0:
        n -= 1


def run(workers, n):
    start = time.perf_counter()
    with ProcessPoolExecutor(workers) as pool:
        list(pool.map(count, [n] * workers))
    return time.perf_counter() - start


if __name__ == "__main__":
    print(f"one process:    {run(1, 300_000_000):.2f} s")
    print(f"four processes: {run(4, 75_000_000):.2f} s")
```

```bash
python speed_proc.py
```

```
one process:    5.90 s
four processes: 1.83 s
```

For the first time with normal Python, four workers really counted at the same moment. (In the video: 3.33 seconds against 1.00, about three times faster.) Not four times faster, and that is honest: starting workers costs time, other programs were running, and many computers have some fast cores and some slower power-saving ones. Your numbers will differ; the direction is the point.

### 2. Four offices, four pens

Picture the office again. One pen, four workers, and only the worker holding the pen can write. That was threads. Now picture four separate offices, each with one worker and one pen of its own. Nobody waits for a pen, so four reports get written at the same time. In Python each office is a **process**: a separate copy of Python with its own memory and its own GIL, its own pen. The operating system (the software that runs your whole computer) gives each process its own space. A thread is one more worker inside an office; a process is a whole extra office. More pens means more cores working together. But setting up an office costs more than adding a worker.

Two differences matter most: threads share one memory, processes share nothing; and threads start quickly, processes take longer. That is why the map from lesson 1 says: heavy computing, use processes.

### 3. What happens when the pool starts

Python asks the operating system for a brand-new Python program, one for each worker, and each starts completely empty. On a Mac and on Windows each new Python then loads your file again, from the top, to learn what your functions are. This way of starting is called **spawn**. Remember it: your file runs again inside every worker. Then the job travels: Python packs the function and its argument into bytes (this is called *pickling*) and sends them through a pipe (a tube between two programs: bytes go in at one end and come out at the other) to the worker. The answer comes back the same way.

Proof that the workers are separate. This file starts four workers and asks each one for its process id (the number the operating system gives to every running program), then prints three facts:

```python
import multiprocessing as mp
import os
import time
from concurrent.futures import ProcessPoolExecutor


def whoami(_):
    time.sleep(0.1)
    return os.getpid()


if __name__ == "__main__":
    mine = os.getpid()
    with ProcessPoolExecutor(4) as pool:
        ids = set(pool.map(whoami, range(8)))
    print("workers used:", len(ids))
    print("is one of them me?", mine in ids)
    print("how they start:", mp.get_start_method())
```

```bash
python who.py
```

```
workers used: 4
is one of them me? False
how they start: spawn
```

Four workers were used. Is one of them me? `False`: the workers are not my program, they are other copies of Python. And how they start: `spawn` on a Mac or Windows (Linux uses another start method by default, so you may see a different word there).

Separate also means separate memory. Here `names` is an empty list; `add` puts a name into it and returns how long the list is. One worker is asked to add three names:

```python
from concurrent.futures import ProcessPoolExecutor

names = []


def add(name):
    names.append(name)
    return len(names)


if __name__ == "__main__":
    with ProcessPoolExecutor(1) as pool:
        print(list(pool.map(add, ["Asha", "Lukas", "Priya"])))
    print(names)
```

```bash
python own_memory.py
```

```
[1, 2, 3]
[]
```

The worker's list grew (1, 2, 3), but my list is still empty. The worker changed its own copy. Each office has a whiteboard of its own. This is the biggest difference from threads: threads share one whiteboard, processes each have their own and share nothing, unless we arrange it (step 7).

### 4. How many workers?

What if we change this? Eight workers instead of four, each counting a smaller share (37.5 million). Faster, slower, or the same?

```python
import time
from concurrent.futures import ProcessPoolExecutor


def count(n):
    while n > 0:
        n -= 1


def run(workers, n):
    start = time.perf_counter()
    with ProcessPoolExecutor(workers) as pool:
        list(pool.map(count, [n] * workers))
    return time.perf_counter() - start


if __name__ == "__main__":
    print(f"one process:     {run(1, 300_000_000):.2f} s")
    print(f"eight processes: {run(8, 37_500_000):.2f} s")
```

```bash
python speed8_proc.py
```

```
one process:     6.41 s
eight processes: 1.35 s
```

Faster again, because this computer has more than four cores. How many workers should you start? A good start is one per core. Python can tell you:

```python
import os

print(os.cpu_count())
```

```bash
python cpu_count.py
```

```
10
```

(On the video's Mac the answer is 10.) If you give the pool no number at all, it uses exactly that.

### 5. The guard is required

Remember that spawn runs your file again inside every worker. This file has the guard removed: the pool starts at the top of the file. Guess the output. (The real output is long, with the same error repeated by every worker; only the key lines are shown here, and `...` marks cut parts.)

```python
from concurrent.futures import ProcessPoolExecutor


def double(x):
    return x * 2


with ProcessPoolExecutor(2) as pool:
    print(list(pool.map(double, [1, 2, 3])))
```

```bash
python no_guard.py
```

```
Traceback (most recent call last):
  File "no_guard.py", line 9, in <module>
    print(list(pool.map(double, [1, 2, 3])))
  ...
RuntimeError: 
        An attempt has been made to start a new process before the
        current process has finished its bootstrapping phase.
        ...
  ...
concurrent.futures.process.BrokenProcessPool: A process in the process pool was terminated abruptly while the future was running or pending.
```

The key line says `RuntimeError: An attempt has been made to start a new process before the current process has finished its bootstrapping phase.` (Bootstrapping means starting up.) What happened: each worker loaded the file from the top and reached the pool line, so each worker tried to start workers of its own. Without a stop that would go on for ever; Python stopped it with this error.

The guard is the stop. When Python loads your file inside a worker, the name tag is not `__main__`; it is `__mp_main__`. So the guard's lines are skipped, and only the file you started runs the pool. The rule: with processes, everything that starts workers goes under the guard. Functions and imports stay at the top. Even where a missing guard seems to work, keep it, so your code runs on every system.

### 6. Processes are not free

Starting a process means starting a whole Python, and every job travels as packed bytes. So tiny jobs lose. In this file, twenty thousand tiny jobs each square one number. Three timings: a plain loop; four processes with `pool.map`; and the same pool with `chunksize`, explained after the result. Guess the output.

```python
import time
from concurrent.futures import ProcessPoolExecutor


def square(x):
    return x * x


if __name__ == "__main__":
    numbers = range(20_000)
    start = time.perf_counter()
    [square(x) for x in numbers]
    print(f"one by one:    {time.perf_counter() - start:.3f} s")
    start = time.perf_counter()
    with ProcessPoolExecutor(4) as pool:
        list(pool.map(square, numbers))
    print(f"4 processes:   {time.perf_counter() - start:.3f} s")
    start = time.perf_counter()
    with ProcessPoolExecutor(4) as pool:
        list(pool.map(square, numbers, chunksize=2_500))
    print(f"in big chunks: {time.perf_counter() - start:.3f} s")
```

```bash
python tiny.py
```

```
one by one:    0.001 s
4 processes:   3.980 s
in big chunks: 0.075 s
```

The simple loop takes about a thousandth of a second. The pool takes more than a thousand times longer: the workers spent all their time packing and sending twenty thousand small messages. `chunksize` is the fix for part of it: instead of one message per number, `map` sends 2,500 numbers in each message (eight messages instead of twenty thousand) and the time drops a lot. But look: still far slower than the loop. This job is simply too small for processes. The rule: measure first. A job should be big compared with the cost of starting workers and sending messages.

The second cost is the data itself. This file packs a list of five million numbers the way the pool would, unpacks it again, and then adds the numbers up. Which of the three takes longest?

```python
import pickle
import time

data = list(range(5_000_000))
start = time.perf_counter()
blob = pickle.dumps(data)
took = time.perf_counter() - start
print(f"packed {len(blob) // 1_000_000} MB: {took:.2f} s")
start = time.perf_counter()
pickle.loads(blob)
took = time.perf_counter() - start
print(f"unpacked: {took:.2f} s")
start = time.perf_counter()
sum(data)
took = time.perf_counter() - start
print(f"added up: {took:.2f} s")
```

```bash
python big_data.py
```

```
packed 24 MB: 0.06 s
unpacked: 0.17 s
added up: 0.01 s
```

Packing and unpacking took many times longer than adding the numbers up. Moving the data cost far more than the work. One more limit comes from the packing: only things that pickling can pack can travel. Numbers, text, lists and dictionaries are fine. A lambda has no name to pack. Here `pool.map` receives a lambda (the real output is longer; only the key lines are shown):

```python
from concurrent.futures import ProcessPoolExecutor

if __name__ == "__main__":
    with ProcessPoolExecutor(2) as pool:
        print(list(pool.map(lambda x: x * 2, [1, 2, 3])))
```

```bash
python lambda_fail.py
```

```
Traceback (most recent call last):
  ...
_pickle.PicklingError: Can't pickle <function <lambda> at 0x105ce9170>: it's not found as __main__.<lambda>
```

`PicklingError: Can't pickle <function <lambda> ...>`. The fix is a plain function with a name, defined with `def` at the top of the file. The same call with a `def` function works:

```python
from concurrent.futures import ProcessPoolExecutor


def double(x):
    return x * 2


if __name__ == "__main__":
    with ProcessPoolExecutor(2) as pool:
        print(list(pool.map(double, [1, 2, 3])))
```

```bash
python lambda_fix.py
```

```
[2, 4, 6]
```

### 7. Processes share nothing: three safe ways to share results

Since processes share nothing, how do they work together? There are three ways. **The best way is also the plainest: return values.** Each worker returns its answer and the main program collects them. Asha's real job: how many prime numbers are there below one million? A prime divides only by 1 and itself. `is_prime` tries the divisors up to the square root, and `count_primes` counts the primes in one slice.

`primes_lib.py`:

```python
def is_prime(n):
    if n < 2:
        return False
    for d in range(2, int(n ** 0.5) + 1):
        if n % d == 0:
            return False
    return True


def count_primes(start, stop):
    found = [n for n in range(start, stop) if is_prime(n)]
    return len(found)
```

The main file cuts the range into one hundred pieces of 10,000 (the starts and the stops). The first timing uses plain `map` and `sum` with one process. The second has the same shape, with the pool:

```python
import time
from concurrent.futures import ProcessPoolExecutor

from primes_lib import count_primes

if __name__ == "__main__":
    starts = list(range(0, 1_000_000, 10_000))
    stops = [s + 10_000 for s in starts]
    begin = time.perf_counter()
    one = sum(map(count_primes, starts, stops))
    took = time.perf_counter() - begin
    print(f"one process:    {one} primes, {took:.2f} s")
    begin = time.perf_counter()
    with ProcessPoolExecutor(4) as pool:
        four = sum(pool.map(count_primes, starts, stops))
    took = time.perf_counter() - begin
    print(f"four processes: {four} primes, {took:.2f} s")
```

```bash
python primes.py
```

```
one process:    78498 primes, 2.59 s
four processes: 78498 primes, 0.83 s
```

Both find 78,498 primes: the same answer, and four processes are faster, with no locks and no sharing. (Video: 1.14 seconds against 0.43.)

**The second way is a queue**: a pipe that many processes can put things into and one can take things out of, the process version of the queue from the last lesson. Here we start the processes by hand, each puts its result in the queue, and the main program takes four results out:

```python
import multiprocessing as mp


def worker(name, queue):
    queue.put((name, len(name)))


if __name__ == "__main__":
    queue = mp.Queue()
    people = ["Asha", "Lukas", "Priya", "Meera"]
    procs = [mp.Process(target=worker, args=(p, queue))
             for p in people]
    for p in procs:
        p.start()
    results = sorted(queue.get() for _ in procs)
    for p in procs:
        p.join()
    print(results)
```

```bash
python queue_demo.py
```

```
[('Asha', 4), ('Lukas', 5), ('Meera', 5), ('Priya', 5)]
```

Four results, sorted. The order in which workers finish can change from run to run, so we sort them. Always `join` the processes at the end: `join` waits for each one to finish, as with threads.

**The third way is shared memory.** `counters.py` has two worker functions. Each adds one to a shared counter 50,000 times. The second wraps the addition in `with counter.get_lock():`.

`counters.py`:

```python
def add_unsafe(counter):
    for _ in range(50_000):
        counter.value += 1


def add_safe(counter):
    for _ in range(50_000):
        with counter.get_lock():
            counter.value += 1
```

In `shared_value.py`, `mp.Value("i", 0)` from the `multiprocessing` module makes one whole number, starting at zero, that every process can reach. `run` starts four processes, and we call it twice. The right answer is 200,000.

```python
import multiprocessing as mp

from counters import add_safe, add_unsafe


def run(target):
    counter = mp.Value("i", 0)
    procs = [mp.Process(target=target, args=(counter,))
             for _ in range(4)]
    for p in procs:
        p.start()
    for p in procs:
        p.join()
    return counter.value


if __name__ == "__main__":
    print("without a lock:", run(add_unsafe))
    print("with a lock:   ", run(add_safe))
```

```bash
python shared_value.py
```

```
without a lock: 64238
with a lock:    200000
```

Without a lock many additions were lost (the video: 61,845), the same race as the threads in module 11, lesson 3 and in the last lesson. With a lock: 200,000, exactly right. So the order to try is: return values first, a queue second, and a value with a lock only for a small shared number. A manager can also share whole lists and dictionaries between processes, but every access goes through a slow pipe, so avoid it for busy code.

### 8. Four pitfalls

**1. No guard.** You saw it: a long `RuntimeError` and a broken process pool. Put everything that starts workers under `if __name__ == "__main__":`.

**2. Tiny jobs.** Twenty thousand tiny squares took a thousandth of a second in a loop and over a second with a pool. Measure first and make each job big.

**3. Sending something that cannot be packed.** A lambda raised a `PicklingError`. Use a plain function defined at the top of the file.

**4. Expecting shared variables.** The worker's list grew to three names and mine stayed empty. If a worker must tell you something, it returns it, or puts it in a queue.

## Common mistakes

1. Starting a pool without the `if __name__ == "__main__":` guard.

2. Using processes for tiny jobs: the cost of starting and packing is bigger than the work.

3. Passing a lambda (or anything that cannot be pickled) to a pool.

4. Expecting a worker's change to a global list to show up in the main program.

5. Forgetting to `join` processes started by hand.

6. Counting on `os.cpu_count()` workers when the other programs on the machine are busy: measure.

## Clean up

Nothing to clean up. Delete the folder if you want it gone.

## Next

Next lesson: [M12-L04 · asyncio from Scratch](../m12-l04-asyncio-from-scratch/README.md). One more way to wait on many things at once, with no threads and no processes at all.

Your turn first: run the counting file with two, then eight workers; remove the guard and read the error; time the tiny jobs with different chunk sizes; and run the shared value file a few times.
