# M13-L03 · Mocking

> Video: Module 13, Lesson 3. Watch it first, then follow along here.

## What you'll learn

- Why a test that calls a real service is slow and fragile, and when a stand-in (a mock) is worth it
- How to swap a name or a setting for one test with pytest's `monkeypatch`, and why it undoes itself
- How `unittest.mock.Mock` records every call, and how `return_value` and `side_effect` decide what it answers
- How `patch` (with block and decorator) swaps a name and hands you the mock
- How to fake the clock, the network and randomness
- Four traps: patching in the wrong place, mocking too much, typos hidden by loose mocks, stale mocks

## Before you start

- Python 3.14 or newer. Check with `python --version`.
- Docker is not needed.
- You should know basic pytest from `m13-l01-your-first-pytest-tests` and `m13-l02-fixtures-and-parametrize`.
- Create a virtual environment and install the pinned packages:

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Files in this folder

| File | What it is |
|------|------------|
| `requirements.txt` | pytest 9.1.1 and httpx 0.28.1 |
| `service.py` | A tiny fake pricing service on port 8133. It waits half a second per answer, like a slow real service |
| `store.py` | The code under test: `fetch_price`, `gst_percent`, `price_with_gst`, `safe_price`, `buy`, `Gateway` |
| `shop.py` | Priya's file, used for the "patch where it is used" trap |
| `promo.py` | `lucky_price`, which uses `random` |
| `toolkit.py` | The `cache_for` decorator from Module 9 (it reads `time.monotonic`) |
| `hook/` | The opening example: `store.py` and `test_hook.py` that really call the service |
| `test_patch.py`, `test_undo.py`, `test_env.py` | `monkeypatch` tests |
| `mock_basics.py`, `mock_effects.py`, `mock_magic.py`, `mock_spec.py` | Small scripts that show `Mock`, `side_effect`, `MagicMock` and `spec` |
| `test_buy.py`, `test_buy_wrong.py`, `test_bank_down.py` | Tests with a mock gateway |
| `test_patch_cm.py`, `test_promo.py` | `patch` as a with block and as a decorator |
| `test_cache_slow.py`, `test_cache_fake.py` | A cache tested by sleeping, then with a fake clock |
| `test_net.py`, `test_down.py` | A fake network, and a fake outage |
| `test_wrong_place.py`, `test_right_place.py` | The wrong and the right address to patch |
| `test_over.py` | An over-mocked test |
| `bug/` | A copy of `store.py` where `+` became `-` (tax taken off), plus two tests |

All prices, names and the port are demo values. Nothing goes to the internet: the "service" runs on your own machine.

## Follow along

### 1. The problem: a test that calls the real service

Start the fake pricing service in one terminal and leave it running:

```bash
python service.py
```

In a second terminal (with the virtual environment active), run the opening test:

```bash
cd hook
python -m pytest test_hook.py
```

You should see (yours will differ in timing):

```text
collected 1 item

test_hook.py .                                 [100%]

================= 1 passed in 0.65s ==================
```

Green, but half a second for one tiny test, because it really called the service. Now stop the service (Ctrl+C in the first terminal), and run the same test again:

```bash
python -m pytest test_hook.py --tb=short
```

```text
E   httpx.ConnectError: [Errno 61] Connection refused
FAILED test_hook.py::test_price_with_gst - httpx.Co...
================= 1 failed in 0.24s ==================
```

Nobody touched the code, yet the test is red. The test was checking the service and the network, not `price_with_gst`. (On Windows the error number differs. The traceback above it is long, so only the last lines are shown.)

Go back up to the lesson folder: `cd ..`. Keep the service stopped from now on, except where a step says to start it.

### 2. `monkeypatch`: swap a name for one test

`test_patch.py`:

```python
import store


def test_gst_added(monkeypatch):
    monkeypatch.setattr(
        store,
        "fetch_price",
        lambda course_id: 500,
    )
    assert store.price_with_gst("c101") == 590
```

```bash
python -m pytest test_patch.py
```

