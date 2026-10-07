"""Existing wire/consumer check. No mocks or third-party dependencies."""
import argparse
import json
from pathlib import Path
import subprocess
import sys
from urllib.request import urlopen
from reporting.month_end import read_total


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--evidence", default="evidence/api.json")
    args = parser.parse_args()
    server = subprocess.Popen([sys.executable, "api.py"], stdout=subprocess.PIPE,
                              stderr=subprocess.DEVNULL, text=True)
    record = {}
    try:
        port = int(server.stdout.readline())
        with urlopen(f"http://127.0.0.1:{port}/invoice", timeout=5) as response:
            payload = json.load(response)
        assert read_total(payload) == "12.50", payload
        record = {"response": payload, "consumer": "reporting/month_end.py", "consumer_total": read_total(payload)}
        if "total" in payload:
            assert payload["total"] == 12.5, payload
        print(json.dumps(record))
    finally:
        server.terminate()
        server.wait(timeout=5)
        record["server_stopped"] = server.poll() is not None
        output = Path(args.evidence)
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(json.dumps(record, indent=2), encoding="utf-8")
