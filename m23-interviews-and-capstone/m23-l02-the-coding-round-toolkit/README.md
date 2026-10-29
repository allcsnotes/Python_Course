# M23-L02 · The Coding Round Toolkit

> Video: Module 23, Lesson 2. Watch it first, then follow along here.

## What you'll learn
- How to say how fast a solution is, in big O, and how to check it with a stopwatch
- The Python tools that make interview answers short: `sorted` with a key, `Counter`, `defaultdict`, `heapq`, `bisect`, `itertools`, `functools.cache`
- How to talk through a problem in five steps: clarify, examples, brute force, improve, test
- Three classic problems, solved live: two sum, top K frequent words, shortest way through a maze (BFS)
- The usual mistakes in a coding round, and a rough plan for a 45 minute round

## Before you start
- Python 3.14 or newer. Check with `python --version`.
- Standard library only: no packages, no Docker.
- You should know lists, dictionaries, sets and recursion (M04, M05, M09-L05). Lesson [M23-L01](../m23-l01-the-python-gotchas/) comes just before this one.
- All commands run from inside this folder.

**About the timings.** Lines that show milliseconds or microseconds come from a quiet machine, as in the video. Yours will
differ, sometimes a lot (a busy laptop can be two or three times slower). The gaps between the slow and fast versions
stay huge, and the shapes (for example "doubling the input makes the slow one about four times slower") stay the same.
Lines without timings are exactly what you will see.

## Files in this folder
| File | What it is |
|---|---|
| `growth.py` | Duplicate check, slow (two loops) versus fast (a set), timed on 1000, 2000, 4000 numbers |
| `idioms1.py` | `enumerate`, `zip`, reverse slice, palindrome |
| `sorting.py` | `sorted` with a key: stability and tuple keys |
| `collections1.py` | Anagram groups with `defaultdict`, `Counter` |
| `heap1.py` | `heapq`: `nlargest`, `nsmallest`, push and pop |
| `heap_time.py` | Top 10 of a million numbers: sort versus `nlargest` |
| `bisect1.py` | `bisect_left` and `insort` |
| `bisect_time.py` | `list.index` versus `bisect_left` on a million numbers |
| `itertools1.py` | `combinations`, `permutations`, `accumulate` |
| `memo.py` | Climbing stairs, plain recursion (millions of calls) |
| `memo_cache.py` | The same with `@cache` (35 calls) |
| `deep1.py` | The recursion limit: stairs of 5000 fails (on purpose) |
| `deep2.py` | Two fixes: `setrecursionlimit`, and a loop |
| `strings_sets.py` | Real palindrome check, set operations, `split` and `join` |
| `two_sum.py` | Problem 1: `two_sum_slow` (two loops) and `two_sum` (dictionary) |
| `ts_cases.py`, `ts_time.py` | Six test cases for two sum, and the timing |
| `topk_slow.py`, `topk.py` | Problem 2: top K words with a full sort, and with a heap |
| `topk_cases.py`, `topk_time.py` | Test cases for top K, and the timing |
| `bfs.py` | Problem 3: shortest path in a maze with breadth first search |
| `bfs_test.py` | Three maze tests |

## Follow along

### 1. The warm-up: does a list contain a duplicate?
Asha writes two correct answers. `slow` compares every number with every number after it. `fast` puts the numbers into a
set and checks whether the length shrank. The test uses numbers with no duplicate, the hardest case. Guess first: how
much faster is the set?

```bash
python growth.py
```
```
1000 6.9 0.006
2000 30.2 0.012
4000 125.8 0.019
```
Columns: number of items, slow in milliseconds, fast in milliseconds. At 4000 numbers the set version is more than six
thousand times faster. Both are correct; in an interview, only one is a good answer.

### 2. Big O in one page
Call the size of the input N. Big O asks: when N grows, how does the work grow?

Picture a party where every guest shakes hands with every other guest: 10 guests make 45 handshakes, 20 make 190, 40
make 780. Double the guests and the handshakes grow about four times. That is the slow duplicate check: O(N squared).

