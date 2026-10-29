# M22-L03 · Data Analysis Taster

> Video: Module 22, Lesson 3. Watch it first, then follow along here.

## What you'll learn

- What a pandas `DataFrame` and a `Series` are, and why you work on whole columns instead of looping over rows
- How to load a messy CSV file and fix its types (dates, prices written as text) and its missing values
- How to merge two tables, pick columns, filter rows, add a column, and change values safely with `.loc`
- How to answer business questions with `groupby`, `pivot_table` and `resample`
- How to draw two charts with matplotlib and write the results back to CSV and Excel
- When pandas is the wrong tool (tiny data, huge data)

## Before you start

- Python 3.14 or newer. Check with `python --version`.
- [uv](https://docs.astral.sh/uv/), the package tool from Module 7. No Docker is needed in this lesson.
- Ideas from earlier lessons: the `csv` module (M06), dictionaries (M05), NumPy arrays (M11-L04), and `openpyxl` (M22-L01).
- No earlier lesson folder is needed. All the data is made by a small program in this folder, with a fixed seed, so
  your numbers match the video. The data is not from the real site.

## Files in this folder

| File | What it is |
|------|------------|
| `pyproject.toml`, `uv.lock` | The project: pandas 3.1.0, NumPy 2.5.4, matplotlib 3.11.2, openpyxl 3.1.5 (pinned) |
| `make_data.py` | Creates `enrollments.csv` (1,115 rows) and `courses.csv` (6 rows) with a fixed random seed |
| `enrollments.csv`, `courses.csv` | The two data files, as `make_data.py` writes them |
| `hook.py` | The plain `csv` loop that crashes on a hand-typed price |
| `tiny.py` | A three-row DataFrame built from a dictionary |
| `c1_read.py` | `read_csv`, `head`, `info` |
| `d1_types.py` | Fix the dates and the prices |
| `e1_merge.py` | Merge the course names into the enrollments |
| `f1_missing.py` | Count and fill the missing prices |
| `prep.py` | `load()`: loading plus all the cleaning, so every later script starts with two lines |
| `g1_select.py` | Pick columns, filter rows, combine two conditions |
| `g2_column.py` | Add a `weekday` column and count with `value_counts` |
| `g3_chain.py` | The chained-assignment trap (this one does not work, on purpose) |
| `g4_loc.py` | The fix with `.loc` |
| `h1_group.py` | `groupby`: count, sum and mean for each course |
| `h2_pivot.py` | `pivot_table`: course by country |
| `i1_week.py` | `resample("W")`: enrollments per week |
| `j1_bar.py` | Bar chart of revenue per course (writes `revenue.png`) |
| `j2_line.py` | Line chart of enrollments per week (writes `weekly.png`) |
| `k1_write.py` | Write the results to CSV and Excel |
| `k2_back.py` | Read the Excel file back with `openpyxl` |
| `howlong.py` | How long `import pandas` takes |

## Follow along

### 1. Set up the project

Run these in this folder:

```bash
uv sync
source .venv/bin/activate
```

On Windows, activate with `.venv\Scripts\activate` instead. From now on `python` means the Python of this project.
(If you prefer, skip the activation and write `uv run python script.py` everywhere.)

### 2. Make the data

```bash
python make_data.py
```

```
wrote enrollments.csv: 1,115 rows, courses.csv: 6 rows
```

Run it again and you get the same files, because the random generator starts from the fixed number 2026.

### 3. The problem: a plain loop

`hook.py` reads the file with the `csv` module (Module 6) and adds up the prices in a dictionary:

```bash
python hook.py
```

```
Traceback (most recent call last):
  File "hook.py", line 7, in <module>
    totals[course] = totals.get(course, 0) + int(row["price"])
                                             ~~~^^^^^^^^^^^^^^^^
ValueError: invalid literal for int() with base 10: 'Rs 1,999'
```

(The file path in your traceback is longer.) Someone typed that price by hand as `Rs 1,999`, and some prices are
missing. Real exports are messy. This is the job for pandas.

### 4. A DataFrame is a spreadsheet in code

```python
import pandas as pd

courses = pd.DataFrame({
    "title": ["Python", "SQL", "Git"],
    "price": [2999, 1499, 999],
})
print(courses)
print(courses["price"])
print(courses["price"].sum())
print(courses["price"].to_numpy())
```

```bash
python tiny.py
```

```
    title  price
0  Python   2999
1     SQL   1499
2     Git    999
0    2999
1    1499
2     999
Name: price, dtype: int64
5497
[2999 1499  999]
```

The table has an index (the numbers on the left). One column alone is a `Series`: a list of values with one name and one
type. `sum()` adds the whole column in one go, and `to_numpy()` hands you the NumPy array underneath. You never loop
over the rows: you tell the whole column what to do.

### 5. Load the real file

```python
df = pd.read_csv("enrollments.csv")
print(df.head())
df.info()
```

```bash
python c1_read.py
```

```
   enrollment_id enrolled_on  student_id  course_id  country     price refunded
0              1  2026-08-03         642          6    India      2499       no
1              2  2026-08-03         427          4    India  Rs 1,999       no
2              3  2026-08-03         543          2      USA      1499       no
3              4  2026-08-03         455          3  Germany       999      yes
4              5  2026-08-03         563          1      USA      2999       no
<class 'pandas.DataFrame'>
RangeIndex: 1115 entries, 0 to 1114
Data columns (total 7 columns):
 #   Column         Non-Null Count  Dtype
---  ------         --------------  -----
 0   enrollment_id  1115 non-null   int64
 1   enrolled_on    1115 non-null   str
 2   student_id     1115 non-null   int64
 3   course_id      1115 non-null   int64
 4   country        1115 non-null   str
 5   price          1094 non-null   str
 6   refunded       1115 non-null   str
dtypes: int64(3), str(4)
memory usage: 61.1 KB
```

Two problems: `enrolled_on` is plain text (`str`), not a date, and `price` is text with only 1,094 values (21 are missing).

### 6. Fix the types

```bash
python d1_types.py
```

`parse_dates=["enrolled_on"]` makes real dates. For the price, `.str.replace` removes `Rs ` and the commas on every
value at once, then `pd.to_numeric` makes numbers:

```
enrollment_id             int64
enrolled_on      datetime64[us]
student_id                int64
course_id                 int64
country                     str
price                   float64
refunded                    str
dtype: object
```

`price` is a float because the missing prices are still there as `NaN` ("not a number"), and a whole-number column
cannot hold them.

### 7. Merge in the course names

`course_id` is only a number. The names live in `courses.csv`. Joining two tables on a shared column is a merge (the
spreadsheet VLOOKUP, for all rows at once):

```bash
python e1_merge.py
```

```
   enrollment_id  course_id   title   price  list_price
0              1          6     DSA  2499.0        2499
1              2          4  Docker  1999.0        1999
2              3          2     SQL  1499.0        1499
3              4          3     Git   999.0         999
4              5          1  Python  2999.0        2999
```

### 8. Fill the missing prices

A missing price means the export lost the number, so the list price is our best answer.

```bash
python f1_missing.py
```

```
21
0
```

`isna().sum()` counts the missing values. `fillna(df["list_price"])` fills each gap from the list price of the same row,
and `astype(int)` makes whole numbers again.

All of steps 6 to 8 now live in one function, `load()` in `prep.py`. From here on every script starts with
`from prep import load` and `df = load()`.

### 9. Ask questions: columns, rows, conditions

```bash
python g1_select.py
```

```
    title country  price
0     DSA   India   2499
1  Docker   India   1999
2     SQL     USA   1499
44 104956
253
```

- `df[["title", "country", "price"]]`: the outer brackets select, the inner list holds the names.
- `df[df["refunded"] == "yes"]`: a column of `True`/`False` inside the brackets keeps only the true rows.
- Two conditions: use `&` and put each condition in round brackets. The word `and` does not work on whole columns.

So: 44 refunds worth 104,956 rupees, and 253 Indian enrollments above 2,000.

### 10. Add a column

```bash
python g2_column.py
```

```
  enrolled_on weekday
0  2026-08-03  Monday
1  2026-08-03  Monday
2  2026-08-03  Monday
weekday
Tuesday     175
Saturday    163
Friday      162
Name: count, dtype: int64
```

### 11. The trap: changing values on a copy

Meera says refunded money is not income, so set the price of refunded rows to zero. `g3_chain.py` does it the
"obvious" way: `df[df["refunded"] == "yes"]["price"] = 0`.

```bash
python g3_chain.py
```

```
g3_chain.py:5: ChainedAssignmentError: A value is being set on a copy of a DataFrame or Series through chained assignment.
Such chained assignment never works to update the original DataFrame or Series, ...
2402885
2402885
```

(The warning is longer on your screen, and the file path in it is longer too.) The total is
the same before and after: the first brackets made a copy, we changed the copy, and the copy was thrown away.

The fix is `.loc`, which takes rows and column together, in one step, on the original table:

```bash
python g4_loc.py
```

```
2402885
2297929
```

The total drops by the refunds. The rule: to change values, use `.loc`.

### 12. Group: money for each course

```bash
python h1_group.py
```

```
         count     sum    mean
title                         
Python     218  653782  2999.0
FastAPI    143  500357  3499.0
DSA        144  359856  2499.0
Docker     135  269865  1999.0
Git        264  263736   999.0
SQL        167  250333  1499.0
```

`groupby` splits the table into one small table per course, adds up each, and combines the results. Git has the most
paying students (264), but Python earns the most money. Counting people and counting money give different answers.

### 13. A pivot table: course by country

```bash
python h2_pivot.py
```

```
country  Brazil  Germany   India     UK     USA
title                                          
DSA       22491    57477  169932  47481   62475
Docker    27986    59970  115942  25987   39980
FastAPI   52485    94473  220437  52485   80477
Git       25974    27972  136863  19980   52947
Python    71976    65978  323892  47984  143952
SQL       26982    35976  119920  17988   49467
```

### 14. Resample: which week was busiest?

```bash
python i1_week.py
```

```
enrolled_on
2026-08-09     61
2026-08-16     72
2026-08-23     73
2026-08-30     79
2026-09-06     69
2026-09-13     88
2026-09-20     84
2026-09-27    159
2026-10-04    106
2026-10-11    105
2026-10-18    118
2026-10-25    101
Freq: W-SUN, Name: enrollment_id, dtype: int64
```

`set_index("enrolled_on")` makes the date the label of each row, and `resample("W")` cuts the timeline into weeks that
end on a Sunday. The jump in the week ending 27 September is a pretend promotion put into the generated data.

### 15. Two charts

```bash
python j1_bar.py
python j2_line.py
```

```
saved revenue.png
saved weekly.png
```

Open `revenue.png` (revenue per course, in thousands of rupees, the number written on every bar) and `weekly.png` (the
line with the jump to 159). Both follow the same five steps: pick a style, make a figure and axes, draw, add a title and
axis labels with units, and `fig.savefig(...)`. `ax.set_ylim(bottom=0)` starts the Y axis at zero, so the jump is not
made to look bigger than it is.

If you run these on a computer with no screen (a server), set `MPLBACKEND=Agg` first.

### 16. Write the results back

Meera uses Excel, so write the results back:

```bash
python k1_write.py
cat revenue_by_course.csv
python k2_back.py
```

```
saved the csv and the Excel file
title,count,sum
Python,218,653782
FastAPI,143,500357
DSA,144,359856
Docker,135,269865
Git,264,263736
SQL,167,250333
('title', 'count', 'sum')
('Python', 218, 653782)
('FastAPI', 143, 500357)
('DSA', 144, 359856)
('Docker', 135, 269865)
('Git', 264, 263736)
('SQL', 167, 250333)
```

`weekly_report.xlsx` is a real workbook with a sheet called `Courses`. Open it in Excel or LibreOffice.

### 17. When not to use pandas

```bash
python howlong.py
```

```
import pandas took 0.30 seconds
```

Yours will differ (the first run on a new machine is slower, often 1 to 4 seconds). For ten rows and one total, a
five-line loop with the `csv` module is simpler and needs no install. For tens of millions of rows, pandas holds the
whole table in memory, so look at polars or DuckDB. The ideas (filter, groupby, merge) carry over.

## Common mistakes

- Looping over the rows of a DataFrame. Use a column operation, `filter`, or `groupby`: they run in fast compiled code,
  once, instead of one Python step per row.
- `df[condition]["price"] = 0`: this changes a copy. Use `df.loc[condition, "price"] = 0`.
- `and` / `or` between two conditions: use `&` / `|` and put each condition in round brackets.
- Skipping the types: a price stored as text cannot be added up. Look at `df.info()` first.
- Dropping rows with missing values without thinking: real enrollments disappear from the counts.
- A chart with no title, no axis names or units, or tiny text.

## Clean up

The scripts write `revenue.png`, `weekly.png`, `revenue_by_course.csv` and `weekly_report.xlsx` into this folder. Delete
them, and the virtual environment, when you are done:

```bash
rm -f revenue.png weekly.png revenue_by_course.csv weekly_report.xlsx
rm -rf .venv
```

## Next

Next is the last build of the module: [M22-B15 · Build a Weekly Report Bot](../m22-b15-build-a-weekly-report-bot/).
