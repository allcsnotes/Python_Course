#!/usr/bin/env bash
# Run the real workflow file locally with act. Usage: ci.sh NAME
# Retries only when the failure was the network (GitHub unreachable), never a real failure.
cd "$(dirname "$0")/../allcs"
log="../rehearsal/logs/$1.log"
for try in 1 2 3; do
  docker ps -a --format '{{.Names}}' | grep '^act-pipeline-' | xargs -r docker rm -f >/dev/null 2>&1
  docker network ls --format '{{.Name}}' | grep '^act-pipeline' | xargs -r docker network rm >/dev/null 2>&1
  act push -P ubuntu-latest=catthehacker/ubuntu:act-latest \
    --container-architecture linux/arm64 --pull=false --concurrent-jobs 1 \
    --action-offline-mode > "$log" 2>&1
  code=$?
  [ $code = 0 ] && break
  grep -qE "Connect Timeout|TLS handshake timeout|ETIMEDOUT|ECONNRESET|getaddrinfo|port is already allocated|driver failed programming" "$log" || break
  cp "$log" "../rehearsal/logs/$1.network-try$try.log"
  echo "network trouble, trying again ($try)"
done
echo "act exit code $code" | tee -a "$log"
