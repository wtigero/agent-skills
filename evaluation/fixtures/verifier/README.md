# Local task API

Python 3.9+ standard library only. This project has an existing real API harness:

```bash
python verify.py --evidence artifacts/verification/my-run
```

It starts taskapp.py on a local ephemeral port with owned temporary JSON data,
checks health, creates a task, lists it and checks persistence, saves a receipt
and server stderr, stops its process and removes its temporary data. Evidence
is written outside the temporary directory and reopened after cleanup.

To launch manually: `python taskapp.py --data <owned-temp-path>/tasks.json --port 0`.
It prints the URL on stdout. GET `/health`, POST `/tasks` with JSON `id` and
`title`, and GET `/tasks` are the available routes. Stop only your own process.
No external service or login is required.
