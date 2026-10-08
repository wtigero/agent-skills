"""Safety checks for opt-in evaluation setup; no provider or network calls."""

import base64
import importlib.util
import json
import os
from pathlib import Path
import tempfile
import time
import unittest
from unittest.mock import patch

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


if __name__ == "__main__":
    unittest.main()
