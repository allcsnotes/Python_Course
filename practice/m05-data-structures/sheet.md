# Module 05 · Practice Sheet: 25 Data Structure Exercises

Write each program yourself before you open the answer. Every exercise is a small Python file you can run in the terminal. The exercises use Module 5 (lists, tuples, dictionaries, sets, comprehensions, names and mutability) and may also use anything from Modules 1 to 4.

**How to work:**
- Use **Python 3.14** (check with `python --version`; on Mac or Linux the command may be `python3`).
- Put each program in its own file, `Ex01.py` to `Ex25.py`. Run it with **`python Ex01.py`**.
- The exercises use the allcsvideos platform and its cast: Asha, Lukas, Priya, Meera and Rahul (plus Sofia, Arjun, Mia and Chen as extra students). Money is written as **Rs**.
- They go from easy to harder, **about four per lesson**. Some are **predict the output** (guess on paper first, then run), some are **fix the broken code** (read the error, or the wrong output, then repair it), and some build a small program.
- Each answer has a hint, a short explanation, a full solution, and the **real output** from running it with Python 3.14. Open the hint first, and only then the solution.
- All 25 solutions are in the folder **`solutions/`** next to this sheet. Run them with `python Ex07.py` from inside that folder.
- None of the exercises read from the keyboard, so nothing needs typing while a program runs.
- Where a set holds text, the solutions print `sorted(...)` of it, because Python does not promise any order inside a set.

---


## M05 · L01 Lists

### 1 · The course playlist
Asha is planning the lesson order for a new allcsvideos course. Make a list called `playlist` that starts with three lessons: `"Intro"`, `"Variables"`, `"Loops"`. Then change it step by step, and print the list after every step with a short heading:

1. `append` the lesson `"Functions"` at the end
2. `insert` the lesson `"Setup"` at position 1 (right after `"Intro"`)
3. `extend` it with two more lessons at once: `"Lists"` and `"Tuples"`
4. print how many lessons there are (`len`), the first lesson and the last lesson (use `[0]` and `[-1]`)
5. rename the first lesson to `"Welcome"` by assigning to `playlist[0]`, and print it

**Expected output:**

```text
Start: ['Intro', 'Variables', 'Loops']
After append: ['Intro', 'Variables', 'Loops', 'Functions']
After insert: ['Intro', 'Setup', 'Variables', 'Loops', 'Functions']
After extend: ['Intro', 'Setup', 'Variables', 'Loops', 'Functions', 'Lists', 'Tuples']
Count: 7
First: Intro
Last: Tuples
Renamed first: Welcome
```

### 2 · Predict the output (indexes, slices and methods)
**Write your guesses first.** The label `marks` holds Lukas's quiz marks. Predict what each of the 13 `print` lines shows (some print more than one thing, and the list changes as the file runs).

```python
marks = [40, 85, 70, 55, 90, 70]
print(marks[0], marks[-1])
print(marks[1:4])
print(marks[:2], marks[4:])
print(marks[::2])
print(marks[::-1])
print(marks[2:100])
print(len(marks), marks.count(70), marks.index(70))
print(85 in marks, 100 in marks, 100 not in marks)
last = marks.pop()
print(last, marks)
first = marks.pop(0)
print(first, marks)
marks.remove(70)
print(marks)
del marks[1]
print(marks)
print(marks + [1, 2], [0] * 3)
```

Run it and mark your wrong guesses. Draw the list as boxes numbered 0 to 5 if you get stuck on a slice.

### 3 · Fix the broken list code
Meera sent five tiny files about lists. Run each one and read what happens. Files a, b, d and e crash; file c does **not** crash but prints something strange. Fix them all, then put the repaired versions in one file.

```python
# file a
scores = [70, 80, 90]
print(scores[3])
```
```python
# file b
names = ["Asha", "Lukas"]
names.remove("Priya")
print(names)
```
```python
# file c
marks = [3, 1, 2]
result = marks.sort()
print(result)
```
```python
# file d
guests = ["Asha"]
guests = guests + "Rahul"
print(guests)
```
```python
# file e
team = ["Asha"]
team.append("Lukas", "Meera")
print(team)
```

What Python says:

```text
a: IndexError: list index out of range
b: ValueError: list.remove(x): x not in list
c: (no error) prints   None
d: TypeError: can only concatenate list (not "str") to list
e: TypeError: list.append() takes exactly one argument (2 given)
```

**Goal after fixing all five** (put the repaired versions in one file, in the same order):

```text
90
Priya is not enrolled
['Asha', 'Lukas']
[1, 2, 3]
['Asha', 'Rahul']
['Asha', 'Lukas', 'Meera']
```

### 4 · Sorting the ratings
Students rate allcsvideos courses. Given these two lists:

```python
ratings = [4.5, 3.8, 4.9, 4.1, 3.2]
courses = ["Python", "SQL", "Go", "Docker", "Spring Boot"]
```

Print, with these headings:

1. `sorted(ratings)`, and then the original `ratings` to show it did **not** change
2. sort `ratings` **in place**, biggest first (`sort(reverse=True)`), and print it
3. the best and worst rating (`max`, `min`) and the average rounded to 2 decimals (`sum` and `len`)
4. the courses A to Z, the courses sorted by name length (`key=len`), and the courses sorted by their **last letter** (`key=lambda name: name[-1]`)
5. the courses backwards with a slice (`courses[::-1]`), and then `courses` again to show the slice did not change it

**Expected output:**

```text
sorted(): [3.2, 3.8, 4.1, 4.5, 4.9]
original: [4.5, 3.8, 4.9, 4.1, 3.2]
sort(reverse=True): [4.9, 4.5, 4.1, 3.8, 3.2]
Best: 4.9 Worst: 3.2
Average: 4.1
A to Z: ['Docker', 'Go', 'Python', 'SQL', 'Spring Boot']
By length: ['Go', 'SQL', 'Python', 'Docker', 'Spring Boot']
By last letter: ['SQL', 'Python', 'Go', 'Docker', 'Spring Boot']
Backwards: ['Spring Boot', 'Docker', 'Go', 'SQL', 'Python']
Courses still: ['Python', 'SQL', 'Go', 'Docker', 'Spring Boot']
```

### 5 · Top marks, zeros removed
Rahul's quiz marks contain zeros for quizzes he skipped:

```python
raw = [0, 72, 95, 0, 88, 61, 95]
```

1. Write a function `best_marks(marks, n=3)` that returns the `n` highest **non-zero** marks, biggest first. Use a loop with `append` to collect the non-zero marks, then `sort(reverse=True)` and a slice. The function must **not** change the list it receives.
2. Print the result for the default `n`, for `n=2`, and for `n=10` (more than exist).
3. Print `raw` again to show it is unchanged.
4. Now clean `raw` **in place**: `while 0 in raw:` remove a zero. Print the cleaned list.

**Expected output:**

```text
Raw: [0, 72, 95, 0, 88, 61, 95]
Top 3: [95, 95, 88]
Top 2: [95, 95]
Top 10: [95, 95, 88, 72, 61]
Raw after: [0, 72, 95, 0, 88, 61, 95]
Cleaned in place: [72, 95, 88, 61, 95]
```


## M05 · L02 Tuples and Unpacking

### 6 · Predict the output (tuples and unpacking)
**Write your guesses first.** Predict every line this file prints (it prints 15 lines).

```python
point = (3, 4)
print(point, type(point), len(point))
print(point[0], point[-1])
single = (5,)
not_a_tuple = (5)
print(type(single), type(not_a_tuple))
x, y = point
print(x + y)
a, b = 1, 2
a, b = b, a
print(a, b)
first, *middle, last = [10, 20, 30, 40, 50]
print(first, middle, last)
cheapest, *others = (499, 999, 1499)
print(cheapest, others)
empty = ()
print(type(empty), len(empty))
titles = ("Python", "SQL", "Docker")
prices = (1499, 999, 799)
for number, title in enumerate(titles, start=1):
    print(number, title)
for title, price in zip(titles, prices):
    print(title, price)
print(point == (3, 4), point == [3, 4])
```

Run it. Pay special attention to line 3 of the output (what makes a tuple?), the star line, and the two loops (`enumerate` and `zip`).

### 7 · Fix the broken tuple code
Four more broken files. Files a, c and d crash; file b does not crash but gives the wrong kind of thing. Fix them and put the repaired versions in one file.

```python
# file a
course = ("Python", 1499)
course[1] = 999
print(course)
```
```python
# file b
one = ("Asha")
print(type(one))
```
```python
# file c
name, price = ("Python", 1499, 12)
print(name, price)
```
```python
# file d
students = ("Lukas", "Asha")
students.sort()
print(students)
```

What Python says:

```text
a: TypeError: 'tuple' object does not support item assignment
b: (no error) prints   <class 'str'>
c: ValueError: too many values to unpack (expected 2, got 3)
d: AttributeError: 'tuple' object has no attribute 'sort'
```

**Goal after fixing all four:**

```text
('Python', 999)
<class 'tuple'>
Python 1499 12
['Asha', 'Lukas']
```

### 8 · Many answers from one function
Lukas wants a small report on a list of marks, and the function must give back **three answers at once**.

```python
marks = [72, 95, 88, 61, 79]
names = ["Asha", "Lukas", "Priya"]
scores = [92, 78, 85]
```

1. Write `summarise(marks)` that returns the lowest mark, the highest mark and the average rounded to 1 decimal, all in one `return`.
2. Call it and unpack the answers into `lowest, highest, average`, then print them. Also print what you get **without** unpacking, and its `type`.
3. Loop over `names` and `scores` together with `for name, score in zip(names, scores):` and print each line as the name padded to width 8 followed by the score right-aligned in width 4.
4. Sort the pairs by score, biggest first: `ranking = sorted(zip(names, scores), key=lambda pair: pair[1], reverse=True)`. Unpack with `winner, *others = ranking` and print both.
5. Print the ranking with places: `for place, pair in enumerate(ranking, start=1):` and print the place, then the name (`pair[0]`), then the score (`pair[1]`).
6. Two students swap seats: `seat_a = "Asha"`, `seat_b = "Lukas"`. Swap them in one line and print both.

