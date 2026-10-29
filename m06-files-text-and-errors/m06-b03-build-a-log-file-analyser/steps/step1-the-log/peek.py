from pathlib import Path

log = Path("server.log")
print(log.exists())
with log.open(encoding="utf-8") as f:
    for number, line in enumerate(f, start=1):
        print(number, line.rstrip())
        if number == 4:
            break
