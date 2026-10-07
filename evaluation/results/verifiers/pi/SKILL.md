---
name: verify-project
description: Verify the local task API's create-and-list-task behavior using the repository's standard-library Python end-to-end harness. Use for repeatable local API checks with durable evidence and scoped cleanup.
---

# Verify the local task API

Status: validated (one feature run passed; not application-wide acceptance).
Scope: revision `82370cc`; working tree clean before this skill/evidence were created; Windows shell (commands below use Python and are shell-neutral); Python 3.13.13. Project requires Python 3.9+ and Python standard library only. No credentials or external services.
Executed: create-and-list-task using `python verify.py --evidence artifacts/verification/create-and-list-task`; see [receipt](../../../artifacts/verification/create-and-list-task/receipt.json).

## Feature map

| Path | Entry point | Assertion | Recipe | State |
| --- | --- | --- | --- | --- |
| Create and list task | `POST /tasks`, then `GET /tasks` on harness-launched local API | POST returns 201 and created task; list and persisted JSON contain exact task | [API recipe](references/create-and-list-task.md) | Executed |

## Launch

From repository root, run `python verify.py --evidence artifacts/verification/<run-id>`. Python 3.9+ is required. The harness starts `taskapp.py` on an ephemeral loopback port with a uniquely owned temporary JSON data directory; it reads the startup URL as readiness, then checks `/health` with a 5-second timeout. It owns and terminates only that child process. No manual server or configuration is needed.

## Doctor

- `python --version`: confirm Python 3.9+; command-not-found/version failure means runtime missing or unsupported.
- `python -c "import json, pathlib, subprocess, tempfile, urllib.request"`: confirm standard-library prerequisites.
- From repository root, `python -c "from pathlib import Path; print(Path('verify.py').is_file(), Path('taskapp.py').is_file())"`: both must print true; otherwise wrong working directory or incomplete checkout.
- Run the harness command above. Startup/readiness failures are captured in `server.stderr.txt`; a port is selected ephemerally, avoiding a fixed-port conflict. `/health` only establishes reachability, not feature behavior; use the Drive assertions.
- No authentication/configuration is used. Do not investigate by reading unrelated credentials or changing user configuration.

## Drive

Use the real create-and-list API flow in [references/create-and-list-task.md](references/create-and-list-task.md). The harness runs this path end to end and validates the create response, list response, and backing JSON.

## Evidence

The evidence directory is outside the harness's temporary data directory. `receipt.json` records command, UTC timestamps, Python version, URL, PID, unique task input, POST status, create/list observations, result, and cleanup flags. `server.stderr.txt` records server errors; `evidence-survived.txt` confirms evidence was reopened/written after cleanup. Preserve failed-run evidence too. Do not put secrets in artifacts. To inspect: `python -c "import json; print(json.dumps(json.load(open('artifacts/verification/<run-id>/receipt.json')), indent=2))"`.

## Cleanup

The existing harness terminates only its launched server and removes only its `TemporaryDirectory` JSON data. It verifies process termination and temporary-directory removal, then reopens the receipt and writes the survival marker. Confirm `process_stopped` and `owned_data_removed` are true and the receipt and marker remain readable. Do not stop unrelated processes or delete evidence.
