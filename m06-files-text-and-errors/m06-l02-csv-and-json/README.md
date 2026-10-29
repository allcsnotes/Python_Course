# M06-L02 · CSV and JSON

> Video: Module 6, Lesson 2. Watch it first, then follow along here.

## What you'll learn

- Why plain text is not enough to save a dictionary (`str` is a one-way street)
- How to save and load a table with the `csv` module, and why numbers come back as text
- Why you always open CSV files with `newline=""`
- How to save and load nested data with the `json` module (`dumps`, `loads`, `dump`, `load`)
- Which Python values survive JSON and which do not (tuples, sets, number keys)
- How to choose CSV or JSON, and how the expense tracker keeps its list between runs

## Before you start

- Python 3.14 or newer. Check with `python --version`.
- The previous lesson, [M06-L01 · Reading and Writing Files](../m06-l01-reading-and-writing-files/README.md): `open`, `with`, `encoding="utf-8"` and `pathlib.Path`.
- Copy the `.py` files of this folder into an empty working folder and run the commands from there. The programs create their own data files (`expenses.csv`, `expenses.json`, and others).
- On Windows, use `type` instead of `cat`.

## Files in this folder

| File | What it is |
|------|------------|
| `save_as_text.py` | The hook: save a dictionary with `str`, read it back, and fail |
| `csv_write.py` | Writes `expenses.csv` with `csv.writer` |
| `csv_raw.py` | Shows the raw text of the file with `repr` |
| `csv_win.py` | Pretends to be Windows to show the extra-empty-row trap |
| `csv_comma.py` | A comma inside a cell: `split` breaks it, the `csv` module does not |
| `csv_read.py` | Reads rows with `csv.reader` |
| `csv_text.py` | Proves that CSV values come back as text |
| `dict_write.py` | Writes the expense list with `csv.DictWriter` |
| `dict_read.py` | Reads it with `csv.DictReader` (amounts are still text) |
| `dict_fix.py` | Converts the amounts with `float`: a perfect round trip |
| `csv_sum.py` | Pitfall: adding CSV text to a number |
| `csv_sumfix.py` | The fix: `float(row["amount"])` |
| `json_vs.py` | A Python dictionary next to the same data as JSON text |
| `json_basic.py` | `json.dumps` and `json.loads` |
| `json_indent.py` | `indent=2` for readable JSON |
| `json_file.py` | `json.dump` and `json.load` with a file |
| `json_types.py` | One of each type JSON knows |
| `json_tuple.py` | A tuple comes back as a list |
| `json_set.py` | A set cannot be saved (`TypeError`) |
| `json_setfix.py` | The fix: `sorted(tags)` |
| `nested_csv.py` | A list inside a CSV cell comes back as text |
| `nested_json.py` | The same list inside JSON comes back as a list |
| `tracker.py` | The expense tracker that remembers its list in `expenses.json` |
| `json_keys.py` | Pitfall: number keys become text |
| `json_bad.py` | Pitfall: single quotes are not valid JSON |

## Follow along

Run each program with `python <file>`.

### 1. The hook: a dictionary saved with `str`

`save_as_text.py`:

```python
expense = {"amount": 250.0, "category": "food", "note": "Lunch"}
with open("expense.txt", "w", encoding="utf-8") as file:
    file.write(str(expense))
with open("expense.txt", encoding="utf-8") as file:
    back = file.read()
print(back)
print(type(back))
print(back["note"])
```

```bash
python save_as_text.py
```

```text
{'amount': 250.0, 'category': 'food', 'note': 'Lunch'}
<class 'str'>
Traceback (most recent call last):
  File "save_as_text.py", line 8, in <module>
    print(back["note"])
          ~~~~^^^^^^^^
TypeError: string indices must be integers, not 'str'
```

What came back is text, and text has no keys. The file only holds letters; it has no idea they once formed a dictionary. To save structured data, we use a format: an agreed layout for writing data, so any program that knows the format can rebuild the same data. If what comes back equals what went in, it is called a round trip. Python ships with two formats that work both ways: `csv` and `json`.

### 2. Write a CSV file

