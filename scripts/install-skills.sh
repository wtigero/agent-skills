#!/usr/bin/env bash
set -euo pipefail
REPO="$(cd "$(dirname "$0")/.." && pwd)"
source "$REPO/scripts/python.sh"
runtime="$1"
shift
extra=()
if [ -n "${CODEX_HOME:-}" ]; then extra+=(--codex-home "$CODEX_HOME"); fi
if [ -n "${XDG_CONFIG_HOME:-}" ]; then extra+=(--config-home "$XDG_CONFIG_HOME"); fi
if [ -n "${PI_CODING_AGENT_DIR:-}" ]; then extra+=(--pi-home "$PI_CODING_AGENT_DIR"); fi
exec "$PYTHON" "$REPO/scripts/skills.py" install --repo "$REPO" \
  --runtime "$runtime" --home "$HOME" --project "$PWD" "${extra[@]}" "$@"
