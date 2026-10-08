---
name: verify-project
description: Verify the local task API create-and-list-task path with the repository's Python end-to-end harness, durable evidence, and cleanup checks.
---

# Verify the local task API

Status: validated on Windows, PowerShell, Python 3.13.13, at revision `1eb39e1` with a clean starting tree. The run evidence below records the actual working tree and result. This guide requires Python 3.9+ and PowerShell on Windows; it uses only Python's standard library. No credentials or external service are needed.

Executed: create and list a task through the real local HTTP API. See the latest run under `artifacts/verification/`; each run has its own directory.

## Feature map

| User path | Entry point | Assertion | Recipe | State |
| --- | --- | --- | --- | --- |
| Create and list a task | `POST /tasks`, then `GET /tasks` on the owned local server | Create returns 201 and the same task; list and JSON data file contain it | [Create and list](references/create-and-list.md) | Executed |

## Launch

From the repository root, run `powershell -NoProfile -File .agents/skills/verify-project/references/run.ps1` (or `pwsh -NoProfile -File ...`). The script checks Python, creates `artifacts/verification/<UTC timestamp>-<ID>/`, and invokes the existing `python verify.py --evidence <run directory>` with the repository as working directory. `verify.py` owns a temporary `verify-task-*` data directory and starts `taskapp.py --data <that directory>/tasks.json --port 0`. The app prints its ephemeral loopback URL and the harness checks `GET /health` with a five second request timeout. The runner limits the harness to 30 seconds and records its process ID. Keep the resulting run directory; it is the durable evidence.

## Doctor

Run from the repository root:

```powershell
python --version
python -m py_compile taskapp.py verify.py
git rev-parse --short HEAD
```

Python must be 3.9 or newer. `py_compile` checks syntax, not behavior; its `__pycache__` files can be removed after the check. If Python is absent or syntax fails, fix that before running. The harness uses the current `taskapp.py` source directly, so stale builds do not apply. It binds port `0`, avoiding a fixed-port conflict. No auth or configuration file is required. A failed `/health` or a startup timeout means the local instance did not become reachable; a successful `/health` alone does not prove the task feature.

## Drive

Read [the create-and-list recipe](references/create-and-list.md). Run `references/run.ps1`; inspect `receipt.json`, `runner.json`, `harness.stdout.txt`, `harness.stderr.txt`, and `server.stderr.txt` in the new evidence directory. The recipe specifies the requests and required assertions.

## Evidence

The run directory is outside the temporary data directory. `receipt.json` records input, HTTP results, assertions, Python version, URL, server PID, UTC timestamps, and cleanup fields. `runner.json` records the exact command and working directory, revision and initial working tree, OS/shell, UTC timestamps, harness PID, exit code, timeout, and post-cleanup checks. The stdout/stderr files preserve command output. Treat a passing feature claim as valid only when `receipt.passed`, `receipt.process_stopped`, `receipt.owned_data_removed`, and `runner.evidence_readable` are true, and `runner.exit_code` is 0. Inspect failed runs as well; do not convert a health pass into a feature pass.

## Cleanup

The harness terminates only its own `taskapp.py` process and deletes only its owned `verify-task-*` temporary directory. The runner kills its owned harness process tree only if the 30 second timeout expires. It then verifies the server PID is gone, the temporary directory is gone, and the receipt remains readable. Keep the run directory. If cleanup flags are false, use the recorded PIDs and owned path to finish cleanup before retrying; do not remove unrelated data or processes.
