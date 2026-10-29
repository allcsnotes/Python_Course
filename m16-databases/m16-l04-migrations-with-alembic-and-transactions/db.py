from sqlalchemy import create_engine

URL = "postgresql+psycopg://allcs:secret@localhost:15404/allcsvideos"
engine = create_engine(URL)
