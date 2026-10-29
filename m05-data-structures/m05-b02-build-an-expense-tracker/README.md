# M05-B02 · Build an Expense Tracker

> Video: Module 5, Build 2. Watch it first, then follow along here.

A small terminal program for allcsvideos.com students (and Asha) to see where the money goes. You add what you spent, see a neat table of everything, and see the total for each category. It uses everything from Modules 1 to 5: lists, dictionaries, sets, functions, `match`, loops and f-strings.

## What you'll learn

- How to plan a program on paper (requirements first) before writing code
- How to store data as a list of dictionaries, and reach a fact with a double lookup: `expenses[1]["note"]`
- One function per job, with the list passed in as a parameter instead of a global name
- Neat tables with f-string widths, and totals with a dictionary and `.get(cat, 0)`
- Guarding input with `replace` and `isdigit`, and a menu built from `while True` and `match`

## Before you start

- Python 3.14 or newer. Check with `python --version`.
- Docker is not used. No packages to install.
- Modules 1 to 5 (especially Lesson 6 of Module 5, on how a list passed to a function is the same list).

## Files in this folder

| File | What it is |
|------|------------|
| `expenses.py` | The finished program (95 lines), as at the end of the video |
| `step1/data.py` | Step 1: the shape of the data |
| `step2/tracker.py` | Step 2: `add_expense` |
| `step3/tracker.py` | Step 3: `show_expenses`, the table |
| `step3/width.py` | A note longer than its column is not cut by a width |
| `step3/tracker_cut.py` | Step 3 with long notes cut using a slice |
| `step4/tracker.py` | Step 4: `totals_by_category` and `show_totals` |
| `step5/check.py` | Testing the `replace` + `isdigit` guard |
| `step5/tracker.py` | Step 5: `ask_amount` and `ask_text` |
| `extra/float_trap.py`, `extra/paise.py`, `extra/keyerr.py` | The "what breaks" demos from the end of the video |

## Run it

From this folder:

```bash
python expenses.py
```

You will see the menu `1 Add   2 List   3 Totals   4 Quit`. Type the answers below; each line after `Choose:` or a question is what you type.

```text
1 Add   2 List   3 Totals   4 Quit
Choose: 1
Amount: 250
Category: Food
Note: Lunch
Saved.

1 Add   2 List   3 Totals   4 Quit
Choose: 1
Amount: 80.5
Category: travel
Note: Auto ride
Saved.

1 Add   2 List   3 Totals   4 Quit
Choose: 1
Amount: 120
Category: FOOD
Note: Dinner
Saved.

1 Add   2 List   3 Totals   4 Quit
Choose: 2
Category    Note                  Amount
----------------------------------------
food        Lunch                 250.00
travel      Auto ride              80.50
food        Dinner                120.00

1 Add   2 List   3 Totals   4 Quit
Choose: 3
Category         Total
----------------------
food            370.00
travel           80.50
----------------------
All             450.50
2 categories used

1 Add   2 List   3 Totals   4 Quit
Choose: x
Please choose 1, 2, 3 or 4.

1 Add   2 List   3 Totals   4 Quit
Choose: 4
Goodbye!
```

`FOOD` joined the `food` pile because the category is lower-cased. The letter `x` simply brings the menu back.

## Build it step by step

### Plan on paper

The tracker must: (1) add an expense with an amount, a category and a note; (2) show all expenses in a table; (3) show the total for each category; (4) refuse nonsense such as the word `banana` as an amount; (5) keep showing a menu until you choose quit; (6) keep every job in its own function.

One expense is a dictionary (like a shop slip: amount, category, note). All expenses together are a list of dictionaries, in the order added. The list lives in `main` only, and every job that needs it receives it as a parameter.

The jobs: `add_expense`, `show_expenses`, `totals_by_category`, `show_totals`, the helpers `ask_amount`, `ask_text`, `show_menu`, and one boss, `main`.

### Step 1: the data

Run `step1/data.py` (from inside `step1`):

```bash
cd step1
python data.py
cd ..
```

```text
2
auto ride
[{'amount': 250.0, 'category': 'food', 'note': 'lunch'}, {'amount': 80.5, 'category': 'travel', 'note': 'auto ride'}]
```

`expenses[1]["note"]` is a double lookup: first the place in the list (index 1 is the second slip), then the key in the dictionary. The amount is a float because rupees can have a part, like 80.5 (see "What breaks").

### Step 2: add an expense

`step2/tracker.py` defines `add_expense(expenses)`: `float(input(...))` for the amount, `.strip().lower()` for the category (so `Food`, `FOOD` and `food` are one category), `.strip()` for the note, then builds the dictionary, appends it and prints `Saved.`. It has no `return`, because `append` changes the very list that was passed in.

```bash
cd step2
python tracker.py
cd ..
```

Type `250`, `Food`, `Lunch`, then `80.5`, `travel`, `Auto ride`:

```text
Amount: 250
Category: Food
Note: Lunch
Saved.
Amount: 80.5
Category: travel
Note: Auto ride
Saved.
[{'amount': 250.0, 'category': 'food', 'note': 'Lunch'}, {'amount': 80.5, 'category': 'travel', 'note': 'Auto ride'}]
```

`Food` became `food`; the note keeps its capital `L`.

### Step 3: the table

