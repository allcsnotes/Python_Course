#!/bin/zsh
# usage: run_step.sh <image tag> <csv prefix> [POOL_SIZE] [MAX_OVERFLOW]
# the same Locust run for every step: 20 users, 5 new users per second, 60 seconds
cd "${0:A:h}/stack"
export TAG=$1 POOL_SIZE=${3:-5} MAX_OVERFLOW=${4:-10}
docker compose up -d --force-recreate api >/dev/null 2>&1
for i in {1..40}; do curl -sf localhost:8204/health/ready >/dev/null && break; sleep 1; done
docker exec m20l04-redis redis-cli flushall >/dev/null
cd ..
locust -f locustfile.py --headless --host http://localhost:8204 -u 20 -r 5 -t 60s --csv runs/$2 --only-summary > runs/$2.out 2>&1
python3 - <<PY
import csv
for x in csv.DictReader(open('runs/$2_stats.csv')):
    print('$2'.ljust(10), x['Name'].ljust(16), x['Request Count'].rjust(5), 'rps %5.1f' % float(x['Requests/s']), 'p50', x['50%'].rjust(5), 'p95', x['95%'].rjust(5), 'p99', x['99%'].rjust(5), 'fail', x['Failure Count'])
PY
