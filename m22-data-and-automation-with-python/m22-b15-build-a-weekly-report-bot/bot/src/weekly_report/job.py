import logging
from datetime import timedelta

from weekly_report import analyse, excel, mail, marker, pdf
from weekly_report.api import fetch_with_tries
from weekly_report.weeks import week_bounds, week_label

log = logging.getLogger("weekly_report")


def make_files(summary, label, out):
    out.mkdir(parents=True, exist_ok=True)
    book, page = out / f"{label}.xlsx", out / f"{label}.pdf"
    chart = out / f"{label}.png"
    excel.build_workbook(summary, label, book)
    pdf.draw_chart(summary, chart)
    pdf.build_pdf(summary, label, chart, page)
    return [book, page]


def make_body(summary, label):
    if summary.enrollments == 0:
        return f"A quiet week: no enrollments in {label}."
    top = summary.per_course.index[0]
    return (
        f"{summary.enrollments} new enrollments "
        f"(last week {summary.before}).\n"
        f"Revenue Rs {summary.gross}, "
        f"refunds Rs {summary.refunded}, "
        f"net Rs {summary.net}.\n"
        f"Top course: {top}.\n"
    )


def get_summary(settings, client, monday):
    start, end = week_bounds(monday, settings.timezone)
    before = start - timedelta(days=7)
    log.info("week %s to %s", start.date(), end.date())
    data = fetch_with_tries(client, settings, before, end)
    summary = analyse.summarise(
        data, start, end, settings.timezone
    )
    log.info(
        "%d enrollments, %d refunds",
        summary.enrollments,
        summary.refunds,
    )
    return summary


def build_message(settings, summary, label):
    files = []
    if summary.enrollments:
        files = make_files(summary, label, settings.out_dir)
    return mail.make_message(
        settings,
        f"Weekly report {label}",
        make_body(summary, label),
        settings.mail_to,
        files,
    )


def run_week(
    settings,
    monday,
    client,
    dry_run=False,
    force=False,
    send=mail.send,
):
    label = week_label(monday)
    if marker.already_sent(settings, label) and not force:
        log.info("week %s already sent, skipping", label)
        return "skipped"
    summary = get_summary(settings, client, monday)
    message = build_message(settings, summary, label)
    if dry_run:
        log.info("dry run: nothing sent")
        return "dry"
    send(settings, message)
    marker.mark_sent(settings, label, settings.mail_to)
    log.info("sent %s to %s", label, settings.mail_to)
    return "sent"


def alert(settings, label, err, send=mail.send):
    send(
        settings,
        mail.make_message(
            settings,
            f"ALERT: report {label} failed",
            f"The report could not be made.\nReason: {err}\n",
            settings.alert_to,
        ),
    )
    log.error("alert sent to %s", settings.alert_to)
