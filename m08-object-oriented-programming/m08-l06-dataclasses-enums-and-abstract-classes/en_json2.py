import json
from enum import Enum


class Level(Enum):
    BEGINNER = 1
    INTERMEDIATE = 2
    ADVANCED = 3


text = json.dumps({"level": Level.BEGINNER.value})
print(text)
data = json.loads(text)
print(Level(data["level"]))
