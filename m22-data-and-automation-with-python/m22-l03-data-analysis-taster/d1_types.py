import pandas as pd

df = pd.read_csv(
    "enrollments.csv", parse_dates=["enrolled_on"]
)
price = df["price"].str.replace("Rs ", "")
price = price.str.replace(",", "")
df["price"] = pd.to_numeric(price)
print(df.dtypes)
