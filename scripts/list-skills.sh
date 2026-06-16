#!/usr/bin/env bash
set -euo pipefail

REPO="$(cd "$(dirname "$0")/.." && pwd)"
SCRIPT_DIR="$REPO/scripts"

cd "$REPO"
"$SCRIPT_DIR/published-skill-dirs.sh" |
  sed "s|^$REPO/||; s|$|/SKILL.md|" |
  sort