```text
test_patch.py .                                [100%]

================= 1 passed in 0.05s ==================
```

No waiting and no network. `price_with_gst` looked for the name `fetch_price`, found the lambda, and got 500.

### 3. The patch is undone after each test

`test_undo.py` has two tests: the first patches, the second does not. The service is still stopped.

```bash
python -m pytest test_undo.py -v --tb=short
```

```text
test_undo.py::test_with_stand_in PASSED        [ 50%]
test_undo.py::test_without_it FAILED           [100%]
...
E   httpx.ConnectError: [Errno 61] Connection refused
FAILED test_undo.py::test_without_it - httpx.Connec...
============ 1 failed, 1 passed in 0.26s =============
```

`monkeypatch` put the name back as soon as the first test ended. One test can never leave a fake behind for the next one.

### 4. Settings: `monkeypatch.setenv`

`gst_percent()` reads the environment variable `GST_PERCENT` (18 if it is missing). `test_env.py` sets it to 5 for one test: 5 percent of 500 is 25, so the price is 525.

```bash
python -m pytest test_env.py
```

```text
test_env.py .                                  [100%]

================= 1 passed in 0.07s ==================
```

Afterwards the variable is gone again. Relatives to know: `monkeypatch.delenv` removes a variable and `monkeypatch.setitem` changes a dictionary. All undo themselves.

### 5. `Mock` and its diary

`mock_basics.py`:

```python
from unittest.mock import Mock

gateway = Mock()
gateway.charge.return_value = "ok"
print(gateway.charge("Priya", 590))
print(gateway.charge.call_count)
print(gateway.charge.call_args)
gateway.charge("Lukas", 590)
print(gateway.charge.call_args_list)
```

```bash
python mock_basics.py
```

```text
ok
1
call('Priya', 590)
[call('Priya', 590), call('Lukas', 590)]
```

Nobody wrote a `charge` method. The mock made it up when we used it, and it wrote down every call.

### 6. Test `buy` with a mock gateway

`test_buy.py` patches the price with `monkeypatch` and passes a `Mock()` as the gateway. The key line is `gateway.charge.assert_called_once_with("Priya", 590)`.

```bash
python -m pytest test_buy.py
```

```text
test_buy.py .                                  [100%]

================= 1 passed in 0.06s ==================
```

Now the wrong version, `test_buy_wrong.py`, which expects 500 and forgets the tax:

```bash
python -m pytest test_buy_wrong.py --tb=short
```

```text
E   AssertionError: expected call not found.
E   Expected: charge('Priya', 500)
E     Actual: charge('Priya', 590)
FAILED test_buy_wrong.py::test_buy_charges_once - A...
================= 1 failed in 0.14s ==================
```

### 7. Failure on demand: `side_effect`

`mock_effects.py` gives the mock a list: the first call raises, the second returns a value.

```bash
python mock_effects.py
```

```text
first: busy
second: ok
```

`test_bank_down.py` sets `gateway.charge.side_effect = ConnectionError("bank is down")` and checks with `pytest.raises` that `buy` lets the error through:

```bash
python -m pytest test_bank_down.py
```

```text
test_bank_down.py .                            [100%]

================= 1 passed in 0.05s ==================
```

### 8. `Mock` versus `MagicMock`

```bash
python mock_magic.py
```

```text
'unittest.mock.Mock' object does not support the context manager protocol (missed __exit__ method)
MagicMock works with with
```

A plain `Mock` has no double-underscore methods. Use `MagicMock` when your code uses `with`, `len()` or square brackets on the object.

### 9. `patch`: swap a name and get the mock back

With block (`test_patch_cm.py`) and decorator (`test_promo.py`):

```bash
python -m pytest test_patch_cm.py test_promo.py
```

```text
test_patch_cm.py .                             [ 50%]
test_promo.py .                                [100%]
```

The address text `"store.fetch_price"` means: in the module `store`, the name `fetch_price`. In `test_promo.py` we patch `promo.random`, set `choice.return_value = 50`, and the "lucky" price is exactly 250.

