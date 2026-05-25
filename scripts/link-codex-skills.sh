#!/usr/bin/env bash
set -euo pipefail

# Links all shippable skills in the repository to ~/.codex/skills, so that
# they can be used by Codex.

REPO="$(cd "$(dirname "$0")/.." && pwd)"
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

  if [ -e "$target" ] && [ ! -L "$target" ]; then
    echo "skip $name: $target exists and is not a symlink" >&2
    continue
  fi

  ln -sfn "$src" "$target"
  echo "linked $name -> $src"
done
