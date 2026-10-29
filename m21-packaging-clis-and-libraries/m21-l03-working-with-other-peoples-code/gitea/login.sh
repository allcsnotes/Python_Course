#!/usr/bin/env bash
# Run INSIDE a clone: ./path/to/gitea/login.sh asha
# Tells this one clone to use the demo login of a local Gitea user, so git does not ask
# for a password and does not store it anywhere else (keychain, global config).
# The password is a demo value that only exists in your throwaway local Gitea.
set -euo pipefail
USER_NAME="${1:?usage: login.sh asha|meera}"
HERE="$(cd "$(dirname "$0")" && pwd)"
mkdir -p "$HERE/.local"
echo "http://$USER_NAME:demo-password-123@localhost:21303" > "$HERE/.local/cred-$USER_NAME"
chmod 600 "$HERE/.local/cred-$USER_NAME"
git config credential.helper ""
git config --add credential.helper "store --file=$HERE/.local/cred-$USER_NAME"
git config user.name "$(echo "$USER_NAME" | awk '{print toupper(substr($0,1,1)) substr($0,2)}')"
git config user.email "$USER_NAME@example.test"
echo "This clone now acts as $USER_NAME on http://localhost:21303"
