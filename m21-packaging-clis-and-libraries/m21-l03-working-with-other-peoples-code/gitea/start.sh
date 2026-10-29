#!/usr/bin/env bash
# Starts a throwaway Gitea server (a small "GitHub" on your laptop), creates two DEMO users and
# puts a copy of humanize under Meera. Nothing goes to GitHub.
#
# Usage:  ./gitea/start.sh /path/to/your/humanize/clone
#
# All values below are demo values for this local lab only. Registration is closed and SSH is off.
set -euo pipefail
CLONE="${1:?usage: start.sh /path/to/humanize/clone}"
HERE="$(cd "$(dirname "$0")" && pwd)"
NAME=pyrepo-m21-gitea
PORT=21303
PW="demo-password-123"            # demo value, only for the two local users below
mkdir -p "$HERE/.local"

docker rm -f -v "$NAME" >/dev/null 2>&1 || true
docker run -d --name "$NAME" -p "$PORT:3000" \
  -e GITEA__security__INSTALL_LOCK=true \
  -e GITEA__server__ROOT_URL="http://localhost:$PORT/" \
  -e GITEA__server__DISABLE_SSH=true \
  -e GITEA__service__DISABLE_REGISTRATION=true \
  -e GITEA__database__DB_TYPE=sqlite3 \
  gitea/gitea:1.24.6 >/dev/null
for _ in $(seq 60); do
  curl -sf "http://localhost:$PORT/api/healthz" >/dev/null && break
  sleep 1
done

mkuser() {   # name, extra flags
  docker exec -u git "$NAME" gitea admin user create --username "$1" --password "$PW" \
    --email "$1@example.test" --must-change-password=false $2 >/dev/null
  docker exec -u git "$NAME" gitea admin user generate-access-token --username "$1" \
    --token-name lab --scopes all --raw > "$HERE/.local/$1.token"
}
mkuser meera --admin
mkuser asha ""

# Meera's repository: a copy of humanize
curl -sf -X POST "http://localhost:$PORT/api/v1/user/repos" \
  -H "Authorization: token $(cat "$HERE/.local/meera.token")" -H 'Content-Type: application/json' \
  -d '{"name":"humanize","default_branch":"main"}' >/dev/null
git -C "$CLONE" -c credential.helper= push "http://meera:$(cat "$HERE/.local/meera.token")@localhost:$PORT/meera/humanize.git" HEAD:refs/heads/main >/dev/null 2>&1
echo "Gitea is running at http://localhost:$PORT  (users: meera, asha; demo password: $PW)"
echo "Tokens are in $HERE/.local/ (local, demo, not for sharing)"
