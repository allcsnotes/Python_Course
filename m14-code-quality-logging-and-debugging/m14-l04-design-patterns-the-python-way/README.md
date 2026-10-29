# M14-L04 · Design Patterns the Python Way

> Video: Module 14, Lesson 4. Watch it first, then follow along here.

## What you'll learn

- What a design pattern is: a named, proven way to arrange code
- Strategy: the part that changes becomes a function, kept in a dictionary or passed as a parameter
- Factory: a function (or a dictionary of classes) that makes the right object
- Observer: a list of callbacks, and a `try` block so one broken listener does not stop the rest
- Dependency injection: pass what a function needs as a parameter, so tests pass a fake
- Three pitfalls: a shared list in a class body, a pattern for nothing, a singleton you do not need

## Before you start

- Python 3.14 or newer. Check with `python --version`.
- `pytest` for the test steps: `pip install pytest` in a virtual environment (or `uv add --dev pytest`). The video used pytest 9.1.1.
- Optional: `pyright` (`pip install pyright`) for step 8. The video used pyright 1.1.414.
- No Docker needed. Earlier lessons: M13-L03 (mocking), M10-L02 (Protocol), M08 (dataclasses).
- Run every command from inside this folder. Timings ("yours will differ") depend on your machine.

## Files in this folder

| File | What it is |
|------|------------|
| `hook.py` | The `if/elif` chain and the silent typo |
| `classy.py`, `plain.py` | The same idea as classes and as plain functions |
| `discounts.py`, `try_discounts.py`, `add_rule.py` | Strategy: rules in a dictionary, the loud typo, a new rule |
| `cart.py`, `cut_by.py` | A rule as a parameter, and rules built with a closure |
| `recall_factory.py` | `default_factory=list` as a small factory |
| `payments.py`, `make_demo.py` | Factory: card and UPI gateways (fake, wait 0.5 s) and `make_gateway` |
| `events.py`, `listeners.py`, `observer_demo.py` | Observer: subscribe and publish |
| `crash_demo.py`, `safe_events.py`, `safe_demo.py` | A listener that crashes, and the protected `publish` |
| `checkout_hard.py`, `test_hard.py`, `test_hard_patched.py` | A hidden dependency, a slow test, a monkeypatched test |
| `checkout.py`, `test_checkout.py`, `bad_fake.py` | Dependency injection with a `Protocol`, a fake gateway, a broken fake |
| `shop.py`, `app.py`, `test_shop.py` | All four patterns together |
| `shared_list.py`, `fixed_list.py` | Pitfall one |
| `too_much.py` | Pitfall two |
| `config.py`, `single.py` | Pitfall three: a module is a singleton |

## Follow along

### 1. The problem

```bash
python hook.py
```

```text
800
1000
```

`hook.py` has `final_price(price, kind)` with `student` (20 percent off), `festival` (10), `bulk` (15), and the price back unchanged for any other kind. The second line has the word `student` mistyped (`studnet`): no error, no warning, Lukas got no discount. And a new offer means editing this working function again.

### 2. What is a pattern?

A design pattern is a name for a proven way to arrange code, like "fry" or "boil" in cooking. You get a tested solution and a shared word for the team. Four patterns today: strategy (choose standard or express delivery: same order, different way), factory (say "one latte" and one arrives), observer (the bell on a video channel), dependency injection (a lamp has a plug, not a power station).

Python needs fewer classes because functions are values, classes are objects, and duck typing can be written down as a `Protocol`. Compare `classy.py` (a `StudentDiscount` class with `apply`, and a `Checkout` class) with `plain.py` (a function `student` and a `total` that calls whatever function it is given):

```bash
python classy.py
python plain.py
```

```text
800
800
```

When a class has one method and no data, a plain function does the same job with less to read.

### 3. Strategy

The part that changes becomes a function, and the functions go in a dictionary. The values are the functions themselves, with no round brackets, because we only store them (`discounts.py`):