| Big O | Meaning | Example |
|---|---|---|
| O(1) | same work for any size | dictionary or set lookup |
| O(log N) | each step halves what is left | binary search |
| O(N) | one pass over the data | one loop; `Counter` |
| O(N log N) | what a good sort needs | `sorted` |
| O(N squared) | two nested loops | compare every pair |

Our slow timings (6.9, 30.2, 125.8 ms) are about four times more each time the input doubled: the signature of N squared.
Three honest notes: big O is about growth, not a stopwatch (for ten items everything is fast); it hides constant factors
(a sort written in C can beat a Python loop for a long time); and memory counts too (O(N) space means N extra things
stored). When unsure, say the big O and measure (M11-L04). Finish every answer with one sentence: "This runs in O(N) time
and uses O(N) extra space."

### 3. The toolbox
Eleven tools. Most are old friends; the new ones are `heapq`, `bisect` and `permutations`.

**Enumerate, zip, slices** (M05-L02, M02-L03)
```bash
python idioms1.py
```
```
1 Lukas 82
2 Priya 95
3 Asha 82
['Asha', 'Priya', 'Lukas']
['Lukas', 'Priya'] Asha
True
```

**Sorted with a key** (M05-L01). Priya and Meera both have 95 and Priya comes first in the list. Guess who is first.
```bash
python sorting.py
```
```
[('Priya', 95), ('Meera', 95), ('Lukas', 82), ('Asha', 82)]
[('Meera', 95), ('Priya', 95), ('Asha', 82), ('Lukas', 82)]
```
Sorting is stable: equal items keep their old order, even with `reverse=True`. The second line breaks ties on purpose with
a tuple key: minus the score (bigger first), then the name. One key, two rules.

**Counting and grouping** (M06-L05, M09-L05). Sorted letters make a key that all anagrams share.
```bash
python collections1.py
```
```
{'aet': ['eat', 'tea', 'ate'], 'ant': ['tan', 'nat'], 'abt': ['bat']}
True
[('l', 2)]
```
Counting is one pass, so O(N).

**The heap.** Picture a hospital waiting room: patients arrive all day, but the doctor always sees the most urgent one
next. A heap is a pile that always keeps the smallest item on top. Taking the smallest and adding an item both cost
O(log N). Python keeps a heap in an ordinary list with the module `heapq`. It is a min heap; for a max heap, push the
numbers with a minus sign.
```bash
python heap1.py
```
```
[9, 8, 5]
[1, 2]
1
1
2
[3, 5, 8, 9]
```
After pushing 5, 1, 8, 3, 9, 2 the list is `[1, 3, 2, 5, 9, 8]`: every parent is smaller than its children, so `heap[0]`
is the smallest. The rest is only partly sorted, and that is enough.

Is it worth it? The ten biggest of a million random numbers. Guess how many times faster `nlargest` is.
```bash
python heap_time.py
```
```
True
sorted 132 ms
nlargest 6 ms
```
About twenty times faster. Sorting everything is O(N log N); `nlargest` keeps a heap of only K items, so it costs
O(N log K). When K is close to N there is no gain, so just sort.

**Bisect: binary search.** On a sorted list, look at the middle, forget the half that cannot hold the target, repeat. A
million items need about twenty looks. `bisect_left` returns the place where a value is, or where it would have to go.
```bash
python bisect1.py
```
```
2
3
[9, 11, 14, 15, 18, 20]
```
Search is O(log N), but `insort` has to shift items, so it costs O(N). And the list must already be sorted.

A race on a sorted list of a million numbers, target at the very end:
```bash
python bisect_time.py
```
```
True
index 6002 microseconds
bisect 2 microseconds
```
About three thousand times faster. (A microsecond is a millionth of a second.)

**itertools** (M06-L05, M09-L05). New: `permutations`, every possible order.
```bash
python itertools1.py
```
```
[('Asha', 'Lukas'), ('Asha', 'Priya'), ('Lukas', 'Priya')]
[('Asha', 'Lukas'), ('Asha', 'Priya'), ('Lukas', 'Asha'), ('Lukas', 'Priya'), ('Priya', 'Asha'), ('Priya', 'Lukas')]
40320
[3, 4, 8, 9, 14]
```
Three pairs but six orders. Orders grow like a factorial: 8 items have 40,320, 10 items have 3,628,800, 15 items have more
than a trillion. Never try every order unless the input is tiny.

