I’ll audit the supplied source and evidence statically, focusing on installer safety, evaluation failure paths, and qualification claims. I’ll keep code-supported findings separate from checks that remain unexecuted.


The source shows an order-dependent conflict check: installing shared skills and then Claude skills can create duplicates in OpenCode’s declared search paths. The POSIX timeout path also lacks forced termination if SIGTERM fails. The qualification report clearly preserves the default-sandbox blocks and identifies its acceptance verdicts as implementing-agent assessments.


Three actionable findings are supported by the supplied code. They concern newly added code; the reproductions below are **unexecuted**, with expected results distinguished from observations.

1. **`blocking` · `supported` — POSIX timeout cleanup can leave the evaluator-owned process running and lose partial output.**  
   **Evidence:** `evaluation/run.py:244` sends only `SIGTERM`; line 245 waits another 15 seconds without escalation. If the child ignores SIGTERM, that second `communicate()` raises `TimeoutExpired`. The outer handler at line 340 records the exception, but never reaches the stream-saving statements at lines 330–331 and never kills the remaining process.

   **Trigger and consequence:** A CLI or subprocess that does not terminate on SIGTERM outlives the failed evaluation, while its partial transcript is absent from the result directory. This contradicts the timeout guarantee in `evaluation/README.md:99`.

   **Recommendation:** Add bounded forced termination of the owned process group after graceful termination fails, then collect output. This sacrifices graceful shutdown after the grace period but fulfills the stated ownership and evidence-retention contract.

   Small POSIX reproducer, run from the checkout; it cleans up its own child:

   ```bash
   python -B - <<'PY'
   import os, runpy, signal, subprocess, sys
   from unittest.mock import patch

   runner = runpy.run_path("evaluation/run.py")
   original_popen = subprocess.Popen
   owned = []

   def capture(*args, **kwargs):
       process = original_popen(*args, **kwargs)
       owned.append(process)
       return process

   command = [
       sys.executable, "-B", "-u", "-c",
       "import signal,time; "
       "signal.signal(signal.SIGTERM, signal.SIG_IGN); "
       "print('partial output', flush=True); time.sleep(60)"
   ]
   try:
       with patch.object(subprocess, "Popen", capture):
           runner["call_session"](command, ".", {}, None, 2)
   except subprocess.TimeoutExpired as exc:
       print("second timeout:", exc.timeout)
       print("owned process still alive:", owned[0].poll() is None)
   finally:
       if owned and owned[0].poll() is None:
           os.killpg(owned[0].pid, signal.SIGKILL)
           owned[0].communicate(timeout=5)
   PY
   ```

   **Expected, not observed here:** second timeout is `15`; owned process remains alive before the reproducer’s cleanup.

2. **`consider` · `supported` — Shared/Claude duplicate prevention depends on installation order.**  
   **Evidence:** `scripts/skills.py:132` declares that OpenCode searches both `.agents/skills` and `.claude/skills`. However, line 142 checks the union of consumers only for `runtime == "shared"`; a Claude installation checks only Claude roots from line 130.

   **Trigger and consequence:** Install shared skills, then Claude skills into the same HOME. Both installations succeed, creating two copies of every published name in OpenCode’s declared search paths. Repeating the shared installation then fails because it detects the Claude copies. Reversing the original installation order already produces a conflict. This also contradicts the intended conflict behavior noted in `tests/test_bundle.py:113`.

   **Recommendation:** Consider checking overlapping consumers when installing into `.claude/skills`, or explicitly document this exception. Broader checking protects OpenCode users, though it also restricts installations for users who never run OpenCode.

   Reproducer using the existing isolated, temporary-HOME fixture:

   ```bash
   python -B - <<'PY'
   import runpy

   case = runpy.run_path("tests/test_bundle.py")["InstallerTests"]()
   case.setUp()
   try:
       for runtime in ("agent", "claude"):
           result = case.run_install(runtime, "--copy")
           print(runtime, result.returncode, result.stderr)
           assert result.returncode == 0
       result = case.run_install("agent", "--copy")
       print("repeat shared:", result.returncode, result.stderr)
       assert result.returncode != 0
   finally:
       case.tearDown()
   PY
   ```

   **Expected, not observed here:** both initial installs succeed; the shared repeat reports duplicate-name conflicts.

3. **`consider` · `supported` — Revision-resolution failures reserve a result directory without recording the failure.**  
   **Evidence:** `evaluation/run.py:271` creates `result_dir`; lines 274–275 resolve revisions before entering the `try` at line 280. A failed Git invocation therefore bypasses the blocker handler and `run.json` write at line 344. The existence guard at lines 269–270 subsequently refuses that result path.

   **Trigger and consequence:** An invalid `--baseline` leaves an empty reserved result directory, no durable failure record, and a retry rejected as an existing result.

   **Recommendation:** Validate revisions before reserving the directory, or include revision resolution in the recorded failure path. The former keeps invalid-input retries simple; the latter better preserves setup-attempt evidence.

   Self-contained fault-injection check; no provider is invoked:

   ```bash
   python -B - <<'PY'
   import json, runpy, subprocess, tempfile
   from pathlib import Path
   from types import SimpleNamespace
   from unittest.mock import patch

   runner = runpy.run_path("tests/test_evaluation.py")["RUNNER"]
   with tempfile.TemporaryDirectory() as folder:
       root = Path(folder)
       config = root / "config.json"
       config.write_text(json.dumps({"codex": {
           "command": ["unused"], "provider": "fixture",
           "model": "fixture", "effort": "medium"
       }}), encoding="utf-8")
       args = SimpleNamespace(
           output=str(root / "output"), config=str(config),
           runtime="codex", scenario="small",
           variant="candidate", baseline="missing"
       )
       with patch.object(runner, "git", side_effect=
                         subprocess.CalledProcessError(
                             128, ["git", "rev-parse", "missing"])):
           try:
               runner.run(args)
           except subprocess.CalledProcessError:
               pass

       result = root / "output/results/codex/small/candidate"
       print("directory exists:", result.exists())
       print("run.json exists:", (result / "run.json").exists())
       try:
           runner.run(args)
       except RuntimeError as exc:
           print("retry:", exc)
   PY
   ```

   **Expected, not observed here:** directory exists, `run.json` does not, and retry reports “result already exists.”

A further **`consider` concern has an `unverified` runtime consequence**: `scripts/skills.py:157–158` treats `name: prove-it # local copy` as the literal name `prove-it # local copy`. Consequently, line 203 does not recognize it as a published-name collision when it resides in another folder. The parser behavior is source-supported; acceptance and interpretation of that commented frontmatter by the pinned runtimes were not verified. The smallest resolving check is to load such an aliased skill in the relevant runtime. If accepted as `prove-it`, handling comments or conservatively rejecting ambiguous headers would improve duplicate protection without necessarily adding a general YAML dependency.

The supplied qualification report distinguishes manual verdicts from runner statuses and preserves the earlier Codex blocks alongside the changed-version/full-access follow-up. I found no contradiction in the reported test counts or cohort arithmetic.

Material limits: this was a static packet audit, with no tools, executions, or external API checks. The packet omits baseline source contents, several changed files, and portions of the artifact exports, so complete committed-diff coverage and independent verification of all fingerprints, transcripts, provider persistence, and acceptance verdicts remain **unverified**. This review does not establish publication approval.