# M08-L06 · Dataclasses, Enums and Abstract Classes

> Video: Module 8, Lesson 6. Watch it first, then follow along here.

## What you'll learn

- Build a class from a short list of fields with `@dataclass`, and give fields safe defaults (`default_factory` for lists)
- Lock an object with `frozen=True`, and check rules with `__post_init__`
- Make a fixed menu of choices with `Enum`, and avoid its two traps (comparing, JSON)
- Write a rule that subclasses must follow with `ABC` and `@abstractmethod`
- Put the three tools together in a piece of the allcsvideos.com model

## Before you start

- Python 3.14 or newer. Check with `python --version` (use `python3 --version` if `python` is not found).
- Lessons M08-L04 (inheritance) and M08-L05 (dunder methods, `__hash__`), and M04 (default values, the mutable default trap).
- Run the commands from this folder (`m08-l06-dataclasses-enums-and-abstract-classes`).

Tracebacks below are shortened to the last line or two. Yours will show the full file path and extra lines; the last line is the one to compare.

## Files in this folder

| File | What it is |
|------|------------|
| `hook_long.py` | A `Lesson` class with `__init__`, `__repr__` and `__eq__` written by hand |
| `hook_short.py` | The same class with `@dataclass` |
| `dc_types.py` | Annotations are not checked at run time |
| `dc_kw.py` | Keywords in any order, editing a field, comparing |
| `dc_default.py` | A field with a default value |
| `dc_order.py` | Error: a required field after a default one |
| `dc_list_bad.py` | Error: a list as a default |
| `dc_factory.py` | `field(default_factory=list)` |
| `dc_frozen.py` | `frozen=True`: read-only objects |
| `dc_unhash.py` | A normal dataclass is unhashable |
| `dc_hash.py` | A frozen dataclass can live in a set |
| `dc_post.py` | `__post_init__` checks a rule |
| `en_str.py` | The problem with text choices |
| `en_basic.py` | A first `Enum`: member, name, value, lookups |
| `en_loop.py` | Looping over an enum |
| `en_typo.py` | A typo in a member name is an error |
| `en_bad.py` | A wrong value is an error |
| `en_cmp.py` | Trap 1: comparing members |
| `en_json1.py` | Trap 2: an enum member in JSON |
| `en_json2.py` | The fix: save `.value`, rebuild with `Level(...)` |
| `ab_silent.py` | The problem: a base class that quietly does nothing |
| `ab_abc.py` | An abstract class cannot be created |
| `ab_missing.py` | A subclass that forgot `pay` cannot be created |
| `ab_ok.py` | Both subclasses write `pay` |
| `domain.py` | `Level`, `Lesson` and `Course` together |
| `ab_forgot.py` | Pitfall: `@abstractmethod` without inheriting from `ABC` |
| `tryit.py` | The "try it yourself" solution |

## Follow along

### 1. The problem: a box of three values needs a lot of typing

Asha writes the `Lesson` class for allcsvideos.com: a title, a length in minutes and a flag saying whether it is free. Written by hand it needs `__init__`, `__repr__` and `__eq__`: eleven lines, and the class has not done anything yet.

```bash
python hook_long.py
```

```
Lesson(Variables, 12, True)
True
```

Now the same class with a data class: five lines plus one import.

```python
from dataclasses import dataclass


@dataclass
class Lesson:
    title: str
    minutes: int
    free: bool
```

```bash
python hook_short.py
```

```
Lesson(title='Variables', minutes=12, free=True)
True
```

Same behaviour, less than half the lines, and the print shows the name of every value. Python wrote the boring methods.

Three pictures for the three tools of this lesson. A data class is a paper form: you list the labelled boxes and Python builds the rest. An enum is a drop-down menu: a fixed list of allowed choices, and a wrong choice is caught at once. An abstract class is a head-office rule book: every payment method must have a `pay` method, and the rule book itself is not a shop you can use.

### 2. Data classes

`@dataclass` is a decorator (a label above a class, like `@property` and `@classmethod`) that says "write the boring methods for this class". Each field line has a name, a colon and a kind of value (`str` for text, `int` for a whole number, `bool` for True or False). That note is called an annotation. From the fields Python writes `__init__`, `__repr__` (class name plus every field) and `__eq__` (compares all fields).

Keywords in any order, editing a field, and comparing:

```bash
python dc_kw.py
```

```
Lesson(title='Variables', minutes=12)
15
False
```

A data class object is an ordinary object and can be edited. The comparison is False because minutes is now 15 and the other lesson says 12: every field must match.

Is the annotation checked? Here `minutes` gets the text `"twelve"`:

```bash
python dc_types.py
```

```
Lesson(title='Variables', minutes='twelve')
```

Nothing happens. The annotation is a note for readers and tools; Python does not enforce it at run time. Module 10 (type hints) shows tools that read these notes and warn you.

