# Q36 - Indexes, proved with EXPLAIN ANALYZE (Postgres in Docker)
import psycopg

URL = "postgresql://practice:practice@localhost:23604/practice"

with psycopg.connect(URL, autocommit=True) as conn:
    conn.execute("DROP TABLE IF EXISTS q36_enrollment")
    conn.execute("CREATE TABLE q36_enrollment (id serial PRIMARY KEY, student_id int, course_id int)")
    conn.execute("""INSERT INTO q36_enrollment (student_id, course_id)
                    SELECT n % 50000, n % 40 FROM generate_series(1, 300000) n""")
    conn.execute("ANALYZE q36_enrollment")

    def plan(label):
        rows = conn.execute("EXPLAIN (ANALYZE, COSTS OFF, TIMING OFF) "
                            "SELECT * FROM q36_enrollment WHERE student_id = 4242").fetchall()
        lines = [r[0] for r in rows]
        print(label)
        for line in lines:
            if "Scan" in line or "Execution" in line or "Rows Removed" in line:
                print("  ", line.strip())

    plan("without an index:")
    conn.execute("CREATE INDEX q36_student_idx ON q36_enrollment (student_id)")
    conn.execute("ANALYZE q36_enrollment")
    plan("with an index:")
    conn.execute("DROP TABLE q36_enrollment")
