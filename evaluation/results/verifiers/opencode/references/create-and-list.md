# Create and list a task

Run from the repository root in PowerShell. This recipe uses the project's
existing end-to-end harness, which drives the real HTTP API; no browser or
additional dependency is needed.

1. Choose a new evidence directory, for example
   `artifacts/verification/create-and-list-task`.
2. Run:

   ```powershell
   python verify.py --evidence artifacts/verification/create-and-list-task
   ```

3. Expect a JSON result on stdout. Check `passed` is true, `post_status` is
   `201`, `created` matches the generated task, and `listed` contains it. The
   harness also checks that the task is in the on-disk JSON data before cleanup.
   HTTP requests use a 5-second timeout.
4. Check `process_stopped` and `owned_data_removed` are true. Open
   `artifacts/verification/create-and-list-task/receipt.json` and
   `evidence-survived.txt` after the run; the receipt must be valid JSON and
   the marker must say the receipt was readable after process/data cleanup.
   `server.stderr.txt` captures server diagnostics.

The harness launches `taskapp.py` on loopback port 0 and terminates only that
child. It uses a fresh temporary directory for data, deleting that directory
afterward; evidence remains in the chosen durable path. If startup, an HTTP
assertion, process shutdown, or evidence read-back fails, retain the evidence
and report the observed failure rather than treating the run as passed.
