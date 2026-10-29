from prep import load

df = load()
print(df["price"].sum())
df[df["refunded"] == "yes"]["price"] = 0
print(df["price"].sum())
