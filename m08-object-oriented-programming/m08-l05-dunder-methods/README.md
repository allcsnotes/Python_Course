# M08-L05 · Dunder Methods

> Video: Module 8, Lesson 5. Watch it first, then follow along here.

## What you'll learn

- What a dunder method is, and the rule of this lesson: you do not call them, you write them and Python calls them
- `__str__` versus `__repr__`: text for people versus text for programmers
- `__eq__` and `__hash__`: what "equal" means for your class, and why the two go together
- `__len__`, `__iter__` and `__getitem__`: make your class behave like a collection
- `__lt__`: sorting, `min` and `max`
- Three beginner pitfalls

## Before you start

- Python 3.14 or newer. Check with `python --version` (use `python3 --version` if `python` is not found).
- Lessons M08-L01 to M08-L04 (classes, `__init__`, `isinstance`). Sets and dictionaries (Module 5) help for the `__hash__` part.
- Run the commands from this folder (`m08-l05-dunder-methods`).

In the video every stage program is the same file called `shop.py`, which grows step by step. To keep each stage runnable on its own, this folder saves every stage as a separate file (`s1_str.py`, `s2_list.py` ...). Tracebacks below are shortened to the last line; the file name in yours will match the file you ran.

## Files in this folder

| File | What it is |
|------|------------|
| `hook.py` | The problem: printing a plain `Course` |
| `s1_str.py` | Adds `__str__` |
| `s2_list.py` | A list of courses still shows the ugly default |
| `s3_repr.py` | Adds `__repr__` |
| `s3b_repronly.py` | Only `__repr__`, no `__str__` |
| `s4_eq0.py` | Default `==`: two equal-looking courses are different |
| `s5_eq1.py` | Adds `__eq__` |
| `s5b_eqerr.py` | Pitfall: comparing a course with the number 5 |
| `s6_eq2.py` | `__eq__` with `isinstance` and `NotImplemented` |
| `s7_hash0.py` | Putting equal courses in a set: unhashable |
| `s8_hash.py` | Adds `__hash__` |
| `s9_len0.py` | `len(course)` fails |
| `s10_len.py` | Adds `__len__` |
| `s10b_bool.py` | A course with no lessons counts as False |
| `s11_iter0.py` | A `for` loop over a course fails |
| `s12_iter.py` | Adds `__iter__` |
| `s13_get0.py` | `course[0]` fails |
| `s14_get.py` | Adds `__getitem__` |
| `s15_sort0.py` | `sorted` of courses fails |
| `s16_lt.py` | Adds `__lt__` |
| `s17_key.py` | Sorting by title with `key=` |
| `course.py` | The final `Course` class with all nine dunder methods |
| `demo.py` | Imports `Course` and uses it like a built-in type |
| `p1_strint.py` | Pitfall 1: `__str__` returns a number |
| `p2_typo.py` | Pitfall 2: a typo in the dunder name |
| `p3_mutate.py` | Pitfall 3: changing the title of a course that is in a set |

## Follow along

### 1. The problem: printing a course

Asha has a `Course` class for allcsvideos.com. A course has a title, a price and a list of lessons. She makes one and prints it.

```bash
python hook.py
```

```
<__main__.Course object at 0x104cd9fd0>
```

Not the title, not the price: just the object's place in memory. The number will differ on your computer. Printing is only the first problem. `len(course)`, a `for` loop over the lessons, comparing two identical courses and sorting a list of courses all fail too. Python's own lists, strings and numbers do all of this because they have special methods with double underscores, called dunder methods. Today we give them to our own class.

Think of sockets in a wall: every socket has the same shape, and any machine with the matching plug works. Python's features (print, length, the `for` loop, `==`, sorting) are the sockets. A method with the exact right name is the plug. The map for today:

- `print` asks for `__str__`
- `==` asks for `__eq__`
- `len` asks for `__len__`
- a `for` loop asks for `__iter__`
- square brackets ask for `__getitem__`
- `<` (which sorting uses) asks for `__lt__`

You never call a dunder method yourself, just like `__init__`.

### 2. `__str__`: readable text

```python
    def __str__(self):
        return f"{self.title} (Rs {self.price})"
```

```bash
python s1_str.py
```

```
Python Basics (Rs 499)
Now watching: Python Basics (Rs 499)
```

An f-string, and the `str()` function, ask the object for its text the same way `print` does, so they use `__str__` too. The method must return a string.

### 3. The catch: lists use the exact text

```bash
python s2_list.py
```

```
Python Basics (Rs 499)
[<__main__.Course object at 0x109bb9fd0>, <__main__.Course object at 0x109b9a490>]
```

