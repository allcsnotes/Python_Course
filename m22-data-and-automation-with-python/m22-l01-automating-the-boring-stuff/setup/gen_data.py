"""Course setup (not shown): a messy downloads folder and the Excel file Meera sends. Fixed seed."""
import random
from datetime import date, timedelta
from pathlib import Path
from openpyxl import Workbook
from openpyxl.styles import Alignment

H = Path(__file__).resolve().parent.parent
NAMES = ["enrollments 2026-10-19.csv", "enrollments 2026-10-26.csv", "Refunds copy.csv", "Report Final.xlsx", "report-final.xlsx",
         "IMG_2041.JPG", "IMG_2042.jpg", "Screenshot 2026-10-20 at 9.14.png", "invoice oct.pdf", "Meera slides.pdf", "notes.txt", "setup.exe", "archive.zip"]
src = H / "downloads_src"; src.mkdir(exist_ok=True)
for n in NAMES: (src / n).write_text("demo file " + n + "\n")

random.seed(22)
courses = [("Python Basics", 1499), ("SQL in Two Weeks", 999), ("Git and GitHub", 799), ("Docker for Python Apps", 1299)]
wb = Workbook(); ws = wb.active; ws.title = "Enrollments"
ws.append(["Date", "Student", "Course", "Price"])
d0 = date(2026, 10, 19)
rows = []
for i in range(14):
    c = random.choices(courses, weights=[5, 3, 2, 3])[0]
    rows.append((d0 + timedelta(days=random.randint(0, 6)), f"S-{random.randint(1000, 1099)}", c[0], c[1]))
rows.sort()
for r in rows: ws.append(list(r))
for r in ws.iter_rows(min_row=2, max_col=1):
    r[0].alignment = Alignment(horizontal="left")
for col, w in zip("ABCD", (14, 12, 26, 10)): ws.column_dimensions[col].width = w
(H / "data").mkdir(exist_ok=True)
wb.save(H / "data" / "enrollments_week.xlsx")
print(len(rows), "rows")
