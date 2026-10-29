# M08-L04 · Inheritance and Composition

> Video: Module 8, Lesson 4. Watch it first, then follow along here.

## What you'll learn

- Why copying the same code into two classes goes wrong, and how inheritance fixes it
- How to write a child class (`class Student(Person)`), use `super()` and override a method
- How to ask what kind of object you have: `isinstance` versus `type(...) is`
- How Python searches the family tree (the method resolution order, MRO), and what a class method does in a child class
- Why your own errors are subclasses of `Exception`, and why double underscore names exist
- Composition ("has a") and the rule: when in doubt, compose

## Before you start

- Python 3.14 or newer. Check with `python --version` (use `python3 --version` if `python` is not found).
- Lessons M08-L01 to M08-L03 (classes, `__init__`, class methods, private names) and M06-L04 (custom exceptions) help, but no earlier folder is needed. Every file here is self-contained.
- Run the commands from this folder (`m08-l04-inheritance-and-composition`).

## Files in this folder

| File | What it is |
|------|------------|
| `hook.py` | The problem: two classes with the same code, and the greetings have drifted apart |
| `inherit1.py` | `Student(Person)` with `pass`: everything is inherited |
| `child_init.py` | `Student` with its own `__init__`, using `super().__init__(name)` |
| `override.py` | `Instructor` overrides `greet` |
| `super_greet.py` | `Instructor` extends the parent's `greet` with `super().greet()` |
| `isinst.py` | `isinstance` versus `type(...) is` |
| `cm_cls.py` | A class method that uses `cls`: a child builds the right kind of object |
| `cm_person.py` | The same class method written with the class name `Person`: the trap |
| `mangle_inherit.py` | Double underscore names stay separate in parent and child |
| `mro.py` | The method resolution order for `Student` |
| `diamond.py` | Two parents, and which `role` wins |
| `payment.py` | `PaymentError` and `CardDeclinedError`: custom exceptions are subclasses |
| `payment_mro.py` | The MRO of `CardDeclinedError` |
| `wrong.py` | The wrong choice: `Course(Lesson)` |
| `compose.py` | The right choice: a `Course` that has `Lesson` objects |
| `no_super.py` | Pitfall 1: forgetting `super().__init__` |
| `super_args.py` | Pitfall 2: calling `super().__init__()` without the name |
| `tryit.py` | The "try it yourself" solution |

## Follow along

### 1. The problem: the same code in two places

Asha is building the people part of allcsvideos.com. Students and instructors both have a name and both can greet. She wrote one class for each. Last week she changed the student greeting to "Namaste" and forgot the instructor class.

```bash
python hook.py
```

```
Namaste, I am Lukas
Hello, I am Meera
```

The same code lived in two places, and a change was made in only one. With ten classes it gets much worse. Inheritance lets you write the shared part once.

Some words first. A child inherits from a parent, like a bus is a vehicle and gets wheels and an engine for free. The general class is the parent class (or base class). The more special class is the child class (or subclass). The test for when this fits: say "a child is a parent". A student is a person: true. A course is a lesson: false (a course has lessons, which is composition, see step 12).

### 2. A child class with `pass`

```python
class Person:
    def __init__(self, name):
        self.name = name

    def greet(self):
        return f"Hello, I am {self.name}"


class Student(Person):
    pass


lukas = Student("Lukas")
print(lukas.name)
print(lukas.greet())
```

```bash
python inherit1.py
```

```
Lukas
Hello, I am Lukas
```

`Student` wrote nothing, and still can be created with a name and can greet. For `lukas.greet`, Python looks in `Student` first, does not find it, goes up to `Person`, and finds it. The round brackets after the class name declare the family.

### 3. `super()`: the parent part of me

Students need an email too. `Student` gets its own `__init__`. Writing `self.name = name` again would copy `Person`'s code, so we let `Person` do that job with `super()`.

```bash
python child_init.py
```

```
Priya
priya@example.com
Hello, I am Priya
```

The name came from `Person`, the email from `Student`, and `greet` was inherited. Think of a relay race: `Student` passes the name up with `super()`, `Person` stores it and hands control back, then `Student` stores the email.

### 4. Override a method

An instructor should not greet like a student. A method with the same name in the child is called overriding.

```bash
python override.py
```

```
Hello, I am Lukas
Welcome! I am Meera, your instructor
```

Python starts in the child. For `Instructor` it finds `greet` right there and stops. The `greet` of `Person` is never reached.

### 5. Extend instead of replace

`super().greet()` calls the parent's version, so you add to it. `super()` works in any method, not only `__init__`.

```bash
python super_greet.py
```

```
Hello, I am Meera, and I teach here
```

Now the shared greeting lives in `Person`. Change it once and every child follows, unless a child overrides it on purpose.

### 6. What kind of object is it? `isinstance`

```bash
python isinst.py
```

```
True
True
False
False
```

In order: Lukas is a `Student` (True), is a `Person` (True), is an `Instructor` (False), and `type(lukas) is Person` is False because `type` gives exactly one class, `Student`. `isinstance` respects the family, so it is usually the better check: with `Person` it accepts a student, an instructor, and any kind you add next year.

### 7. Class methods and inheritance (a promise from M08-L03)

Asha reads names from a text file, one per line, so `Person` gets a second way in: a class method `from_line`. We call it on `Student`.

```bash
python cm_cls.py
```

```
Priya
True
```

`Student` wrote no class method, so it inherited this one. When called on `Student`, `cls` is `Student`, so the new object really is a `Student`. The class in front of the dot decides.

Now the trap: writing the class name `Person` inside the method instead of `cls`.

```bash
python cm_person.py
```

