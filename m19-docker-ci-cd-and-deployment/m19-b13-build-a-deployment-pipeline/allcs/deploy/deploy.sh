#!/usr/bin/env bash
# Runs ON THE SERVER, in /opt/allcs.
#   deploy.sh deploy TAG   roll out image TAG with no downtime
#   deploy.sh rollback     go back to the previous version
#   deploy.sh status
set -euo pipefail
export HOME="${HOME:-/root}"   # SSM runs us without a home
cd /opt/allcs

dc() { docker compose --env-file .env --env-file state.env "$@"; }
load() { . ./.env; . ./state.env; }
setvar() { sed -i "s|^$1=.*|$1=$2|" state.env; }
other() { if [ "$1" = blue ]; then echo green; else echo blue; fi; }
tagof() { local v; v="$(echo "$1" | tr a-z A-Z)_TAG"; echo "${!v:-}"; }

upstream() { # file color
  printf 'reverse_proxy api-%s:8000 {\n\thealth_uri /health/ready\n\thealth_interval 2s\n\tlb_try_duration 5s\n}\n' "$2" > "caddy/$1.tmp"
  mv "caddy/$1.tmp" "caddy/$1"
}
reload_caddy() { dc exec -T caddy caddy reload --config /etc/caddy/Caddyfile >/dev/null 2>&1; }

wait_healthy() { # color
  local id state
  for _ in $(seq 1 45); do
    id="$(dc ps -q "api-$1" || true)"
    state="$( [ -n "$id" ] && docker inspect -f '{{.State.Health.Status}}' "$id" || echo none)"
    echo "  api-$1 health: $state"
    [ "$state" = healthy ] && return 0
    sleep 2
  done
  return 1
}

registry_login() {
  case "$REGISTRY" in
    *.amazonaws.com)
      aws ecr get-login-password --region us-east-1 \
        | docker login --username AWS --password-stdin "$REGISTRY" ;;
  esac
}

switch_to() { # color
  upstream active.caddy "$1"; reload_caddy; setvar ACTIVE "$1"
}

rollback() {
  load
  local target; target="$(other "$ACTIVE")"
  local tag; tag="$(tagof "$target")"
  [ -n "$tag" ] || { echo "nothing to roll back to"; exit 1; }
  local bad="$ACTIVE"
  echo "ROLLBACK: $bad ($(tagof "$bad")) -> $target ($tag)"
  dc up -d --no-deps "api-$target"
  wait_healthy "$target" \
    || { echo "rollback target is not healthy"; exit 1; }
  switch_to "$target"
  load
  ./smoke.sh http://127.0.0.1 "$tag"
  dc logs --tail 15 "api-$bad" || true
  dc stop "api-$bad" >/dev/null
  setvar "$(echo "$bad" | tr a-z A-Z)_TAG" ""
  echo "ROLLBACK DONE: serving $tag from $target"
}

deploy() {
  local tag="$1"
  load
  registry_login
  local idle=blue                                     # first deploy -> blue
  [ -z "${ACTIVE:-}" ] || idle="$(other "$ACTIVE")"
  local IDLE; IDLE="$(echo "$idle" | tr a-z A-Z)"
  echo "DEPLOY $tag -> $idle (active now: ${ACTIVE:-none})"

  abort() { # reason
    echo "ABORT: $1 - visitors still get ${ACTIVE:-nothing}, untouched"
    dc logs --tail 20 "api-$idle" 2>/dev/null || true
    dc rm -sf "api-$idle" >/dev/null 2>&1 || true
    setvar "${IDLE}_TAG" ""
    exit 1
  }

  setvar "${IDLE}_TAG" "$tag"; setvar MIGRATE_TAG "$tag"; load
  dc pull -q "api-$idle" || abort "image $tag could not be pulled"
  dc up -d postgres redis caddy
  echo "-- migrate"
  dc run --rm -T migrate || abort "migration failed"
  if [ -z "${ACTIVE:-}" ]; then
    echo "-- first deploy: seed"
    dc run --rm -T seed || abort "seed failed"
  fi
  echo "-- start $idle"
  dc up -d --no-deps --force-recreate "api-$idle"
  upstream preview.caddy "$idle"; reload_caddy
  wait_healthy "$idle" || abort "new version never became healthy"
  ./smoke.sh http://127.0.0.1:8081 "$tag" \
    || abort "smoke test failed on the new version"

  echo "-- switch traffic to $idle"
  local old="${ACTIVE:-}"
  switch_to "$idle"; load
  if ! ./smoke.sh http://127.0.0.1 "$tag"; then
    echo "smoke test failed after the switch"
    if [ -n "$old" ]; then rollback; fi
    exit 1
  fi
  prev="${old:-none} $([ -z "$old" ] || tagof "$old")"
  echo "DEPLOY OK: $tag live on $idle (previous: $prev)"
}

case "${1:-}" in
  deploy)   deploy "${2:?tag}" ;;
  rollback) rollback ;;
  status)   load; echo "active=$ACTIVE blue=$BLUE_TAG green=$GREEN_TAG"; docker ps --format 'table {{.Names}}\t{{.Image}}\t{{.Status}}' ;;
  *) echo "usage: deploy.sh deploy TAG | rollback | status"; exit 2 ;;
esac