**Expected output:**

```text
Lowest: 61 Highest: 95 Average: 79.0
(61, 95, 79.0) <class 'tuple'>
Asha      92
Lukas     78
Priya     85
Winner: ('Asha', 92)
Others: [('Priya', 85), ('Lukas', 78)]
1 Asha 92
2 Priya 85
3 Lukas 78
Lukas Asha
```


## M05 · L03 Dictionaries

### 9 · A student record
Priya's profile on allcsvideos is a dictionary. Do these steps and print after each:

1. Create `student = {"name": "Asha", "course": "Python", "lessons_done": 12}` and print it
2. Print the name and the lessons done by looking up their keys
3. Change `lessons_done` to 13 and add a new key `email` with the value `"asha@mail.com"`. Print the whole dictionary
4. `pop` the email (print what pop gave back), then `del` the key `course`. Print the dictionary and its `len`
5. Print whether `"name"` is in the dictionary and whether `"Asha"` is in it

**Expected output:**

```text
{'name': 'Asha', 'course': 'Python', 'lessons_done': 12}
Asha 12
{'name': 'Asha', 'course': 'Python', 'lessons_done': 13, 'email': 'asha@mail.com'}
Removed: asha@mail.com
{'name': 'Asha', 'lessons_done': 13} 2
True False
```

### 10 · Predict the output (dictionaries)
**Write your guesses first.** Predict every line this file prints (the loops print several lines each).

```python
prices = {"Python": 1499, "SQL": 999, "Docker": 799}
print(prices["SQL"])
print(prices.get("Docker"), prices.get("Go"), prices.get("Go", 0))
print("SQL" in prices, 999 in prices, "Go" not in prices)
prices["SQL"] = 899
prices["Go"] = 699
print(prices)
print(prices.pop("Python"))
print(len(prices))
del prices["Go"]
print(prices)
for course, price in prices.items():
    print(course, "->", price)
for price in prices.values():
    print(price)
for key in prices:
    print(key)
nested = {"Asha": {"marks": [80, 90]}}
print(nested["Asha"]["marks"][-1])
counts = {}
counts["a"] = counts.get("a", 0) + 1
counts["a"] = counts.get("a", 0) + 1
print(counts)
```

Run it. The `get` line, the `in` line and the `pop` line are the ones people usually get wrong.

### 11 · Fix the broken dictionary code
Five broken files. Files a to d crash; file e does not crash but quietly loses data. Fix them and put the repaired versions in one file.

```python
# file a
student = {"name": "Asha"}
print(student["email"])
```
```python
# file b
course_key = ["python", 3]
prices = {course_key: 1499}
print(prices)
```
```python
# file c
scores = {"Asha": 80, "Lukas": 40, "Rahul": 65}
for name in scores:
    if scores[name] < 50:
        del scores[name]
print(scores)
```
```python
# file d
student = {"name": "Asha", "city": "Pune"}
for key, value in student:
    print(key, "=", value)
```
```python
# file e
prices = {"python": 1499, "python": 1299}
print(prices, len(prices))
```

What Python says:

```text
a: KeyError: 'email'
b: TypeError: cannot use 'list' as a dict key (unhashable type: 'list')
c: RuntimeError: dictionary changed size during iteration
d: ValueError: too many values to unpack (expected 2)
e: (no error) prints   {'python': 1299} 1
```

**Goal after fixing all five:**

```text
no email
{('python', 3): 1499}
{'Asha': 80, 'Rahul': 65}
name = Asha
city = Pune
{'python': 1499, 'python_advanced': 1299} 2
```

### 12 · Count the votes
Lukas ran a poll: which course should allcsvideos make next? The votes arrived as a list.

```python
votes = ["Python", "Docker", "Python", "SQL", "Python", "Docker", "Go", "SQL", "Python"]
```

1. Build a dictionary `tally` of how many votes each course got. Start with an empty `{}` and use `tally[choice] = tally.get(choice, 0) + 1` inside a loop. Print `tally`.
2. Sort the pairs from most to fewest votes: `by_votes = sorted(tally.items(), key=lambda pair: pair[1], reverse=True)`.
3. The first pair is the winner. Unpack it with `winner, count = by_votes[0]` and print the winner with its vote count.
4. Print every course, one line each: the course name padded to width 8, then one `#` per vote, then a space and the count.
5. Count the letters of the word `"banana"` the other way, with an `if letter in counts:` / `else:` check instead of `get`, and print the dictionary.

**Expected output:**

```text
{'Python': 4, 'Docker': 2, 'SQL': 2, 'Go': 1}
Winner: Python with 4 votes
Python  #### 4
Docker  ## 2
SQL     ## 2
Go      # 1
{'b': 1, 'a': 3, 'n': 2}
```

### 13 · The nested catalog
The allcsvideos catalog is a dictionary of dictionaries.

```python
catalog = {
    "Python": {"price": 1499, "lessons": 104, "tags": ["beginner", "backend"]},
    "SQL": {"price": 999, "lessons": 30, "tags": ["data"]},
    "Docker": {"price": 799, "lessons": 25, "tags": ["devops"]},
}
```

1. Print the Python price, and the first tag of Python (`catalog["Python"]["tags"][0]`).
2. Add a new course `"Git"` with price 499, 12 lessons and an empty tag list. Take Rs 100 off the SQL price with `-=`, and `append` the tag `"popular"` to Python's tags.
3. Loop with `for slug, info in catalog.items():` and print one line per course, e.g. `Python   Rs  1499  104 lessons  tags=['beginner', 'backend', 'popular']` (name padded to width 8, price right-aligned in 5, lessons right-aligned in 3).
4. Add up all prices with a loop over `catalog.values()` and print the total.
5. Group students by course. From the list `enrolments`, build `by_course`, a dictionary from course to a **list of student names**. For each pair, if the course is not yet a key, first set it to an empty list, then `append` the name. Print it.
6. Print the price of a course that does not exist using `catalog.get("Go", {}).get("price", "not sold")`.

```python
enrolments = [("Asha", "Python"), ("Lukas", "SQL"), ("Priya", "Python"),
              ("Meera", "Git"), ("Rahul", "Python")]
```

**Expected output:**

```text
1499
beginner
Python   Rs  1499  104 lessons  tags=['beginner', 'backend', 'popular']
SQL      Rs   899   30 lessons  tags=['data']
Docker   Rs   799   25 lessons  tags=['devops']
Git      Rs   499   12 lessons  tags=[]
Whole catalog: Rs 3696
{'Python': ['Asha', 'Priya', 'Rahul'], 'SQL': ['Lukas'], 'Git': ['Meera']}
not sold
```


## M05 · L04 Sets

### 14 · Predict the output (sets)
**Write your guesses first.** Predict every line this file prints. Where a set holds text, the file uses `sorted(...)` because Python does not promise any order inside a set.

```python
a = {1, 2, 3, 3, 2}
print(a, len(a))
b = {3, 4, 5}
print(a | b, a & b, a - b, b - a, a ^ b)
print(a.union(b), a.intersection(b), a.difference(b), a.symmetric_difference(b))
print(2 in a, 9 in a, 9 not in a)
a.add(10)
a.add(1)
print(sorted(a))
a.discard(99)
a.remove(10)
print(sorted(a))
print(type({}), type(set()), type({1}))
log = ["Lukas", "Priya", "Lukas", "Asha", "Priya"]
print(len(log), len(set(log)), sorted(set(log)))
print(len(set([1, 1, 1, 2])))
print(sorted({"Mia", "Chen"} | {"Sofia"}))
```

Run it. Remember: `{}` on its own is **not** an empty set.

### 15 · Fix the broken set code
Five broken files, and all five crash. Fix them and put the repaired versions in one file.

```python
# file a
viewers = {}
viewers.add("Asha")
print(viewers)
```
```python
# file b
tags = {"b", "a"}
print(tags[0])
```
```python
# file c
points = {[1, 2], 3}
print(len(points))
```
```python
# file d
s = {1, 2}
s.remove(5)
print(s)
```
```python
# file e
print({1, 2} + {3})
```

What Python says:

```text
a: AttributeError: 'dict' object has no attribute 'add'
b: TypeError: 'set' object is not subscriptable
c: TypeError: cannot use 'list' as a set element (unhashable type: 'list')
d: KeyError: 5
e: TypeError: unsupported operand type(s) for +: 'set' and 'set'
```

**Goal after fixing all five:**

```text
{'Asha'}
a
2
{1, 2}
{1, 2, 3}
```

### 16 · Who watched what
Two lists show who watched which course on allcsvideos. Some students appear twice because they re-watched.

```python
python_viewers = ["Asha", "Lukas", "Priya", "Asha", "Rahul", "Lukas"]
sql_viewers = ["Priya", "Meera", "Rahul", "Priya"]
```

Turn each into a set (`py` and `sq`) and print, always wrapped in `sorted(...)` so the order is stable:

1. the Python viewers, then the list length next to the number of **different** viewers (`6 -> 4`)
2. students who watched **both**, **either** course, **only** Python, **only** SQL, and **exactly one** course
3. whether `"Asha"` watched Python (use `in` on the set)
4. the Python viewers with duplicates removed **but in their first-seen order**: loop over `python_viewers`, keep a set `seen`, and `append` a name to a list only if it is not in `seen` yet

**Expected output:**

