"""Scheduled export reader. It consumes JSON, not a Python function call."""
import json
from pathlib import Path
import sys


def read_total(payload):
    cents = payload["total_cents"]
    if type(cents) is not int:
        raise TypeError("total_cents must remain integer cents")
    return f"{cents / 100:.2f}"


if __name__ == "__main__":
    print(read_total(json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))))
