from prep import load

df = load()
print(df[["title", "country", "price"]].head(3))

refunds = df[df["refunded"] == "yes"]
print(len(refunds), refunds["price"].sum())

big = df[(df["country"] == "India") & (df["price"] > 2000)]
print(len(big))
