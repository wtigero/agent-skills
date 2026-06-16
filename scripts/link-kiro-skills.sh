#!/usr/bin/env bash
set -euo pipefail

# Copies all published skills in the repository to ~/.kiro/skills, so that
# they can be used by Kiro without relying on symlinks (Kiro does not resolve
# symlinked skill directories).

REPO="$(cd "$(dirname "$0")/.." && pwd)"
SCRIPT_DIR="$REPO/scripts"
DEST="$HOME/.kiro/skills"

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
  tmp="$DEST/.$name.tmp"

  rm -rf "$tmp"
  cp -R "$src" "$tmp"
  rm -rf "$target"
  mv "$tmp" "$target"

  echo "copied $name -> $target"
done
