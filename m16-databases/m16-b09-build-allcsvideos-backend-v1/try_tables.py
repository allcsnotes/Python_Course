from sqlalchemy.schema import CreateTable

from app.db import engine
from app.models import Course

print(CreateTable(Course.__table__).compile(engine))
