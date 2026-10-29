from pathlib import Path


def save_roster(course, folder):
    path = Path(folder) / "roster.txt"
    path.write_text("\n".join(course.students))
    return path


def load_roster(path):
    return Path(path).read_text().splitlines()


def announce(course):
    taken = len(course.students)
    print(f"{course.title}: {taken} of {course.seats} seats taken")