### 3. Defaults

Most lessons are not free, so `free: bool = False`. This is the same idea as default parameters in Module 4.

```bash
python dc_default.py
```

```
Lesson(title='Variables', minutes=12, free=False)
Lesson(title='Welcome', minutes=3, free=True)
Lesson(title='Loops', minutes=15, free=True)
```

The first uses the default, the other two replace it, one by position and one by keyword. The same rule as for functions: fields without a default come first.

```bash
python dc_order.py
```

```
TypeError: non-default argument 'minutes' follows default argument 'free'
```

The error comes the moment the class is defined, because Python tried to write `__init__` and could not. Put required fields first and optional fields after.

### 4. A list as a default: `default_factory`

```bash
python dc_list_bad.py
```

```
ValueError: mutable default <class 'list'> for field lessons is not allowed: use default_factory
```

The data class saw the trap from Module 4 and refused, which plain functions never did. A factory is a recipe that makes a new thing each time. `field` is a second tool from `dataclasses`. Notice `list` has no brackets: we hand over the recipe, not a finished list.

```python
@dataclass
class Course:
    title: str
    lessons: list = field(default_factory=list)
```

```bash
python dc_factory.py
```

```
Course(title='Python', lessons=['Variables'])
Course(title='SQL', lessons=[])
```

Each course got its own list. The rule: for a list, dictionary or set always use `default_factory` with `list`, `dict` or `set`. Numbers, text, `True`, `False` and `None` are safe as plain defaults.

### 5. Frozen objects

If Priya edits the minutes of a published lesson by accident, the bug is hard to find. `@dataclass(frozen=True)` locks the objects.

```bash
python dc_frozen.py
```

```
Lesson(title='Variables', minutes=12)
Traceback (most recent call last):
  ...
dataclasses.FrozenInstanceError: cannot assign to field 'minutes'
```

The object is read only, like a tuple. To change a lesson, make a new one.

A frozen object has a second gift. Last lesson: when a class defines `__eq__`, its objects lose their hash. A normal data class writes `__eq__` for you, so it has the same problem:

```bash
python dc_unhash.py
```

```
TypeError: cannot use 'Lesson' as a set element (unhashable type: 'Lesson')
```

With `frozen=True` Python also writes `__hash__` from the fields, so a frozen lesson can live in a set or be a dictionary key. Three lessons, two identical:

```bash
python dc_hash.py
```

```
2
```

Choose by one question. Will the object be edited later? Normal data class. Should it never change, or be used in sets and as a key? Frozen.

### 6. Rules with `__post_init__`

A data class writes `__init__` for you, so a rule such as "minutes must be positive" goes into `__post_init__`, which Python calls right after `__init__` has stored the values.

```bash
python dc_post.py
```

```
Lesson(title='Variables', minutes=12)
Traceback (most recent call last):
  ...
ValueError: minutes must be positive
```

In the full traceback, the line named `__init__` with `File "<string>"` is the method the data class wrote. It called our `__post_init__`, which raised the error. A data class is still a normal class: you can add methods.

Recap: `@dataclass` writes init, repr and eq from the annotated fields. Defaults go last, a list needs `default_factory`. `frozen=True` makes an object read only and hashable, and `__post_init__` checks the rules.

### 7. Enums: the drop-down menu

The simplest way to store a course level is text. Here the level is "Beginner" with a capital B, and the check uses a small b:

```bash
python en_str.py
```

```
No badge
```

No error. One capital letter (or a typo) silently broke the check. An `Enum` is a fixed list of named choices. Each choice is a member, with a name in capital letters and a value.

```python
class Level(Enum):
    BEGINNER = 1
    INTERMEDIATE = 2
    ADVANCED = 3
```

```bash
python en_basic.py
```

```
Level.BEGINNER
BEGINNER
1
Level.INTERMEDIATE
Level.ADVANCED
```

In order: the member, its `.name`, its `.value`, a lookup by value `Level(2)`, and a lookup by name `Level["ADVANCED"]`.

Looping over the whole menu, in the order written:

```bash
python en_loop.py
```

```
1 BEGINNER
2 INTERMEDIATE
3 ADVANCED
3
```

A typo is now an error at once, with a hint:

```bash
python en_typo.py
```

```
AttributeError: type object 'Level' has no attribute 'BEGINER'. Did you mean: 'BEGINNER'?
```

A wrong value is caught too:

```bash
python en_bad.py
```

```
ValueError: 9 is not a valid Level
```

Wrong name: attribute error. Wrong value: value error. Nothing slips through quietly.

### 8. Two enum traps

Trap 1, comparing. A member is not its value.

```bash
python en_cmp.py
```

```
True
False
True
Traceback (most recent call last):
  ...
TypeError: '<' not supported between instances of 'Level' and 'Level'
```

