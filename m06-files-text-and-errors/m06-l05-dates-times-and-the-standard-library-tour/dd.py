from collections import defaultdict

courses = ["Python", "SQL", "Python", "SQL"]
names = ["Lukas", "Priya", "Meera", "Rahul"]
by_course = defaultdict(list)
for course, name in zip(courses, names):
    by_course[course].append(name)
for course, group in by_course.items():
    print(course, group)
