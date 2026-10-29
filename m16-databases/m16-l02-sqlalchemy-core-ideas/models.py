from sqlalchemy.orm import (
    DeclarativeBase, Mapped, mapped_column,
)


class Base(DeclarativeBase):
    pass


class Course(Base):
    __tablename__ = "courses"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]
    price: Mapped[int]
    level: Mapped[str]
    description: Mapped[str | None]

    def __repr__(self):
        return f"Course({self.id}, {self.title!r}, {self.price})"
