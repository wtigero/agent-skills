# Create and list a task (API)

Run from the repository root on Python 3.9+. No credentials or external services are required. The existing harness owns the server process and temporary JSON store; do not start an additional server.

## Run

```bash
python verify.py --evidence artifacts/verification/<run-id>
```

Choose a fresh, descriptive `<run-id>` for each run. The harness starts `taskapp.py --data <owned-temp>/tasks.json --port 0`, reads its JSON startup URL, and requests `GET /health` (5-second timeout; expected `200` and `{"ok":true}`). It then submits a unique JSON task to `POST /tasks` with `Content-Type: application/json`, expected status `201`, and reads `GET /tasks`. The task shape is `{"id":"verify-<unique>","title":"write a verifier"}`.

Assertions: POST response exactly equals the submitted task; list includes that task; backing JSON includes it. The command exits successfully only after assertions. This exercises the real local HTTP handlers and persistence read-back, not merely health. Nonzero exit or missing assertions means the feature did not pass; retain the run's evidence and inspect `server.stderr.txt`.

## Evidence and cleanup

The harness prints the observed result and saves `receipt.json`, `server.stderr.txt`, and `evidence-survived.txt` beneath `artifacts/verification/<run-id>`. Receipt includes actual command, timestamps, runtime, URL, PID, task, HTTP status, create/list results, assertion result, and cleanup checks. After the command, inspect the receipt and require `passed`, `process_stopped`, and `owned_data_removed` all true. Confirm the receipt and survival marker are readable. The harness removes its owned temporary store and terminates its own server; it leaves durable evidence in place. It does not clean up arbitrary files or processes.
