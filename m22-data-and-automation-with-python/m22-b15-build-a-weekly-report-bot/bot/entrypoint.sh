#!/bin/sh
printenv | grep -E '^(API_|SMTP_|MAIL_|ALERT_|OUT_DIR|TZ)' > /etc/weekly-report.env
chown app /etc/weekly-report.env && chmod 600 /etc/weekly-report.env
exec cron -f
