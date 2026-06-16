#!/usr/bin/env bash
set -euo pipefail

# Links all published skills in the repository to ~/.codex/skills, so that
# they can be used by Codex.

REPO="$(cd "$(dirname "$0")/.." && pwd)"
SCRIPT_DIR="$REPO/scripts"
DEST="${CODEX_HOME:-$HOME/.codex}/skills"

if [ -L "$DEST" ]; then
  resolved="$(readlink -f "$DEST")"
  case "$resolved" in
    "$REPO"|"$REPO"/*)
      echo "error: $DEST is a symlink into this repo ($resolved)." >&2
      echo "Remove it and re-run; the script will recreate it as a real dir." >&2
      exit 1
      ;;
  esac
fi

mkdir -p "$DEST"

"$SCRIPT_DIR/published-skill-dirs.sh" |
while IFS= read -r src; do
  name="$(basename "$src")"
  target="$DEST/$name"

  if [ -e "$target" ] && [ ! -L "$target" ]; then
    echo "skip $name: $target exists and is not a symlink" >&2
    continue
  fi

  ln -sfn "$src" "$target"
  echo "linked $name -> $src"
done