```python
DISCOUNTS = {
    "student": student,
    "festival": festival,
    "bulk": bulk,
}


def final_price(price, kind):
    return DISCOUNTS[kind](price)
```

```bash
python try_discounts.py
```

```text
800
Traceback (most recent call last):
  File "try_discounts.py", line 4, in <module>
    print(final_price(1000, "studnet"))
          ~~~~~~~~~~~^^^^^^^^^^^^^^^^^^
  File "discounts.py", line 21, in final_price
    return DISCOUNTS[kind](price)
           ~~~~~~~~~^^^^^^
KeyError: 'studnet'
```

(The `~~^^` markers may differ a little in your output.) The typo is now a loud error. Meera's launch offer is one new entry (`add_rule.py`):

```bash
python add_rule.py
```

```text
750
```

A function is a value, so it can also be handed to another function (`cart.py`):

```bash
python cart.py
```

```text
1200
1300
```

Rules that differ only in a number can be built with a closure (`cut_by.py`):

```bash
python cut_by.py
```

```text
800 900
400
```

Use a class for a strategy when a rule needs several methods or keeps changing data (for example, a rule that counts how often it was used). A `Protocol` can list the methods every rule must have.

### 4. Factory

`recall_factory.py` shows a factory you already know: `field(default_factory=list)`. Each `Order` gets its own new list.

```bash
python recall_factory.py
```

```text
['c101'] []
```

`payments.py` has `CardGateway` and `UpiGateway` (each `charge` waits half a second to pretend to ask a bank) and a dictionary of classes, no round brackets, because a class is an object too:

```python
GATEWAYS = {"card": CardGateway, "upi": UpiGateway}


def make_gateway(kind):
    if kind not in GATEWAYS:
        raise ValueError(f"unknown payment kind: {kind}")
    return GATEWAYS[kind]()
```

```bash
python make_demo.py
```

```text
UpiGateway
upi: charged Lukas Rs 590
Traceback (most recent call last):
  ...
ValueError: unknown payment kind: crypto
```

The caller never wrote a class name. Bank transfer later means one new class and one new dictionary entry. A factory in Python is just a function that returns an object, or a dictionary of classes.

### 5. Observer

`events.py` is a small class with a list of listeners (plain functions). `subscribe` appends, `publish` loops and calls each listener with the student and the amount. `listeners.py` has `send_receipt`, `count_sale` and `send_sms` (which raises `ConnectionError`, fake).

```bash
python observer_demo.py
```

```text
email: receipt for Lukas, Rs 590
stats: one more sale, Rs 590
```

Email first, then stats: the order of the `subscribe` lines. Now subscribe `send_sms` in the middle, with the SMS service "down":

```bash
python crash_demo.py
```

```text
email: receipt for Lukas, Rs 590
Traceback (most recent call last):
  ...
ConnectionError: sms service is down
```

The stats line never appears: the error stopped the `for` loop. The fix (`safe_events.py`) wraps each call in `try` / `except Exception as error`, reports which listener failed, and carries on. In a real program you would write that report with logging (last lesson).

```bash
python safe_demo.py
```

```text
email: receipt for Lukas, Rs 590
send_sms failed: sms service is down
stats: one more sale, Rs 590
```

### 6. Dependency injection

`checkout_hard.py` builds a `CardGateway` inside the function, so the function decides which bank it talks to. Its test goes to the "bank":

```bash
pytest test_hard.py
```

```text
test_hard.py .                                                           [100%]

============================== 1 passed in 0.52s ===============================
```

Passed, but in about half a second (yours will differ slightly) because it really called the gateway. The mocking fix (`test_hard_patched.py`) moves the name `CardGateway` inside the module `checkout_hard` to a fake class with `monkeypatch`:

```bash
pytest test_hard_patched.py
```

```text
============================== 1 passed in 0.01s ===============================
```

It works, but the test must know the module and the hidden name inside; rename the class and the test breaks or silently misses. The simpler way is a parameter (`checkout.py`). Whoever calls `checkout` hands in the gateway:

