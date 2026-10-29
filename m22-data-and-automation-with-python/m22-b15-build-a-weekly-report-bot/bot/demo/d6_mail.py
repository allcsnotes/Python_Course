from weekly_report.mail import make_message, send
from weekly_report.settings import Settings

settings = Settings()
out = settings.out_dir
message = make_message(
    settings,
    "Weekly report 2026-W43",
    "36 new enrollments (last week 14).",
    settings.mail_to,
    [out / "2026-W43.xlsx", out / "2026-W43.pdf"],
)
send(settings, message)
print("sent to", settings.mail_to)
