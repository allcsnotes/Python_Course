from pydantic import BaseModel, ConfigDict, ValidationError


class Loose(BaseModel):
    title: str
    sale_price: int | None = None


class Strict(Loose):
    model_config = ConfigDict(extra="forbid")


data = {"title": "Python", "sale_prise": 999}
print(Loose(**data))
try:
    Strict(**data)
except ValidationError as err:
    print(err.errors()[0]["msg"])
