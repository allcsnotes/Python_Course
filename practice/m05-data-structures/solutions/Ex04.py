# Exercise 04 - Sorting the ratings
ratings = [4.5, 3.8, 4.9, 4.1, 3.2]
courses = ["Python", "SQL", "Go", "Docker", "Spring Boot"]

print("sorted():", sorted(ratings))
print("original:", ratings)

ratings.sort(reverse=True)
print("sort(reverse=True):", ratings)

print("Best:", max(ratings), "Worst:", min(ratings))
print("Average:", round(sum(ratings) / len(ratings), 2))

print("A to Z:", sorted(courses))
print("By length:", sorted(courses, key=len))
print("By last letter:", sorted(courses, key=lambda name: name[-1]))

print("Backwards:", courses[::-1])
print("Courses still:", courses)
