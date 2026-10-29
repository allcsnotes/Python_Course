from pathlib import Path

from mailer import send_report

send_report(Path("report.xlsx"), "meera@allcsvideos.com")
print("sent")
