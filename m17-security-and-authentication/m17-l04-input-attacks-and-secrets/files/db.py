from sqlalchemy import create_engine

URL = "postgresql+psycopg://postgres:devpass@localhost:17404/allcs"
engine = create_engine(URL)
