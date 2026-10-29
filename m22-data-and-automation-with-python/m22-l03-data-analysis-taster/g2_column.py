from prep import load

df = load()
df["weekday"] = df["enrolled_on"].dt.day_name()
print(df[["enrolled_on", "weekday"]].head(3))
print(df["weekday"].value_counts().head(3))
