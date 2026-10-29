import sys
import psycopg
seats = int(sys.argv[1]) if len(sys.argv) > 1 else 30
with psycopg.connect("postgresql://allcs:secret@localhost:15404/allcsvideos", autocommit=True) as c:
    c.execute("DELETE FROM enrollments")
    c.execute("UPDATE courses SET seats = %s WHERE id = 3", (seats,))