CSV stands for comma separated values: a table saved as plain text, one row per line, a comma between the cells. The first line holds the column names. `csv_write.py`:

```python
import csv

rows = [
    ["amount", "category", "note"],
    [250.0, "food", "Lunch"],
    [80.5, "travel", "Auto ride"],
    [120.0, "food", "Dinner"],
]

with open("expenses.csv", "w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerows(rows)
```

```bash
python csv_write.py
cat expenses.csv
```

Nothing prints from the program. The file contains:

```text
amount,category,note
250.0,food,Lunch
80.5,travel,Auto ride
120.0,food,Dinner
```

`writerows` (with an s) writes all rows; `writerow` writes one. The numbers were turned into text for you.

### 3. Why `newline=""`

`csv_raw.py` shows the file as Python really holds it. `repr` spells out invisible characters:

```python
with open("expenses.csv", newline="", encoding="utf-8") as file:
    print(repr(file.read()))
```

```bash
python csv_raw.py
```

```text
'amount,category,note\r\n250.0,food,Lunch\r\n80.5,travel,Auto ride\r\n120.0,food,Dinner\r\n'
```

The `csv` module ends every row with `\r\n` (a carriage return and a new line). On Windows, Python also turns every `\n` into `\r\n` for text files, so a row would end with three characters and spreadsheets would show an empty line after every row. `newline=""` tells Python to leave line endings alone. `csv_win.py` pretends to be Windows, so you can see the trap on any computer:

```python
import csv

rows = [["amount", "category"], [250.0, "food"], [80.5, "travel"]]

with open("windows.csv", "w", newline="\r\n", encoding="utf-8") as file:
    csv.writer(file).writerows(rows)

with open("windows.csv", newline="", encoding="utf-8") as file:
    for row in csv.reader(file):
        print(row)
```

```bash
python csv_win.py
```

```text
['amount', 'category']
[]
['250.0', 'food']
[]
['80.5', 'travel']
[]
```

Six rows instead of three. The rule: when you open a CSV file, for reading or for writing, always add `newline=""`.

### 4. Commas inside a cell

`csv_comma.py`:

```python
import csv

line = "250.0,food,Chai, snacks"
print(line.split(","))

row = [250.0, "food", "Chai, snacks"]
with open("chai.csv", "w", newline="", encoding="utf-8") as file:
    csv.writer(file).writerow(row)

with open("chai.csv", newline="", encoding="utf-8") as file:
    print(repr(file.read()))

with open("chai.csv", newline="", encoding="utf-8") as file:
    print(list(csv.reader(file)))
```

```bash
python csv_comma.py
```

```text
['250.0', 'food', 'Chai', ' snacks']
'250.0,food,"Chai, snacks"\r\n'
[['250.0', 'food', 'Chai, snacks']]
```

`split` gives four pieces. The writer wraps the cell in double quotes, and the reader understands the quotes. Never cut CSV lines yourself.

### 5. Read a CSV file

`csv_read.py`:

```python
import csv

with open("expenses.csv", newline="", encoding="utf-8") as file:
    reader = csv.reader(file)
    for row in reader:
        print(row)
```

```bash
python csv_read.py
```

```text
['amount', 'category', 'note']
['250.0', 'food', 'Lunch']
['80.5', 'travel', 'Auto ride']
['120.0', 'food', 'Dinner']
```

The header comes back too (the reader does not know it is special). And look at the quotes: even `250.0` is text. A CSV file has no types. `csv_text.py` proves it:

```python
import csv

with open("expenses.csv", newline="", encoding="utf-8") as file:
    rows = list(csv.reader(file))

amount = rows[1][0]
print(amount, type(amount))
print(amount * 2)
print(float(amount) * 2)
```

```bash
python csv_text.py
```

```text
250.0 <class 'str'>
250.0250.0
500.0
```

### 6. DictWriter and DictReader

Counting cells by position is easy to get wrong. `csv.DictWriter` and `csv.DictReader` use the column names as keys, and fit our expense list (a list of dictionaries). `dict_write.py`:

