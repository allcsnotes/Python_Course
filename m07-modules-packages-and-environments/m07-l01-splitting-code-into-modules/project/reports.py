import csv
import json


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
