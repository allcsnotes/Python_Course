from sqlalchemy import event
from fastapi.testclient import TestClient

from app.db import engine
from app.main import app

statements = []
with engine.connect():
    pass


@event.listens_for(engine, "before_cursor_execute")
def record(conn, cursor, statement, *rest):
    statements.append(" ".join(statement.split()))


client = TestClient(app)
client.get("/courses?limit=6")
print(len(statements), "queries")
for sql in statements:
    print(sql[:58])
