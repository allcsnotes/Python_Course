# M04-L04 · Scope: What a Function Can See

> Video: Module 4, Lesson 4. Watch it first, then follow along here.

## What you'll learn

- Scope: where a name can be seen. Local names (inside a function) and global names (in the file)
- Why an assignment inside a function makes a new local name and does not change the global one
- The `UnboundLocalError`, and the two fixes: the `global` keyword, or (better) a parameter plus `return`
- Functions inside functions, and the `nonlocal` keyword
- The LEGB rule: Local, Enclosing, Global, Built-in, the order Python searches for a name
- Two traps (hiding a built-in name, and loops that do not make a scope) and why globals cause bugs

## Before you start

- Python 3.14 or newer (`python --version`). Do [M04-L03](../m04-l03-args-and-kwargs/) first.
- A terminal opened in this folder.

## Files in this folder

| File | What it is |
|------|------------|
| `hook.py` | The opening puzzle: a local name used outside its function |
| `room.py`, `same_name.py`, `fresh.py` | Local and global names, a local that hides a global, and a fresh start on every call |
| `read_ok.py`, `unbound.py`, `global_fix.py`, `return_fix.py` | Reading a global, the `UnboundLocalError`, and two fixes |
| `nested.py`, `inner_out.py`, `nonlocal_bad.py`, `nonlocal_ok.py` | Functions inside functions and `nonlocal` |
| `builtin.py`, `legb1.py`, `legb2.py`, `legb3.py`, `legb4.py` | Built-in names, and the LEGB search step by step |
| `shadow.py`, `shadow_fix.py`, `loop_scope.py` | The two traps |
| `global_bug.py`, `global_fix2.py` | Why a global hurts, and the parameter version |

## Follow along

### 1. The puzzle

A function makes a message and prints it. Then, outside it, we print the message again:

**`hook.py`**

```python
def greet():
    message = "Hello, Lukas"
    print(message)

greet()
print(message)
```

```text
$ python hook.py
Hello, Lukas
Traceback (most recent call last):
  File "hook.py", line 6, in <module>
    print(message)
          ^^^^^^^
NameError: name 'message' is not defined
```

The first line works. Then `NameError: name 'message' is not defined`. But `message` was defined, inside the function! The answer is a rule about where a name can be seen: scope.

### 2. Rooms and a notice board

Every meeting room has its own whiteboard, used during the meeting and wiped afterwards. The corridor has a big notice board that every room can see. A name made inside a function is local: it lives only in that function's room. A name made in the file, outside any function, is global: it sits on the notice board. The part of the program where a name can be seen is its scope.

**`room.py`**

```python
course = "Python"

def show():
    lesson = "Scope"
    print(course, lesson)

show()
```

```text
$ python room.py
Python Scope
```

Inside `show` we can use our own local `lesson` and also the global `course`. When `show` finishes, its room is cleaned, `lesson` is gone, and only the notice board stays. Rule 1: a name made inside a function cannot be used outside that function.

### 3. A local name is private

Outside the function `price` is 499. Inside, `price = 100` is an assignment:

**`same_name.py`**

```python
price = 499

def discount():
    price = 100
    print("inside", price)

discount()
print("outside", price)
```

```text
$ python same_name.py
inside 100
outside 499
```

The global did not change. A name is a label stuck on a box. Inside `discount`, the new label `price` is stuck on 100, a new local name. It does not reach out and change the global label. A second fact: every call starts fresh. The first call wrote on its whiteboard, and the board was wiped at the end:

**`fresh.py`**

```python
def visit():
    count = 0
    count += 1
    print(count)

visit()
visit()
```

```text
$ python fresh.py
1
1
```

### 4. Changing a global from a function

`students` counts the enrolments, and reading a global from inside a function works:

**`read_ok.py`**

```python
students = 10

def show():
    print(students)

show()
```

```text
$ python read_ok.py
10
```

Now a function that changes it:

**`unbound.py`**

```python
students = 10

def enroll():
    students += 1
    print(students)

enroll()
```