```python
import csv

expenses = [
    {"amount": 250.0, "category": "food", "note": "Lunch"},
    {"amount": 80.5, "category": "travel", "note": "Auto ride"},
    {"amount": 120.0, "category": "food", "note": "Dinner"},
]

with open("expenses.csv", "w", newline="", encoding="utf-8") as file:
    fields = ["amount", "category", "note"]
    writer = csv.DictWriter(file, fieldnames=fields)
    writer.writeheader()
    writer.writerows(expenses)
```

```bash
python dict_write.py
```

The file is the same table as before. Now `dict_read.py`:

```python
import csv

expenses = [
    {"amount": 250.0, "category": "food", "note": "Lunch"},
    {"amount": 80.5, "category": "travel", "note": "Auto ride"},
    {"amount": 120.0, "category": "food", "note": "Dinner"},
]

with open("expenses.csv", newline="", encoding="utf-8") as file:
    loaded = list(csv.DictReader(file))

print(loaded[0])
print(loaded[0]["note"])
print(loaded == expenses)
```

```bash
python dict_read.py
```

```text
{'amount': '250.0', 'category': 'food', 'note': 'Lunch'}
Lunch
False
```

`False`, because the amount is the text `'250.0'`, not a float. The fix is to convert after loading. `dict_fix.py` is the same program with this loop added after the `loaded = ...` lines:

```python
for e in loaded:
    e["amount"] = float(e["amount"])

print(loaded[0])
print(loaded == expenses)
```

```bash
python dict_fix.py
```

```text
{'amount': 250.0, 'category': 'food', 'note': 'Lunch'}
True
```

### 7. Pitfall: CSV gives text

`csv_sum.py` adds the amounts:

```python
import csv

with open("expenses.csv", newline="", encoding="utf-8") as file:
    rows = list(csv.DictReader(file))

total = 0
for row in rows:
    total += row["amount"]
print(total)
```

```bash
python csv_sum.py
```

```text
Traceback (most recent call last):
  File "csv_sum.py", line 8, in <module>
    total += row["amount"]
TypeError: unsupported operand type(s) for +=: 'int' and 'str'
```

`csv_sumfix.py` changes that line to `total += float(row["amount"])`:

```bash
python csv_sumfix.py
```

```text
450.5
```

### 8. JSON: Python-like text

JSON (said like the name Jason) stands for JavaScript Object Notation. It looks like Python: curly brackets for keys and values, square brackets for lists. `json_vs.py`:

```python
import json

student = {"name": "Lukas", "active": True, "coupon": None}
print(student)
print(json.dumps(student))
```

```bash
python json_vs.py
```

```text
{'name': 'Lukas', 'active': True, 'coupon': None}
{"name": "Lukas", "active": true, "coupon": null}
```

Three differences: JSON uses double quotes only, `true` is lowercase, and `None` is written `null`.

### 9. `dumps` and `loads` (text in memory)

`json_basic.py`:

```python
import json

expense = {"amount": 250.0, "category": "food", "note": "Lunch"}

text = json.dumps(expense)
print(text)
print(type(text))

back = json.loads(text)
print(back)
print(back == expense)
```

```bash
python json_basic.py
```

```text
{"amount": 250.0, "category": "food", "note": "Lunch"}
<class 'str'>
{'amount': 250.0, 'category': 'food', 'note': 'Lunch'}
True
```

`dumps` turns a Python value into JSON text; `loads` turns it back. The `s` stands for string. The float stayed a float.

`json_indent.py` adds `indent=2` for people:

```python
import json

expense = {"amount": 250.0, "category": "food", "note": "Lunch"}
print(json.dumps(expense))
print(json.dumps(expense, indent=2))
```

```bash
python json_indent.py
```

```text
{"amount": 250.0, "category": "food", "note": "Lunch"}
{
  "amount": 250.0,
  "category": "food",
  "note": "Lunch"
}
```

`indent` changes nothing about the data, only how readable the text is.

### 10. `dump` and `load` (files)

Drop the `s` to work with files. `json_file.py`:

```python
import json

expenses = [
    {"amount": 250.0, "category": "food", "note": "Lunch"},
    {"amount": 80.5, "category": "travel", "note": "Auto ride"},
    {"amount": 120.0, "category": "food", "note": "Dinner"},
]

with open("expenses.json", "w", encoding="utf-8") as file:
    json.dump(expenses, file, indent=2)

with open("expenses.json", encoding="utf-8") as file:
    loaded = json.load(file)

print(loaded == expenses)
print(loaded[1]["amount"] + 1)
```

