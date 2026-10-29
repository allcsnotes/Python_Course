# Exercise 12 - Count the votes
votes = ["Python", "Docker", "Python", "SQL", "Python", "Docker", "Go", "SQL", "Python"]

tally = {}
for choice in votes:
    tally[choice] = tally.get(choice, 0) + 1
print(tally)

by_votes = sorted(tally.items(), key=lambda pair: pair[1], reverse=True)
winner, count = by_votes[0]
print("Winner:", winner, "with", count, "votes")

for choice, count in by_votes:
    print(f"{choice:<8}{'#' * count} {count}")

counts = {}
for letter in "banana":
    if letter in counts:
        counts[letter] += 1
    else:
        counts[letter] = 1
print(counts)
