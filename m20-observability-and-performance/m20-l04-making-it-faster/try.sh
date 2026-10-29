#!/bin/zsh
cd "${0:A:h}/stack"
for v in $@; do
  TAG=$v docker compose up -d --force-recreate api >/dev/null 2>&1; 
  for i in {1..30}; do curl -sf localhost:8204/health/live >/dev/null && break; sleep 1; done
  T=$(curl -s -X POST localhost:8204/auth/login -d 'username=meera@example.com&password=meera-demo-pass' | python3 -c 'import sys,json;print(json.load(sys.stdin)["access_token"])')
  curl -s -o /dev/null -H "Authorization: Bearer $T" localhost:8204/me/dashboard
  for i in 1 2 3; do curl -s -o /dev/null -w "$v %{http_code} %{time_total}\n" -H "Authorization: Bearer $T" localhost:8204/me/dashboard; done
  curl -s -H "Authorization: Bearer $T" localhost:8204/me/dashboard | md5
done
