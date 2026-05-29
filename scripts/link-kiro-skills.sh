#!/usr/bin/env bash
set -euo pipefail

# Copies all shippable skills in the repository to ~/.kiro/skills, so that
# they can be used by Kiro without relying on symlinks.

REPO="$(cd "$(dirname "$0")/.." && pwd)"
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

find "$REPO/skills" -name SKILL.md \
  -not -path '*/node_modules/*' \
  -not -path '*/deprecated/*' \
  -not -path '*/drafts/*' \
  -not -path '*/in-progress/*' \
  -not -path '*/local/*' \
  -not -path '*/personal/*' \
  -print0 |
while IFS= read -r -d '' skill_md; do
  src="$(dirname "$skill_md")"
  name="$(basename "$src")"
  target="$DEST/$name"

  tmp="$DEST/.$name.tmp"

  rm -rf "$tmp"
  cp -R "$src" "$tmp"
  rm -rf "$target"
  mv "$tmp" "$target"

  echo "copied $name -> $target"
done
