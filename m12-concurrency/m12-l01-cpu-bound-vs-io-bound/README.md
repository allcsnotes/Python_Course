# M12-L01 · CPU-Bound vs IO-Bound

> Video: Module 12, Lesson 1. Watch it first, then follow along here.

## What you'll learn

- The two kinds of slow: waiting (I/O-bound) and computing (CPU-bound)
- How to read two clocks, `time.perf_counter()` (wall) and `time.process_time()` (CPU), to tell them apart
- How to use the busy share (CPU time divided by wall time) and what to do when a job is a mix
- How to sort real jobs into waiting or computing
- A map of which tool to use in the rest of the module: processes, threads or asyncio

## Before you start

- Python 3.14 or newer. Check with `python --version`.
- No Docker needed.
- [M11-L04 · Measuring and Improving Speed](../../m11-python-under-the-hood/m11-l04-measuring-and-improving-speed/README.md) and [M11-L03](../../m11-python-under-the-hood/m11-l03-the-gil-and-free-threaded-python/README.md) (the GIL).
- **Timings depend on your computer.** All seconds below come from one real run on one Mac, so yours will differ (and the video's numbers differ again), especially the last step, which uses all your cores. The pattern (equal wall times, busy 100% against 0%, about the middle for a mixed job) will be the same.

## Files in this folder

| File | What it is |
|------|------------|
| `jobs.py` | The two slow jobs: `build_report` (computing) and `check_pages` (waiting) |
| `stopwatch.py` | Times both jobs with the wall clock only |
| `two_clocks.py` | Times both jobs with two clocks and prints the busy share |
| `clocks.py` | The `measure` function with two clocks, as a module |
| `receipts.py` | A mixed job: fetch payments (wait), draw receipts (compute) |
| `taste.py` | A first taste of threads, processes and asyncio on the two kinds of job |

## Follow along

### 1. The hook: two slow jobs that look alike

Asha's allcsvideos.com has two slow jobs in `jobs.py`. `build_report` adds up a huge pile of numbers one by one (a stand-in for building the weekly report: pure computing). `check_pages` visits four course pages and, for each one, waits half a second (`sleep` is the stand-in for waiting on a slow server, as in module 11). `stopwatch.py` times both with the `perf_counter` clock from module 5. A teammate says: just add more workers. First, a simpler question. How different will the two stopwatch times be?

```python
import time


def build_report():
    total = 0
    for n in range(140_000_000):
        total += n


def check_pages():
    for page in range(4):
        time.sleep(0.5)
```

```python
import time
from jobs import build_report, check_pages


def measure(name, job):
    start = time.perf_counter()
    job()
    wall = time.perf_counter() - start
    print(f"{name}: wall {wall:.2f} s")


measure("build_report", build_report)
measure("check_pages", check_pages)
```

```bash
python stopwatch.py
```

```
build_report: wall 3.60 s
check_pages: wall 2.01 s
```

Almost the same. The stopwatch sees two slow jobs and cannot tell them apart. But these are opposite problems. One job is busy every single moment; the other does nothing at all. The right fix for one is the wrong fix for the other. To tell them apart you need a second clock.

### 2. Laundry day: two kinds of slow

Laundry day, four loads. **Washing is a waiting job**: you put a load in the machine, press start, and the machine does the work, so you are free to do something else. All four loads can wash at the same time: you start the first machine, then the second, the third, the fourth. You did not need four people; you only needed to stop standing there staring at one machine. **Folding is a doing job**: nothing happens unless your hands are moving. Starting more machines does not help at all. Only more people with more hands make the folding finish sooner.

Programs have the same two kinds of slow. A job that spends its time waiting (for a server, a file or a database) is **I/O-bound**: its limit is the waiting. A job that spends its time computing, with the processor busy every moment, is **CPU-bound**: its limit is how fast the processor can work (counting, sorting, drawing and compressing). The cures are different. For waiting, you do other things while you wait. For computing, you need more hands: more processor cores all working at the same moment. That is the whole module in two sentences.

### 3. Two clocks: wall and CPU

How do we tell which kind of job we have? We read two clocks. The **wall clock** is the clock on the wall: how much real time went by, from start to finish, whatever the computer was doing. The **CPU clock** counts only the seconds the processor was really working on your program. A cook: the wall clock shows how long dinner took; the CPU clock shows how long the cook's hands were actually busy. While your program waits, the CPU clock stands still, so the gap between the two clocks is exactly the waiting.

Python gives you both in the `time` module: `time.perf_counter()` reads the wall clock and `time.process_time()` reads the CPU clock. Divide the CPU time by the wall time and you get a **busy share**: 100 percent means computing the whole time, 0 percent means waiting the whole time. Here is the same `measure` function with a second clock. What will the CPU clock say for `build_report`? And for `check_pages`, which only sleeps?

```python
import time
from jobs import build_report, check_pages


def measure(name, job):
    wall_start = time.perf_counter()
    cpu_start = time.process_time()
    job()
    wall = time.perf_counter() - wall_start
    cpu = time.process_time() - cpu_start
    busy = cpu / wall * 100
    print(f"{name}: wall {wall:.2f} s, cpu {cpu:.2f} s, busy {busy:.0f}%")


measure("build_report", build_report)
measure("check_pages", check_pages)
```

```bash
python two_clocks.py
```

```
build_report: wall 2.98 s, cpu 2.58 s, busy 87%
check_pages: wall 2.02 s, cpu 0.00 s, busy 0%
```

`build_report`: the CPU time is about the same as the wall time, busy 100%. The processor worked the entire time. `check_pages`: wall about 2 seconds, CPU 0.00, busy 0%. The program waited the whole time and the processor did nothing for it. Same wall time as in the hook, two completely different stories. Near 100%: CPU-bound. Near 0: I/O-bound. And sleep is not special: a real wait for a server, a database or a disk looks the same, with the wall clock running and the CPU clock standing still.

### 4. Mixed jobs: split and measure each half

Real jobs are often both. `make_receipts` first asks the payment service for the payments and waits, then draws the receipts, which is computing. The `measure` function now lives in its own file, `clocks.py` (module 7), and at the bottom of `receipts.py` we measure the whole job and then each half on its own. How busy will `make_receipts` be: mostly waiting, mostly computing, or somewhere in the middle?

`clocks.py`:

```python
import time


def measure(name, job):
    wall_start = time.perf_counter()
    cpu_start = time.process_time()
    job()
    wall = time.perf_counter() - wall_start
    cpu = time.process_time() - cpu_start
    busy = cpu / wall * 100
    print(f"{name}: wall {wall:.2f} s, cpu {cpu:.2f} s, busy {busy:.0f}%")
```

```python
import time
from clocks import measure


def fetch_payments():
    time.sleep(1.5)


def draw_receipts():
    sum(range(400_000_000))


def make_receipts():
    fetch_payments()
    draw_receipts()


measure("make_receipts", make_receipts)
measure("fetch_payments", fetch_payments)
measure("draw_receipts", draw_receipts)
```

```bash
python receipts.py
```

```
make_receipts: wall 4.49 s, cpu 2.17 s, busy 48%
fetch_payments: wall 1.50 s, cpu 0.00 s, busy 0%
draw_receipts: wall 2.30 s, cpu 2.08 s, busy 90%
```

Right in the middle (about half). Neither kind. A number in the middle is a clue, not an answer: some of the job waits and some of it computes. So we look at the halves: `fetch_payments` busy 0%, `draw_receipts` busy 100%. A mixed job is really two jobs glued together. The waiting half can overlap with other work; the computing half needs more cores. Different halves, different cures. So the habit is: measure the whole job, and if the busy share is in the middle, measure each stage and fix the biggest one. Never guess which half hurts.

### 5. Practice: waiting or computing?

Six jobs from allcsvideos.com. For each one decide: waiting or computing? (1) Send a welcome email to a new student. (2) Shrink a thousand course thumbnails. (3) Ask the payment service if a payment went through. (4) Sort a million enrollments by date. (5) Download a lesson file from the storage server. (6) Compress a lesson video file. Pause and decide.

Answers: the email, the payment check and the download all **wait** (I/O-bound). The thumbnails, the sorting and the compressing all **compute** (CPU-bound). A rule of thumb: if the job needs another computer or a disk to answer, it waits; if it needs only your own processor, it computes. But a rule of thumb is a guess. When it matters, read the two clocks.

### 6. A map for the rest of the module

Start with the measurement. Read the busy share: near 100%, computing; near 0, waiting; in the middle, split the job and measure each half. **Computing** needs more cores working together: that is **processes**, lesson 3 (remember M11-L03: threads do not speed up counting on normal Python). **Waiting with a handful of tasks** wants **threads**, lesson 2. **Waiting with a huge number of tasks**, like a busy server with thousands of connections, wants **asyncio**, lessons 4 and 5.

`taste.py` gives a first taste of all three on the two kinds of job: ten pages of half a second each, one by one and in threads; four reports one by one, in threads and in processes; and a thousand waits of half a second all at once with asyncio. Do not worry about the code, each later lesson does it properly:

```python
import asyncio
import time
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor


def check_page(n):
    time.sleep(0.5)


def build_report(n):
    total = 0
    for i in range(35_000_000):
        total += i


async def check_page_async(n):
    await asyncio.sleep(0.5)


async def many(count):
    await asyncio.gather(*(check_page_async(n) for n in range(count)))


def timed(label, fn):
    start = time.perf_counter()
    fn()
    print(f"{label}: {time.perf_counter() - start:.2f} s")


if __name__ == "__main__":
    pages = range(10)
    jobs = range(4)
    timed("10 pages, one by one", lambda: [check_page(n) for n in pages])
    with ThreadPoolExecutor(10) as pool:
        timed("10 pages, threads", lambda: list(pool.map(check_page, pages)))
    timed("4 reports, one by one", lambda: [build_report(n) for n in jobs])
    with ThreadPoolExecutor(4) as pool:
        timed("4 reports, threads", lambda: list(pool.map(build_report, jobs)))
    with ProcessPoolExecutor(4) as pool:
        timed("4 reports, processes", lambda: list(pool.map(build_report, jobs)))
    timed("1000 pages, asyncio", lambda: asyncio.run(many(1000)))
```

```bash
python taste.py
```

```
10 pages, one by one: 5.03 s
10 pages, threads: 0.51 s
4 reports, one by one: 3.15 s
4 reports, threads: 2.74 s
4 reports, processes: 1.11 s
1000 pages, asyncio: 0.51 s
```

Waiting: threads (and asyncio) turn many half-second waits into about half a second in total. Computing: threads do not help (a little worse than one by one), processes do (they use several cores; how much faster depends on how many fast cores you have). These numbers are only a taste, from a computer with other programs running, so yours will differ. One rule from module 11, lesson 4 still holds: if the program is already fast enough, stop.

### 7. Three pitfalls

**1. Judging a job by how the code looks.** `build_report` and `check_pages` are both a short loop, yet one is busy 100% of the time and the other 0%. Code that looks alike can be the opposite kind. Measure.

**2. Reading only the CPU clock.** `check_pages` shows CPU 0.00, which looks wonderful, but a student waited two seconds. The CPU clock hides waiting. Always read both clocks.

**3. The wrong cure for the kind.** Four threads on the computing job took slightly longer than one by one (see the `taste.py` output). No gain. Match the tool to the kind.

## Common mistakes

1. Judging a job by how its code looks instead of measuring.

2. Reading only the CPU clock: it hides waiting.

3. Using threads for a computing job, or processes for a handful of waits.

4. Optimising a job that is already fast enough.

## Clean up

Nothing to clean up. Delete the folder if you want it gone.

## Next

Next lesson: [M12-L02 · Threads](../m12-l02-threads/README.md). You have met threads twice already. Now you will use them properly, speed up a real waiting job, and add the lock that module 11 promised.

Your turn first: run `two_clocks.py` on a function of your own, change the sleep to one second and watch the two clocks, measure the halves of a script you wrote, and sort the six jobs again for a project of yours.