```
Priya
False
```

The object is only a `Person`, even though we called the method on `Student`. Use `cls` in class methods so children get the right kind of object.

### 8. Double underscore names (a promise from M08-L02)

A name with two leading underscores gets the class name put in front. Here is why: two classes can pick the same word without clashing.

```bash
python mangle_inherit.py
```

```
{'name': 'Lukas', '_Person__token': 'person-token', '_Student__token': 'student-token'}
```

Both survive, each with its own class name in front. With a single underscore the child would have replaced the parent's value. It is rare in everyday code, but now you know why it exists. (The tokens are demo values.)

### 9. The method resolution order (MRO)

The ordered list of classes Python searches is the method resolution order.

```bash
python mro.py
```

```
(<class '__main__.Student'>, <class '__main__.Person'>, <class 'object'>)
['Student', 'Person', 'object']
```

Every class quietly inherits from `object`, the grandparent of everything. The second line uses a list comprehension to print only the names.

A class can have two parents. Both `Student` and `Instructor` have a `role` method. Which one wins for a `TeachingAssistant(Student, Instructor)`?

```bash
python diamond.py
```

```
learns
['TeachingAssistant', 'Student', 'Instructor', 'Person', 'object']
```

Python searches left to right, in the order of the brackets, so `Student` wins. This family shape is called a diamond, and the fixed order gives exactly one answer. It is good to know and rare to need: if you ever meet more than one parent, print the MRO.

### 10. Your own errors are subclasses (a promise from M06-L04)

`class PaymentError(Exception): pass` now reads clearly: `PaymentError` is a child of `Exception`. `CardDeclinedError` is a child of `PaymentError`.

```bash
python payment.py
```

```
paid
Payment problem: card was declined
```

The `except PaymentError` catches the `CardDeclinedError`, because a card declined error is a payment error.

```bash
python payment_mro.py
```

```
['CardDeclinedError', 'PaymentError', 'Exception', 'BaseException', 'object']
```

This is also why `except Exception` catches almost everything: almost every error is a child of `Exception`. A good design is one parent error per area and a child for each specific problem. Callers choose how precise to be.

### 11. Composition: "has a"

First, what happens if you ignore the "is a" test:

```bash
python wrong.py
```

```
True
```

Python does not complain. It cannot read the sentence "a course is a lesson", it only follows your brackets. Now a `Course` claims to be a `Lesson`, and anything expecting a lesson accepts a course by mistake.

### 12. Composition done right

`Lesson` stays a small class. `Course` keeps a list of lessons, `add` puts one in, and `total_minutes` adds them up.

```bash
python compose.py
```

```
30
```

Twelve plus eighteen. Read it from the inside: `basics.lessons` is a list and each item is a `Lesson` object with its own `minutes`. Objects holding objects.

Why many programmers prefer it: it is easier to change (the course can change how it stores lessons), the pieces stay independent (a lesson knows nothing about courses), and there are no long family trees.

The rule: if the child really is a special kind of the parent, inherit. If one thing holds another, compose. When in doubt, compose. In allcsvideos.com a Student is a Person, a Course has Lessons, and an Enrollment has a Student and a Course.

### 13. Pitfall: forgetting `super().__init__`

```bash
python no_super.py
```

```
priya@example.com
Traceback (most recent call last):
  File "no_super.py", line 13, in <module>
    print(priya.name)
          ^^^^^^^^^^
AttributeError: 'Student' object has no attribute 'name'
```

Once a child writes its own `__init__`, Python no longer calls the parent's, so the name was never stored. Fix: call `super().__init__(name)` inside the child's `__init__`.

### 14. Pitfall: calling `super()` without the arguments

```bash
python super_args.py
```

```
Traceback (most recent call last):
  File "super_args.py", line 12, in <module>
    priya = Student("Priya", "priya@example.com")
  File "super_args.py", line 8, in __init__
    super().__init__()
    ~~~~~~~~~~~~~~~~^^
TypeError: Person.__init__() missing 1 required positional argument: 'name'
```

Read the traceback: the call is on line 12, the failing line is 8. Fix: pass it on, `super().__init__(name)`. (The path in your traceback may be longer.)

### 15. Try it yourself

The task from the video: `Person` with a name and `greet`; `Instructor` as a child with an extra `subject`, using `super()` in `__init__`, overriding `greet` to extend the parent's greeting with the subject; create Meera, print her greeting, and print `isinstance` of Meera and `Person`.

```bash
python tryit.py
```

```
Hello, I am Meera, I teach Python
True
```

Try writing it yourself before you open `tryit.py`.

## Common mistakes

- Forgetting `super().__init__(...)` in a child that has its own `__init__` (step 13).
- Calling `super().__init__()` without passing what the parent needs (step 14).
- Using inheritance only to reuse code, or building tall family trees (a child of a child of a child). After three levels nobody remembers which class does what. Ask the "is a" question first; if the answer is no, use composition.
- Writing the class name instead of `cls` in a class method (step 7).
- Using `type(x) is Person` when you mean "any kind of person": use `isinstance`.

Interview tip (Rahul asks: difference between inheritance and composition?). Inheritance models "is a": the subclass receives the parent's attributes and methods, can override them, and calls the parent with `super()`. Composition models "has a": an object holds other objects as attributes and uses them. Use inheritance when the child really is a special kind of the parent; otherwise prefer composition, because it keeps classes independent and avoids deep family trees that break when a parent changes.

## Clean up

Nothing to clean up. Python may create a `__pycache__` folder; you can delete it.

## Next

[M08-L05 · Dunder Methods](../m08-l05-dunder-methods/README.md)
