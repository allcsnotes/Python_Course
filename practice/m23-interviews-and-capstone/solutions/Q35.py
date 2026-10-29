# Q35 - Transactions: all or nothing (Postgres in Docker)
import psycopg

URL = "postgresql://practice:practice@localhost:23604/practice"

with psycopg.connect(URL, autocommit=True) as setup:
    setup.execute("DROP TABLE IF EXISTS q35_wallet")
    setup.execute("CREATE TABLE q35_wallet (name text PRIMARY KEY, rupees int CHECK (rupees >= 0))")
    setup.execute("INSERT INTO q35_wallet VALUES ('Asha', 500), ('Lukas', 100)")

def balances():
    with psycopg.connect(URL) as conn:
        return dict(conn.execute("SELECT name, rupees FROM q35_wallet ORDER BY name").fetchall())

def transfer(sender, receiver, amount):
    with psycopg.connect(URL) as conn:          # one transaction: commit on success, rollback on error
        conn.execute("UPDATE q35_wallet SET rupees = rupees - %s WHERE name = %s", (amount, sender))
        conn.execute("UPDATE q35_wallet SET rupees = rupees + %s WHERE name = %s", (amount, receiver))

print("start      :", balances())
transfer("Asha", "Lukas", 200)
print("after 200  :", balances())
try:
    transfer("Asha", "Lukas", 900)              # the first UPDATE breaks the CHECK
except psycopg.errors.CheckViolation as error:
    print("failed     :", type(error).__name__)
print("after fail :", balances(), "(nothing half-done)")

with psycopg.connect(URL, autocommit=True) as setup:
    setup.execute("DROP TABLE q35_wallet")