(Your memory addresses will differ.) Python keeps two kinds of text for an object. `__str__` is for the person using the program: friendly and short. `__repr__` (short for representation) is for the programmer: exact, with every detail. A list always uses the exact kind for the things inside it.

### 4. `__repr__`: exact text

The goal is text that looks like the code that builds the same object. `!r` after a value means "show it the exact way", which keeps the quote marks on the title.

```python
    def __repr__(self):
        return f"Course({self.title!r}, {self.price}, {self.lessons})"
```

```bash
python s3_repr.py
```

```
Python Basics (Rs 499)
[Course('Python Basics', 499, ['Intro', 'Loops']), Course('Loops Deep Dive', 299, ['while', 'for'])]
```

You could copy that text, paste it into a file and rebuild the course. That is the mark of a good `__repr__`.

The REPL (the interactive prompt, start it with `python`) shows the exact kind too:

```python
>>> lesson = "Intro"
>>> lesson
'Intro'
>>> print(lesson)
Intro
>>> ["Intro", "Loops"]
['Intro', 'Loops']
```

This is the same split, and it is why a list of words always shows quote marks. Try the same with our class, from this folder:

```python
>>> from course import Course
>>> basics = Course("Python Basics", 499, ["Intro", "Loops"])
>>> basics
Course('Python Basics', 499, ['Intro', 'Loops'])
>>> print(basics)
Python Basics (Rs 499)
```

One rescue rule: if a class has only `__repr__` and no `__str__`, `print` uses `__repr__`.

```bash
python s3b_repronly.py
```

```
Course('Python Basics', 499, ['Intro', 'Loops'])
```

The other way round does not work, so if you write just one, write `__repr__`. To remember: `__str__` is for people (print, f-strings), `__repr__` is for programmers (lists, the REPL, debugging tools).

### 5. `__eq__`: when are two courses equal?

Two courses with the same title, price and lessons:

```bash
python s4_eq0.py
```

```
False
False
```

The first line is `first == second`, the second is `first is second` (the very same object). Python's default: two objects are equal only if they are the very same object, like two sheets of paper with the same words on them. For a course we want: the same title means the same course.

```python
    def __eq__(self, other):
        return self.title == other.title
```

The object on the left of `==` is `self`, the one on the right is `other`.

```bash
python s5_eq1.py
```

```
True
False
```

`==` follows our rule. `is` still asks the strict question, so it is still False. `!=` works too: Python flips our answer.

Now a pitfall: comparing a course with the number 5.

```bash
python s5b_eqerr.py
```

```
AttributeError: 'int' object has no attribute 'title'
```

Python handed our method `5` as `other`, and `5` has no title. The fix: check with `isinstance` and return the special value `NotImplemented` ("this is not my business"). Python then answers False.

```python
    def __eq__(self, other):
        if not isinstance(other, Course):
            return NotImplemented
        return self.title == other.title
```

```bash
python s6_eq2.py
```

```
True
False
```

### 6. `__hash__`: equal things need the same locker number

A set keeps each thing only once. Put the two equal courses in a set:

```bash
python s7_hash0.py
```

```
TypeError: cannot use 'Course' as a set element (unhashable type: 'Course')
```

The moment we wrote `__eq__`, Python quietly removed the default hash. A set or dictionary finds things by a locker number, the hash. The rule: things that are equal must get the same locker number. The default number came from the object's place in memory, which breaks the rule once we change what equal means, so Python refuses instead of giving wrong answers.

The cure is `__hash__`, using exactly the field that `__eq__` compares:

```python
    def __hash__(self):
        return hash(self.title)
```

```bash
python s8_hash.py
```

```
1
3
```

The set holds one course, not two. The dictionary stored `3` under `first`, and asking with `second` (a different but equal object) finds it. Rule to keep: if you write `__eq__`, write `__hash__` from the same field, and only use values that never change.

### 7. `__len__`: the length of a course

```bash
python s9_len0.py
```

```
TypeError: object of type 'Course' has no len()
```

```python
    def __len__(self):
        return len(self.lessons)
```

```bash
python s10_len.py
```

```
2
```

Bonus: Python uses the length for truth tests too. An empty course counts as False, even though it is a course.

```bash
python s10b_bool.py
```

```
True
False
```

### 8. `__iter__`: loop over the lessons

```bash
python s11_iter0.py
```

```
TypeError: 'Course' object is not iterable
```

"Iterable" means you can go through it one item at a time. A `for` loop looks for `__iter__`. We pass the list's own walker along (how a walker works is the first lesson of Module 9):

