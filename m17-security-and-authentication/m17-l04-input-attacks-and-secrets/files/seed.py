from sqlalchemy import text

from db import engine

COURSES = [
    ("Python Basics", "Learn Python from zero.", 449, True),
    ("SQL in Two Weeks", "Tables, joins and indexes.", 399, True),
    ("FastAPI in Practice", "Build a real API.", 599, True),
    ("Draft: Launch Plan", "Not public yet.", 0, False),
    ("Draft: Price Review", "Not public yet.", 0, False),
]
STUDENTS = [
    ("Lukas", "lukas@example.com"),
    ("Priya", "priya@example.com"),
    ("Ben", "ben@example.com"),
]

with engine.begin() as conn:
    conn.execute(text("DROP TABLE IF EXISTS courses, students"))
    conn.execute(text(
        "CREATE TABLE courses (id serial PRIMARY KEY, title text,"
        " description text, price int, published boolean)"))
    conn.execute(text(
        "CREATE TABLE students (id serial PRIMARY KEY,"
        " name text, email text)"))
    for t, d, p, pub in COURSES:
        conn.execute(text(
            "INSERT INTO courses (title, description, price, published)"
            " VALUES (:t, :d, :p, :pub)"),
            {"t": t, "d": d, "p": p, "pub": pub})
    for n, e in STUDENTS:
        conn.execute(text(
            "INSERT INTO students (name, email) VALUES (:n, :e)"),
            {"n": n, "e": e})
