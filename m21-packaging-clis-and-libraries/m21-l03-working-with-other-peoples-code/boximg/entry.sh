#!/bin/sh
cp -r /src /work && cd /work
pip install -q --root-user-action=ignore --no-build-isolation --no-deps . 2>&1 | grep -v '^$' || true
exec "$@"
