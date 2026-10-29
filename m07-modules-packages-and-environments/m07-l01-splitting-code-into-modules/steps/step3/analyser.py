from pathlib import Path

from counting import analyse
from reports import write_csv, write_json, write_report

LOG_FILE = Path("server.log")
REPORT_DIR = Path("report")


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
