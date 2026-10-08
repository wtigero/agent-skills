#!/usr/bin/env bash
set -euo pipefail

REPO="$(cd "$(dirname "$0")/.." && pwd)"
source "$REPO/scripts/python.sh"
exec "$PYTHON" "$REPO/scripts/skills.py" list --repo "$REPO"
