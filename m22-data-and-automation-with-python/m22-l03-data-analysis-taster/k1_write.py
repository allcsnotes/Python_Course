from prep import load

df = load()
paid = df[df["refunded"] == "no"]
by_title = paid.groupby("title")["price"]
stats = by_title.agg(["count", "sum"])
stats = stats.sort_values("sum", ascending=False)

stats.to_csv("revenue_by_course.csv")
stats.to_excel("weekly_report.xlsx", sheet_name="Courses")
print("saved the csv and the Excel file")
