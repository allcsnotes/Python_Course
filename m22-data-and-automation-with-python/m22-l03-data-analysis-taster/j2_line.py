import matplotlib.pyplot as plt
from prep import load

plt.style.use("dark_background")
plt.rcParams["font.size"] = 16

df = load()
weekly = (
    df.set_index("enrolled_on")
    .resample("W")["enrollment_id"]
    .count()
)

fig, ax = plt.subplots(figsize=(11, 6.4))
ax.plot(weekly, marker="o", color="#4c9dff", linewidth=3)
ax.set_title("Enrollments per week")
ax.set_xlabel("Week ending (Sunday)")
ax.set_ylabel("Enrollments")
ax.set_ylim(bottom=0)
fig.autofmt_xdate()
fig.savefig("weekly.png", dpi=110)
print("saved weekly.png")
