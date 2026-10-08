# Create and list a task

Run from the repository root in PowerShell:

```powershell
powershell -NoProfile -File .agents/skills/verify-project/references/run.ps1
```

The existing `verify.py` creates an owned server on `127.0.0.1` and a unique task with `id` beginning `verify-` and `title` `write a verifier`. It sends:

1. `GET /health`, expecting JSON `{"ok": true}`.
2. `POST /tasks` with `Content-Type: application/json` and the task JSON, expecting HTTP 201 and the same JSON body.
3. `GET /tasks`, expecting an array containing that task.
4. A read of the owned `tasks.json`, expecting that task to persist there.

Each HTTP request has a five second timeout. The harness records the created and listed responses in `receipt.json`; the runner records stdout, stderr, exit code, revision, environment, and post-cleanup checks. The script prints the evidence path. A nonzero exit, missing receipt, failed assertion, timeout, or incomplete cleanup is a failed run. Inspect its files and do not claim the feature passed.
