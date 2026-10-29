# M05-L02 · Tuples and Unpacking

> Video: Module 5, Lesson 2. Watch it first, then follow along here.

## What you'll learn

- What a tuple is, and why the comma (not the brackets) makes it
- Why a tuple cannot be changed, and how to get a new value anyway
- Unpacking a tuple into labels, with `_` to ignore and `*` to collect the rest
- How a function gives back several values as one tuple
- `enumerate` and `zip`, and the two-label `for` loop
- When to choose a tuple and when a list

## Before you start

- Python 3.14 or newer. Check with `python --version`.
- No Docker needed. Best after M05-L01 (lists) in the folder `../m05-l01-lists/`; it also uses `*args` from M04-L03.

## Files in this folder

| File | What it is |
|------|------------|
| `hook.py` | divmod, the swap and the bag of extra values |
| `tuple_make.py` | A tuple of title, price and level, read by index |
| `tuple_walk.py` | Slice and for loop on a tuple |
| `bracket_cards.py` | Maths brackets against tuple commas |
| `comma.py` | Types of a, b, c and d |
| `lessons.py` | Pack on the right, unpack on the left |
| `immut_bad.py` | TypeError on purpose |
| `immut_new.py` | A new tuple with the new price |
| `long_way.py` | Picking each value by index |
| `unpack.py` | Unpacking a tuple into three labels |
| `unpack_few.py` | ValueError: two labels for three values |
| `unpack_many.py` | ValueError: four labels for three values |
| `swap.py` | The swap with the tuple made visible |
| `ignore.py` | Skip the price |
| `star.py` | cheapest, *others and friends |
| `star_edge.py` | Nothing left over: an empty list |
| `star_two.py` | Two stars: SyntaxError on purpose |
| `star_summary.py` | The three uses of the star |
| `return_split.py` | Split an amount in paise into rupees and paise |
| `return_range.py` | Return the smallest and largest price |
| `enum_pairs.py` | Printing each pair as a tuple |
| `enum_loop.py` | Unpacking each pair in the for line |
| `zip_pairs.py` | Printing each zipped pair |
| `zip_loop.py` | Unpacking each pair in the for line |
| `record_cards.py` | Three tuple records: course, map point, colour |
| `len_bug.py` | Six letters, or one value? |
| `append_bad.py` | AttributeError on purpose |
| `zip_short.py` | Three titles, two prices |
| `tryit.py` | A possible answer to Your turn |

There is nothing to install: every file is plain Python and runs on its own.

## Follow along

Open a terminal in this folder. Each step shows the code, the command, and the output you should see.

### 1. Three odd things from earlier modules

Three times Python showed us something odd and we said: we will explain that later. `divmod` gave a pair, `a, b = b, a` swapped two labels, and the bag of extra values in a `def` line printed in round brackets. All three are the same idea: a tuple.

`hook.py`:
```python
print(divmod(17, 5))

a, b = 1, 2
a, b = b, a
print(a, b)

def show(*prices):
    print(prices)
show(1499, 999, 1999)
```
```bash
python hook.py
(3, 2)
2 1
(1499, 999, 1999)
```

Round brackets with commas between the values: that is a tuple.

### 2. Make a tuple

A course has a title, a price and a level. Think of a printed train ticket: a few facts in a fixed order, printed once. A list is the sign-up sheet that changes; a tuple is the printed ticket. Indexes, negative indexes and `len` work as they do on text. Square brackets pick a slot, even though the tuple is written with round brackets. Python prints the text inside with single quotes: that is only its habit.

`tuple_make.py`:
```python
course = ("Python Basics", 1499, "beginner")
print(course)
print(type(course))
print(course[0])
print(course[-1])
print(len(course))
```
```bash
python tuple_make.py
('Python Basics', 1499, 'beginner')
<class 'tuple'>
Python Basics
beginner
3
```

### 3. Slice and loop

Slices make a new tuple, and `for` walks through one value at a time.

`tuple_walk.py`:
```python
course = ("Python Basics", 1499, "beginner")
print(course[:2])
for part in course:
    print(part)
```
```bash
python tuple_walk.py
('Python Basics', 1499)
Python Basics
1499
beginner
```

### 4. The comma makes the tuple

Brackets in maths only group things, so `(5)` is just the number 5. A single value needs its comma: `(5,)`. `5, 6` is a tuple even with no brackets. The empty tuple is the one exception: it has no commas, so it needs `()`.

`bracket_cards.py`:
```python
print((2 + 3) * 4)
print((5))
x = 5,
print(x)
y = 5, 6
print(y)
```
```bash
python bracket_cards.py
20
5
(5,)
(5, 6)
```

`comma.py`:
```python
a = (5)
b = (5,)
c = 5, 6
d = ()
print(type(a))
print(type(b))
print(c)
print(d)
```
```bash
python comma.py
<class 'int'>
<class 'tuple'>
(5, 6)
()
```

### 5. The other half of the module 2 line