```text
Python viewers: ['Asha', 'Lukas', 'Priya', 'Rahul']
Unique counts: 6 -> 4
Both: ['Priya', 'Rahul']
Either: ['Asha', 'Lukas', 'Meera', 'Priya', 'Rahul']
Only Python: ['Asha', 'Lukas']
Only SQL: ['Meera']
Exactly one course: ['Asha', 'Lukas', 'Meera']
Asha watched Python? True
In first-seen order: ['Asha', 'Lukas', 'Priya', 'Rahul']
```


## M05 · L05 Comprehensions

### 17 · Loops into comprehensions
Each of these loops builds a list. Rewrite every one as a **list comprehension** and print both versions to see they match.

```python
prices = [1499, 999, 799, 499]
names = ["asha", "lukas", "priya"]

squares = []
for n in range(1, 6):
    squares.append(n * n)

evens = []
for n in range(1, 11):
    if n % 2 == 0:
        evens.append(n)

with_gst = []
for p in prices:
    with_gst.append(p * 118 // 100)

shouting = []
for name in names:
    shouting.append(name.upper())

lengths = []
for name in names:
    lengths.append(len(name))
```

For each one, print a line such as `squares: [1, 4, 9, 16, 25]` from the loop version, and a line `squares (comprehension): ...` from your version. Finish with `print(squares == squares2)` style checks collected in one `print` that shows `True` five times (for example `print(a == a2, b == b2, ...)`).

**Expected output:**

```text
squares: [1, 4, 9, 16, 25]
squares (comprehension): [1, 4, 9, 16, 25]
evens: [2, 4, 6, 8, 10]
evens (comprehension): [2, 4, 6, 8, 10]
with GST: [1768, 1178, 942, 588]
with GST (comprehension): [1768, 1178, 942, 588]
shouting: ['ASHA', 'LUKAS', 'PRIYA']
shouting (comprehension): ['ASHA', 'LUKAS', 'PRIYA']
lengths: [4, 5, 5]
lengths (comprehension): [4, 5, 5]
True True True True True
```

### 18 · Predict the output (comprehensions)
**Write your guesses first.** Predict what each of the 13 `print` lines shows. Take your time with lines 3 (`if` / `else` in front of the `for`), 6 (a set) and 7 (two `for` parts).

```python
print([n * 2 for n in range(5)])
print([n for n in range(10) if n % 3 == 0])
print(["even" if n % 2 == 0 else "odd" for n in range(4)])
print([c.upper() for c in "abc"])
print({n: n * n for n in range(4)})
print(sorted({len(w) for w in ["go", "sql", "java", "rust"]}))
print([(x, y) for x in [1, 2] for y in "ab"])
print([[0] * 2 for row in range(2)])
print([x for x in [1, 2, 3] if x > 5])
words = ["apple", "kiwi", "fig"]
print({w: len(w) for w in words})
print([w for w in words if len(w) > 3])
print(sum([n * n for n in range(4)]))
print([n for n in range(3)][::-1])
```

Run it and mark your wrong guesses.

### 19 · Dictionary and set comprehensions
Use **one comprehension per line** for each task below. Start from:

```python
prices = {"python": 1499, "sql": 999, "docker": 799, "go": 699}
names = ["Asha", "Arjun", "Priya", "Mia", "Meera"]
```

1. `cheap`: only the courses under Rs 1000, as a dictionary
2. `discounted`: every course with 10 percent off (`price * 90 // 100`)
3. `shout`: the same prices with the course names in capital letters
4. `inverse`: swap keys and values, so the prices become keys
5. `lengths`: a dictionary from each name to its length
6. `initials`: the **set** of first letters of the names
7. Print each result with its label, then print `sum(cheap.values())` and `sorted(initials)`

**Expected output:**

```text
cheap: {'sql': 999, 'docker': 799, 'go': 699}
discounted: {'python': 1349, 'sql': 899, 'docker': 719, 'go': 629}
shout: {'PYTHON': 1499, 'SQL': 999, 'DOCKER': 799, 'GO': 699}
inverse: {1499: 'python', 999: 'sql', 799: 'docker', 699: 'go'}
lengths: {'Asha': 4, 'Arjun': 5, 'Priya': 5, 'Mia': 3, 'Meera': 5}
initials: ['A', 'M', 'P']
cheap total: 2497
```

### 20 · Know when to stop
Comprehensions are great until they are too clever. Part 1 uses them well; part 2 asks you to rescue a bad one.

**Part 1.** Given a grid of lessons per week:

```python
grid = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
```

- `flat`: all nine numbers in one list, with a comprehension that has two `for` parts (`for row in grid for n in row`)
- `column_sums`: a list with the sum of each **column**: `[grid[0][i] + grid[1][i] + grid[2][i] for i in range(3)]`

**Part 2.** This one-liner works but nobody can read it:

```python
messy = [n * n if n % 2 == 0 else -n for n in range(10) if n != 5 and (n % 3 != 0 or n == 0)]
```

Rewrite it with two small functions, `transform(n)` (square the even numbers, make the odd numbers negative) and `keep(n)` (the filter condition), and then a short comprehension that uses them. Check that your result equals `messy`.

**Part 3.** One more rule: do not build a list just to print. Print the names `"Asha"`, `"Lukas"`, `"Priya"` one per line with a normal `for` loop.

**Expected output:**

```text
flat: [1, 2, 3, 4, 5, 6, 7, 8, 9]
column sums: [12, 15, 18]
messy: [0, -1, 4, 16, -7, 64]
clean: [0, -1, 4, 16, -7, 64]
same: True
Asha
Lukas
Priya
```


## M05 · L06 Names, Objects and Mutability

### 21 · Predict the output (two names, one list?)
**Write your guesses first.** This is the most important prediction exercise of the module. Predict every line this file prints (it prints 9 lines).

```python
a = [1, 2, 3]
b = a
b.append(4)
print(a, b)
print(a is b, a == b)
c = a.copy()
c.append(5)
print(a, c)
print(a is c, a == c[:4])
d = a[:]
d[0] = 99
print(a, d)
x = 10
y = x
y += 1
print(x, y)
s = "abc"
t = s.upper()
print(s, t)
e = [1]
f = e
f = f + [2]
print(e, f)
g = (1, [2])
g[1].append(3)
print(g)
```

Run it. For every wrong guess, say whether you forgot that two labels can point at the **same** object, or that a new object was made.

### 22 · Fix the sharing bugs
Four programs that **do not crash** but print the wrong thing, because two names share one list. Run each, find the sharing, and fix it. Then put the repaired versions in one file.

```python
# file a
scores = [70, 80]
backup = scores
scores.append(95)
print("Scores:", scores, "Backup:", backup)
```
```python
# file b
grid = [[0] * 3] * 3
grid[0][0] = 1
print(grid)
```
```python
# file c
def add_course(course, cart=[]):
    cart.append(course)
    return cart


print(add_course("Python"))
print(add_course("SQL"))
```
```python
# file d
def top_mark(marks):
    marks.sort()
    return marks[-1]


marks = [50, 90, 30]
print(top_mark(marks), marks)
```

What the broken versions print (a vertical bar `|` separates two output lines):

```text
a: (no error) prints   Scores: [70, 80, 95] Backup: [70, 80, 95]
b: (no error) prints   [[1, 0, 0], [1, 0, 0], [1, 0, 0]]
c: (no error) prints   ['Python'] | ['Python', 'SQL']
d: (no error) prints   90 [30, 50, 90]
```

**Goal after fixing all four:**

```text
Scores: [70, 80, 95] Backup: [70, 80]
[[1, 0, 0], [0, 0, 0], [0, 0, 0]]
['Python']
['SQL']
90 [50, 90, 30]
```

### 23 · Shallow and deep copies
Lukas keeps the batches of a course as a list of lists, and copies it in four ways. Then he adds a student to the first batch of the original. Which copies change?

```python
import copy

batches = [["Lukas", "Priya"], ["Asha"]]
alias = batches
shallow = batches.copy()
sliced = batches[:]
deep = copy.deepcopy(batches)
```

1. Now change the original: `batches[0].append("Meera")` and `batches.append(["Rahul"])`.
2. Print `batches`, `alias`, `shallow`, `sliced`, `deep`, each with a label.
3. Print the answer of these `is` checks, one per line: `alias is batches`, `shallow is batches`, `shallow[0] is batches[0]`, `deep[0] is batches[0]`.
4. A course record: `course = {"name": "Python", "tags": ["beginner"]}`. Make `backup = copy.deepcopy(course)`, then change the original with `course["name"] = "Python 2"` and `course["tags"].append("hot")`. Print `course` and `backup`.

**Expected output:**

```text
batches: [['Lukas', 'Priya', 'Meera'], ['Asha'], ['Rahul']]
alias  : [['Lukas', 'Priya', 'Meera'], ['Asha'], ['Rahul']]
shallow: [['Lukas', 'Priya', 'Meera'], ['Asha']]
sliced : [['Lukas', 'Priya', 'Meera'], ['Asha']]
deep   : [['Lukas', 'Priya'], ['Asha']]
True
False
True
False
course: {'name': 'Python 2', 'tags': ['beginner', 'hot']}
backup: {'name': 'Python', 'tags': ['beginner']}
```

### 24 · Does the function change my list?
**Predict, then run.** Rahul wrote five small helpers. For each call, decide: does it change the list that was passed in, or not? Write down what each `print` shows.

```python
def add_bonus_in_place(marks, bonus):
    for i, mark in enumerate(marks):
        marks[i] = mark + bonus


def with_bonus(marks, bonus):
    result = []
    for mark in marks:
        result.append(mark + bonus)
    return result


def reassign(marks):
    marks = [0, 0, 0]


def extend_in_place(marks):
    marks.extend([100])


def concat(marks):
    marks = marks + [100]
    return marks


original = [50, 60, 70]

new_list = with_bonus(original, 5)
print(original, new_list)

reassign(original)
print(original)

concat(original)
print(original)

extend_in_place(original)
print(original)

add_bonus_in_place(original, 10)
print(original)

result = concat(original)
print(result is original, result == original + [100])
```

