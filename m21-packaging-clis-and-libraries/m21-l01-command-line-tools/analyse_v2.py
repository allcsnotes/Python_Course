import argparse
from pathlib import Path

from logtools import analyse

parser = argparse.ArgumentParser(description="Analyse a server log.")
parser.add_argument("logfile", type=Path, help="the log file to read")
parser.add_argument(
    "--level", choices=["INFO", "WARNING", "ERROR"], default="ERROR"
)
parser.add_argument("--top", type=int, default=3, help="how many")
args = parser.parse_args()

with args.logfile.open(encoding="utf-8") as f:
    result = analyse(f, args.level)
count = result["levels"][args.level]
print(f"{args.logfile}: {count} lines with level {args.level}")
for message, number in result["kinds"].most_common(args.top):
    print(f"{number:>5}  {message}")
