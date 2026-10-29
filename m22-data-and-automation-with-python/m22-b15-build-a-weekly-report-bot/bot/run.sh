#!/bin/sh
# cron starts jobs with an almost empty environment,
# so load the settings that the container was started with
set -a
. /etc/weekly-report.env
exec /app/.venv/bin/weekly-report run
