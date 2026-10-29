from prep import load

df = load()
weekly = (
    df.set_index("enrolled_on")
    .resample("W")["enrollment_id"]
    .count()
)
print(weekly)
