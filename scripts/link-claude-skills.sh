#!/usr/bin/env bash
set -euo pipefail

REPO="$(cd "$(dirname "$0")/.." && pwd)"
exec bash "$REPO/scripts/install-skills.sh" claude "$@"