```bash
python json_file.py
cat expenses.json
```

```text
True
81.5
```

The amount is a real number again, no conversion step. The file contains the list as JSON:

```json
[
  {
    "amount": 250.0,
    "category": "food",
    "note": "Lunch"
  },
  {
    "amount": 80.5,
    "category": "travel",
    "note": "Auto ride"
  },
  {
    "amount": 120.0,
    "category": "food",
    "note": "Dinner"
  }
]
```

### 11. Which values can go into JSON

`json_types.py`:

```python
import json

student = {
    "name": "Lukas",
    "courses": 3,
    "rating": 4.5,
    "active": True,
    "coupon": None,
    "tags": ["python", "csv"],
}
print(json.dumps(student))
```

```bash
python json_types.py
```

```text
{"name": "Lukas", "courses": 3, "rating": 4.5, "active": true, "coupon": null, "tags": ["python", "csv"]}
```

The whole table: dictionary becomes object, list becomes array, text becomes string, whole numbers and decimals become number, `True` and `False` become `true` and `false`, `None` becomes `null`. These are all the types JSON knows.

A tuple is not in the table. `json_tuple.py`:

```python
import json

point = (3, 4)
text = json.dumps(point)
print(text)

back = json.loads(text)
print(back)
print(back == point)
```

```bash
python json_tuple.py
```

```text
[3, 4]
[3, 4]
False
```

The tuple is written as an array and comes back as a list, and a list never equals a tuple. Convert it back yourself when you need one.

A set fails. `json_set.py`:

```python
import json

tags = {"python", "csv"}
print(json.dumps(tags))
```

```bash
python json_set.py
```

```text
Traceback (most recent call last):
  File "json_set.py", line 4, in <module>
    print(json.dumps(tags))
          ~~~~~~~~~~^^^^^^
  ...
TypeError: Object of type set is not JSON serializable
```

(`...` is a few lines inside the `json` module, trimmed. Serializable means "can be turned into text for saving".) `json_setfix.py` hands over a list, which JSON knows:

```python
import json

tags = {"python", "csv"}
print(json.dumps(sorted(tags)))
```

```bash
python json_setfix.py
```

```text
["csv", "python"]
```

`sorted` also keeps the order the same every time.

### 12. Compare the two files

Run `python dict_write.py` and `python json_file.py` so both files hold the same three expenses, then count characters (on Windows, look at the file sizes in Explorer):

```bash
wc -c expenses.csv expenses.json
```

```text
      82 expenses.csv
     230 expenses.json
     312 total
```

CSV is small: the column names appear once. JSON repeats the keys on every expense, but it carries its own labels, and numbers stay numbers.

CSV has a deeper limit: a cell is one piece of text. `nested_csv.py` saves a list inside an item as CSV:

```python
import csv

item = {"note": "Lunch", "tags": ["office", "weekday"]}

with open("item.csv", "w", newline="", encoding="utf-8") as file:
    writer = csv.DictWriter(file, fieldnames=["note", "tags"])
    writer.writeheader()
    writer.writerow(item)

with open("item.csv", newline="", encoding="utf-8") as file:
    rows = list(csv.DictReader(file))
print(rows[0]["tags"], type(rows[0]["tags"]))
print(rows[0]["tags"][0])
```

```bash
python nested_csv.py
```

```text
['office', 'weekday'] <class 'str'>
[
```

It looks like a list, but it is a string, and the first character is `[`. `nested_json.py` does the same with JSON:

```python
import json

item = {"note": "Lunch", "tags": ["office", "weekday"]}

back = json.loads(json.dumps(item))
print(back["tags"], type(back["tags"]))
print(back["tags"][0])
```

```bash
python nested_json.py
```

```text
['office', 'weekday'] <class 'list'>
office
```

How to choose: CSV for a flat table that people open in a spreadsheet. JSON when the data has lists or dictionaries inside, when numbers, `true` and `false` must survive, or when you talk to a website.