```python
class Gateway(Protocol):
    def charge(self, student: str, amount: int) -> str: ...


def checkout(student: str, price: int, gateway: Gateway) -> str:
    return gateway.charge(student, price)
```

Anything with a `charge` method that takes a student and an amount and returns text counts as a `Gateway`: the card gateway, the UPI gateway, and a fake with no inheritance. (This is also what `buy` did in the mocking lesson: it took the gateway as a parameter, and a `Mock` went in with no patch.) `test_checkout.py` uses a small `FakeGateway` that records charges in a list:

```bash
pytest test_checkout.py
```

```text
============================== 1 passed in 0.01s ===============================
```

About 0.01 s against 0.5 s before (yours will differ). Who builds the real gateway? The start-up code at the edge of the program: `checkout("Priya", 590, make_gateway("upi"))` in production, a fake in a test.

### 7. All four together

`shop.py`:

```python
def place_order(student, price, discount, gateway, events):
    amount = discount(price)
    receipt = gateway.charge(student, amount)
    events.publish(student, amount)
    return receipt
```

The discount is a strategy; the gateway and the events are injected. `app.py` builds the real parts: two listeners, `DISCOUNTS["student"]`, `make_gateway("upi")`.

```bash
python app.py
```

```text
email: receipt for Lukas, Rs 800
stats: one more sale, Rs 800
upi: charged Lukas Rs 800
```

(It takes half a second because of the fake bank wait.) `test_shop.py` uses a fake gateway, a lambda listener that saves what it hears, and a lambda discount (`p - 50`):

```bash
pytest test_shop.py
```

```text
============================== 1 passed in 0.01s ===============================
```

Four patterns and not one patch. The only new class is the little fake.

### 8. The Protocol protects the fakes (optional, needs pyright)

`bad_fake.py` has a fake whose method is named `pay` instead of `charge`:

```bash
pyright bad_fake.py
python bad_fake.py
```

```text
bad_fake.py:9:24 - error: Argument of type "BrokenGateway" cannot be assigned to parameter "gateway" of type "Gateway" in function "checkout"
    "BrokenGateway" is incompatible with protocol "Gateway"
      "charge" is not present (reportArgumentType)
1 error, 0 warnings, 0 informations
...
AttributeError: 'BrokenGateway' object has no attribute 'charge'
```

(Pyright prints the full file path before `:9:24`.) The checker tells you before you run; Python only complains when the line runs.

### 9. The pitfalls

Pitfall one: a list written in the class body, outside `__init__`, is a class attribute shared by every object (`shared_list.py`). The fix creates it inside `__init__` (`fixed_list.py`). The question is: how many listeners does `second` have when only `first` subscribed?

```bash
python shared_list.py
python fixed_list.py
```

```text
1
0
```

Pitfall two: a pattern for nothing. `too_much.py` prints "hello" with a strategy class, a factory class and a chain of calls, then with `print("hello")`:

```bash
python too_much.py
```

```text
hello
hello
```

Patterns are tools for a pain you can name. Write plain code first. Reach for a pattern when you edit the same `if/elif` chain a third time, or when a test is hard to write.

Pitfall three: you do not need a singleton. A module runs once on import, so it is already one. `config.py` holds a settings dictionary; `single.py` imports it under two names:

```bash
python single.py
```

```text
USD
True
```

## Common mistakes

1. A list in the class body shared by every object. Create it in `__init__`.
2. Using a pattern with no pain behind it. Plain code first.
3. Writing a singleton class. A module with a dictionary is Python's singleton.
4. Calling the function when you store it: `"student": student()` runs it now. Store `student`, with no round brackets.
5. In observer, letting one failing listener stop the rest. Catch the error inside `publish` and report it.

## Clean up

```bash
rm -rf __pycache__ .pytest_cache
```

## Next

[M15-L01 · How the Web Works and Your First Endpoint](../../m15-web-apis-with-fastapi/m15-l01-how-the-web-works-and-your-first-endpoint/)