```text
$ python unbound.py
Traceback (most recent call last):
  File "unbound.py", line 7, in <module>
    enroll()
    ~~~~~~^^
  File "unbound.py", line 4, in enroll
    students += 1
    ^^^^^^^^
UnboundLocalError: cannot access local variable 'students' where it is not associated with a value
```

`UnboundLocalError: cannot access local variable 'students' where it is not associated with a value`. It talks about a local variable, but we never made one, or did we? `students += 1` is short for `students = students + 1`, and an assignment anywhere in a function makes that name local for the whole function. (Remember [M01-L04](../../m01-getting-started/m01-l04-what-happens-when-you-run-python/): Python reads the whole function first, before it runs it.) So when `enroll` runs, `students` is local and still empty, and the line wants to read it to add one. The rule: reading a global is fine, but assign to a name anywhere in a function and that name is local there.

There are two fixes. Fix 1 is the keyword `global`. Write it inside the function, before the name is used:

**`global_fix.py`**

```python
students = 10

def enroll():
    global students
    students += 1

enroll()
enroll()
print(students)
```

```text
$ python global_fix.py
12
```

Starting from 10 and two calls: 12. Both calls changed the real global and the change stayed after the function ended. That works, but I would reach for the second fix first. Fix 2: do not touch the global at all. Hand the value in as a parameter and get the result back with `return`:

**`return_fix.py`**

```python
def enroll(students):
    return students + 1

students = 10
students = enroll(students)
print(students)
```

```text
$ python return_fix.py
11
```

The function sees only what you hand it and tells you the result with `return`. No hidden changes.

### 5. Functions inside functions

You can write a `def` inside another `def`. The small room can look out into the big room:

**`nested.py`**

```python
def welcome():
    course = "Python"

    def say():
        print("Welcome to", course)

    say()

welcome()
```

```text
$ python nested.py
Welcome to Python
```

But it only works one way. The big room cannot see the small room's names, and the inner function is not available outside:

**`inner_out.py`**

```python
def welcome():
    def say():
        print("Hi")

say()
```

```text
$ python inner_out.py
Traceback (most recent call last):
  File "inner_out.py", line 5, in <module>
    say()
    ^^^
NameError: name 'say' is not defined
```

One more keyword. Suppose the inner function wants to change a name of the outer function. It has the same problem as before:

**`nonlocal_bad.py`**

```python
def count_seats():
    seats = 0

    def add():
        seats += 1

    add()
    print(seats)

count_seats()
```

```text
$ python nonlocal_bad.py
Traceback (most recent call last):
  File "nonlocal_bad.py", line 10, in <module>
    count_seats()
    ~~~~~~~~~~~^^
  File "nonlocal_bad.py", line 7, in count_seats
    add()
    ~~~^^
  File "nonlocal_bad.py", line 5, in add
    seats += 1
    ^^^^^
UnboundLocalError: cannot access local variable 'seats' where it is not associated with a value
```

`nonlocal` says "this name belongs to the function around me":

**`nonlocal_ok.py`**

```python
def count_seats():
    seats = 0

    def add():
        nonlocal seats
        seats += 1

    add()
    add()
    print(seats)

count_seats()
```

```text
$ python nonlocal_ok.py
2
```

Two. Without the `nonlocal` line we get the unbound local error again, for the same reason as in step 4.

### 6. Built-in names and LEGB

Since your first lesson you have used `print`, `len`, `int`, `input` and `type` without defining them. They live in the built-in names, which every function in every file can use:

**`builtin.py`**

```python
def count_letters(word):
    return len(word)

print(count_letters("Python"))
```

```text
$ python builtin.py
6
```

