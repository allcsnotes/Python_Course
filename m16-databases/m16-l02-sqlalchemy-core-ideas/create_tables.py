from db import engine, show_sql
from models import Base

show_sql()
Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)
