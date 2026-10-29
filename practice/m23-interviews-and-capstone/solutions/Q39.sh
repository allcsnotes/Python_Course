#!/bin/sh
# Q39 - A non-root container configured by environment variables
cd "$(dirname "$0")/Q39_docker"
docker build -q -t m23p04-app:1 . >/dev/null
echo "--- who am I inside?"
docker run --rm --entrypoint id m23p04-app:1 -un
echo "--- defaults"
docker run --rm m23p04-app:1
echo "--- production values from the environment"
docker run --rm -e DEBUG=false -e WORKERS=8 -e DATABASE_URL=postgresql://db/prod m23p04-app:1
docker rmi -f m23p04-app:1 >/dev/null
