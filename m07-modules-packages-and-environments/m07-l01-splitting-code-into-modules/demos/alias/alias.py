from pathlib import Path

import counting as cnt

result = cnt.analyse(Path("server.log"))
print(result["total"])
