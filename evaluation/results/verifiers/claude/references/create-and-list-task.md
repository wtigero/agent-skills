# Recipe: create-and-list-task

Run from the repository root. Pick `RUN=artifacts/verification/<name>` (must be new or reusable; files are overwritten).

## Run
```bash
RUN=artifacts/verification/cold-$(date +%Y%m%d-%H%M%S)
mkdir -p "$RUN"
git rev-parse --short HEAD > "$RUN/revision.txt"; git status --short >> "$RUN/revision.txt"
timeout 60 python verify.py --evidence "$RUN" > "$RUN/run.txt" 2> "$RUN/run.stderr.txt"; echo "exit=$?" >> "$RUN/run.txt"
```
(PowerShell: use `python verify.py --evidence $RUN` and redirect output similarly; `timeout` is not needed if the tool has its own limit.)

## Assertions (all must hold)
Checked inside verify.py: health `{"ok": true}`; POST /tasks `{"id": "verify-<uuid>", "title": "write a verifier"}` returns 201 and echoes the task; GET /tasks contains it; the data file contains it.
Check afterwards from the receipt:
```bash
python -I - "$RUN" <<'PY'
import json, sys, os
from pathlib import Path
run = Path(sys.argv[1]); r = json.loads((run/"receipt.json").read_text(encoding="utf-8"))
assert r["passed"] is True and r["post_status"] == 201 and r["created"] in r["listed"]
assert r["process_stopped"] is True and r["owned_data_removed"] is True
assert not os.path.exists(r["owned_data_dir"]), "temp dir remains"
for f in ("receipt.json", "server.stderr.txt", "evidence-survived.txt", "run.txt"):
    assert (run/f).read_text(encoding="utf-8") is not None, f
print("OK cleanup+evidence verified, pid", r["pid"])
PY
```
Process-gone check: Windows `tasklist /FI "PID eq <pid>"` / POSIX `kill -0 <pid>` should show no such process (pid may be reused; the receipt's `process_stopped` is the primary signal).

## Failure interpretation
- Exit non-zero with `passed: false`: read `receipt.json` and `server.stderr.txt`; AssertionError means a contract change (status/body/persistence).
- No receipt: harness crashed before the evidence dir was created; check run.stderr.txt and cwd.
- `process_stopped` false or temp dir present: cleanup bug; report it, remove only the dir named in `owned_data_dir`.

Limit: one happy-path task; no duplicate ids, validation, concurrency or error-route coverage.