Remember this line from module 2. The right side is a tuple made by a comma with no brackets at all; the left side is the other half of the idea, unpacking.

`lessons.py`:
```python
lessons_completed, lessons_total = 12, 104
print(lessons_completed, lessons_total)
```
```bash
python lessons.py
12 104
```

### 6. A tuple cannot be changed

The price drops, so we try to put 999 into slot 1.

`immut_bad.py`:
```python
course = ("Python Basics", 1499)
course[1] = 999
```
```bash
python immut_bad.py
Traceback (most recent call last):
  File "immut_bad.py", line 2, in <module>
    course[1] = 999
    ~~~~~~^^^
TypeError: 'tuple' object does not support item assignment
```

You can read every slot, but you cannot write to one.

### 7. Build a new tuple instead

We do not change the old tuple. We build a new one from pieces and put the label back onto it.

`immut_new.py`:
```python
course = ("Python Basics", 1499)
course = (course[0], 999)
print(course)
```
```bash
python immut_new.py
('Python Basics', 999)
```

Why would anyone want something that cannot change? Because it is a promise: a course record, a point on a map or a colour should never change by accident.

### 8. Unpacking: the long way and the short way

We could write three lines, one label per slot. Python has a shorter way.

`long_way.py`:
```python
course = ("Python Basics", 1499, "beginner")
title = course[0]
price = course[1]
level = course[2]
print(title, price, level)
```
```bash
python long_way.py
Python Basics 1499 beginner
```

`unpack.py`:
```python
course = ("Python Basics", 1499, "beginner")
title, price, level = course
print(title)
print(price)
print(level)
```
```bash
python unpack.py
Python Basics
1499
beginner
```

Python matches by position: the first label gets the first value, and so on. This is called unpacking. The number of labels must match the number of values.

### 9. Too few or too many labels

Break it on purpose, both ways round.

`unpack_few.py`:
```python
course = ("Python Basics", 1499, "beginner")
title, price = course
```
```bash
python unpack_few.py
Traceback (most recent call last):
  File "unpack_few.py", line 2, in <module>
    title, price = course
    ^^^^^^^^^^^^
ValueError: too many values to unpack (expected 2, got 3)
```

`unpack_many.py`:
```python
course = ("Python Basics", 1499, "beginner")
title, price, level, rating = course
```
```bash
python unpack_many.py
Traceback (most recent call last):
  File "unpack_many.py", line 2, in <module>
    title, price, level, rating = course
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^
ValueError: not enough values to unpack (expected 4, got 3)
```

Python tells you both numbers. The cure is always the same: count the values, and count the labels.

### 10. The swap, in the open

`a, b = b, a` first works out the right side, which makes a tuple, then unpacks that tuple onto `a` and `b`.

`swap.py`:
```python
a = 1
b = 2
pair = (b, a)
print(pair)
a, b = pair
print(a, b)
```
```bash
python swap.py
(2, 1)
2 1
```

No third cup was needed, because the tuple holds both values safely for a moment.

### 11. Ignore a value with an underscore

The underscore is an ordinary label. It only tells the reader: I do not care about this one.

`ignore.py`:
```python
course = ("Python Basics", 1499, "beginner")
title, _, level = course
print(title, level)
```
```bash
python ignore.py
Python Basics beginner
```

### 12. Star: collect the leftovers

The star you know from `*args` also works on the left of an unpacking. The starred label takes everything that is left over.

`star.py`:
```python
prices = (499, 999, 1499, 1999)
cheapest, *others = prices
print(cheapest)
print(others)
*front, last = prices
print(front, last)
first, *middle, last = prices
print(middle)
```
```bash
python star.py
499
[999, 1499, 1999]
[499, 999, 1499] 1999
[999, 1499]
```

`star_edge.py`:
```python
pair = (499, 1999)
first, *middle, last = pair
print(middle)
```
```bash
python star_edge.py
[]
```

`star_two.py`:
```python
prices = (499, 999, 1499, 1999)
first, *a, *b = prices
```
```bash
python star_two.py
  File "star_two.py", line 2
    first, *a, *b = prices
    ^^^^^^^^^^^^^
SyntaxError: multiple starred expressions in assignment
```

The leftovers are always collected into a list, even though `prices` is a tuple. Only one starred label is allowed in one unpacking.

### 13. Three stars side by side

In a `def` line a star packs extra values into a tuple. In a call a star unpacks a bundle into separate values. On the left of an equals sign a star packs the leftovers into a list.

`star_summary.py`:
```python
def show(*prices):
    print(prices)

show(1, 2)
prices = (1, 2, 3)
print(*prices)
first, *rest = prices
print(rest)
```
```bash
python star_summary.py
(1, 2)
1 2 3
[2, 3]
```

### 14. Return several values

A function can return only one thing, but that one thing can be a tuple. `return a, b` is exactly `return (a, b)`. There is no special feature for several return values: the caller unpacks the tuple. That is how `divmod` gave us its pair.