### 13. The expense tracker that remembers

Delete `expenses.json` first (`rm expenses.json`), so the tracker starts fresh. `tracker.py`:

```python
import json
from pathlib import Path

path = Path("expenses.json")


def save_expenses(expenses):
    with open(path, "w", encoding="utf-8") as file:
        json.dump(expenses, file, indent=2)


def load_expenses():
    if not path.exists():
        return []
    with open(path, encoding="utf-8") as file:
        return json.load(file)


expenses = load_expenses()
print("Loaded:", len(expenses))

amount = float(input("Amount: "))
category = input("Category: ").lower()
note = input("Note: ")
expenses.append({"amount": amount, "category": category, "note": note})

save_expenses(expenses)
print("Saved:", len(expenses))
```

Run it twice. First run, type `250`, `Food`, `Lunch`:

```bash
python tracker.py
```

```text
Loaded: 0
Amount: 250
Category: Food
Note: Lunch
Saved: 1
```

Second run, type `80.5`, `Travel`, `Auto ride`:

```bash
python tracker.py
```

```text
Loaded: 1
Amount: 80.5
Category: Travel
Note: Auto ride
Saved: 2
```

The expense from the first run survived. `expenses.json` now holds two expenses (the category is lowercase because of `.lower()`):

```json
[
  {
    "amount": 250.0,
    "category": "food",
    "note": "Lunch"
  },
  {
    "amount": 80.5,
    "category": "travel",
    "note": "Auto ride"
  }
]
```

`load_expenses` returns an empty list when the file is missing. The next lesson shows another way to handle that with `try` and `except`.

### 14. Pitfall: number keys become text

`json_keys.py`:

```python
import json

students = {1: "Lukas", 2: "Priya"}
text = json.dumps(students)
print(text)

back = json.loads(text)
print(back == students)
print(back[1])
```

```bash
python json_keys.py
```

```text
{"1": "Lukas", "2": "Priya"}
False
Traceback (most recent call last):
  File "json_keys.py", line 9, in <module>
    print(back[1])
          ~~~~^^^
KeyError: 1
```

JSON keys are always text. Use text keys from the start, or convert with `int` after loading.

### 15. Pitfall: single quotes

`json_bad.py`:

```python
import json

text = "{'amount': 250.0}"
print(json.loads(text))
```

```bash
python json_bad.py
```

```text
Traceback (most recent call last):
  File "json_bad.py", line 4, in <module>
    print(json.loads(text))
          ~~~~~~~~~~^^^^^^
  ...
json.decoder.JSONDecodeError: Expecting property name enclosed in double quotes: line 1 column 2 (char 1)
```

The column points at the first single quote. This is also why the hook in step 1 failed: `str` writes Python text, not JSON. Always write JSON with `dump` or `dumps`, never by hand and never with `str`.

## Common mistakes

- Saving data with `str` and expecting to read the structure back.
- Forgetting `newline=""` when opening a CSV file (empty rows on Windows).
- Cutting CSV lines with `split(",")` instead of the `csv` module.
- Forgetting that CSV values always come back as text: convert with `float` or `int` after loading.
- Putting lists or dictionaries into a CSV cell.
- Expecting tuples to stay tuples, or saving a set: tuples come back as lists, sets are a `TypeError`.
- Using number keys in a dictionary you save as JSON: they come back as text.
- Writing JSON by hand with single quotes: JSON allows double quotes only.
- A missing or broken file still raises an error. That is the next lesson.

Interview tip. Your app saves a list of orders to a file: CSV or JSON, and what do you lose with CSV? It depends on the shape of the data. CSV is a flat table of text: small, and every spreadsheet opens it, but it has no types (every value comes back as text) and it cannot hold nested data. JSON holds lists and dictionaries inside each other and keeps numbers, `true`, `false` and `null`. Orders with items inside need JSON.

Before you go on: save your own list of dictionaries in both formats and compare the files.

## Clean up

Delete the files the programs created in your working folder: `expense.txt`, `expenses.csv`, `expenses.json`, `windows.csv`, `chai.csv` and `item.csv`.

## Next

[M06-L03 · Exceptions](../m06-l03-exceptions/README.md)
