#!/usr/bin/env bash
# Usage: smoke.sh BASE_URL [EXPECTED_VERSION]
# A few real requests; any failure stops the deploy.
base="${1:?base url}"
want="${2:-}"
fail=0
check() { # name, expected code, path, [grep text]
  local name="$1" code="$2" path="$3" text="${4:-}" out got
  out="$(mktemp)"
  got="$(curl -s -m 5 -o "$out" -w '%{http_code}' "$base$path" || true)"
  if [ "$got" = "$code" ] && { [ -z "$text" ] || grep -q "$text" "$out"; }; then
    echo "  ok    $name ($got)"
  else
    echo "  FAIL  $name: wanted $code${text:+ with $text}, got $got"; fail=1
  fi
  rm -f "$out"
}
echo "smoke test on $base"
check "live"             200 /health/live alive
check "ready"            200 /health/ready '"postgres":"ok"'
if [ -n "$want" ]; then
  check "version is $want" 200 /version "\"version\":\"$want\""
fi
check "course list"      200 '/courses?limit=5' '"items"'
check "login is required" 401 /me
if [ "$fail" = 0 ]; then echo "SMOKE PASSED"
else echo "SMOKE FAILED"; exit 1; fi