**The cache for recursion** (M04-L05, M09-L05). Stairs: you climb 1 or 2 steps at a time; in how many ways can you reach
step 35? Ways to reach step N = ways to reach N-1 plus ways to reach N-2. Guess how many calls.
```bash
python memo.py
```
```
14930352 18454929 calls
0.69 seconds
```
The same small questions are asked again and again. Now `memo_cache.py` has one extra line, `@cache`, above the `def`:
```bash
python memo_cache.py
```
```
14930352 35 calls
0.05 milliseconds
```
Same answer, only 35 calls. The cost went from exponential to O(N), and the notebook takes O(N) memory.

**The recursion limit.** Python allows about 1000 nested calls. Guess what the last line of `deep1.py` does.
```bash
python deep1.py
```
```
1000
105 digits
Traceback (most recent call last):
  File "deep1.py", line 12, in <module>
    print(len(str(stairs(5000))), "digits")
                  ~~~~~~^^^^^^
  File "deep1.py", line 8, in stairs
    return stairs(n - 1) + stairs(n - 2)
           ~~~~~~^^^^^^^
  [Previous line repeated 996 more times]
RecursionError: maximum recursion depth exceeded
```
(The file path in the traceback is your own folder. The video trimmed the repeated lines; the error is meant to happen.)

Two fixes in `deep2.py`: `sys.setrecursionlimit(20000)` raises the limit (but every frame uses memory and a limit that
is too high can crash Python itself on some systems), and a loop with two variables `a` and `b` (no recursion, no limit,
O(1) memory).
```bash
python deep2.py
```
```
1045 digits
True
```
Say both in an interview: recursion with a cache is easy to read; a loop is safest for big inputs.

**Strings and sets** (M02-L03, M05-L04)
```bash
python strings_sets.py
```
```
amanaplanacanalpanama
True
['Lukas', 'Meera'] ['Asha', 'Priya'] 5
4 ['a', 'b', 'c'] a-b-c
```
For a real palindrome, clean the text first (`isalnum`, lower case). `&` is who is in both, `-` who is only in mine, `|`
everybody. Sets have no order, so the lists were sorted before printing.

**The toolbox on one card.** Sets and dictionaries look up in O(1). A heap pushes and pops in O(log N); `bisect` searches
in O(log N). Sorting is O(N log N). A `Counter` counts in one pass. A `deque` has two fast ends. The cache turns repeated
work into one answer per input.

### 4. How to talk: five steps
1. **Clarify.** Ask about the input and what to return.
2. **Examples.** Work a small one by hand, out loud.
3. **Brute force first.** Say the simple answer and its big O, even if it is slow.
4. **Improve.** Find what is repeated, and ask which tool removes it.
5. **Test.** Run the examples and the edge cases: empty, one item, duplicates, negatives.

### 5. Problem 1: two sum
Rahul: "Here is a list of numbers and a target. Return the positions of two numbers that add up to the target." Asha
clarifies: the same item may not be used twice; at most one answer; numbers can be negative; if there is no answer, return
an empty list. By hand: `[2, 7, 11, 15]` with target 9 gives positions 0 and 1; `[3, 3]` with target 6 gives 0 and 1.

**Brute force** (`two_sum_slow` in `two_sum.py`): try every pair. Two loops: O(N squared) time, O(1) extra space.

**Improve:** for every number we search the rest of the list for its partner (`target - number`). Searching a list is
O(N), but a dictionary lookup is O(1). So walk once and remember every number seen, and its position (`two_sum`). We check
before we store, so an item can never pair with itself.

Test with six cases, guess the last two first:
```bash
python ts_cases.py
```
```
[0, 1]
[1, 2]
[0, 1]
[2, 4]
[]
[]
```
Then measure, on 5000 numbers with no answer (the worst case), best of three runs:
```bash
python ts_time.py
```
```
two_sum_slow 216.34 ms
two_sum 0.2 ms
```
About a thousand times faster. Say it: O(N) time because of one pass, O(N) space because the dictionary can hold every
number. We traded memory for time, the heart of many interview answers.

