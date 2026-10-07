# Qualification report

Status: in progress. Publishing is gated until the recorded checks and all four
runtime behavioral lanes have been reviewed. See [the evaluation protocol](../evaluation/README.md).

Baseline: `e003656917fbe06d00e23c82a2de3955f7aa66b6`.
Candidate: recorded in each run's `run.json`, with skill-directory fingerprints.

## Deterministic checks

Linux (Ubuntu/WSL, Python 3.12.3) and Windows (native Git Bash, Python 3.13) ran
the temporary-HOME bundle suite. Linux exercised real symlinks; Windows lacks
symlink privilege and exercised `--copy`, fake-link rejection and NTFS junction
protection. Exact final counts and retained evidence will be recorded below.

## Behavioral gates

| Runtime | Small | API/consumer | Contradictory bug | Council | Verifier + cold handoff | Gate |
| --- | --- | --- | --- | --- | --- | --- |
| Codex | pending | pending | pending | pending | pending | pending |
| Claude Code | pending | pending | pending | pending | pending | pending |
| Pi | pending | pending | pending | pending | pending | pending |
| OpenCode | pending | pending | pending | pending | pending | pending |

These are case-specific observations. CI/packaging does not imply runtime
behavior, UI coverage, application acceptance, deployment or publishing.
