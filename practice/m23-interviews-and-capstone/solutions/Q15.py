# Q15 - Dataclasses and abstract classes
from abc import ABC, abstractmethod
from dataclasses import dataclass, field

@dataclass(frozen=True, slots=True)
class Lesson:
    title: str
    minutes: int = 10
    tags: tuple = ()

@dataclass
class Course:
    title: str
    lessons: list[Lesson] = field(default_factory=list)   # never = []

l = Lesson("Loops", 20)
print(l, l == Lesson("Loops", 20))
try:
    l.minutes = 5
except Exception as error:
    print(type(error).__name__ + ":", error)

class Payment(ABC):
    @abstractmethod
    def pay(self, amount): ...

class Card(Payment):
    def pay(self, amount):
        print(f"Charged Rs {amount}")

Card().pay(499)
try:
    Payment()
except TypeError as error:
    print("TypeError:", error)