### 6. Problem 2: top K frequent words
Rahul: "Given a list of words and a number K, return the K words that appear most often." Ties: alphabetical order. If K
is bigger than the number of different words, return all. Example: "the cat and the dog and the bird saw a cat" with K=2
gives `the`, `and` (`and` before `cat`).

**Brute force** (`top_k_sorted`): count with a `Counter`, sort every different word by (minus count, word), cut K. With M
different words: O(N) to count, O(M log M) to sort.

**Improve** (`top_k`): we sort M words but need only K. `heapq.nsmallest(k, counts, key=...)` with the same tuple key
keeps a heap of only K items: O(M log K).
```bash
python topk_cases.py
```
```
['the', 'and']
['the', 'and', 'cat', 'a', 'bird', 'dog', 'saw']
[]
```
```bash
python topk_time.py
```
```
top_k_sorted 343 ms
top_k 163 ms
```
(One million words, 200,000 different, K=10.) About twice as fast. Honest note: most of that time is the counting, the same
in both, so the gain is smaller than for the sort step alone. Big O: O(N) to count plus O(M log K) to select, O(M) space.

### 7. Problem 3: the shortest way through a maze
Rahul draws a grid: `S` start, `G` goal, `#` walls. Move up, down, left or right, one step at a time, never through a
wall. Return the fewest steps, or -1 if there is no way. No diagonals; if the start is the goal, the answer is 0.

**Brute force:** try every path with recursion and keep the shortest. The number of paths grows exponentially, and you
must avoid walking in circles. Say that, and move on.

**Improve:** think of a stone dropped in a pond. The ripple reaches every cell one step away, then two, then three. The
first time it reaches `G` is the fewest steps. This is breadth first search (BFS). It needs a queue, first in first out;
Python's queue is `collections.deque`, because `popleft()` is fast. `seen` is a set so we never go round in circles. We
mark a cell as seen when we add it, not when we take it out, or the same cell enters the queue many times.

```bash
python bfs_test.py
```
```
15
0
-1
```
Fifteen steps for the maze in the file, 0 when start equals goal, -1 when a wall blocks the way (`["S#G"]`). Big O: every
cell is queued at most once, so time and space are both O(rows times columns). With a list instead of a `deque`, `pop(0)`
shifts all items and is much slower (M09-L05). Also check the edges of the grid before you read a cell.

## Interview tip
Rahul: "You are given a problem you have never seen. What do you do in the first five minutes?" A good answer: do not
start with code. Repeat the problem in your own words, ask about input, output and edge cases, work a small example by
hand, state the brute force and its big O, and ask what is repeated that a dictionary, a heap or sorting could remove. Then
write the code, test it with an empty input and a tiny one, and finish with time and space.

A rough plan for a 45 minute round: 5 minutes to clarify and work examples, 5 for the brute force and its cost, 15 to write
the better answer, 10 to test and fix, the rest for the interviewer's questions. Guides, not rules.

## Common mistakes
1. Jumping into code in silence.
2. Asking no questions, and solving a different problem.
3. Skipping the brute force, so the interviewer never sees your reasoning.
4. Never testing. An empty list finds most bugs.
5. Claiming the wrong big O.
6. Trying every order (`permutations`) on anything but a tiny input.
7. Marking a BFS cell as seen when you take it out of the queue instead of when you add it.
8. Using a `list` as a queue (`pop(0)`) instead of a `deque`.

If you are stuck, say what you know, say what you tried, and ask for a hint. A hint is not a failure. It is a conversation.

## Try it yourself
1. Group the anagrams again, and print the biggest group first.
2. Return the three cheapest prices with `heapq`.
3. Change the maze so diagonal moves are allowed, then check the answer by hand.

For each one, say the big O out loud. (Answers are not given: you can check them by running your code on the lists and the
maze above.)

## Clean up
Nothing to clean up. The files only print to the screen. (Delete a `__pycache__` folder if Python made one.)

## Next
[M23-L03 · The Backend Interview Round](../m23-l03-the-backend-interview-round/)
