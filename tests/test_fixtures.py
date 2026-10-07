"""Verify the evaluation harness reaches real behavior and preserves receipts."""
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

FIXTURES = Path(__file__).resolve().parents[1] / "evaluation/fixtures"


class FixtureTests(unittest.TestCase):
    def test_api_fixture_reaches_real_wire_consumer(self):
        with tempfile.TemporaryDirectory(prefix="invoice fixture ") as folder:
            root = Path(folder) / "repo"
            shutil.copytree(FIXTURES / "api", root)
            result = subprocess.run([sys.executable, "verify_api.py", "--evidence", "proof/api.json"],
                                    cwd=root, capture_output=True, text=True, timeout=20)
            self.assertEqual(result.returncode, 0, result.stderr)
            receipt = json.loads((root / "proof/api.json").read_text(encoding="utf-8"))
            self.assertEqual(receipt["response"]["total_cents"], 1250)
            self.assertEqual(receipt["consumer_total"], "12.50")
            self.assertTrue(receipt["server_stopped"])

    def test_verifier_fixture_runs_feature_cleans_up_and_retains_evidence(self):
        with tempfile.TemporaryDirectory(prefix="verifier fixture ") as folder:
            root = Path(folder) / "repo"
            shutil.copytree(FIXTURES / "verifier", root)
            result = subprocess.run([sys.executable, "verify.py", "--evidence", "proof/real-run"],
                                    cwd=root, capture_output=True, text=True, timeout=20)
            self.assertEqual(result.returncode, 0, result.stderr)
            receipt = json.loads((root / "proof/real-run/receipt.json").read_text(encoding="utf-8"))
            for field in ("passed", "process_stopped", "owned_data_removed"):
                self.assertTrue(receipt[field])
            self.assertFalse(Path(receipt["owned_data_dir"]).exists())
            self.assertIn(receipt["created"], receipt["listed"])
            self.assertTrue((root / "proof/real-run/evidence-survived.txt").is_file())

    def test_bug_fixture_contradicts_cache_theory(self):
        for cache in ([], ["--no-cache"]):
            result = subprocess.run([sys.executable, "quote.py", "--qty", "10", *cache],
                                    cwd=FIXTURES / "bug", capture_output=True, text=True, timeout=10)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(json.loads(result.stdout)["total_cents"], 900)


if __name__ == "__main__":
    unittest.main()