Then write one sentence for each helper: "changes the caller's list" or "leaves it alone", and say **why**.

### 25 · The class gradebook
Put the whole module together. The allcsvideos teachers keep marks in a dictionary from student name to a **list** of marks:

```python
gradebook = {
    "Asha": [92, 88, 95],
    "Lukas": [70, 65],
    "Priya": [85, 90, 78, 88],
    "Rahul": [],
    "Meera": [60, 72, 58],
}
```

Write these pieces and then the report.

1. `average(marks)`: the average rounded to 1 decimal, or `0` if the list is empty.
2. `add_mark(book, name, mark)`: add the mark to that student's list. If the name is not in the book yet, create it with an empty list first. It changes the book and returns nothing.
3. `ranking(book)`: a list of `(name, average)` tuples, best average first (`sorted` with a `lambda` key). Build the pairs with a **list comprehension**.
4. `passed(book, limit=60)`: the **set** of names whose average is at least `limit` (a set comprehension).
5. `group_by_grade(book)`: a dictionary from the letter `"A"` (average 85 or more), `"B"` (70 to 84.9), `"C"` (below 70) to a **list** of names. Use `if` / `elif` / `else` and the "create the list if the key is new" step.

Then run this story and print exactly what is shown:

- add the mark 81 to Rahul, then add the mark 77 to a **new** student `"Sofia"`
- print the ranking, one line per student: use `for position, pair in enumerate(ranking(gradebook), start=1):` and print the position with a dot, the name (`pair[0]`) padded to width 8, then the average (`pair[1]`) right-aligned in 6
- print `sorted(passed(gradebook))`
- print `group_by_grade(gradebook)`
- make a `backup = copy.deepcopy(gradebook)`, add the mark 100 to Lukas, then print Lukas's marks in the real book and in the backup

**Expected output:**

```text
1. Asha      91.7
2. Priya     85.2
3. Rahul     81.0
4. Sofia     77.0
5. Lukas     67.5
6. Meera     63.3
['Asha', 'Lukas', 'Meera', 'Priya', 'Rahul', 'Sofia']
{'A': ['Asha', 'Priya'], 'C': ['Lukas', 'Meera'], 'B': ['Rahul', 'Sofia']}
Real book: [70, 65, 100]
Backup   : [70, 65]
```


---

## Answers

Click an exercise to open its solution. Your code does not have to match line for line; it should produce the same output.


<details>
<summary><b>1 · The course playlist</b></summary>

**Hint.** `append` adds **one** thing at the end. `insert(position, thing)` pushes everything after it one step to the right. `extend` takes a whole list and adds each item. Positions start at 0, and `-1` is the last item.

Lists are changed in place: the same list gets longer, and the label `playlist` keeps pointing at it. The methods `append`, `insert` and `extend` do the changing and give back nothing, so you never write `playlist = playlist.append(...)`.

`solutions/Ex01.py`, run with `python Ex01.py`:

```python
# Exercise 01 - The course playlist
playlist = ["Intro", "Variables", "Loops"]
print("Start:", playlist)

playlist.append("Functions")
print("After append:", playlist)

playlist.insert(1, "Setup")
print("After insert:", playlist)

playlist.extend(["Lists", "Tuples"])
print("After extend:", playlist)

print("Count:", len(playlist))
print("First:", playlist[0])
print("Last:", playlist[-1])

playlist[0] = "Welcome"
print("Renamed first:", playlist[0])
```

Output (Python 3.14):

```text
Start: ['Intro', 'Variables', 'Loops']
After append: ['Intro', 'Variables', 'Loops', 'Functions']
After insert: ['Intro', 'Setup', 'Variables', 'Loops', 'Functions']
After extend: ['Intro', 'Setup', 'Variables', 'Loops', 'Functions', 'Lists', 'Tuples']
Count: 7
First: Intro
Last: Tuples
Renamed first: Welcome
```

</details>


<details>
<summary><b>2 · Predict the output (indexes, slices and methods)</b></summary>

**Hint.** A slice `marks[a:b]` starts at `a` and stops **before** `b`. `pop()` removes **and returns** the last item, `pop(0)` the first. `remove(70)` deletes only the **first** 70 it finds. `index(70)` tells where the first 70 sits.

Slices never fail when the numbers are too big (`marks[2:100]` just stops at the end), but a single index does (`marks[100]` is an `IndexError`). `+` joins two lists into a new one, `*` repeats a list. After `pop()` and `pop(0)` the list is shorter, so every later line sees the shorter list.

`solutions/Ex02.py`, run with `python Ex02.py`:

```python
# Exercise 02 - Predict the output (indexes, slices and methods)
marks = [40, 85, 70, 55, 90, 70]
print(marks[0], marks[-1])
print(marks[1:4])
print(marks[:2], marks[4:])
print(marks[::2])
print(marks[::-1])
print(marks[2:100])
print(len(marks), marks.count(70), marks.index(70))
print(85 in marks, 100 in marks, 100 not in marks)
last = marks.pop()
print(last, marks)
first = marks.pop(0)
print(first, marks)
marks.remove(70)
print(marks)
del marks[1]
print(marks)
print(marks + [1, 2], [0] * 3)
```

Output (Python 3.14):

```text
40 70
[85, 70, 55]
[40, 85] [90, 70]
[40, 70, 90]
[70, 90, 55, 70, 85, 40]
[70, 55, 90, 70]
6 2 2
True False True
70 [40, 85, 70, 55, 90]
40 [85, 70, 55, 90]
[85, 55, 90]
[85, 90]
[85, 90, 1, 2] [0, 0, 0]
```

</details>


<details>
<summary><b>3 · Fix the broken list code</b></summary>

**Hint.** a: a list with 3 items has positions 0, 1, 2. b: ask `in` before you `remove`. c: `sort()` changes the list and returns `None`, so the label `result` holds `None`. d: `+` joins a list with another **list**, not with text. e: `append` takes exactly one thing; to add several, use `extend`.

Fixes: `scores[2]` (or `scores[-1]`) for a; an `if "Priya" in names` check for b; call `marks.sort()` on its own line and print `marks` for c (or use `sorted(marks)` if you want a new list); `names + ["Rahul"]` for d; `names.extend(["Lukas", "Meera"])` for e. In each case the error message names the exact rule that was broken.

`solutions/Ex03.py`, run with `python Ex03.py`:

```python
# Exercise 03 - Fix the broken list code (all five repaired)
scores = [70, 80, 90]
print(scores[2])                 # was scores[3]: only positions 0, 1, 2 exist

names = ["Asha", "Lukas"]
if "Priya" in names:             # was: names.remove("Priya") with no check
    names.remove("Priya")
else:
    print("Priya is not enrolled")
print(names)

marks = [3, 1, 2]
marks.sort()                     # was: result = marks.sort()  (sort returns None)
print(marks)

guests = ["Asha"]
guests = guests + ["Rahul"]      # was: guests + "Rahul"  (list + text)
print(guests)

team = ["Asha"]
team.extend(["Lukas", "Meera"])  # was: team.append("Lukas", "Meera")
print(team)
```

Output (Python 3.14):

```text
90
Priya is not enrolled
['Asha', 'Lukas']
[1, 2, 3]
['Asha', 'Rahul']
['Asha', 'Lukas', 'Meera']
```

</details>


<details>
<summary><b>4 · Sorting the ratings</b></summary>

**Hint.** `sorted(x)` builds a **new** list and leaves `x` alone. `x.sort()` changes `x` itself and returns `None`. A `key` is a tiny function: Python calls it on each item and sorts by the answer. `lambda name: name[-1]` is a nameless function from Module 4 that returns the last letter. A slice always makes a brand new list.

The pair `sorted` / `sort` is the first mutable-or-not choice of the module: the first keeps the original, the second changes it. When two items have the same key (Python and Docker both have length 6), their original order is kept. Capital letters sort before small ones, which is why `"SQL"` comes before `"Spring Boot"` in the A to Z list.

`solutions/Ex04.py`, run with `python Ex04.py`:

```python
# Exercise 04 - Sorting the ratings
ratings = [4.5, 3.8, 4.9, 4.1, 3.2]
courses = ["Python", "SQL", "Go", "Docker", "Spring Boot"]

print("sorted():", sorted(ratings))
print("original:", ratings)

ratings.sort(reverse=True)
print("sort(reverse=True):", ratings)

print("Best:", max(ratings), "Worst:", min(ratings))
print("Average:", round(sum(ratings) / len(ratings), 2))

print("A to Z:", sorted(courses))
print("By length:", sorted(courses, key=len))
print("By last letter:", sorted(courses, key=lambda name: name[-1]))

print("Backwards:", courses[::-1])
print("Courses still:", courses)
```

Output (Python 3.14):

```text
sorted(): [3.2, 3.8, 4.1, 4.5, 4.9]
original: [4.5, 3.8, 4.9, 4.1, 3.2]
sort(reverse=True): [4.9, 4.5, 4.1, 3.8, 3.2]
Best: 4.9 Worst: 3.2
Average: 4.1
A to Z: ['Docker', 'Go', 'Python', 'SQL', 'Spring Boot']
By length: ['Go', 'SQL', 'Python', 'Docker', 'Spring Boot']
By last letter: ['SQL', 'Python', 'Go', 'Docker', 'Spring Boot']
Backwards: ['Spring Boot', 'Docker', 'Go', 'SQL', 'Python']
Courses still: ['Python', 'SQL', 'Go', 'Docker', 'Spring Boot']
```

</details>


<details>
<summary><b>5 · Top marks, zeros removed</b></summary>

