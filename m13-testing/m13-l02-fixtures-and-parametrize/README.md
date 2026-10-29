# M13-L02 · Fixtures and Parametrize

> Video: Module 13, Lesson 2. Watch it first, then follow along here.

## What you'll learn

- Why copy-pasted test setup breaks, and how a fixture (`@pytest.fixture`) puts it in one place
- How `yield` splits a fixture into setup and teardown, and why teardown runs even when the test fails
- How `scope="module"` makes a slow fixture run once, and how `conftest.py` shares fixtures with no import
- How `@pytest.mark.parametrize` runs one test over a table of cases, with readable ids
- How the markers `skip`, `skipif`, `xfail` and your own registered marker work
- How `tmp_path` and `capsys` test code that writes files and prints text, plus four fixture and parametrize traps

## Before you start

- Python 3.14 or newer. Check with `python --version`.
- Docker is not needed.
- You should know basic pytest from [m13-l01-your-first-pytest-tests](../m13-l01-your-first-pytest-tests/README.md).
- Install pytest 9.1.1 in a virtual environment (the video uses `uv add --dev pytest`, which gives the same result):

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install pytest==9.1.1
```

## Files in this folder

Each step is a small folder of its own, so that you can run it without the other steps getting in the way. Every command below starts with `cd` into the step folder. Each step folder holds only the files that step needs.

| Step folder | What it is |
|-------------|------------|
| `s01-repeat` | `course.py` (the `Course` class) and three tests that copy the same setup line; one has the wrong seat number |
| `s02-fixture` | The same tests with a `course` fixture |
| `s03-fresh` | A fixture that prints, to show every test gets a fresh value |
| `s04-chain` | A fixture that asks for another fixture (`full_course` asks for `course`) |
| `s05-yield` | A fixture with `yield`: setup, test, teardown |
| `s06-scope-function`, `s07-scope-module` | A slow `catalog` fixture, with the default scope and with `scope="module"` |
| `s08-conftest` | `conftest.py` shares the `course` fixture between two test files |
| `s09-price-copy` to `s13-combo` | `pricing.py` with `final_price`, and `parametrize` in its forms |
| `s14-marks` | `skip`, `skipif` and `xfail` |
| `s15-unregistered-marker`, `s16-registered-marker` | A custom `slow` marker, before and after registering it in `pyproject.toml` |
| `s17-files` | `roster.py` and tests with `tmp_path` and `capsys` |
| `s18-where` | A test that prints the name of its `tmp_path` folder |
| `s19-direct` to `s22-argname` | The four pitfalls |

The course names (Asha, Lukas, Priya, Meera), prices and seat numbers are all demo values.

## Follow along

Timing, the platform line and the paths in the output depend on your machine. The header lines (`platform ...`, `rootdir ...`) are left out below.

### 1. The problem: setup copied into every test

`course.py` has a small `Course` class (a title, a number of seats, `enroll` and `seats_left`). `enroll` refuses a name that is already there and raises `CourseFullError` when the course is full.

`s01-repeat/test_repeat.py` makes `Course("Python Basics", 2)` at the top of every test. Priya asks for a change, Asha edits the number by hand, and she misses the third test, which still says `3`.

```bash
cd s01-repeat
pytest
```

```text
collected 3 items

test_repeat.py ..F                               [100%]

======================= FAILURES =======================
___________________ test_full_course ___________________

    def test_full_course():
        course = Course("Python Basics", 3)
        course.enroll("Lukas")
        course.enroll("Priya")
>       with pytest.raises(CourseFullError):
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
E       Failed: DID NOT RAISE CourseFullError

test_repeat.py:22: Failed
=============== short test summary info ================
FAILED test_repeat.py::test_full_course - Failed: DID...
============= 1 failed, 2 passed in 0.02s ==============
```

The checks were fine. The copy and paste was the problem: one change needs three edits, and one gets forgotten.

### 2. Write the setup once: a fixture

```python
@pytest.fixture
def course():
    return Course("Python Basics", 2)


def test_enroll_adds_student(course):
    course.enroll("Lukas")
    assert course.students == ["Lukas"]
```

A fixture is a function that prepares something a test needs. The decorator hands it to pytest, which remembers it under the name `course`. A test asks for it by writing the name as a parameter. Nobody calls the test with a value: pytest looks at the parameter names, calls the fixture whose name matches, and passes the result in.

```bash
cd ../s02-fixture
pytest
```

```text
collected 3 items

test_fixture.py ...                              [100%]

