#!/usr/bin/env bash
# Removes the Gitea container and its data.
docker rm -f -v pyrepo-m21-gitea
rm -rf "$(cd "$(dirname "$0")" && pwd)/.local"
