import numpy as np
import pandas as pd

rng = np.random.default_rng(2026)

courses = pd.DataFrame({
    "course_id": [1, 2, 3, 4, 5, 6],
    "title": ["Python", "SQL", "Git", "Docker", "FastAPI", "DSA"],
    "list_price": [2999, 1499, 999, 1999, 3499, 2499],
})
courses.to_csv("courses.csv", index=False)

# 12 weeks of enrollments: Monday 3 August to Sunday 25 October 2026
days = pd.date_range("2026-08-03", "2026-10-25")
per_day = rng.poisson(8 + 0.12 * np.arange(len(days)))
promo = (days >= "2026-09-21") & (days < "2026-09-28")
per_day = per_day + np.where(promo, rng.poisson(9, len(days)), 0)
dates = np.repeat(days, per_day)
n = len(dates)
weights = np.array([0.20, 0.14, 0.27, 0.12, 0.14, 0.13])
course_id = rng.choice(courses["course_id"], size=n, p=weights)
price = courses.set_index("course_id").loc[course_id, "list_price"].to_numpy()
country = rng.choice(["India", "Germany", "USA", "UK", "Brazil"], size=n, p=[0.45, 0.15, 0.2, 0.1, 0.1])
refunded = np.where(rng.random(n) < 0.045, "yes", "no")

df = pd.DataFrame({
    "enrollment_id": np.arange(1, n + 1),
    "enrolled_on": pd.Series(dates).dt.strftime("%Y-%m-%d"),
    "student_id": rng.integers(1, 700, size=n),
    "course_id": course_id,
    "country": country,
    "price": price.astype(str),
    "refunded": refunded,
})
# a messy export: some prices typed by hand as "Rs 1,499", some missing
text = rng.random(n) < 0.06
df.loc[text, "price"] = ["Rs {:,}".format(int(p)) for p in price[text]]
df.loc[rng.random(n) < 0.02, "price"] = np.nan
df.to_csv("enrollments.csv", index=False)
print(f"wrote enrollments.csv: {n:,} rows, courses.csv: {len(courses)} rows")
