import matplotlib.pyplot as plt
from prep import load

plt.style.use("dark_background")
plt.rcParams["font.size"] = 16

df = load()
paid = df[df["refunded"] == "no"]
revenue = paid.groupby("title")["price"].sum()
revenue = revenue.sort_values(ascending=False)

fig, ax = plt.subplots(figsize=(11, 6.4))
bars = ax.bar(revenue.index, revenue / 1000, color="#4c9dff")
ax.bar_label(bars, fmt="%.0f")
ax.set_title("Revenue per course")
ax.set_xlabel("Course")
ax.set_ylabel("Revenue (thousand Rs)")
fig.savefig("revenue.png", dpi=110)
print("saved revenue.png")