================== 3 passed in 0.01s ===================
```

### 3. Every test gets a fresh value

```bash
cd ../s03-fresh
pytest -v -s
```

`-v` lists each test, and `-s` lets `print` show.

```text
test_fresh.py::test_first making a course
['Lukas']
PASSED
test_fresh.py::test_second making a course
[]
PASSED
```

"making a course" appears twice, once before each test. The first test enrols Lukas; the second sees an empty list. By default pytest calls the fixture again for every test, so tests cannot disturb each other. That is called isolation.

### 4. Fixtures can ask for other fixtures

```python
@pytest.fixture
def full_course(course):
    course.enroll("Lukas")
    course.enroll("Priya")
    return course
```

```bash
cd ../s04-chain
pytest
```

```text
collected 2 items

test_chain.py ..                                 [100%]

================== 2 passed in 0.02s ===================
```

pytest builds the chain: first `course`, then `full_course`, then the test.

### 5. Clean up with yield

Everything before `yield` is the setup. The value after `yield` goes to the test. Everything after `yield` is the teardown, and it runs after the test is over.

```python
@pytest.fixture
def course():
    print("  setup: the course opens")
    course = Course("Python Basics", 2)
    yield course
    print("  teardown: the course closes")
```

`test_broken` is wrong on purpose (it expects 5 seats left).

```bash
cd ../s05-yield
pytest -v -s --tb=no
```

`--tb=no` hides the long failure report.

```text
collected 2 items

test_yield.py::test_enroll   setup: the course opens
  test: enrolling
PASSED  teardown: the course closes

test_yield.py::test_broken   setup: the course opens
  test: broken
FAILED  teardown: the course closes


=============== short test summary info ================
FAILED test_yield.py::test_broken - AssertionError: a...
============= 1 failed, 1 passed in 0.02s ==============
```

The broken test says `FAILED`, and it still gets its teardown. Use this shape whenever you can say "set up, then clean up": a database connection to open and close, a temporary file to delete, a setting to switch back.

### 6. Scope: do slow setup only once

`catalog` sleeps half a second to pretend it is slow. Three tests use it.

```bash
cd ../s06-scope-function
pytest -v -s
```

```text
collected 3 items

test_scope.py::test_has_python   loading the catalog (slow)
PASSED
test_scope.py::test_has_git   loading the catalog (slow)
PASSED
test_scope.py::test_size   loading the catalog (slow)
PASSED

================== 3 passed in 1.53s ===================
```

The default scope is `function`: one fresh value per test, so the catalog loaded three times. Now add `scope="module"` to the decorator (this is `s07-scope-module`):

```python
@pytest.fixture(scope="module")
def catalog():
```

```bash
cd ../s07-scope-module
pytest -v -s
```

```text
collected 3 items

test_scope_module.py::test_has_python   loading the catalog (slow)
PASSED
test_scope_module.py::test_has_git PASSED
test_scope_module.py::test_size PASSED

================== 3 passed in 0.52s ===================
```

The scopes, from shortest to longest life: `function` (the default), `class`, `module`, `package` and `session` (the whole test run). A wide scope shares one object between tests, so use it only for things tests do not change (see mistake 3).

### 7. Share fixtures with conftest.py

Copying the fixture into every file brings the old problem back. Put it in `conftest.py` and every test file in that folder, and below, can use it with no import.

```python
# conftest.py
import pytest

from course import Course


@pytest.fixture
def course():
    return Course("Python Basics", 2)
```

```bash
cd ../s08-conftest
pytest -v
```

```text
collected 4 items

test_enrol.py::test_enroll_adds_student PASSED   [ 25%]
test_enrol.py::test_full_course PASSED           [ 50%]
test_seats.py::test_all_seats_free PASSED        [ 75%]
test_seats.py::test_one_seat_taken PASSED        [100%]

================== 4 passed in 0.02s ===================
```

Look at `test_enrol.py`: no import for `course`, and not even `import pytest` in `test_seats.py`.

### 8. Parametrize: one test, a table of cases

`pricing.py` has `final_price(price, percent)`: it raises `ValueError` unless the percent is 0 to 100, and otherwise takes the discount off, rounded down. `s09-price-copy` has four tests that are the same except for the numbers (they pass):

```bash
cd ../s09-price-copy
pytest
```

```text
collected 4 items

test_price_copy.py ....                          [100%]

================== 4 passed in 0.02s ===================
```

Now write the test once, with the table of cases next to it (`s10-price`):

```python
@pytest.mark.parametrize(
    "price, percent, expected",
    [
        (1000, 10, 900),
        (1000, 0, 1000),
        (1000, 100, 0),
        (999, 15, 850),
    ],
)
def test_final_price(price, percent, expected):
    assert final_price(price, percent) == expected
```

The first text names the parameters. The list has one tuple per case, and the function takes the same three names. Four tuples, four tests.

```bash
cd ../s10-price
pytest -v
```

```text
collected 4 items

test_price.py::test_final_price[1000-10-900] PASSED [ 25%]
test_price.py::test_final_price[1000-0-1000] PASSED [ 50%]
test_price.py::test_final_price[1000-100-0] PASSED [ 75%]
test_price.py::test_final_price[999-15-850] PASSED [100%]

