#!/bin/zsh
# count the SQL queries that ONE request to /me/dashboard runs
psql() { docker exec m20l04-pg psql -U allcs -tA "$@"; }
T=$(curl -s -X POST localhost:8204/auth/login -d 'username=meera@example.com&password=meera-demo-pass' | python3 -c 'import sys,json;print(json.load(sys.stdin)["access_token"])')
curl -s -o /dev/null -H "Authorization: Bearer $T" localhost:8204/me/dashboard
psql -c "select pg_stat_statements_reset()" >/dev/null
curl -s -o /dev/null -H "Authorization: Bearer $T" localhost:8204/me/dashboard
n=$(psql -c "select sum(calls) from pg_stat_statements where query ~* '^select' and query not ilike 'select \$1' and query not like '%pg_stat_statements%'")
echo "one request ran $n queries"
