#!/usr/bin/env bash
# A visitor who never stops: ask for /version every 50 ms, count failures.
# Usage: hammer.sh URL SECONDS LOGFILE
url="$1"; secs="$2"; log="$3"
end=$((SECONDS + secs)); n=0; bad=0; : > "$log"
while [ $SECONDS -lt $end ]; do
  out="$(curl -s -m 3 -w ' %{http_code}' "$url/version" || echo ' 000')"
  code="${out##* }"; n=$((n+1))
  if [ "$code" != 200 ]; then bad=$((bad+1)); fi
  echo "$(date +%T) $code ${out% *}" >> "$log"
  sleep 0.05
done
echo "requests=$n failures=$bad" | tee -a "$log"
