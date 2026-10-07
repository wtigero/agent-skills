#!/usr/bin/env bash
# Source this file; do not install anything when Python is missing.
PYTHON=""
for candidate in python3 python; do
  if command -v "$candidate" >/dev/null 2>&1 &&
     "$candidate" -c 'import sys; raise SystemExit(sys.version_info < (3, 9))' >/dev/null 2>&1; then
    PYTHON="$candidate"
    break
  fi
done
if [ -z "$PYTHON" ]; then
  echo "error: Python 3.9+ is required (python3 or python on PATH); nothing installed" >&2
  exit 1
fi
