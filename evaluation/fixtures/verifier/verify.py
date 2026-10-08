"""Existing end-to-end harness: launch -> real HTTP feature -> evidence -> cleanup."""
import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
import subprocess
import sys
import tempfile
from urllib.request import Request, urlopen
from uuid import uuid4


def main(evidence):
    evidence.mkdir(parents=True, exist_ok=True)
    record = {"started_at": datetime.now(timezone.utc).isoformat(), "command": sys.argv,
              "python": sys.version.split()[0], "feature": "create-and-list-task", "passed": False}
    process = None
    try:
        with tempfile.TemporaryDirectory(prefix="verify-task-") as folder:
            data = Path(folder) / "tasks.json"
            record["owned_data_dir"] = folder
            with (evidence / "server.stderr.txt").open("w", encoding="utf-8") as errors:
                process = subprocess.Popen([sys.executable, "taskapp.py", "--data", str(data), "--port", "0"],
                                           stdout=subprocess.PIPE, stderr=errors, text=True)
                try:
                    startup = json.loads(process.stdout.readline())
                    record.update(startup)
                    record["pid"] = process.pid
                    url = startup["url"]
                    with urlopen(url + "/health", timeout=5) as response:
                        assert json.load(response) == {"ok": True}
                    task = {"id": "verify-" + uuid4().hex, "title": "write a verifier"}
                    request = Request(url + "/tasks", data=json.dumps(task).encode(),
                                      headers={"Content-Type": "application/json"}, method="POST")
                    with urlopen(request, timeout=5) as response:
                        record["post_status"] = response.status
                        record["created"] = json.load(response)
                    with urlopen(url + "/tasks", timeout=5) as response:
                        record["listed"] = json.load(response)
                    assert record["post_status"] == 201 and record["created"] == task
                    assert task in record["listed"]
                    assert task in json.loads(data.read_text(encoding="utf-8"))
                    record["passed"] = True
                finally:
                    process.terminate()
                    process.wait(timeout=5)
                    record["process_stopped"] = process.poll() is not None
        record["owned_data_removed"] = not Path(record["owned_data_dir"]).exists()
    finally:
        record["finished_at"] = datetime.now(timezone.utc).isoformat()
        receipt = evidence / "receipt.json"
        receipt.write_text(json.dumps(record, indent=2), encoding="utf-8")
        assert json.loads(receipt.read_text(encoding="utf-8")) == record
        (evidence / "evidence-survived.txt").write_text("Receipt readable after process/data cleanup.\n", encoding="utf-8")
    print(json.dumps(record))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--evidence", type=Path, required=True)
    args = parser.parse_args()
    main(args.evidence)