**Hint.** Inside the function, build a **new** list called `valid` and never touch `marks` itself. `valid[:n]` is safe even when `n` is bigger than the list. For the last step, `remove(0)` deletes the first 0 it finds, so repeat while one is left.

Two different ways to clean a list: the function builds a **new** list and returns it (the caller's list is untouched), while the `while` loop changes the **same** list in place. Knowing which one a piece of code does is the main skill of this module, and Exercises 21 to 24 practise it.

`solutions/Ex05.py`, run with `python Ex05.py`:

```python
# Exercise 05 - Top marks, zeros removed
def best_marks(marks, n=3):
    valid = []
    for mark in marks:
        if mark > 0:
            valid.append(mark)
    valid.sort(reverse=True)
    return valid[:n]


raw = [0, 72, 95, 0, 88, 61, 95]
print("Raw:", raw)
print("Top 3:", best_marks(raw))
print("Top 2:", best_marks(raw, 2))
print("Top 10:", best_marks(raw, 10))
print("Raw after:", raw)

while 0 in raw:
    raw.remove(0)
print("Cleaned in place:", raw)
```

Output (Python 3.14):

```text
Raw: [0, 72, 95, 0, 88, 61, 95]
Top 3: [95, 95, 88]
Top 2: [95, 95]
Top 10: [95, 95, 88, 72, 61]
Raw after: [0, 72, 95, 0, 88, 61, 95]
Cleaned in place: [72, 95, 88, 61, 95]
```

</details>


<details>
<summary><b>6 · Predict the output (tuples and unpacking)</b></summary>

**Hint.** The comma makes the tuple, not the brackets: `(5)` is just the number 5 in brackets, while `(5,)` is a tuple with one item. `first, *middle, last = ...` puts everything left over into `middle`, and `middle` is always a **list**. `enumerate(titles, start=1)` hands out a counter with every item, and `zip(titles, prices)` walks two rows side by side.

Unpacking matches names to items by position, so `x, y = point` gives `x` the first item and `y` the second. `a, b = b, a` first builds the tuple `(b, a)` and then unpacks it, which is why the swap works without a helper. Each step of `enumerate` and `zip` is a small tuple, and the `for` line unpacks it. A tuple can be compared with `==` but a tuple is never equal to a list, even with the same items.

`solutions/Ex06.py`, run with `python Ex06.py`:

```python
# Exercise 06 - Predict the output (tuples and unpacking)
point = (3, 4)
print(point, type(point), len(point))
print(point[0], point[-1])
single = (5,)
not_a_tuple = (5)
print(type(single), type(not_a_tuple))
x, y = point
print(x + y)
a, b = 1, 2
a, b = b, a
print(a, b)
first, *middle, last = [10, 20, 30, 40, 50]
print(first, middle, last)
cheapest, *others = (499, 999, 1499)
print(cheapest, others)
empty = ()
print(type(empty), len(empty))
titles = ("Python", "SQL", "Docker")
prices = (1499, 999, 799)
for number, title in enumerate(titles, start=1):
    print(number, title)
for title, price in zip(titles, prices):
    print(title, price)
print(point == (3, 4), point == [3, 4])
```

Output (Python 3.14):

```text
(3, 4) <class 'tuple'> 2
3 4
<class 'tuple'> <class 'int'>
7
2 1
10 [20, 30, 40] 50
499 [999, 1499]
<class 'tuple'> 0
1 Python
2 SQL
3 Docker
Python 1499
SQL 999
Docker 799
True False
```

</details>


<details>
<summary><b>7 · Fix the broken tuple code</b></summary>

**Hint.** a: tuples cannot be changed, so build a **new** tuple. b: the comma makes the tuple. c: the number of names on the left must match the number of items on the right. d: tuples have no `sort`, but the helper `sorted` works on any collection and gives back a list.

Fixes: a becomes `course = (course[0], 999)` (a new tuple replaces the old one under the same label); b becomes `("Asha",)`; c needs three names, for example `name, price, lessons`; d uses `sorted(students)`. The rule behind a and d: a tuple is read-only, so you look at it or build a new thing from it.

`solutions/Ex07.py`, run with `python Ex07.py`:

```python
# Exercise 07 - Fix the broken tuple code (all four repaired)
course = ("Python", 1499)
course = (course[0], 999)        # was: course[1] = 999
print(course)

one = ("Asha",)                  # was: ("Asha")  (no comma)
print(type(one))

name, price, lessons = ("Python", 1499, 12)   # was: only two names
print(name, price, lessons)

students = ("Lukas", "Asha")
print(sorted(students))          # was: students.sort()
```

Output (Python 3.14):

```text
('Python', 999)
<class 'tuple'>
Python 1499 12
['Asha', 'Lukas']
```

</details>


<details>
<summary><b>8 · Many answers from one function</b></summary>

**Hint.** `return a, b, c` returns **one** tuple `(a, b, c)`. The brackets are optional. `zip` pairs the first name with the first score, and so on. In `winner, *others = ranking`, `winner` is the first tuple and `others` is a list of the remaining tuples. `enumerate(..., start=1)` counts from 1.

This is the everyday use of tuples: a function that returns several values, a loop over pairs, a swap. Tuples are the right choice when the items are a fixed little record (a name and a score) and a list is the right choice when the collection grows and shrinks.

`solutions/Ex08.py`, run with `python Ex08.py`:

```python
# Exercise 08 - Many answers from one function
def summarise(marks):
    return min(marks), max(marks), round(sum(marks) / len(marks), 1)


marks = [72, 95, 88, 61, 79]
names = ["Asha", "Lukas", "Priya"]
scores = [92, 78, 85]

lowest, highest, average = summarise(marks)
print("Lowest:", lowest, "Highest:", highest, "Average:", average)
everything = summarise(marks)
print(everything, type(everything))

for name, score in zip(names, scores):
    print(f"{name:<8}{score:>4}")

ranking = sorted(zip(names, scores), key=lambda pair: pair[1], reverse=True)
winner, *others = ranking
print("Winner:", winner)
print("Others:", others)

for place, pair in enumerate(ranking, start=1):
    print(place, pair[0], pair[1])

seat_a = "Asha"
seat_b = "Lukas"
seat_a, seat_b = seat_b, seat_a
print(seat_a, seat_b)
```

Output (Python 3.14):

```text
Lowest: 61 Highest: 95 Average: 79.0
(61, 95, 79.0) <class 'tuple'>
Asha      92
Lukas     78
Priya     85
Winner: ('Asha', 92)
Others: [('Priya', 85), ('Lukas', 78)]
1 Asha 92
2 Priya 85
3 Lukas 78
Lukas Asha
```

</details>


<details>
<summary><b>9 · A student record</b></summary>

**Hint.** `student["key"]` looks a value up, and assigning to a key either changes it (if it exists) or adds it (if it does not). `pop(key)` removes the key and **returns** its value. `in` checks the **keys**, not the values.

A dictionary is a set of labelled drawers: you ask for a value by its key, not by its position. Each key appears once. `"Asha" in student` is `False` because `"Asha"` is a value, and `in` only looks at keys.

`solutions/Ex09.py`, run with `python Ex09.py`:

```python
# Exercise 09 - A student record
student = {"name": "Asha", "course": "Python", "lessons_done": 12}
print(student)

print(student["name"], student["lessons_done"])

student["lessons_done"] = 13
student["email"] = "asha@mail.com"
print(student)

removed = student.pop("email")
print("Removed:", removed)
del student["course"]
print(student, len(student))

print("name" in student, "Asha" in student)
```

Output (Python 3.14):

```text
{'name': 'Asha', 'course': 'Python', 'lessons_done': 12}
Asha 12
{'name': 'Asha', 'course': 'Python', 'lessons_done': 13, 'email': 'asha@mail.com'}
Removed: asha@mail.com
{'name': 'Asha', 'lessons_done': 13} 2
True False
```

</details>


<details>
<summary><b>10 · Predict the output (dictionaries)</b></summary>

**Hint.** `get(key, default)` never crashes: it gives the default (or `None`) when the key is missing. `in` checks the **keys**, not the values. `pop(key)` removes the key **and returns its value**. A plain `for` loop over a dictionary gives the keys; `.items()` gives (key, value) pairs and `.values()` gives only the values.

Assigning to an existing key changes its value and keeps its place; a new key goes to the end. `del prices["Go"]` removes a key without giving anything back. Dictionaries remember the order in which keys were added. The last lines show the two patterns you will use constantly: digging into a dictionary of dictionaries, and counting with `get(key, 0) + 1`.

`solutions/Ex10.py`, run with `python Ex10.py`:

```python
# Exercise 10 - Predict the output (dictionaries)
prices = {"Python": 1499, "SQL": 999, "Docker": 799}
print(prices["SQL"])
print(prices.get("Docker"), prices.get("Go"), prices.get("Go", 0))
print("SQL" in prices, 999 in prices, "Go" not in prices)
prices["SQL"] = 899
prices["Go"] = 699
print(prices)
print(prices.pop("Python"))
print(len(prices))
del prices["Go"]
print(prices)
for course, price in prices.items():
    print(course, "->", price)
for price in prices.values():
    print(price)
for key in prices:
    print(key)
nested = {"Asha": {"marks": [80, 90]}}
print(nested["Asha"]["marks"][-1])
counts = {}
counts["a"] = counts.get("a", 0) + 1
counts["a"] = counts.get("a", 0) + 1
print(counts)
```

Output (Python 3.14):

```text
999
799 None 0
True False True
{'Python': 1499, 'SQL': 899, 'Docker': 799, 'Go': 699}
1499
3
{'SQL': 899, 'Docker': 799}
SQL -> 899
Docker -> 799
899
799
SQL
Docker
90
{'a': 2}
```

</details>


<details>
<summary><b>11 · Fix the broken dictionary code</b></summary>

**Hint.** a: use `get` with a default. b: keys must be unchangeable, so use a tuple instead of a list. c: do not change a dictionary while you loop over it; first **collect** the names to remove in a list, then delete them in a second loop. d: looping over a dictionary gives only keys; ask for `.items()`. e: a key can appear only once, so the second `"python"` replaced the first.

Fixes: `student.get("email", "no email")`; the key `("python", 3)`; one loop that appends the low scorers to a list `to_remove`, then a second loop with `del`; `for key, value in student.items():`; and a second key with a different name. For c, the error message says exactly what happened: the dictionary changed size while Python was walking through it.

`solutions/Ex11.py`, run with `python Ex11.py`:

```python
# Exercise 11 - Fix the broken dictionary code (all five repaired)
student = {"name": "Asha"}
print(student.get("email", "no email"))     # was: student["email"]

course_key = ("python", 3)                  # was: a list
prices = {course_key: 1499}
print(prices)

scores = {"Asha": 80, "Lukas": 40, "Rahul": 65}
to_remove = []
for name in scores:                         # first collect ...
    if scores[name] < 50:
        to_remove.append(name)
for name in to_remove:                      # ... then delete
    del scores[name]
print(scores)

student = {"name": "Asha", "city": "Pune"}
for key, value in student.items():          # was: for key, value in student
    print(key, "=", value)

prices = {"python": 1499, "python_advanced": 1299}   # was: "python" twice
print(prices, len(prices))
```

Output (Python 3.14):

```text
no email
{('python', 3): 1499}
{'Asha': 80, 'Rahul': 65}
name = Asha
city = Pune
{'python': 1499, 'python_advanced': 1299} 2
```

</details>


<details>
<summary><b>12 · Count the votes</b></summary>

**Hint.** `tally.get(choice, 0)` is the number so far, or 0 for a new course. Add 1 and store it back. `tally.items()` gives pairs, and `pair[1]` is the count. After sorting, the winner sits at position 0.

Counting with a dictionary is the most common dictionary pattern in real programs: words in a text, errors in a log, orders per customer. Both ways (`get` with 0, or `in` with `else`) do the same job; use whichever you find easier to read. When two courses tie (Docker and SQL both have 2), `sorted` keeps them in the order they first appeared.

`solutions/Ex12.py`, run with `python Ex12.py`:

```python
# Exercise 12 - Count the votes
votes = ["Python", "Docker", "Python", "SQL", "Python", "Docker", "Go", "SQL", "Python"]

tally = {}
for choice in votes:
    tally[choice] = tally.get(choice, 0) + 1
print(tally)

by_votes = sorted(tally.items(), key=lambda pair: pair[1], reverse=True)
winner, count = by_votes[0]
print("Winner:", winner, "with", count, "votes")

for choice, count in by_votes:
    print(f"{choice:<8}{'#' * count} {count}")

counts = {}
for letter in "banana":
    if letter in counts:
        counts[letter] += 1
    else:
        counts[letter] = 1
print(counts)
```

Output (Python 3.14):

```text
{'Python': 4, 'Docker': 2, 'SQL': 2, 'Go': 1}
Winner: Python with 4 votes
Python  #### 4
Docker  ## 2
SQL     ## 2
Go      # 1
{'b': 1, 'a': 3, 'n': 2}
```

</details>


<details>
<summary><b>13 · The nested catalog</b></summary>

**Hint.** You can chain lookups: `catalog["Python"]` gives the inner dictionary, and `["price"]` looks inside it. Values can be anything, even lists, so `catalog["Python"]["tags"].append(...)` changes the list inside the dictionary. For the grouping, test with `if slug not in by_course:`.

A dictionary whose values are lists is the normal way to group things: all students of one course, all orders of one customer. The last line shows a safe way to dig two levels deep: the first `get` returns an empty dictionary when the course is missing, so the second `get` still works.

`solutions/Ex13.py`, run with `python Ex13.py`:

```python
# Exercise 13 - The nested catalog
catalog = {
    "Python": {"price": 1499, "lessons": 104, "tags": ["beginner", "backend"]},
    "SQL": {"price": 999, "lessons": 30, "tags": ["data"]},
    "Docker": {"price": 799, "lessons": 25, "tags": ["devops"]},
}
print(catalog["Python"]["price"])
print(catalog["Python"]["tags"][0])

catalog["Git"] = {"price": 499, "lessons": 12, "tags": []}
catalog["SQL"]["price"] -= 100
catalog["Python"]["tags"].append("popular")

for slug, info in catalog.items():
    print(f"{slug:<8} Rs {info['price']:>5}  {info['lessons']:>3} lessons  tags={info['tags']}")

total = 0
for info in catalog.values():
    total += info["price"]
print("Whole catalog: Rs", total)

enrolments = [("Asha", "Python"), ("Lukas", "SQL"), ("Priya", "Python"),
              ("Meera", "Git"), ("Rahul", "Python")]
by_course = {}
for student, slug in enrolments:
    if slug not in by_course:
        by_course[slug] = []
    by_course[slug].append(student)
print(by_course)

print(catalog.get("Go", {}).get("price", "not sold"))
```

Output (Python 3.14):

```text
1499
beginner
Python   Rs  1499  104 lessons  tags=['beginner', 'backend', 'popular']
SQL      Rs   899   30 lessons  tags=['data']
Docker   Rs   799   25 lessons  tags=['devops']
Git      Rs   499   12 lessons  tags=[]
Whole catalog: Rs 3696
{'Python': ['Asha', 'Priya', 'Rahul'], 'SQL': ['Lukas'], 'Git': ['Meera']}
not sold
```

</details>


<details>
<summary><b>14 · Predict the output (sets)</b></summary>

**Hint.** A set keeps each item once and has no positions. `|` (or `union`) is everything, `&` (or `intersection`) is in both, `-` (or `difference`) is in the left only, `^` (or `symmetric_difference`) is in exactly one. `remove` crashes for a missing item, `discard` does not. `{}` is an empty dictionary; an empty set is `set()`.

Sets are built for two jobs: removing duplicates (`set(log)`) and asking "is this in the group?" very fast. The operator and the method with the long name do the same thing. The small integers happen to print in sorted order in Python 3.14, but you must never rely on that.

`solutions/Ex14.py`, run with `python Ex14.py`:

```python
# Exercise 14 - Predict the output (sets)
a = {1, 2, 3, 3, 2}
print(a, len(a))
b = {3, 4, 5}
print(a | b, a & b, a - b, b - a, a ^ b)
print(a.union(b), a.intersection(b), a.difference(b), a.symmetric_difference(b))
print(2 in a, 9 in a, 9 not in a)
a.add(10)
a.add(1)
print(sorted(a))
a.discard(99)
a.remove(10)
print(sorted(a))
print(type({}), type(set()), type({1}))
log = ["Lukas", "Priya", "Lukas", "Asha", "Priya"]
print(len(log), len(set(log)), sorted(set(log)))
print(len(set([1, 1, 1, 2])))
print(sorted({"Mia", "Chen"} | {"Sofia"}))
```

Output (Python 3.14):

```text
{1, 2, 3} 3
{1, 2, 3, 4, 5} {3} {1, 2} {4, 5} {1, 2, 4, 5}
{1, 2, 3, 4, 5} {3} {1, 2} {1, 2, 4, 5}
True False True
[1, 2, 3, 10]
[1, 2, 3]
<class 'dict'> <class 'set'> <class 'set'>
5 3 ['Asha', 'Lukas', 'Priya']
2
['Chen', 'Mia', 'Sofia']
```

</details>


<details>
<summary><b>15 · Fix the broken set code</b></summary>

**Hint.** a: `{}` is a dictionary, so create the set with `set()`. b: a set has no positions, so you cannot ask for `[0]`; sort it first if you need the "first". c: a set item must be unchangeable, so use a tuple. d: `remove` crashes for a missing item, `discard` does not. e: `+` does not exist for sets; the union is `|`.

Fixes: `viewers = set()`; `sorted(tags)[0]`; `{(1, 2), 3}`; `s.discard(5)`; `{1, 2} | {3}`. The common thread: a set is a bag of unchangeable items without positions, so most list habits (`[0]`, `+`, putting a list inside) fail on it.

`solutions/Ex15.py`, run with `python Ex15.py`:

```python
# Exercise 15 - Fix the broken set code (all five repaired)
viewers = set()                    # was: {}  (that is a dictionary)
viewers.add("Asha")
print(viewers)

tags = {"b", "a"}
print(sorted(tags)[0])             # was: tags[0]

points = {(1, 2), 3}               # was: {[1, 2], 3}
print(len(points))

s = {1, 2}
s.discard(5)                       # was: s.remove(5)
print(s)

print({1, 2} | {3})                # was: {1, 2} + {3}
```

Output (Python 3.14):

```text
{'Asha'}
a
2
{1, 2}
{1, 2, 3}
```

</details>


<details>
<summary><b>16 · Who watched what</b></summary>

**Hint.** Think of two circles that overlap. `&` is the overlap, `|` is both circles together, `-` is one circle minus the overlap, `^` is both circles minus the overlap. For step 4: `if name not in seen:` then `seen.add(name)` and `append`.

A set loses the order, so `sorted(set(...))` gives a tidy list but not the original order. The `seen` pattern gives you both: the set answers "have I met this?" instantly, and the list keeps the order. This is how real programs remove duplicates while keeping order.

`solutions/Ex16.py`, run with `python Ex16.py`:

```python
# Exercise 16 - Who watched what
python_viewers = ["Asha", "Lukas", "Priya", "Asha", "Rahul", "Lukas"]
sql_viewers = ["Priya", "Meera", "Rahul", "Priya"]

py = set(python_viewers)
sq = set(sql_viewers)

print("Python viewers:", sorted(py))
print("Unique counts:", len(python_viewers), "->", len(py))
print("Both:", sorted(py & sq))
print("Either:", sorted(py | sq))
print("Only Python:", sorted(py - sq))
print("Only SQL:", sorted(sq - py))
print("Exactly one course:", sorted(py ^ sq))
print("Asha watched Python?", "Asha" in py)

seen = set()
unique_in_order = []
for name in python_viewers:
    if name not in seen:
        seen.add(name)
        unique_in_order.append(name)
print("In first-seen order:", unique_in_order)
```

Output (Python 3.14):

```text
Python viewers: ['Asha', 'Lukas', 'Priya', 'Rahul']
Unique counts: 6 -> 4
Both: ['Priya', 'Rahul']
Either: ['Asha', 'Lukas', 'Meera', 'Priya', 'Rahul']
Only Python: ['Asha', 'Lukas']
Only SQL: ['Meera']
Exactly one course: ['Asha', 'Lukas', 'Meera']
Asha watched Python? True
In first-seen order: ['Asha', 'Lukas', 'Priya', 'Rahul']
```

</details>


<details>
<summary><b>17 · Loops into comprehensions</b></summary>

**Hint.** The pattern is `[expression for item in collection]`, and an `if` at the end filters: `[expression for item in collection if condition]`. The expression is whatever you were passing to `append`. The `for` line and the `if` line keep the same order as in the loop.

A comprehension is a loop that builds a list in one line. It is shorter and usually faster, and it says "this is a list made from that" at a glance. It is meant for building a list: do not use it just to run `print` on each item.

`solutions/Ex17.py`, run with `python Ex17.py`:

```python
# Exercise 17 - Loops into comprehensions
prices = [1499, 999, 799, 499]
names = ["asha", "lukas", "priya"]

squares = []
for n in range(1, 6):
    squares.append(n * n)
evens = []
for n in range(1, 11):
    if n % 2 == 0:
        evens.append(n)
with_gst = []
for p in prices:
    with_gst.append(p * 118 // 100)
shouting = []
for name in names:
    shouting.append(name.upper())
lengths = []
for name in names:
    lengths.append(len(name))

squares2 = [n * n for n in range(1, 6)]
evens2 = [n for n in range(1, 11) if n % 2 == 0]
with_gst2 = [p * 118 // 100 for p in prices]
shouting2 = [name.upper() for name in names]
lengths2 = [len(name) for name in names]

print("squares:", squares)
print("squares (comprehension):", squares2)
print("evens:", evens)
print("evens (comprehension):", evens2)
print("with GST:", with_gst)
print("with GST (comprehension):", with_gst2)
print("shouting:", shouting)
print("shouting (comprehension):", shouting2)
print("lengths:", lengths)
print("lengths (comprehension):", lengths2)
print(squares == squares2, evens == evens2, with_gst == with_gst2,
      shouting == shouting2, lengths == lengths2)
```

Output (Python 3.14):

```text
squares: [1, 4, 9, 16, 25]
squares (comprehension): [1, 4, 9, 16, 25]
evens: [2, 4, 6, 8, 10]
evens (comprehension): [2, 4, 6, 8, 10]
with GST: [1768, 1178, 942, 588]
with GST (comprehension): [1768, 1178, 942, 588]
shouting: ['ASHA', 'LUKAS', 'PRIYA']
shouting (comprehension): ['ASHA', 'LUKAS', 'PRIYA']
lengths: [4, 5, 5]
lengths (comprehension): [4, 5, 5]
True True True True True
```

</details>


<details>
<summary><b>18 · Predict the output (comprehensions)</b></summary>

**Hint.** An `if` **after** the `for` filters items out. An `if ... else ...` **before** the `for` chooses between two results and keeps every item. `{k: v for ...}` is a dictionary, `{x for ...}` is a set, and two `for` parts run like nested loops, the left one outermost.

Square brackets make a list, curly brackets with a colon make a dictionary, curly brackets without a colon make a set. A filter that matches nothing gives an empty list, not an error. A set comprehension drops repeated results, so four words with lengths 2, 3, 4, 4 give the set of lengths `{2, 3, 4}`.

`solutions/Ex18.py`, run with `python Ex18.py`:

```python
# Exercise 18 - Predict the output (comprehensions)
print([n * 2 for n in range(5)])
print([n for n in range(10) if n % 3 == 0])
print(["even" if n % 2 == 0 else "odd" for n in range(4)])
print([c.upper() for c in "abc"])
print({n: n * n for n in range(4)})
print(sorted({len(w) for w in ["go", "sql", "java", "rust"]}))
print([(x, y) for x in [1, 2] for y in "ab"])
print([[0] * 2 for row in range(2)])
print([x for x in [1, 2, 3] if x > 5])
words = ["apple", "kiwi", "fig"]
print({w: len(w) for w in words})
print([w for w in words if len(w) > 3])
print(sum([n * n for n in range(4)]))
print([n for n in range(3)][::-1])
```

Output (Python 3.14):

```text
[0, 2, 4, 6, 8]
[0, 3, 6, 9]
['even', 'odd', 'even', 'odd']
['A', 'B', 'C']
{0: 0, 1: 1, 2: 4, 3: 9}
[2, 3, 4]
[(1, 'a'), (1, 'b'), (2, 'a'), (2, 'b')]
[[0, 0], [0, 0]]
[]
{'apple': 5, 'kiwi': 4, 'fig': 3}
['apple', 'kiwi']
14
[2, 1, 0]
```

</details>


<details>
<summary><b>19 · Dictionary and set comprehensions</b></summary>

**Hint.** Dictionary comprehension: `{key_expression: value_expression for ... in ... if ...}`. To loop over a dictionary's keys and values together, use `prices.items()`. A set comprehension has no colon: `{name[0] for name in names}`.

`inverse` only works because all four prices are different; if two courses cost the same, one would overwrite the other (a key can appear only once). `initials` has 3 letters although there are 5 names, because the set drops the repeated `A` and `M`.

`solutions/Ex19.py`, run with `python Ex19.py`:

```python
# Exercise 19 - Dictionary and set comprehensions
prices = {"python": 1499, "sql": 999, "docker": 799, "go": 699}
names = ["Asha", "Arjun", "Priya", "Mia", "Meera"]

cheap = {c: p for c, p in prices.items() if p < 1000}
discounted = {c: p * 90 // 100 for c, p in prices.items()}
shout = {c.upper(): p for c, p in prices.items()}
inverse = {p: c for c, p in prices.items()}
lengths = {name: len(name) for name in names}
initials = {name[0] for name in names}

print("cheap:", cheap)
print("discounted:", discounted)
print("shout:", shout)
print("inverse:", inverse)
print("lengths:", lengths)
print("initials:", sorted(initials))
print("cheap total:", sum(cheap.values()))
```

Output (Python 3.14):

```text
cheap: {'sql': 999, 'docker': 799, 'go': 699}
discounted: {'python': 1349, 'sql': 899, 'docker': 719, 'go': 629}
shout: {'PYTHON': 1499, 'SQL': 999, 'DOCKER': 799, 'GO': 699}
inverse: {1499: 'python', 999: 'sql', 799: 'docker', 699: 'go'}
lengths: {'Asha': 4, 'Arjun': 5, 'Priya': 5, 'Mia': 3, 'Meera': 5}
initials: ['A', 'M', 'P']
cheap total: 2497
```

</details>


<details>
<summary><b>20 · Know when to stop</b></summary>

**Hint.** Part 2: read the condition piece by piece. `keep(n)` should return `True` for the numbers the filter lets through, so it can be written as `return n != 5 and (n % 3 != 0 or n == 0)`. The loop-style check is `result == messy`.

A good comprehension fits on one line, has one `for` (maybe two) and at most one `if`. Past that, name the pieces with functions, or write a normal loop. The two-`for` flatten is fine because it reads left to right like the loop it replaces, but a comprehension with an `if`/`else` **and** a filter **and** nested loops should be broken up.

`solutions/Ex20.py`, run with `python Ex20.py`:

```python
# Exercise 20 - Know when to stop
grid = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
flat = [n for row in grid for n in row]
column_sums = [grid[0][i] + grid[1][i] + grid[2][i] for i in range(3)]
print("flat:", flat)
print("column sums:", column_sums)

messy = [n * n if n % 2 == 0 else -n for n in range(10) if n != 5 and (n % 3 != 0 or n == 0)]


def transform(n):
    if n % 2 == 0:
        return n * n
    return -n


def keep(n):
    return n != 5 and (n % 3 != 0 or n == 0)


clean = [transform(n) for n in range(10) if keep(n)]
print("messy:", messy)
print("clean:", clean)
print("same:", clean == messy)

for name in ["Asha", "Lukas", "Priya"]:
    print(name)
```

Output (Python 3.14):

```text
flat: [1, 2, 3, 4, 5, 6, 7, 8, 9]
column sums: [12, 15, 18]
messy: [0, -1, 4, 16, -7, 64]
clean: [0, -1, 4, 16, -7, 64]
same: True
Asha
Lukas
Priya
```

</details>


<details>
<summary><b>21 · Predict the output (two names, one list?)</b></summary>

**Hint.** `b = a` makes a second **label** on the same list; no copy is made. `a.copy()` and `a[:]` make a new list. `f = f + [2]` builds a new list and moves the label `f`, so `e` is untouched. Numbers, text and tuples cannot be changed, so they never surprise you this way, but a list **inside** a tuple can still change.

Picture a name tag on a box. `b = a` puts a second tag on the same box, so anything you do through `b` shows up through `a`. `is` asks "same box?" and `==` asks "same contents?". An int and a string are **immutable** boxes: `y += 1` makes a new number and moves the tag `y`, leaving `x` alone. The tuple `g` cannot get a new item, yet its inner list can grow: the tuple holds a tag to the list, and the tag never changed.

`solutions/Ex21.py`, run with `python Ex21.py`:

```python
# Exercise 21 - Predict the output (two names, one list?)
a = [1, 2, 3]
b = a
b.append(4)
print(a, b)
print(a is b, a == b)
c = a.copy()
c.append(5)
print(a, c)
print(a is c, a == c[:4])
d = a[:]
d[0] = 99
print(a, d)
x = 10
y = x
y += 1
print(x, y)
s = "abc"
t = s.upper()
print(s, t)
e = [1]
f = e
f = f + [2]
print(e, f)
g = (1, [2])
g[1].append(3)
print(g)
```

Output (Python 3.14):

```text
[1, 2, 3, 4] [1, 2, 3, 4]
True True
[1, 2, 3, 4] [1, 2, 3, 4, 5]
False True
[1, 2, 3, 4] [99, 2, 3, 4]
10 11
abc ABC
[1] [1, 2]
(1, [2, 3])
```

</details>


<details>
<summary><b>22 · Fix the sharing bugs</b></summary>

**Hint.** a: `backup = scores` is a second label, not a copy. b: `[[0] * 3] * 3` repeats the **same** inner list three times; build each row separately. c: a default value such as `cart=[]` is created **once** and shared by every call; use `None` and make a fresh list inside. d: `marks.sort()` inside a function sorts the **caller's** list; use `max` or `sorted`.

Fixes: `backup = scores.copy()` (or `scores[:]`); `[[0] * 3 for row in range(3)]` (the comprehension runs the inside again for every row, so every row is a new list); `def add_course(course, cart=None): if cart is None: cart = []`; `return max(marks)` or `sorted(marks)[-1]`. The programs don't crash because nothing is illegal, they are just sharing one box, which is why this kind of bug is harder to see than an error message.

`solutions/Ex22.py`, run with `python Ex22.py`:

```python
# Exercise 22 - Fix the sharing bugs (all four repaired)
scores = [70, 80]
backup = scores.copy()                      # was: backup = scores
scores.append(95)
print("Scores:", scores, "Backup:", backup)

grid = [[0] * 3 for row in range(3)]        # was: [[0] * 3] * 3
grid[0][0] = 1
print(grid)


def add_course(course, cart=None):          # was: cart=[]
    if cart is None:
        cart = []
    cart.append(course)
    return cart


print(add_course("Python"))
print(add_course("SQL"))


def top_mark(marks):
    return max(marks)                       # was: marks.sort(); return marks[-1]


marks = [50, 90, 30]
print(top_mark(marks), marks)
```

Output (Python 3.14):

```text
Scores: [70, 80, 95] Backup: [70, 80]
[[1, 0, 0], [0, 0, 0], [0, 0, 0]]
['Python']
['SQL']
90 [50, 90, 30]
```

</details>


<details>
<summary><b>23 · Shallow and deep copies</b></summary>

**Hint.** A shallow copy (`.copy()`, `[:]`, `list(...)`) makes a **new outer list**, but the things inside are the same objects. `copy.deepcopy` copies every level. Appending a whole new batch to `batches` only changes the outer list, so only the alias sees it; appending a name to the first batch changes an inner list that the shallow copies share.

The rule: if a list contains only numbers, text and tuples, a shallow copy is enough. If it contains lists or dictionaries, a shallow copy shares those inner ones, and you need `copy.deepcopy`. Whenever you see a bug where "I copied it but the copy changed too", look for a shallow copy of something nested.

`solutions/Ex23.py`, run with `python Ex23.py`:

```python
# Exercise 23 - Shallow and deep copies
import copy

batches = [["Lukas", "Priya"], ["Asha"]]
alias = batches
shallow = batches.copy()
sliced = batches[:]
deep = copy.deepcopy(batches)

batches[0].append("Meera")
batches.append(["Rahul"])

print("batches:", batches)
print("alias  :", alias)
print("shallow:", shallow)
print("sliced :", sliced)
print("deep   :", deep)

print(alias is batches)
print(shallow is batches)
print(shallow[0] is batches[0])
print(deep[0] is batches[0])

course = {"name": "Python", "tags": ["beginner"]}
backup = copy.deepcopy(course)
course["name"] = "Python 2"
course["tags"].append("hot")
print("course:", course)
print("backup:", backup)
```

Output (Python 3.14):

```text
batches: [['Lukas', 'Priya', 'Meera'], ['Asha'], ['Rahul']]
alias  : [['Lukas', 'Priya', 'Meera'], ['Asha'], ['Rahul']]
shallow: [['Lukas', 'Priya', 'Meera'], ['Asha']]
sliced : [['Lukas', 'Priya', 'Meera'], ['Asha']]
deep   : [['Lukas', 'Priya'], ['Asha']]
True
False
True
False
course: {'name': 'Python 2', 'tags': ['beginner', 'hot']}
backup: {'name': 'Python', 'tags': ['beginner']}
```

</details>


<details>
<summary><b>24 · Does the function change my list?</b></summary>

**Hint.** Inside a function the parameter is a second label on the caller's list. Calling a method such as `append` or `extend`, or doing `marks[i] = ...`, changes the shared list. **Assigning** a new value to the parameter name (`marks = [...]` or `marks = marks + [...]`) only moves the function's own label.

`add_bonus_in_place` and `extend_in_place` change the caller's list (they change the shared box), `with_bonus`, `reassign` and `concat` do not (they build or point at a new list). A good habit: a function either changes its argument and returns nothing, or builds a new list and returns it, but not both. Python's own `list.sort()` returns `None` for exactly this reason, and `sorted()` returns a new list.

`solutions/Ex24.py`, run with `python Ex24.py`:

```python
# Exercise 24 - Does the function change my list?
def add_bonus_in_place(marks, bonus):
    for i, mark in enumerate(marks):
        marks[i] = mark + bonus


def with_bonus(marks, bonus):
    result = []
    for mark in marks:
        result.append(mark + bonus)
    return result


def reassign(marks):
    marks = [0, 0, 0]


def extend_in_place(marks):
    marks.extend([100])


def concat(marks):
    marks = marks + [100]
    return marks


original = [50, 60, 70]

new_list = with_bonus(original, 5)
print(original, new_list)

reassign(original)
print(original)

concat(original)
print(original)

extend_in_place(original)
print(original)

add_bonus_in_place(original, 10)
print(original)

result = concat(original)
print(result is original, result == original + [100])
```

Output (Python 3.14):

```text
[50, 60, 70] [55, 65, 75]
[50, 60, 70]
[50, 60, 70]
[50, 60, 70, 100]
[60, 70, 80, 110]
False True
```

</details>


<details>
<summary><b>25 · The class gradebook</b></summary>

**Hint.** Take it one function at a time and test each with a `print` before the next. For the average, `sum(marks) / len(marks)` fails on an empty list, so check `if not marks:` first (an empty list counts as False). For the ranking: `[(name, average(marks)) for name, marks in book.items()]`, then `sorted(pairs, key=lambda pair: pair[1], reverse=True)`.

This exercise uses a dictionary of lists, a function that mutates its argument on purpose (`add_mark`) and others that only read, tuples inside a list, a comprehension of each kind, a set, grouping and a deep copy. If you can write it without help, you are ready to build the expense tracker.

`solutions/Ex25.py`, run with `python Ex25.py`:

```python
# Exercise 25 - The class gradebook
import copy


def average(marks):
    if not marks:
        return 0
    return round(sum(marks) / len(marks), 1)


def add_mark(book, name, mark):
    if name not in book:
        book[name] = []
    book[name].append(mark)


def ranking(book):
    pairs = [(name, average(marks)) for name, marks in book.items()]
    return sorted(pairs, key=lambda pair: pair[1], reverse=True)


def passed(book, limit=60):
    return {name for name, marks in book.items() if average(marks) >= limit}


def group_by_grade(book):
    groups = {}
    for name, marks in book.items():
        avg = average(marks)
        if avg >= 85:
            grade = "A"
        elif avg >= 70:
            grade = "B"
        else:
            grade = "C"
        if grade not in groups:
            groups[grade] = []
        groups[grade].append(name)
    return groups


gradebook = {
    "Asha": [92, 88, 95],
    "Lukas": [70, 65],
    "Priya": [85, 90, 78, 88],
    "Rahul": [],
    "Meera": [60, 72, 58],
}

add_mark(gradebook, "Rahul", 81)
add_mark(gradebook, "Sofia", 77)

for position, pair in enumerate(ranking(gradebook), start=1):
    print(f"{position}. {pair[0]:<8}{pair[1]:>6}")

print(sorted(passed(gradebook)))
print(group_by_grade(gradebook))

backup = copy.deepcopy(gradebook)
add_mark(gradebook, "Lukas", 100)
print("Real book:", gradebook["Lukas"])
print("Backup   :", backup["Lukas"])
```

Output (Python 3.14):

```text
1. Asha      91.7
2. Priya     85.2
3. Rahul     81.0
4. Sofia     77.0
5. Lukas     67.5
6. Meera     63.3
['Asha', 'Lukas', 'Meera', 'Priya', 'Rahul', 'Sofia']
{'A': ['Asha', 'Priya'], 'C': ['Lukas', 'Meera'], 'B': ['Rahul', 'Sofia']}
Real book: [70, 65, 100]
Backup   : [70, 65]
```

</details>


---

**Score yourself:** 20-25 working programs means you are ready for the expense tracker build and Module 06. Under 15, rewatch the lesson named above the exercises you missed. Exercises 3, 7, 11, 15 and 22 (reading errors and wrong output) and Exercises 21 and 24 (who shares what) are the best practice for every module that follows.

## What next

In **Module 06 · Files, Text and Errors** your data stops living only inside the program. You will read and write files, load CSV and JSON into the lists and dictionaries you just practised, and handle the crashes you met in Exercises 3, 7, 11 and 15 with `try` and `except` instead of letting the program stop.