`return_split.py`:
```python
def split_price(amount):
    return amount // 100, amount % 100

result = split_price(235882)
print(result)
print(type(result))
rupees, paise = split_price(235882)
print(rupees, paise)
```
```bash
python return_split.py
(2358, 82)
<class 'tuple'>
2358 82
```

`return_range.py`:
```python
def price_range(prices):
    return min(prices), max(prices)

low, high = price_range((1499, 999, 1999, 499))
print(low, high)
```
```bash
python return_range.py
499 1999
```

### 15. enumerate hands out pairs

Each pair is a number and a value; `start=1` counts from 1 (without `start` it counts from 0).

`enum_pairs.py`:
```python
courses = ("Python Basics", "SQL Basics", "Git Basics")
for pair in enumerate(courses, start=1):
    print(pair)
```
```bash
python enum_pairs.py
(1, 'Python Basics')
(2, 'SQL Basics')
(3, 'Git Basics')
```

`enum_loop.py`:
```python
courses = ("Python Basics", "SQL Basics", "Git Basics")
for number, title in enumerate(courses, start=1):
    print(f"{number}. {title}")
```
```bash
python enum_loop.py
1. Python Basics
2. SQL Basics
3. Git Basics
```

### 16. zip joins two rows

Like the zip on a jacket: the first of each, then the second of each, and so on. Every joined pair is a tuple.

`zip_pairs.py`:
```python
titles = ("Python Basics", "SQL Basics", "Git Basics")
prices = (1499, 999, 799)
for pair in zip(titles, prices):
    print(pair)
```
```bash
python zip_pairs.py
('Python Basics', 1499)
('SQL Basics', 999)
('Git Basics', 799)
```

`zip_loop.py`:
```python
titles = ("Python Basics", "SQL Basics", "Git Basics")
prices = (1499, 999, 799)
for title, price in zip(titles, prices):
    print(f"{title}: Rs {price}")
```
```bash
python zip_loop.py
Python Basics: Rs 1499
SQL Basics: Rs 999
Git Basics: Rs 799
```

Whenever you see a `for` loop with two labels, a tuple is being unpacked on every trip.

### 17. Tuple or list?

A list is for a collection that grows, shrinks and gets edited: students in a class, items in a cart. A tuple is for a fixed record where each position has its own meaning.

`record_cards.py`:
```python
course = ("Python Basics", 1499, "beginner")
point = (50.11, 8.68)
colour = (255, 140, 0)
print(course)
print(point)
print(colour)
```
```bash
python record_cards.py
('Python Basics', 1499, 'beginner')
(50.11, 8.68)
(255, 140, 0)
```

Ask yourself: would it make sense to add one more value? A third latitude makes no sense, so that is a tuple. One more student always makes sense, so that is a list.

### 18. Mistake 1: the missing comma

`len_bug.py`:
```python
tags = ("python")
print(len(tags))
tags = ("python",)
print(len(tags))
```
```bash
python len_bug.py
6
1
```

Without the comma the brackets did nothing, so `tags` is just the text `python` with 6 letters.

### 19. Mistake 2: a list habit

`append_bad.py`:
```python
course = ("Python Basics", 1499)
course.append("beginner")
```
```bash
python append_bad.py
Traceback (most recent call last):
  File "append_bad.py", line 2, in <module>
    course.append("beginner")
    ^^^^^^^^^^^^^
AttributeError: 'tuple' object has no attribute 'append'
```

A tuple cannot grow, so it has no `append`. Build a new tuple, or use a list from the start.

### 20. Mistake 3: zip stops at the shorter row

`zip_short.py`:
```python
titles = ("Python Basics", "SQL Basics", "Git Basics")
prices = (1499, 999)
for title, price in zip(titles, prices):
    print(f"{title}: Rs {price}")
```
```bash
python zip_short.py
Python Basics: Rs 1499
SQL Basics: Rs 999
```

Only two lines, and no error at all: the third course silently vanishes. Make sure the two rows have the same length.

### 21. Your turn

Write a function that returns the smallest and largest of three prices and unpack the result into `low` and `high`. Then unpack the same three prices with `first` and `*rest`. Here is one answer:

`tryit.py`:
```python
def min_max(prices):
    return min(prices), max(prices)

low, high = min_max((1499, 999, 1999))
print(low, high)
first, *rest = (1499, 999, 1999)
print(first, rest)
```
```bash
python tryit.py
999 1999
1499 [999, 1999]
```

## Common mistakes

- A single value needs its trailing comma: `("python")` is just text, `("python",)` is a tuple.
- Tuples have no `append`; they cannot grow. Build a new tuple or start with a list.
- Wrong number of labels when unpacking is a `ValueError`, and the message tells you both numbers.
- `zip` stops at the shorter row, with no error.
- A tuple cannot change, but if one of its values is a list, that list can still be changed inside. Fixed slots, not fixed insides.

## Clean up

Nothing to clean up: these scripts create no files.

## Next

[M05-L03 - Dictionaries](../m05-l03-dictionaries/)
