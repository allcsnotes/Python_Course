# Exercise 01 - The course playlist
playlist = ["Intro", "Variables", "Loops"]
print("Start:", playlist)

playlist.append("Functions")
print("After append:", playlist)

playlist.insert(1, "Setup")
print("After insert:", playlist)

playlist.extend(["Lists", "Tuples"])
print("After extend:", playlist)

print("Count:", len(playlist))
print("First:", playlist[0])
print("Last:", playlist[-1])

playlist[0] = "Welcome"
print("Renamed first:", playlist[0])
