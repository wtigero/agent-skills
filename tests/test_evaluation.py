"""Safety checks for opt-in evaluation setup; no provider or network calls."""

import base64
import importlib.util
import json
import os
import signal
import subprocess
import sys
from pathlib import Path
import tempfile
import time
import unittest
from unittest.mock import patch
from types import SimpleNamespace

SPEC = importlib.util.spec_from_file_location("evaluation_runner", Path(__file__).resolve().parents[1] / "evaluation/run.py")
RUNNER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(RUNNER)


class EvaluationSetupTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix="agent evaluation ")
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.original = self.root / "original"
        self.codex = self.original / ".codex"
        self.codex.mkdir(parents=True)
        self.env = patch.dict(os.environ, {"CODEX_HOME": str(self.codex)})
        self.env.start()
        self.addCleanup(self.env.stop)

    def credential(self, expires):
        claims = {"exp": expires, "https://api.openai.com/auth": {"chatgpt_account_id": "fixture-account"}}
        payload = base64.urlsafe_b64encode(json.dumps(claims).encode()).decode().rstrip("=")
        token = "fixture." + payload + ".signature"
        raw = json.dumps({"auth_mode": "chatgpt", "tokens": {"access_token": token, "refresh_token": "do-not-copy-refresh"}})
        (self.codex / "auth.json").write_text(raw)
        return token, raw

    def test_native_providers_reuse_access_without_persisting_credentials(self):
        token, raw = self.credential(time.time() + 3600)
        for runtime in ("pi", "opencode"):
            with self.subTest(runtime=runtime):
                home = self.root / runtime
                home.mkdir()
                env, redact = RUNNER.environment(runtime, home, self.original, True, 360)
                self.assertIn(token, redact)
                if runtime == "pi":
                    self.assertEqual(env["AGENT_SKILLS_OPENAI_ACCESS_TOKEN"], token)
                    config = json.loads((home / ".pi/agent/models.json").read_text())
                    self.assertEqual(config["providers"]["openai-codex"]["apiKey"], "$AGENT_SKILLS_OPENAI_ACCESS_TOKEN")
                else:
                    auth = json.loads(env["OPENCODE_AUTH_CONTENT"])["openai"]
                    self.assertEqual(auth["access"], token)
                    self.assertEqual(auth["refresh"], "")
                    self.assertEqual(auth["accountId"], "fixture-account")
                for file in home.rglob("*"):
                    if file.is_file():
                        self.assertNotIn(token, file.read_text())
                        self.assertNotIn("do-not-copy-refresh", file.read_text())
        self.assertEqual((self.codex / "auth.json").read_text(), raw)

    def test_expired_or_near_expiry_blocks_before_creating_auth_config(self):
        for expiry in (time.time() - 10, time.time() + 400, "invalid"):
            self.credential(expiry)
            home = self.root / "blocked"
            with self.assertRaisesRegex(RuntimeError, "expires too soon"):
                RUNNER.environment("pi", home, self.original, True, 360)
            self.assertFalse(home.exists())

    def test_unrelated_runtime_cannot_receive_subscription_access(self):
        self.credential(time.time() + 3600)
        with self.assertRaisesRegex(RuntimeError, "only for Pi/OpenCode"):
            RUNNER.environment("claude", self.root / "blocked", self.original, True)

    def test_opencode_usage_retains_cache_and_reasoning_counters(self):
        events = [json.dumps({"type": "step_finish", "part": {"tokens": {
            "input": 10, "output": 4, "reasoning": 2, "cache": {"read": 7, "write": 3}}}})] * 2
        usage = RUNNER.parse_metrics("opencode", "\n".join(events))["usage"]
        self.assertEqual(usage, {"input": 20, "output": 8, "reasoning": 4, "cache_read": 14, "cache_write": 6})

    def test_codex_full_access_requires_explicit_selection(self):
        config = {"command": ["codex"], "model": "fixture-model", "effort": "medium"}
        default = RUNNER.command("codex", config, self.root, self.root / "prompt.txt")
        self.assertEqual(default[default.index("--sandbox") + 1], "workspace-write")
        explicit = RUNNER.command("codex", config, self.root, self.root / "prompt.txt", "danger-full-access")
        self.assertEqual(explicit[explicit.index("--sandbox") + 1], "danger-full-access")
        self.assertNotIn('windows.sandbox="elevated"', explicit)
        self.assertNotIn("--dangerously-bypass-approvals-and-sandbox", explicit)
        with self.assertRaisesRegex(ValueError, "unsupported Codex"):
            RUNNER.command("codex", config, self.root, self.root / "prompt.txt", "unknown")

    def test_invalid_baseline_leaves_blocked_record_and_preserves_attempt(self):
        config = self.root / "config.json"
        config.write_text(json.dumps({"codex": {"command": ["never-execute-provider"],
                         "provider": "fixture", "model": "fixture", "effort": "medium"}}))
        args = SimpleNamespace(output=str(self.root / "output"), config=str(config), runtime="codex",
                               scenario="small", variant="baseline", baseline="missing-fixture-ref")
        with patch.object(RUNNER, "git", side_effect=subprocess.CalledProcessError(128, "git")), \
                patch.object(RUNNER, "call_session") as session:
            self.assertEqual(RUNNER.run(args), 1)
            session.assert_not_called()
        record_path = Path(args.output) / "results/codex/small/baseline/run.json"
        original = record_path.read_bytes()
        record = json.loads(original)
        self.assertEqual(record["status"], "blocked")
        self.assertEqual(record["baseline_ref"], args.baseline)
        self.assertIsNone(record["baseline_revision"])
        self.assertIn("128", record["blocker"])
        with self.assertRaisesRegex(RuntimeError, "preserve it"):
            RUNNER.run(args)
        self.assertEqual(record_path.read_bytes(), original)

    def test_invalid_config_leaves_blocked_record(self):
        config = self.root / "config.json"
        args = SimpleNamespace(output=str(self.root / "output"), config=str(config), runtime="codex",
                               scenario="small", variant="candidate", baseline="HEAD")
        config.write_text('{}')
        with patch.object(RUNNER, "call_session") as session:
            self.assertEqual(RUNNER.run(args), 1)
            session.assert_not_called()
        record = json.loads((Path(args.output) / "results/codex/small/candidate/run.json").read_text())
        self.assertEqual(record["status"], "blocked")
        self.assertIn("codex", record["blocker"])

    @unittest.skipIf(os.name == "nt", "POSIX process-group termination")
    def test_timeout_forces_owned_group_and_retains_partial_output(self):
        real_popen = subprocess.Popen
        owned = []
        ready = self.root / "child-ready"
        def start(*args, **kwargs):
            process = real_popen(*args, **kwargs)
            owned.append(process)
            deadline = time.monotonic() + 5
            while not ready.exists() and process.poll() is None and time.monotonic() < deadline:
                time.sleep(.01)
            return process
        code = ('import os,signal,time; from pathlib import Path; '
                'signal.signal(signal.SIGTERM, signal.SIG_IGN); '
                'print("ready-output",flush=True); '
                f'Path({str(ready)!r}).write_text("ready"); time.sleep(60)')
        try:
            with patch.object(RUNNER.subprocess, "Popen", side_effect=start):
                stdout, stderr, exit_code = RUNNER.call_session(
                    [sys.executable, "-c", code], self.root, os.environ.copy(), None, .1, terminate_grace=.1)
            self.assertIsNone(exit_code)
            self.assertIn("ready-output", stdout)
            self.assertIn("partial output retained", stderr)
            self.assertIsNotNone(owned[0].poll())
            self.assertEqual(owned[0].returncode, -signal.SIGKILL)
        finally:
            for process in owned:
                if process.poll() is None:
                    if os.getpgid(process.pid) == process.pid:
                        os.killpg(process.pid, signal.SIGKILL)
                    else:
                        process.kill()
                process.communicate(timeout=5)

    @unittest.skipUnless(sys.platform == "linux", "Linux descendant liveness via /proc")
    def test_timeout_stops_descendant_after_parent_closes_pipes(self):
        real_popen = subprocess.Popen
        owned = []
        ready = self.root / "descendant-ready"
        child_code = ('import os,signal,time; from pathlib import Path; '
                      'signal.signal(signal.SIGTERM,signal.SIG_IGN); '
                      f'Path({str(ready)!r}).write_text(str(os.getpid())); time.sleep(60)')
        parent_code = ('import subprocess,sys,time; from pathlib import Path; '
                       f'subprocess.Popen([sys.executable,"-c",{child_code!r}], '
                       'stdin=subprocess.DEVNULL,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL); '
                       f'ready=Path({str(ready)!r});\n'
                       'while not ready.exists(): time.sleep(.01)\n'
                       'print("parent-ready",flush=True); time.sleep(60)')
        def start(*args, **kwargs):
            process = real_popen(*args, **kwargs)
            owned.append(process)
            deadline = time.monotonic() + 5
            while not ready.exists() and process.poll() is None and time.monotonic() < deadline:
                time.sleep(.01)
            return process
        def active(pid):
            try:
                state = Path(f"/proc/{pid}/stat").read_text().split(") ", 1)[1].split()[0]
                return state != "Z"  # A stopped orphan may await its system reaper.
            except FileNotFoundError:
                return False
        try:
            with patch.object(RUNNER.subprocess, "Popen", side_effect=start):
                stdout, stderr, exit_code = RUNNER.call_session(
                    [sys.executable, "-c", parent_code], self.root, os.environ.copy(), None, .1, terminate_grace=.1)
            self.assertTrue(ready.exists())
            pid = int(ready.read_text())
            deadline = time.monotonic() + 2
            while active(pid) and time.monotonic() < deadline:
                time.sleep(.01)
            self.assertFalse(active(pid), "TERM-ignoring descendant survived after pipe EOF")
            self.assertIsNone(exit_code)
            self.assertIn("parent-ready", stdout)
            self.assertIn("partial output retained", stderr)
        finally:
            # Only groups created with start_new_session by this fixture.
            for process in owned:
                descendant_owned = (ready.exists() and active(int(ready.read_text()))
                                    and os.getpgid(int(ready.read_text())) == process.pid)
                if process.poll() is None or descendant_owned:
                    try:
                        os.killpg(process.pid, signal.SIGKILL)
                    except ProcessLookupError:
                        pass
                process.communicate(timeout=5)


if __name__ == "__main__":
    unittest.main()