```python
    def __iter__(self):
        return iter(self.lessons)
```

```bash
python s12_iter.py
```

```
Intro
Loops
True
['Intro', 'Loops']
```

That one method also gave us `"Loops" in basics` and `list(basics)`.

### 9. `__getitem__`: square brackets

```bash
python s13_get0.py
```

```
TypeError: 'Course' object is not subscriptable
```

```python
    def __getitem__(self, index):
        return self.lessons[index]
```

```bash
python s14_get.py
```

```
Intro
Loops
['Intro']
```

Because we pass the index along, negative numbers (`basics[-1]`) and slices (`basics[:1]`) work for free.

### 10. `__lt__`: sorting

```bash
python s15_sort0.py
```

```
TypeError: '<' not supported between instances of 'Course' and 'Course'
```

Sorting asks one question again and again: is this one less than that one? In our shop, cheaper means less.

```python
    def __lt__(self, other):
        return self.price < other.price
```

```bash
python s16_lt.py
```

```
Loops Deep Dive (Rs 299)
Python Basics (Rs 499)
Data Structures (Rs 899)
Loops Deep Dive (Rs 299)
Data Structures (Rs 899)
```

The first three lines are `sorted`, then `min` (the cheapest) and `max` (the dearest). Only `<` is needed for sorting. `>` works because Python turns the question around, but `<=` does not work until you write `__le__` too. In the next lesson a dataclass writes these boring methods for you.

`__lt__` gives the course one natural order. For another order, use the `key=` setting you know from the lists lesson. It wins, and `__lt__` stays as the default:

```bash
python s17_key.py
```

```
Data Structures (Rs 899)
Loops Deep Dive (Rs 299)
Python Basics (Rs 499)
```

### 11. All nine together

`course.py` holds the final class with all the dunder methods. `demo.py` imports it (Module 7) and uses it like something built in:

```bash
python demo.py
```

```
Python Basics (Rs 499)
[Course('Python Basics', 499, ['Intro', 'Loops']), Course('Loops Deep Dive', 299, ['while', 'for'])]
True 1
2 Intro True
Loops Deep Dive (Rs 299)
```

Not one of these lines calls a dunder method by name. The table to remember:

- `print`, f-strings, `str()` call `__str__`
- lists, the REPL, logs call `__repr__`
- `==` calls `__eq__`; sets and dictionaries call `__hash__`
- `len` calls `__len__`; `for` and `in` call `__iter__`; `[ ]` calls `__getitem__`; sorting calls `__lt__`

### 12. Pitfall 1: `__str__` returns a number

```bash
python p1_strint.py
```

```
TypeError: __str__ returned non-string (type int)
```

The method must return a string. Wrap the number in an f-string or in `str(...)`.

### 13. Pitfall 2: a typo in the dunder name

```bash
python p2_typo.py
```

```
<__main__.Course object at 0x1099f9fd0>
```

No error at all, and your address will differ. `__str_` (one underscore at the end) is just another method with an odd name. Dunder names must be exact: two underscores on each side.

### 14. Pitfall 3: changing a value that is hashed

```bash
python p3_mutate.py
```

```
True
False
```

The course is in the set, but after its title changes Python cannot find it: the hash changed, so Python looks in the wrong locker. This is why we hash only values that never change.

### 15. Try it yourself

Write a `Lesson` class with a title and minutes. Give it `__repr__` and `__str__`. Make two equal lessons and print the result of `==`. Then sort a few lessons by minutes. (No solution file: compare with how `Course` does it in `course.py`.)

## Common mistakes

- Calling dunder methods yourself instead of letting Python call them.
- Writing `__eq__` without `__hash__` (the object becomes unusable in sets and as dictionary keys).
- Comparing with `other.title` before checking that `other` is a `Course`.
- `__str__` returning something that is not a string.
- A typo in a dunder name: no error, the feature just does not work.
- Changing a field that `__hash__` uses while the object is in a set or dictionary.

Interview tip (Rahul asks: difference between `__str__` and `__repr__`?). `__str__` gives readable text for the end user; `print` and f-strings use it. `__repr__` gives exact text for developers, ideally code that rebuilds the object; lists, the REPL and logs use it. If only `__repr__` exists, `str()` falls back to it, so write `__repr__` first.

## Clean up

Nothing to clean up. Python may create a `__pycache__` folder (from `import course`); you can delete it.

## Next

[M08-L06 · Dataclasses, Enums and Abstract Classes](../m08-l06-dataclasses-enums-and-abstract-classes/README.md)
