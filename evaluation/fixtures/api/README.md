# Invoice API

Python standard library only. Start with `python api.py --port 0`; it prints its
chosen local port. GET `/invoice` returns the invoice used by the UI. The
existing integration harness is `python verify_api.py --evidence evidence/api.json`.
It launches the real server, checks the wire response, and stops its own process.
