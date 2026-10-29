from pathlib import Path

from sheets import summarise, write_report

summary = summarise(Path("data/enrollments_week.xlsx"))
write_report(summary, Path("report.xlsx"))
print("saved report.xlsx")
