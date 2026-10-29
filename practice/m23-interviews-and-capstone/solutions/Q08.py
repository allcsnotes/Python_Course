# Q08 - How dicts and sets work
scores = {"Asha": 90, "Lukas": 72}
scores["Priya"] = 85
print(list(scores))                 # insertion order is guaranteed
print(scores.get("Meera"), scores.get("Meera", 0))
try:
    scores["Meera"]
except KeyError as error:
    print("KeyError:", error)

counts = {}
for word in "to be or not to be".split():
    counts[word] = counts.get(word, 0) + 1
print(counts)

print({**scores, "Lukas": 80} | {"Mia": 60})   # merge, last one wins
print(hash("abc") == hash("abc"), hash((1, 2)) == hash((1, 2)))

# sets: the same hash idea, keys only
import timeit

names = ["Asha", "Lukas", "Asha", "Priya", "Lukas"]
print(list(dict.fromkeys(names)))   # remove duplicates, keep the order
python = {"Asha", "Lukas", "Priya"}
sql = {"Priya", "Meera"}
print(python & sql, sorted(python | sql), sorted(python - sql), sorted(python ^ sql))

big_list = list(range(100_000))
big_set = set(big_list)
t_list = timeit.timeit(lambda: 99_999 in big_list, number=200)
t_set = timeit.timeit(lambda: 99_999 in big_set, number=200)
print("set lookup is faster:", t_set < t_list)
