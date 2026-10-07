#!/usr/bin/env bash
set -euo pipefail

REPO="$(cd "$(dirname "$0")/.." && pwd)"

source "$REPO/scripts/python.sh"
# Buffer the validated manifest before printing; keep Git Bash POSIX paths.
paths="$("$PYTHON" "$REPO/scripts/skills.py" paths --repo "$REPO")"
while IFS= read -r path; do
  printf '%s/%s\n' "$REPO" "$path"
done <<< "$paths"
