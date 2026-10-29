from datetime import datetime

start = datetime(2026, 11, 2, 18, 0)
for code in ["%Y", "%m", "%d", "%H", "%M", "%A", "%B"]:
    print(code, start.strftime(code))
