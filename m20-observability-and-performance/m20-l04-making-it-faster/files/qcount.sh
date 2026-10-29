#!/bin/zsh
# how many SQL statements does ONE request to /me/dashboard run? (pg_stat_statements)
psql() { docker exec m20l04-pg psql -U allcs -tA "$@"; }
T=$(curl -s -X POST localhost:8204/auth/login -d 'username=meera@example.com&password=meera-demo-pass' | python3 -c 'import sys,json;print(json.load(sys.stdin)["access_token"])')
curl -s -o /dev/null -H "Authorization: Bearer $T" localhost:8204/me/dashboard   # warm up (cache fill etc.)
psql -c "select pg_stat_statements_reset()" >/dev/null
curl -s -o /dev/null -H "Authorization: Bearer $T" localhost:8204/me/dashboard
psql -c "select coalesce(sum(calls),0) from pg_stat_statements where dbid = (select oid from pg_database where datname='allcs') and query ~* '^select' and query !~* '^select \$1$' and query not ilike 'select \$1' and query not like '%pg_stat_statements%'"
