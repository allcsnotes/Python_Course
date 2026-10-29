# Exercise 20 - Fix the broken dataclass and abstract code (all five repaired)
from abc import ABC, abstractmethod
from dataclasses import dataclass, field


@dataclass
class Lesson:
    title: str
    minutes: int                        # was: put after "free: bool = False"
    free: bool = False


print(Lesson("Variables", 12))


@dataclass
class Course:
    title: str
    lessons: list = field(default_factory=list)   # was: lessons: list = []


python = Course("Python")
sql = Course("SQL")
python.lessons.append("Variables")
print(python)
print(sql)


@dataclass(frozen=True)
class Tag:
    name: str


tag = Tag("python")
renamed = Tag("python-3")               # was: tag.name = "python-3"  (frozen)
print(tag, renamed)


class Payment(ABC):                     # was: class Payment:  (no ABC)
    @abstractmethod
    def pay(self, amount):
        pass


class CardPayment(Payment):
    def pay(self, amount):              # was: def charge(self, amount)
        print(f"Charged Rs {amount}")


CardPayment().pay(2499)

try:
    Payment()
except TypeError as error:
    print("TypeError:", error)
