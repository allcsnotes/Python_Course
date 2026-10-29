from sqlalchemy import text

from db import engine

with engine.connect() as conn:
    sql = text(
        "SELECT title, price FROM courses WHERE price < :limit"
    )
    result = conn.execute(sql, {"limit": 400})
    for row in result:
        print(row.title, row.price)
