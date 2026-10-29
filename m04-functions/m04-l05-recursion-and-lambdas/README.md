# M04-L05 · Recursion and Lambdas

> Video: Module 4, Lesson 5. Watch it first, then follow along here.

## What you'll learn

- Recursion: a function that calls itself on a smaller problem, with a base case and a recursive case
- The call stack (one frame per call), and what happens with a missing base case (`RecursionError`)
- Recursive `factorial` and `digit_sum`, and how to write the same job with a loop
- Lambdas: tiny nameless functions, and handing a function to another function (`key=len`, `key=lambda ...`)
- Docstrings and `help()`, so a function explains itself

## Before you start

- Python 3.14 or newer (`python --version`). Do [M04-L04](../m04-l04-scope-what-a-function-can-see/) first.
- A terminal opened in this folder.
- Two files (`no_base.py` and `no_smaller.py`) crash with a very long error on purpose, about 1000 lines. Their output below is shortened with `...`.

## Files in this folder

| File | What it is |
|------|------------|
| `countdown.py`, `no_base.py`, `no_smaller.py`, `countdown_loop.py` | A recursive countdown, two ways to break it, and the loop version |
| `limit.py` | Asks Python for the recursion limit |
| `factorial.py`, `factorial_big.py`, `factorial_loop.py` | Recursive factorial, too deep, and the loop version |
| `digit_sum.py` | The digit sum of a ticket number, recursively |
| `double_def.py`, `double_lambda.py`, `add_lambda.py` | The same function as a `def` and as a lambda |
| `key_len.py`, `key_lambda.py`, `pit_len.py`, `pit_return.py` | Handing a function over (`key=`), and two mistakes |
| `doc.py`, `doc_long.py`, `help_abs.py` | Docstrings and `help()` |

## Follow along

### 1. The puzzle: a countdown with no loop

Asha wants a countdown for the start of every live class. Her function has six lines and no loop, but look at the last line of the function: it calls `countdown` again.

**`countdown.py`**

```python
def countdown(n):
    if n == 0:
        print("Go!")
    else:
        print(n)
        countdown(n - 1)


countdown(3)
```

```text
$ python countdown.py
3
2
1
Go!
```

Three, two, one, go, and it works with no loop. A function that calls itself is a recursive function, and this way of solving a problem is called recursion.

### 2. The queue picture

Lukas is somewhere in a long queue and asks the person in front: "how many people are in front of you?" That person cannot answer either, so they ask the person in front of them. And so on, until the question reaches the first person, who knows the answer without asking: nobody. Then the answers travel back: the second person hears 0 and adds one, and so on down the queue. Everybody asked the same question, but each time about a smaller queue. Two parts: the easy question that answers itself and stops everything is the base case, and the step that asks the same question about a smaller problem is the recursive case.

### 3. Base case and recursive case

In `countdown`: the first part, `if n == 0: print("Go!")`, is the base case (nobody to ask, so stop). The second part is the `else`: print `n`, then call `countdown` again with `n - 1`. The same function, on a smaller problem. Every recursive function has two parts: a base case that answers without calling itself, and a recursive case that calls itself on something smaller, so it gets closer to the base case.

### 4. The call stack

Every call gets its own frame (its own set of local names, from [M04-L04](../m04-l04-scope-what-a-function-can-see/)), and Python keeps the frames in a pile called the call stack, where you only add or remove at the top. For `countdown(3)`: a frame is pushed for `n = 3` and prints 3, then a frame on top for `n = 2`, then one for `n = 1`, then one for `n = 0`, which is the base case. At that moment there are four frames on the stack, each with its own `n` (3, 2, 1, 0), and they never get mixed up. The base case is done, so its frame is popped, and the frame below becomes the top again, and so on until the stack is empty. Only the top frame is running and every frame below it waits.

### 5. A missing base case

What if Asha forgets the base case?

```python
def countdown(n):
    print(n)
    countdown(n - 1)


countdown(3)
```

```text
$ python no_base.py
3
2
1
0
-1
-2
...
  [Previous line repeated 996 more times]
RecursionError: maximum recursion depth exceeded
```

The numbers keep falling and after about a thousand calls Python stops the program with a `RecursionError`. Recursion depth is how many frames are piled on the call stack, and every frame takes a bit of memory. Python protects you with a limit. Ask for it:

