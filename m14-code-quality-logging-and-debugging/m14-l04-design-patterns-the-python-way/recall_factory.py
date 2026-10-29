from dataclasses import dataclass, field


@dataclass
class Order:
    student: str
    items: list = field(default_factory=list)


lukas = Order("Lukas")
priya = Order("Priya")
lukas.items.append("c101")
print(lukas.items, priya.items)
