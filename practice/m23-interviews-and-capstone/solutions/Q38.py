# Q38 - SQL injection and the fix (standard library sqlite3)
import sqlite3

db = sqlite3.connect(":memory:")
db.execute("CREATE TABLE users (name TEXT, role TEXT)")
db.executemany("INSERT INTO users VALUES (?, ?)", [("asha", "admin"), ("lukas", "student")])

def find_unsafe(name):
    return db.execute(f"SELECT name, role FROM users WHERE name = '{name}'").fetchall()

def find_safe(name):
    return db.execute("SELECT name, role FROM users WHERE name = ?", (name,)).fetchall()

attack = "x' OR '1'='1"
print("unsafe, attacker input:", find_unsafe(attack))     # leaks every row
print("safe,   attacker input:", find_safe(attack))        # just a strange name: no match
print("safe,   honest input  :", find_safe("lukas"))
