import logging
from pathlib import Path

from mailer import send_report
from sheets import summarise, write_report

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger("weekly")


def main():
    summary = summarise(Path("data/enrollments_week.xlsx"))
    write_report(summary, Path("report.xlsx"))
    send_report(Path("report.xlsx"), "meera@allcsvideos.com")
    log.info("report sent: %d courses", len(summary))


main()
