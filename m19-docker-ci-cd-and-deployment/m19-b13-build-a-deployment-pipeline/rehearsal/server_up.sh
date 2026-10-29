#!/usr/bin/env bash
# Local rehearsal: a registry and a "server" (Docker inside a container).
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
APP="$HERE/../allcs"
docker network inspect m19b13-net >/dev/null 2>&1 || docker network create m19b13-net >/dev/null
docker volume create m19b13-dind >/dev/null
docker rm -f m19b13-registry m19b13-server >/dev/null 2>&1 || true
docker run -d --name m19b13-registry --network m19b13-net --network-alias registry -p 19050:5000 registry:2 >/dev/null
docker run -d --privileged --name m19b13-server --network m19b13-net -p 8703:80 \
  -e DOCKER_TLS_CERTDIR= -v m19b13-dind:/var/lib/docker \
  docker:dind dockerd --host=unix:///var/run/docker.sock --insecure-registry registry:5000 >/dev/null
for _ in $(seq 1 40); do docker exec m19b13-server docker info >/dev/null 2>&1 && break; sleep 1; done
# start from nothing: forget containers and data left in the inner Docker
docker exec m19b13-server sh -c 'docker rm -f $(docker ps -aq) 2>/dev/null; docker volume prune -af >/dev/null; true'
# what user-data does on AWS: install tools, copy the deploy bundle, prepare /opt/allcs
docker exec m19b13-server apk add --no-cache bash curl openssl >/dev/null
# the same Compose version the AWS user-data installs (this Mac is arm64, AWS is x86_64)
docker exec m19b13-server sh -c 'mkdir -p /usr/local/lib/docker/cli-plugins && curl -fsSL https://github.com/docker/compose/releases/download/v2.29.7/docker-compose-linux-aarch64 -o /usr/local/lib/docker/cli-plugins/docker-compose && chmod +x /usr/local/lib/docker/cli-plugins/docker-compose'
docker exec m19b13-server mkdir -p /opt/allcs
tar czf - -C "$APP/deploy" . | docker exec -i m19b13-server tar xzf - -C /opt/allcs
docker exec -e SEED_ADMIN_PASSWORD=demo-admin-pw m19b13-server bash /opt/allcs/install_app.sh registry:5000
echo "server ready: http://localhost:8703 (registry localhost:19050)"