================== 4 passed in 0.02s ===================
```

To add a case, add one line to the table. In `s11-price-wrong-row` the last row has a wrong expectation, 849 instead of 850:

```bash
cd ../s11-price-wrong-row
pytest -v --tb=short
```

```text
collected 4 items

test_price_bad.py::test_final_price[1000-10-900] PASSED [ 25%]
test_price_bad.py::test_final_price[1000-0-1000] PASSED [ 50%]
test_price_bad.py::test_final_price[1000-100-0] PASSED [ 75%]
test_price_bad.py::test_final_price[999-15-849] FAILED [100%]

======================= FAILURES =======================
_____________ test_final_price[999-15-849] _____________
test_price_bad.py:16: in test_final_price
    assert final_price(price, percent) == expected
E   assert 850 == 849
E    +  where 850 = final_price(999, 15)
=============== short test summary info ================
FAILED test_price_bad.py::test_final_price[999-15-849]
============= 1 failed, 3 passed in 0.02s ==============
```

One bad row does not hide the others, and you always see which row broke.

### 9. Readable ids, errors and combinations

Wrap a case in `pytest.param` to give it an id. A second test checks the error for several bad percents (`s12-price-ids`):

```python
@pytest.mark.parametrize("percent", [-1, 101, 250])
def test_bad_percent(percent):
    with pytest.raises(ValueError):
        final_price(1000, percent)
```

```bash
cd ../s12-price-ids
pytest -v
```

```text
collected 7 items

test_price_ids.py::test_final_price[ten percent] PASSED [ 14%]
test_price_ids.py::test_final_price[no discount] PASSED [ 28%]
test_price_ids.py::test_final_price[free] PASSED [ 42%]
test_price_ids.py::test_final_price[rounds down] PASSED [ 57%]
test_price_ids.py::test_bad_percent[-1] PASSED   [ 71%]
test_price_ids.py::test_bad_percent[101] PASSED  [ 85%]
test_price_ids.py::test_bad_percent[250] PASSED  [100%]

================== 7 passed in 0.01s ===================
```

Stack two `parametrize` lines and pytest tries every combination. Two names and three seat counts make 6 tests:

```bash
cd ../s13-combo
pytest -v
```

```text
collected 6 items

test_combo.py::test_first_student_fits[Lukas-1] PASSED [ 16%]
test_combo.py::test_first_student_fits[Lukas-2] PASSED [ 33%]
test_combo.py::test_first_student_fits[Lukas-3] PASSED [ 50%]
test_combo.py::test_first_student_fits[Priya-1] PASSED [ 66%]
test_combo.py::test_first_student_fits[Priya-2] PASSED [ 83%]
test_combo.py::test_first_student_fits[Priya-3] PASSED [100%]

================== 6 passed in 0.01s ===================
```

Use parametrize when only the data changes. When the steps change, write separate tests.

### 10. Markers: skip, skipif, xfail

A marker is a label on a test. `s14-marks/test_marks.py` has one plain test and one for each built-in marker: `skip` (never run, with a reason), `skipif` (skip only if a condition is true) and `xfail` (expected to fail, because of a known bug).

```bash
cd ../s14-marks
pytest -rsx
```

`-rsx` prints the reason for every skip and expected failure.

```text
collected 4 items

test_marks.py .ssx                               [100%]

=============== short test summary info ================
SKIPPED [1] test_marks.py:12: coupons are not built yet
SKIPPED [1] test_marks.py:17: Linux only
XFAIL test_marks.py::test_rounding_bug - known bug: wrong rounding
======= 1 passed, 2 skipped, 1 xfailed in 0.03s ========
```

A dot, two `s`, and an `x`. The "Linux only" test is skipped here because this was run on a Mac. On Linux you will see 2 passed, 1 skipped. When someone fixes the xfail bug, that test starts to pass, and pytest tells you, so you can remove the marker.

### 11. Your own marker

`s15-unregistered-marker/test_slow.py` labels a test with `@pytest.mark.slow`. Nobody defined `slow`:

```bash
cd ../s15-unregistered-marker
pytest -rsx
```

```text
collected 1 item

test_slow.py .                                   [100%]

=================== warnings summary ===================
test_slow.py:6
  .../test_slow.py:6: PytestUnknownMarkWarning: Unknown pytest.mark.slow - is this a typo?  You can register custom marks to avoid this warning - for details, see https://docs.pytest.org/en/stable/how-to/mark.html
    @pytest.mark.slow

-- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
============= 1 passed, 1 warning in 1.22s =============
```

pytest cannot tell a new label from a spelling mistake. Register it in `pyproject.toml` (this is the file in `s16-registered-marker`):

```toml
[tool.pytest.ini_options]
markers = ["slow: takes more than a second"]
```

Now the warning is gone, and you can choose tests by marker. `-m "not slow"` means: run everything except the slow tests.

```bash
cd ../s16-registered-marker
pytest -m "not slow" -rsx
```

```text
configfile: pyproject.toml
collected 5 items / 1 deselected / 4 selected

test_marks.py .ssx                               [100%]

=============== short test summary info ================
SKIPPED [1] test_marks.py:12: coupons are not built yet
SKIPPED [1] test_marks.py:17: Linux only
XFAIL test_marks.py::test_rounding_bug - known bug: wrong rounding
= 1 passed, 2 skipped, 1 deselected, 1 xfailed in 0.03s =
```

Five tests found, one left out, and the slow one never ran. One more benefit: `pytest --strict-markers` turns a typo in a marker name into an error. Try it back in `s15-unregistered-marker`, where `slow` is not registered:

```text
______________ ERROR collecting test_slow.py ______________
'slow' not found in `markers` configuration option
```

### 12. Testing files and printed text: tmp_path and capsys

`roster.py` saves a course's students into a text file (one name per line), loads them back, and has `announce`, which prints a line about the course. Do not test file code in a real folder: a test could overwrite a real file or leave junk behind. pytest has two built-in fixtures:

- `tmp_path`: a `pathlib.Path` pointing at a brand new, empty folder.
- `capsys`: catches everything the code prints; `capsys.readouterr().out` is the printed text.

```bash
cd ../s17-files
pytest -v
```

```text
collected 3 items

test_files.py::test_roster_round_trip PASSED     [ 33%]
test_files.py::test_missing_file PASSED          [ 66%]
test_files.py::test_announce PASSED              [100%]

================== 3 passed in 0.02s ===================
```

No real folder was touched. Where is `tmp_path`? A tiny test prints the name of its folder:

```bash
cd ../s18-where
pytest -v -s
```

```text
test_where.py::test_first test_first0
PASSED
test_where.py::test_second test_second0
PASSED
```

Each test gets its own folder, named after the test. pytest makes them in the system's temporary area and keeps the last few runs, so you can look inside after a failure. (The full path on your machine will differ.)

## Common mistakes

1. Calling a fixture like a normal function. `s19-direct` has `c = course()` inside the test:

   ```bash
   cd ../s19-direct
   pytest
   ```

   ```text
   ______________________ test_seats ______________________
   Fixture "course" called directly. Fixtures are not meant to be called directly,
   but are created automatically when test functions request them as parameters.
   ```

   Fix: put `course` in the test's brackets, and use what arrives.

2. A typo in the parameter name. `s20-typo` asks for `cours`:

   ```bash
   cd ../s20-typo
   pytest
   ```

   ```text
   test_typo.py E                                   [100%]

   _____________ ERROR at setup of test_seats _____________
   E       fixture 'cours' not found
   >       available fixtures: capfd, capfdbinary, caplog, capsys, ... tmp_path, tmp_path_factory, ...
   ```

   Look at the summary: `E` for error, not `F` for failed. The test never started. The list of available fixtures has no `course`, because this file has none and there is no `conftest.py` here. Its exact list depends on your pytest version.

3. A wide scope on something tests change. In `s21-shared` the fixture has `scope="module"`. The first test enrols Lukas, and the second expects two free seats:

   ```bash
   cd ../s21-shared
   pytest
   ```

   ```text
   test_shared.py .F                                [100%]

   course = Course(title='Python Basics', seats=2, students=['Lukas'])

       def test_empty_at_start(course):
   >       assert course.seats_left() == 2
   E       AssertionError: assert 1 == 2
   ```

   Lukas from the first test is still in the shared course. The bug depends on the order: run the second test alone and it passes. Use a wide scope only for things tests do not change.

4. Parametrize names that do not match the function. `s22-argname` names `price, percent` but the test only takes `price`:

   ```bash
   cd ../s22-argname
   pytest
   ```

   ```text
   collected 0 items / 1 error

   ___________ ERROR collecting test_argname.py ___________
   In test_argname.py::test_x: function uses no argument 'percent'
   !!!!!!!! Interrupted: 1 error during collection !!!!!!!!
   ```

   Zero tests ran. The names in the text and the names in the function must match exactly.

## Clean up

Nothing was created outside this folder except caches. From the folder you ran in:

```bash
find . -name __pycache__ -type d -exec rm -rf {} +
find . -name .pytest_cache -type d -exec rm -rf {} +
deactivate        # leave the virtual environment
```

pytest keeps the `tmp_path` folders in your system's temporary area and clears old ones itself.

## Next

Some code is slow, random, or talks to the internet. The next lesson fakes those parts so tests stay fast and sure: [M13-L03 · Mocking](../m13-l03-mocking/README.md).
