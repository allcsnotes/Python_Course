#!/bin/zsh
# usage: use.sh TAG -> start the api container from image TAG and wait until it is ready
cd "${0:A:h}/stack"; export TAG=$1 POOL_SIZE=${2:-5} MAX_OVERFLOW=${3:-10}
docker compose up -d --force-recreate api >/dev/null 2>&1
for i in {1..40}; do curl -sf localhost:8204/health/ready >/dev/null && break; sleep 1; done
