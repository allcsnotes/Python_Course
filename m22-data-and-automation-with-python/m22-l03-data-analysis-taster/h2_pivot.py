from prep import load

df = load()
paid = df[df["refunded"] == "no"]
table = paid.pivot_table(
    index="title",
    columns="country",
    values="price",
    aggfunc="sum",
)
print(table)
