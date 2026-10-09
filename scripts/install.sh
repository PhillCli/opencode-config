#!/usr/bin/env bash

# Install or refresh this preset in ~/.config/opencode/: the symlinked live
# directories and AGENTS.md, a copy of opencode.json for other projects to
# load, and the plugin shims from scripts/install-plugins.sh.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(dirname "$SCRIPT_DIR")"
DEST_DIR="$HOME/.config/opencode"

mkdir -p "$DEST_DIR"

# Symlink the live sources. Rewrite only on drift so directory watchers
# stay quiet; refuse to replace anything that is not already a symlink.
for item in AGENTS.md commands agents skills; do
  dest="$DEST_DIR/$item"
  if [[ -e "$dest" && ! -L "$dest" ]]; then
    echo "refusing to replace non-symlink $dest" >&2
    exit 1
  fi
  if [[ "$(readlink "$dest" 2>/dev/null || true)" != "$REPO_ROOT/$item" ]]; then
    ln -sfn "$REPO_ROOT/$item" "$dest"
  fi
done

# Global config is a real file, not a symlink, so refuse to write through one.
dest="$DEST_DIR/opencode.json"
if [[ -L "$dest" ]]; then
  echo "refusing to write through symlink $dest" >&2
  exit 1
fi
cmp -s "$REPO_ROOT/opencode.json" "$dest" || cp "$REPO_ROOT/opencode.json" "$dest"

"$SCRIPT_DIR/install-plugins.sh"