Four places where a name can live, from closest to furthest: Local (the function itself), Enclosing (a function around it), Global (the file) and Built-in (Python's own). That is LEGB. When Python meets a name, it looks in exactly this order and stops at the first match. The name `label` is written in three places:

**`legb1.py`**

```python
label = "global"

def outer():
    label = "enclosing"

    def inner():
        label = "local"
        print(label)

    inner()

outer()
```

```text
$ python legb1.py
local
```

Local: Python looked in the closest room first, found `label`, and stopped. Comment out the local line:

**`legb2.py`**

```python
label = "global"

def outer():
    label = "enclosing"

    def inner():
        # label = "local"
        print(label)

    inner()

outer()
```

```text
$ python legb2.py
enclosing
```

Enclosing: nothing local, so Python stepped outward to the function around `inner`. Comment out the enclosing one too:

**`legb3.py`**

```python
label = "global"

def outer():
    # label = "enclosing"

    def inner():
        # label = "local"
        print(label)

    inner()

outer()
```

```text
$ python legb3.py
global
```

Global: it walked out one more room and found it on the notice board. And now comment out the very last label, so the name exists nowhere:

**`legb4.py`**

```python
# label = "global"

def outer():
    # label = "enclosing"

    def inner():
        # label = "local"
        print(label)

    inner()

outer()
```

```text
$ python legb4.py
Traceback (most recent call last):
  File "legb4.py", line 12, in <module>
    outer()
    ~~~~~^^
  File "legb4.py", line 10, in outer
    inner()
    ~~~~~^^
  File "legb4.py", line 8, in inner
    print(label)
          ^^^^^
NameError: name 'label' is not defined
```

Python checks local, enclosing, global and built-in, and finds nothing. This explains the first example: the search only moves outward, never into a function's room.

### 7. Two traps

Pitfall 1: hiding a built-in name. Lukas needs a box for the length of a word and calls it `len`:

**`shadow.py`**

```python
word = "Python"
len = 6
print(len(word))
```

```text
$ python shadow.py
Traceback (most recent call last):
  File "shadow.py", line 3, in <module>
    print(len(word))
          ~~~^^^^^^
TypeError: 'int' object is not callable
```

An `int` is not callable (calling means using round brackets). The real `len` is still there in the built-in room, but the global one stands in front of it. The same trap waits for `print`, `input`, `type`, `int` and `str`. The fix is a better name:

**`shadow_fix.py`**

```python
word = "Python"
length = 6
print(length, len(word))
```

```text
$ python shadow_fix.py
6 6
```

A good habit: if your editor colours a name like a built-in, choose another name.

Pitfall 2, a surprise in the other direction: names made inside a loop do not vanish after it. In Python only a function creates a new scope. Loops, `if` statements and `match` do not:

**`loop_scope.py`**

```python
for i in range(3):
    last = i

print("after the loop:", i, last)
```

```text
$ python loop_scope.py
after the loop: 2 2
```

Both names are still there.

### 8. Why not use global everywhere?

It creates bugs that are very hard to find. Here the same function gives two different answers for the same input:

**`global_bug.py`**

```python
discount = 100

def final_price(price):
    return price - discount

print(final_price(1000))
discount = 500
print(final_price(1000))
```

```text
$ python global_bug.py
900
500
```

The function has a hidden input: it reads `discount` from outside, and nothing in the call shows that. A bug can come from anywhere, and such a function is hard to test. The fix is the one you know, make `discount` a parameter, so the call tells the whole story:

**`global_fix2.py`**

```python
def final_price(price, discount):
    return price - discount

print(final_price(1000, 100))
print(final_price(1000, 500))
```

```text
$ python global_fix2.py
900
500
```

The rule of thumb: a function takes its inputs as parameters and gives its output with `return`. Some globals are fine: constants. A constant is a value that never changes, like a tax rate, and by habit its name is written in capital letters.

## Interview tip

"What is the LEGB rule, and what does the `global` keyword do?" LEGB is the order in which Python searches for a name: Local, Enclosing, Global, Built-in, stopping at the first match. `global` inside a function says that an assignment to that name should change the global name instead of making a local one. Better still, pass values in as parameters and return results.

## Common mistakes

- Using a function's local name outside the function.
- Assigning to a global inside a function without `global` (`UnboundLocalError`).
- Naming a variable `len`, `print`, `input`, `type`, `int` or `str`.
- Expecting names made inside a loop to disappear.
- Using globals as hidden inputs instead of parameters.

## Clean up

Nothing to clean up.

## Next

[M04-L05 · Recursion and Lambdas](../m04-l05-recursion-and-lambdas/)