The same member is equal (True). The member is not the number 1 (False). The values can be compared (True). Members have names, not an order, so `<` fails: if you need order, compare `.value`.

Trap 2, JSON (from Module 6):

```bash
python en_json1.py
```

```
TypeError: Object of type Level is not JSON serializable
when serializing dict item 'level'
```

JSON knows text, numbers, lists and dictionaries, not enum members. Save the value, and rebuild the member when you read it back:

```bash
python en_json2.py
```

```
{"level": 1}
Level.BEGINNER
```

We use this in the build.

### 9. Abstract classes: the rule book

The site takes payments. `Payment` is a base class whose `pay` does nothing yet. `CardPayment` inherits from it but, by mistake, defines `charge` instead of `pay`.

```bash
python ab_silent.py
```

```
Order confirmed
```

Nobody was charged. The call reached the do-nothing `pay` of the base class and returned quietly. A shop that confirms orders without taking money is a disaster, and Python said nothing.

An abstract class makes Python refuse. `ABC` stands for Abstract Base Class. `Payment` inherits from `ABC` and `@abstractmethod` above `pay` marks it as "no real body here, every subclass must write its own".

```python
from abc import ABC, abstractmethod


class Payment(ABC):
    @abstractmethod
    def pay(self, amount):
        pass
```

Can we create a plain `Payment`?

```bash
python ab_abc.py
```

```
TypeError: Can't instantiate abstract class Payment without an implementation for abstract method 'pay'
```

To instantiate means to create an object. An abstract class is only a rule book. Now the card class that typed `charge` instead of `pay`:

```bash
python ab_missing.py
```

```
TypeError: Can't instantiate abstract class CardPayment without an implementation for abstract method 'pay'
```

The error comes at creation, before "Order confirmed" and before any money moves. A silent mistake is now loud and early. With both classes writing `pay`:

```bash
python ab_ok.py
```

```
Paid Rs 2499 by UPI
Paid Rs 2499 by card
```

One call, `method.pay(...)`, and each class does its own version, like overriding in M08-L04. Use an abstract class when a base class is only a template and every subclass must fill in some methods.

### 10. Putting it together

A piece of the allcsvideos.com model. `Level` is the enum from before, `Lesson` is a frozen data class, and `Course` is a data class with a price in whole rupees, a level that starts as `BEGINNER`, and a list of lessons made by `default_factory`. An enum member is safe as a plain default because a member never changes. The list is not, so it uses `default_factory`. The class also has an ordinary method, `total_minutes`.

```bash
python domain.py
```

```
Course(title='Python', price=2499, level=<Level.BEGINNER: 1>, lessons=[Lesson(title='Variables', minutes=12), Lesson(title='Loops', minutes=15)])
27
```

Twelve plus fifteen is 27. The next video, the build, creates the whole model with these tools.

### 11. Pitfall: `@abstractmethod` without `ABC`

```bash
python ab_forgot.py
```

```
Created with no error
```

The `@abstractmethod` line only works inside a class that inherits from `ABC`. Without it there is no protection at all, and nothing warns you. Always write `class Payment(ABC):`.

Which tool when? A class that mostly holds values: a data class. A value from a small fixed list: an enum. A base class that is only a template: an abstract class. A class that is mostly behaviour: a plain class is still right.

### 12. Try it yourself

Write a `Student` data class with a name, a status enum with `ACTIVE` and `PAUSED`, and a list of courses. Then an abstract `Report` class with a `render` method, and one subclass that fills it in. A solution is in `tryit.py`; try first.

```bash
python tryit.py
```

```
ACTIVE active
PAUSED paused
Asha -> ['Python']
Student(name='Asha', status=<Status.ACTIVE: 'active'>, courses=['Python'])
```

## Common mistakes

- Putting a field without a default after a field with one (step 3).
- Using `[]` or `{}` as a data class default instead of `default_factory` (step 4).
- Expecting annotations to be checked: they are not, put rules in `__post_init__` (step 2, 6).
- Comparing an enum member with its value (`level == 1`), or with `<`. Compare member with member, or `.value` with `.value` (step 8).
- Putting an enum member straight into JSON: save `.value` (step 8).
- Forgetting `ABC` when using `@abstractmethod` (step 11).
- Using a data class for something that is mostly behaviour.

Interview tip (Rahul asks: what does the `dataclass` decorator do, and why not write a normal class?). It reads the annotated fields and writes `__init__`, `__repr__` and `__eq__`, so a class that mostly holds data stays short. Mutable defaults like lists need `default_factory`. `frozen=True` makes objects read only and hashable. It does not check types, so rules go in `__post_init__`.

## Clean up

Nothing to clean up. Python may create a `__pycache__` folder; you can delete it.

## Next

[M08-B04 · Build the allcsvideos Domain Model](../m08-b04-build-the-allcsvideos-domain-model/README.md)
