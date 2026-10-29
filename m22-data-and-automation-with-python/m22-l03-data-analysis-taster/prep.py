import pandas as pd


def load():
    df = pd.read_csv(
        "enrollments.csv", parse_dates=["enrolled_on"]
    )
    price = df["price"].str.replace("Rs ", "")
    price = price.str.replace(",", "")
    df["price"] = pd.to_numeric(price)

    courses = pd.read_csv("courses.csv")
    df = df.merge(courses, on="course_id")

    df["price"] = df["price"].fillna(df["list_price"])
    df["price"] = df["price"].astype(int)
    return df
