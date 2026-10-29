"""Read allcsvideos data from CSV files."""

import csv
from dataclasses import dataclass
from datetime import date
from pathlib import Path


@dataclass(frozen=True)
class Course:
    id: int
    title: str
    level: str
    price: int


@dataclass(frozen=True)
class Enrollment:
    student: str
    course_id: int
    day: date


def read_courses(path: Path) -> list[Course]:
    with path.open(newline="") as f:
        return [
            Course(
                int(r["id"]),
                r["title"],
                r["level"],
                int(r["price"]),
            )
            for r in csv.DictReader(f)
        ]


def read_enrollments(path: Path) -> list[Enrollment]:
    with path.open(newline="") as f:
        return [
            Enrollment(
                r["student"],
                int(r["course_id"]),
                date.fromisoformat(r["day"]),
            )
            for r in csv.DictReader(f)
        ]
