from prep import load

df = load()
paid = df[df["refunded"] == "no"]
by_title = paid.groupby("title")["price"]
stats = by_title.agg(["count", "sum", "mean"])
print(stats.sort_values("sum", ascending=False))