`step3/tracker.py` defines `show_expenses(expenses)`. An empty list prints `No expenses yet.` and returns early. Otherwise it prints a header and 40 dashes, then one row per expense, unpacking three facts in one line: `cat, note, amt = e["category"], e["note"], e["amount"]`. Widths: `:<12` pushes text left in 12 places, `:>10.2f` pushes a number right with two decimals.

```bash
cd step3
python tracker.py
```

```text
Category    Note                  Amount
----------------------------------------
food        lunch                 250.00
travel      auto ride              80.50
learning    course               1499.00
food        dinner                120.00
No expenses yet.
```

A width is a minimum, not a maximum. Try `width.py`:

```bash
python width.py
```

```text
python course for beginners|
python course for |
lunch             |
```

The long note is not cut, so it would push the amount out of line. The fix is a slice, `note = note[:18]`, which is what `tracker_cut.py` and the final `expenses.py` do (same output for the short notes):

```bash
python tracker_cut.py
cd ..
```

### Step 4: totals by category

`step4/tracker.py` adds `totals_by_category(expenses)`, which only calculates (it prints nothing). The key line is `totals[cat] = totals.get(cat, 0) + e["amount"]`: `.get` gives the total so far, or `0` for a new pile. `show_totals` prints the table, a running `grand` sum, and ends with a set comprehension, `{e["category"] for e in expenses}`, to count the different categories.

```bash
cd step4
python tracker.py
cd ..
```

```text
{'food': 370.0, 'travel': 80.5, 'learning': 1499.0}
Category         Total
----------------------
food            370.00
travel           80.50
learning       1499.00
----------------------
All            1949.50
3 categories used
```

### Step 5: safe input

In step 2, typing `abc` as the amount crashes the program and loses every expense:

```text
Amount: abc
Traceback (most recent call last):
  File "tracker.py", line 15, in <module>
    add_expense(expenses)
    ~~~~~~~~~~~^^^^^^^^^^
  File "tracker.py", line 2, in add_expense
    amount = float(input("Amount: "))
ValueError: could not convert string to float: 'abc'
```

Module 6 teaches how to catch errors. For now, check the text first. `"80.5".isdigit()` is `False` (the dot is not a digit), so remove one dot first. `step5/check.py`:

```bash
cd step5
python check.py
```

```text
True
False
True
False
```

`"8.0.5"` still has a dot after one is removed, so it stays `False`. `step5/tracker.py` adds `ask_amount` (a `while True` loop that uses `continue` to ask again, and a second guard: the amount must be more than zero) and `ask_text` (keeps asking until the text is not empty). Type `abc`, `80.5.1`, `0`, nothing, `80.5`; then nothing and `Travel`; then nothing and `Auto ride`:

```bash
python tracker.py
cd ..
```

```text
Amount: abc
Please type a number, like 250 or 80.5.
Amount: 80.5.1
Please type a number, like 250 or 80.5.
Amount: 0
The amount must be more than zero.
Amount: 
Please type a number, like 250 or 80.5.
Amount: 80.5
Category: 
Please type something.
Category: Travel
Note: 
Please type something.
Note: Auto ride
Saved.
[{'amount': 80.5, 'category': 'travel', 'note': 'Auto ride'}]
```

Six bad inputs, and no crash.

### Step 6: the menu

`expenses.py` adds `show_menu` and `main`. `main` owns the list (`expenses = []`), loops with `while True`, reads a choice, and uses `match`: `"1"` calls `add_expense(expenses)`, `"2"` calls `show_expenses(expenses)`, `"3"` calls `show_totals(expenses)`, `"4" | "q"` prints `Goodbye!` and `break`s, and `_` catches everything else. The last line of the file calls `main()`. Run it as shown in "Run it" above.

## What breaks (and upgrades to try)

1. The data disappears. The list lives in memory, so after you quit and run again, option 2 prints `No expenses yet.` Module 6, Lesson 1 teaches how to save to a file.
2. Floats and money. Run `python extra/float_trap.py`:

```text
0.30000000000000004
30.299999999999997
False
30.30
```

   The table hides it because `.2f` rounds for display, but a total can be a hair off. The professional fix is to store money in paise (whole numbers). `python extra/paise.py`:

```text
3030
True
Rs 30.30
```

3. Dictionaries trust your spelling. `python extra/keyerr.py` raises `KeyError: 'amout'`. Classes (Module 8) fix this.
4. A wrong expense stays forever; there is no delete or edit.

Five upgrades to try yourself: delete an expense by its number; show only one category; find the biggest expense; warn when a category goes over a budget; after Module 6, save the list to a file and load it at start.

## Common mistakes

- Typing text where `float()` expects a number, with no guard (crash and lost data).
- Using `str.isdigit()` directly on an amount: `"80.5"` fails because of the dot.
- Using a global list instead of passing `expenses` as a parameter.
- Forgetting `.lower()` on the category, so `Food` and `food` get separate totals.
- Writing `match` patterns without quotes for text choices (`case 1` never matches `"1"`).
- Storing money as floats for real accounting.

## Clean up

Nothing to clean up. The program writes no files.

## Next

Try the Module 5 practice sheet: [practice/m05-data-structures](../../practice/m05-data-structures/). Then on to Module 6, Lesson 1, Reading and Writing Files.
