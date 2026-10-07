---
name: verify-project
description: Verify the local task API (taskapp.py) create-and-list-task path using the repo's existing verify.py harness. Use for local behavior checks, repros, and after changing taskapp.py or verify.py, with saved evidence and cleanup.
---

# Verify task API

Status: validated for create-and-list-task only (creator run, not a cold-session run)
Scope: revision b0be7a8, clean tree when run; Windows 11, PowerShell/Git Bash, Python 3.13.13. Stdlib only, no install, no network beyond 127.0.0.1, no credentials.
Executed: create-and-list-task, evidence in `artifacts/verification/cold-test/ (recipe-as-written run; earlier harness-only run in creator-run/)`.

## Feature map

| Path | Entry point | Assertion | Recipe | State |
| --- | --- | --- | --- | --- |
| Create and list task | `POST /tasks`, `GET /tasks` via `python verify.py` | POST returns 201 and echoes task; GET lists it; JSON file contains it | [recipe](references/create-and-list-task.md) | executed |
| Health | `GET /health` | `{"ok": true}` (only a readiness check, not a feature proof) | harness covers it | executed as readiness |
| Unknown route / malformed POST | 404 paths | not mapped | none | unrun |

## Launch

Working directory: repository root (verify.py spawns `taskapp.py` by relative path).
The harness launches `python taskapp.py --data <owned-temp>/tasks.json --port 0` itself, reads the URL from the first stdout line (JSON `{"url": ...}`), and records the pid. Do not start a server separately for this path. Manual launch (only for ad-hoc poking) is in README.md; stop only the process you started.

## Doctor

- `python --version` must be 3.9+ (else dependency problem).
- `python -c "import http.server, json"` succeeds (stdlib present).
- `ls taskapp.py verify.py` from the cwd (wrong directory gives a FileNotFoundError/startup JSON error).
- Port conflicts are not expected (port 0 = ephemeral). A hang on startup means taskapp.py died; read `server.stderr.txt` in the evidence dir.
- Health passing alone proves nothing about the feature.

## Drive

Follow [the recipe](references/create-and-list-task.md). Use a fresh evidence directory per run.

## Evidence

Directory `artifacts/verification/<run-name>/` (outside the temp dir): `receipt.json` (command, python, url, pid, POST status, created, listed, passed, process_stopped, owned_data_removed, timestamps), `server.stderr.txt`, `evidence-survived.txt`. Also save the harness stdout and exit code into `run.txt` (see recipe). A failed run still writes a receipt with `passed: false`; keep it. Contains no secrets. `artifacts/` is untracked; do not commit unless asked.

## Cleanup

The harness terminates its own server and deletes its own temp dir. Confirm independently with the recipe's check commands (pid gone, temp dir gone, evidence files readable). Never kill other python processes or delete other directories.
