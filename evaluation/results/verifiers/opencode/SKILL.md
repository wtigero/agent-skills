---
name: verify-project
description: Verify this repository's local task API, especially creating and listing a task, with its standard-library Python end-to-end harness and durable evidence.
---

# Verify the local task API

Status: validated for the `create-and-list-task` path.
Scope: revision `77873d2` (working tree clean before this guide and evidence); Windows PowerShell 5.1, Python 3.9+; standard library only.
Executed: create-and-list-task via `python verify.py --evidence artifacts/verification/create-and-list-task`; see [evidence](../../../artifacts/verification/create-and-list-task/receipt.json).

## Feature map

| Path | Entry point | Assertion | Recipe | State |
| --- | --- | --- | --- | --- |
| Create and list a task | `POST /tasks`, then `GET /tasks` | POST returns 201 and the submitted task; list includes the task and persisted JSON contains it | [create-and-list](references/create-and-list.md) | executed |

## Launch

From the repository root, run `python verify.py --evidence artifacts/verification/<run-id>` in PowerShell. Use a new run-id directory for each run. Python 3.9+ is required; there are no external services, credentials, or dependencies. The harness starts `taskapp.py` on `127.0.0.1` with an ephemeral port and a uniquely owned temporary JSON data directory. Readiness is the startup URL followed by a successful `/health` response; HTTP calls have a 5-second timeout. The harness owns and stops its child process.

## Doctor

- `python --version`: command failure or a version below 3.9 means Python is missing/too old or unavailable on PATH.
- `python verify.py --help`: confirms the existing harness accepts the evidence argument; this is not a feature check.
- The harness's `/health` check distinguishes a reachable started app from startup failure. A bind/startup error or absent URL points to a local runtime/port/environment problem. Port `0` requests an ephemeral port, avoiding a fixed-port collision.
- A successful health response alone does not verify task behavior; the Drive assertions do.

## Drive

Read and follow [the create-and-list recipe](references/create-and-list.md) against the harness-launched instance. Preserve its assertions and bounded request timeouts.

## Evidence

The harness writes durable files outside its temporary data directory: `receipt.json`, `server.stderr.txt`, and `evidence-survived.txt`. The receipt records the command, Python version, UTC timestamps, URL, child PID, submitted task, HTTP status, list response, and cleanup outcomes. It contains generated non-secret test data only. Use a unique evidence directory per run and inspect the receipt and stderr there.

## Cleanup

The harness terminates and waits for only the child process it started, and its temporary-directory context removes only its owned JSON data. It records both results in the receipt, then reopens the receipt and writes a survival marker after cleanup. Confirm `process_stopped` and `owned_data_removed` are true, and reopen `receipt.json` and `evidence-survived.txt` after the command exits.
