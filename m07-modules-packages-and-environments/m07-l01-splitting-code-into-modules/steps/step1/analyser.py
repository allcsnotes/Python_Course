import csv
import json
import re
from collections import Counter
from pathlib import Path

import lines

LOG_FILE = Path("server.log")
REPORT_DIR = Path("report")


def analyse(path):
    levels = Counter()
    errors_by_hour = Counter()
    kinds = Counter()
    bad = []
    total = 0
    with path.open(encoding="utf-8") as f:
        for number, line in enumerate(f, start=1):
            total += 1
            try:
                when, level, message = lines.parse_line(line)
            except ValueError as err:
                bad.append((number, str(err)))
                continue
            levels[level] += 1
            if level == "ERROR":
                errors_by_hour[when.hour] += 1
                kind = re.sub(r"\d+", "#", message)
                kinds[kind] += 1
    return {
        "total": total,
        "bad": bad,
        "levels": levels,
        "errors_by_hour": errors_by_hour,
        "kinds": kinds,
    }


def write_report(result, folder):
    levels = result["levels"]
    errors = result["errors_by_hour"]
    lines = ["allcsvideos server log report", ""]
    lines.append(f"Lines read: {result['total']}")
    lines.append(f"Bad lines:  {len(result['bad'])}")
    for level in ("INFO", "WARNING", "ERROR"):
        lines.append(f"{level:<8} {levels[level]:>5}")
    lines += ["", "Errors per hour", ""]
    for hour in range(24):
        count = errors[hour]
        bar = "#" * (count // 3)
        lines.append(f"{hour:02d}:00 {bar:<32} {count}")
    lines += ["", "Top error messages", ""]
    for kind, count in result["kinds"].most_common(3):
        lines.append(f"{count:>5}  {kind}")
    lines += ["", "Skipped lines", ""]
    for number, why in result["bad"]:
        lines.append(f"line {number}: {why}")
    path = folder / "report.txt"
    path.write_text("\n".join(lines) + "\n")


def write_csv(result, folder):
    errors = result["errors_by_hour"]
    path = folder / "errors_per_hour.csv"
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["hour", "errors"])
        for hour in range(24):
            writer.writerow([hour, errors[hour]])


def write_json(result, folder):
    hour, count = result["errors_by_hour"].most_common(1)[0]
    summary = {
        "total_lines": result["total"],
        "bad_lines": len(result["bad"]),
        "levels": result["levels"],
        "busiest_hour": hour,
        "errors_in_busiest_hour": count,
    }
    path = folder / "summary.json"
    path.write_text(json.dumps(summary, indent=2) + "\n")


def main():
    if not LOG_FILE.exists():
        print(f"{LOG_FILE} not found: run make_log.py")
        return
    result = analyse(LOG_FILE)
    REPORT_DIR.mkdir(exist_ok=True)
    write_report(result, REPORT_DIR)
    write_csv(result, REPORT_DIR)
    write_json(result, REPORT_DIR)
    print(f"Read {result['total']} lines.")
    print(f"Skipped {len(result['bad'])} bad lines.")
    print(f"Reports are in the {REPORT_DIR} folder.")


main()
