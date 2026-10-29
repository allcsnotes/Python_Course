#!/usr/bin/env bash
# Runs ON THE SERVER after Docker is installed (user-data calls it).
#   install_app.sh REGISTRY [TAG]   prepare /opt/allcs; deploy TAG if given
set -euo pipefail
registry="${1:?registry}"
tag="${2:-}"
cd /opt/allcs
chmod +x deploy.sh smoke.sh
mkdir -p caddy
cp -n Caddyfile caddy/Caddyfile
[ -f caddy/active.caddy ]  || echo 'respond "starting" 503' > caddy/active.caddy
[ -f caddy/preview.caddy ] || echo 'respond "no preview" 503' > caddy/preview.caddy
if [ ! -f .env ]; then
  umask 077
  {
    echo "REGISTRY=$registry"
    echo "SECRET_KEY=$(openssl rand -hex 32)"
    echo "POSTGRES_PASSWORD=$(openssl rand -hex 24)"
    echo "SEED_ADMIN_PASSWORD=${SEED_ADMIN_PASSWORD:-change-me-now}"
  } > .env
fi
[ -f state.env ] || printf 'ACTIVE=\nBLUE_TAG=\nGREEN_TAG=\nMIGRATE_TAG=\n' > state.env
if [ -n "$tag" ]; then ./deploy.sh deploy "$tag"; fi
