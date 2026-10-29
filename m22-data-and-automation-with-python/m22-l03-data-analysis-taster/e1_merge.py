import pandas as pd

df = pd.read_csv(
    "enrollments.csv", parse_dates=["enrolled_on"]
)
price = df["price"].str.replace("Rs ", "")
price = price.str.replace(",", "")
df["price"] = pd.to_numeric(price)

courses = pd.read_csv("courses.csv")
df = df.merge(courses, on="course_id")
cols = ["enrollment_id", "course_id", "title"]
print(df[cols + ["price", "list_price"]].head())