Rule of thumb: `monkeypatch` for a simple value in place, `patch` when you want the mock's diary. Both put everything back.

### 10. Fake the clock

First the slow way, which really sleeps:

```bash
python -m pytest test_cache_slow.py
```

```text
test_cache_slow.py .                           [100%]

================= 1 passed in 1.13s ==================
```

Now `test_cache_fake.py`, which replaces the `time` name inside `toolkit` with a `FakeClock` and moves it forward 61 seconds by changing a number:

```bash
python -m pytest test_cache_fake.py
```

```text
test_cache_fake.py .                           [100%]

================= 1 passed in 0.02s ==================
```

A 60-second cache is tested in a hundredth of a second.

### 11. Fake the network, and an outage

`test_net.py` patches `store.httpx.get`. The chain `reply = mock_get.return_value; reply.json.return_value = {...}` mirrors `get(...).json()`. `test_down.py` gives `mock_get` a `side_effect` of `httpx.ConnectError("service is down")` and checks that `safe_price` returns `None`.

```bash
python -m pytest test_net.py test_down.py
```

```text
test_net.py .                                  [ 50%]
test_down.py .                                 [100%]
```

The outage that spoiled Asha's Monday night is now a test that runs every time.

### 12. Trap 1: patch where the name is used

`shop.py` does `from store import fetch_price`, which makes a second name, `shop.fetch_price`. Start the service so the real price (500) can come through:

```bash
python service.py &        # or run it in another terminal
python -m pytest test_wrong_place.py --tb=short
```

```text
E   AssertionError: assert 'Rs 500' == 'Rs 123'
E     - Rs 123
E     + Rs 500
FAILED test_wrong_place.py::test_label - AssertionE...
================= 1 failed in 0.69s ==================
```

The patch moved `store.fetch_price`, but `label` looks at `shop.fetch_price`. Patch the second name instead (`test_right_place.py`):

```bash
python -m pytest test_right_place.py
```

```text
test_right_place.py .                          [100%]

================= 1 passed in 0.05s ==================
```

Stop the service now (`kill %1`, or Ctrl+C in its terminal).

### 13. Trap 2: mocking too much

Inside `bug/`, `store.py` has the tax taken off (minus instead of plus). Run the honest test and the over-mocked one there:

```bash
cd bug
python -m pytest test_patch.py --tb=short
python -m pytest test_over.py
cd ..
```

```text
E   AssertionError: assert 410 == 590
FAILED test_patch.py::test_gst_added - AssertionErr...
================= 1 failed in 0.07s ==================

test_over.py .                                 [100%]
================= 1 passed in 0.04s ==================
```

(The `0x...` address in the failure message will differ.) The over-mocked test replaces `price_with_gst` itself, so it never runs the broken line. Fake the edges (network, clock, randomness, money) and keep your own logic real.

### 14. Trap 3: `spec` catches typos

```bash
python mock_spec.py
```

```text
loose accepted the typo
Mock object has no attribute 'chrage'
```

`Mock(spec=Gateway)` only knows the real methods, so a spelling mistake fails. `create_autospec` goes further and checks arguments too.

Trap 4 has no code: mocks do not change when the real service changes. Keep a few real tests.

## Common mistakes

- Patching where the name was defined instead of where it is used (`shop.fetch_price`, not `store.fetch_price`).
- Replacing so much of your own code that the test only checks the mocks.
- Using a loose `Mock()` for a class you own, so typos pass silently. Add `spec`.
- Forgetting that mocks go stale. If the real service renames a field, your mock still says the old one.
- Using a plain `Mock` in a `with` block. Use `MagicMock`.

## Clean up

- Stop the demo service if it is still running (it listens on port 8133).
- Remove the virtual environment: `deactivate`, then delete the `.venv` folder.
- Delete `__pycache__` and `.pytest_cache` folders if you like.

## Next

[M13-L04 · Coverage and Property-Based Testing](../m13-l04-coverage-and-property-based-testing/)