**`limit.py`**

```python
import sys

print(sys.getrecursionlimit())
```

```text
$ python limit.py
1000
```

There is a second way to cause the same error: the base case is there, but the recursive call does not move toward it (`countdown(n)` instead of `countdown(n - 1)`):

```python
def countdown(n):
    if n == 0:
        print("Go!")
    else:
        print(n)
        countdown(n)


countdown(3)
```

```text
$ python no_smaller.py
3
3
3
...
  [Previous line repeated 996 more times]
RecursionError: maximum recursion depth exceeded
```

The rule: a recursive function needs a base case, and every recursive call must move toward it.

### 6. Recursion that returns an answer

Usually a recursive function returns an answer. Four factorial (written 4!) is 4 x 3 x 2 x 1. The recursive idea: 4! is 4 times 3!, and 3! is 3 times 2!, and so on. The base case: 1! is 1.

**`factorial.py`**

```python
def factorial(n):
    if n == 1:
        return 1
    return n * factorial(n - 1)


print(factorial(4))
```

```text
$ python factorial.py
24
```

24, as calculated by hand. How many frames at the deepest moment? Four. In the first phase, the calls go down: `factorial(4)` waits for `factorial(3)`, which waits for `factorial(2)`, which waits for `factorial(1)`. The base case returns 1 straight away and its frame is popped. In the second phase the answers travel back up: 2 x 1 = 2, 3 x 2 = 6, 4 x 6 = 24.

### 7. Digit sum

Every ticket for a live class has a number like 4321. The digit sum is its last digit plus the digit sum of all the other digits: `n % 10` is the last digit and `n // 10` is the number without it. The base case: a number below 10 is its own digit sum. Guess the output for 4321:

**`digit_sum.py`**

```python
def digit_sum(n):
    if n < 10:
        return n
    return n % 10 + digit_sum(n // 10)


print(digit_sum(4321))
```

```text
$ python digit_sum.py
10
```

10, which is 4 + 3 + 2 + 1. The call stack again has four frames, and the base case is the last one.

### 8. Recursion or a loop?

Anything recursive can also be written with a loop. First, recursion has a limit. A thousand calls need a thousand frames, which is more than the limit allows:

**`factorial_big.py`**

```python
def factorial(n):
    if n == 1:
        return 1
    return n * factorial(n - 1)


print(factorial(1000))
```

```text
$ python factorial_big.py
Traceback (most recent call last):
  File "factorial_big.py", line 7, in <module>
    print(factorial(1000))
          ~~~~~~~~~^^^^^^
  File "factorial_big.py", line 4, in factorial
    return n * factorial(n - 1)
               ~~~~~~~~~^^^^^^^
  File "factorial_big.py", line 4, in factorial
    return n * factorial(n - 1)
               ~~~~~~~~~^^^^^^^
  File "factorial_big.py", line 4, in factorial
    return n * factorial(n - 1)
               ~~~~~~~~~^^^^^^^
  [Previous line repeated 996 more times]
RecursionError: maximum recursion depth exceeded
```

Now the same job with a loop. `result` starts at 1, and for each number from 2 up to `n` we multiply:

**`factorial_loop.py`**

```python
def factorial(n):
    result = 1
    for number in range(2, n + 1):
        result = result * number
    return result


print(factorial(4))
print(len(str(factorial(1000))))
```

```text
$ python factorial_loop.py
24
2568
```

Factorial of 4 is 24, and the second line asks how many digits factorial of 1000 has: 2568. For plain counting and adding, a loop is simpler and has no limit. Recursion is for problems that are naturally about a smaller version of themselves (later in the course, trees and folders). The loop version of the countdown:

**`countdown_loop.py`**

```python
def countdown(n):
    while n > 0:
        print(n)
        n = n - 1
    print("Go!")


countdown(3)
```

```text
$ python countdown_loop.py
3
2
1
Go!
```

Recap: a recursive function calls itself on a smaller problem, needs a base case, and every call has its own frame on the call stack.

### 9. Lambdas

Every function so far was a proper recipe card with a name. Here is a small function written the normal way:

**`double_def.py`**

```python
def double(x):
    return x * 2


print(double(5))
```

```text
$ python double_def.py
10
```

In Python we can write the same thing in one line with the word `lambda`: the parameters, a colon, and one expression, which is returned:

**`double_lambda.py`**

