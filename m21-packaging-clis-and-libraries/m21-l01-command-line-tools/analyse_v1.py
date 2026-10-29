import sys
from pathlib import Path

from logtools import analyse

path = Path(sys.argv[1])
with path.open(encoding="utf-8") as f:
    result = analyse(f)
errors = result["levels"]["ERROR"]
print(f"{path}: {errors} errors in {result['total']} lines")
