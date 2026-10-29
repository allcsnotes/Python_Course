from dataclasses import dataclass

import pandas as pd

COLUMNS = [
    "student_id",
    "course_id",
    "course",
    "amount",
    "enrolled_at",
    "refunded_at",
]


def to_frame(rows, tz):
    frame = pd.DataFrame(rows, columns=COLUMNS)
    for name in ["enrolled_at", "refunded_at"]:
        frame[name] = pd.to_datetime(
            frame[name], utc=True
        ).dt.tz_convert(tz)
    return frame


@dataclass
class Summary:
    enrollments: int
    before: int
    gross: int
    refunds: int
    refunded: int
    per_course: pd.DataFrame
    rows: pd.DataFrame

    @property
    def net(self):
        return self.gross - self.refunded


def summarise(data, start, end, tz):
    enrolled = to_frame(data["enrollments"], tz)
    refunds = to_frame(data["refunds"], tz)
    week = enrolled[
        (enrolled.enrolled_at >= start)
        & (enrolled.enrolled_at < end)
    ]
    before = enrolled[enrolled.enrolled_at < start]
    paid_back = refunds[
        (refunds.refunded_at >= start)
        & (refunds.refunded_at < end)
    ]
    per_course = (
        week.groupby("course")
        .agg(
            enrollments=("student_id", "count"),
            revenue=("amount", "sum"),
        )
        .sort_values("revenue", ascending=False)
    )
    return Summary(
        len(week),
        len(before),
        int(week.amount.sum()),
        len(paid_back),
        int(paid_back.amount.sum()),
        per_course,
        week,
    )