```python
double = lambda x: x * 2

print(double(5))
print(double)
```

```text
$ python double_lambda.py
10
<function <lambda> at 0x10098b110>
```

A lambda is a function with no name of its own. Here we put it in a box called `double`, but printing `double` shows `<function <lambda> at 0x...>`: it is just a function (the memory address differs on your machine). A lambda can take more than one parameter:

**`add_lambda.py`**

```python
add = lambda a, b: a + b

print(add(3, 4))
```

```text
$ python add_lambda.py
7
```

An honest word: putting a lambda into a name like this is only for learning. If you want a name, use `def`. A lambda is for the place where you need a tiny function once.

### 10. Handing a function over

You can hand a function to another function, like handing someone a tool. Which course name is the longest? `max` calls `len` on each name:

**`key_len.py`**

```python
print(max("SQL", "Python", "Go", key=len))
```

```text
$ python key_len.py
Python
```

Look at how we wrote `len`: with no round brackets. We hand over the function itself and `max` calls it. Round brackets mean "do it now", so with brackets Python would call `len()` straight away:

**`pit_len.py`**

```python
print(max("SQL", "Python", "Go", key=len()))
```

```text
$ python pit_len.py
Traceback (most recent call last):
  File "pit_len.py", line 1, in <module>
    print(max("SQL", "Python", "Go", key=len()))
                                         ~~~^^
TypeError: len() takes exactly one argument (0 given)
```

`len takes exactly one argument (0 given)`. When you hand a function over, write only its name.

What if the rule you want is your own? On a 24-hour clock, live classes start at 9, 14, 18 and 20, and we want the one closest to 17. Nine is 8 away, 14 is 3 away, 18 is 1 away, 20 is 3 away:

**`key_lambda.py`**

```python
closest = min(9, 14, 18, 20, key=lambda hour: abs(hour - 17))
print(closest)
```

```text
$ python key_lambda.py
18
```

That is the real use of a lambda: a tiny rule, written exactly where it is needed, and thrown away afterwards. Two limits: a lambda holds only one expression (no several lines) and no `return` word. If you try:

**`pit_return.py`**

```python
double = lambda x: return x * 2
```

```text
$ python pit_return.py
  File "pit_return.py", line 1
    double = lambda x: return x * 2
                       ^^^^^^
SyntaxError: invalid syntax
```

### 11. Docstrings and help

How do you understand a function that Asha wrote six months ago? A docstring is a piece of text in triple quotes, as the very first line of the function. Python keeps it and shows it to anybody who asks, with the built-in `help()`:

**`doc.py`**

```python
def digit_sum(n):
    """Add up the digits of a whole number."""
    if n < 10:
        return n
    return n % 10 + digit_sum(n // 10)


help(digit_sum)
```

```text
$ python doc.py
Help on function digit_sum in module __main__:

digit_sum(n)
    Add up the digits of a whole number.
```

`help` works on Python's own functions too:

**`help_abs.py`**

```python
help(abs)
```

```text
$ python help_abs.py
Help on built-in function abs in module builtins:

abs(x, /)
    Return the absolute value of the argument.
```

A good docstring says what the function does, in one short sentence, not how it does it. For a longer one, add a blank line and an example:

**`doc_long.py`**

```python
def digit_sum(n):
    """Add up the digits of a whole number.

    digit_sum(4321) gives 10.
    """
    if n < 10:
        return n
    return n % 10 + digit_sum(n // 10)


print(digit_sum(4321))
```

```text
$ python doc_long.py
10
```

## Interview tip

"What is recursion, and what is its danger in Python?" A recursive function solves a problem by calling itself on a smaller one, until a base case stops it. The danger is a missing base case or a call that does not get smaller: every call uses stack memory, and Python stops at about 1000 calls with a `RecursionError`. For plain counting a loop is simpler.

## Common mistakes

- No base case, or a recursive call that does not move toward it (`RecursionError`).
- Using recursion for something that is a plain loop, and deep recursion over about 1000 levels.
- Writing `key=len()` instead of `key=len` (do not call it yourself).
- Putting `return` inside a lambda, or trying to write several lines in one.
- A function without a docstring that nobody understands six months later.

## Clean up

Nothing to clean up.

## Next

You have finished Module 4. [M05-L01 · Lists](../../m05-data-structures/m05-l01-lists/)
