titles = [
    "Python Basics",
    "Loops Deep Dive",
    "Data Structures",
]

lengths = [len(title) for title in titles]
lazy = (len(title) for title in titles)

print(lengths)
print(lazy)
print(list(lazy))
print(sum(len(title) for title in titles))
print(max(len(title) for title in titles))
