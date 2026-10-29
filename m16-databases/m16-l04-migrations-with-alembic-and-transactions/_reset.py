import psycopg
with psycopg.connect("postgresql://allcs:secret@localhost:15404/allcsvideos", autocommit=True) as c:
    c.execute("DROP SCHEMA public CASCADE"); c.execute("CREATE SCHEMA public")
