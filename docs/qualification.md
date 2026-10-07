# Qualification report

**Delivery: ready for code review. Publication: BLOCKED.** Claude Code, Pi and
OpenCode passed the selected candidate cases. Native Windows Codex passed the
first four cases, but could not write the protected project skill target; its
verifier creation and fresh-session handoff remain blocked.

## Revision and evidence

Branch: `improve-portable-verification`.
Baseline: `e003656917fbe06d00e23c82a2de3955f7aa66b6`.
The initial implementation is `9a001276`; council's executable dispute check and
complete fallback packets were refined in `e992ae7` and `4151468`. Each trial
records its exact candidate revision, runner hash and designated skill hashes.
All selected candidate skill hashes match the final public skill bytes. Later
delivery changes cover the runner, its tests, documentation and evidence export.
The original `A:/hobby/agent-skills` checkout remains clean on `main`.

- [Selected runs and excluded-attempt ledger](../evaluation/results/runs.json):
  commands, revisions, versions, provider, requested/observed model, effort,
  timestamps, elapsed time, native usage, session IDs, verdicts and raw hashes.
- [Final responses and decision notes](../evaluation/results/evidence.md).
- [Review packets and investigation artifacts](../evaluation/results/artifacts.json).
- [Verifier receipts](../evaluation/results/verifier-receipts.json).
- [Deterministic test output](../evaluation/results/deterministic.txt).
- Captured generated guides:
  [Claude](../evaluation/results/verifiers/claude/SKILL.md),
  [Pi](../evaluation/results/verifiers/pi/SKILL.md),
  [OpenCode](../evaluation/results/verifiers/opencode/SKILL.md).

Exports replace private local paths and omit resolved credentials. Full raw
transcripts and earlier attempts remain in ignored `.evaluation/`, with SHA-256
pointers in the export. Captured guides belong to their source fixture projects;
their harness/evidence paths are not runnable directly from the export folder.
The implementing agent inspected transcripts and resulting artifacts to assign
the recorded verdicts; these are not an independent human review. The runner's
`completed_needs_review` status alone never means acceptance.
See [the reproducible protocol](../evaluation/README.md).

## Deterministic checks

Both environments ran `python -m unittest discover -s tests -v`: 23 tests for
manifest, public metadata/references, fixtures, provider setup and installer
behavior with temporary HOME and paths containing spaces.

| Environment | Result | Time | Coverage limits |
| --- | --- | --- | --- |
| Ubuntu/WSL, Python 3.12.3 | 22 passed, 1 skipped | 6.137 s | Real symlinks passed; Windows junction case skipped. |
| Windows, Python 3.13.13, Git Bash 5.2.26 | 19 passed, 4 skipped | 38.868 s | Native symlink privilege unavailable (WinError 1314); copy, fake-link rejection and NTFS junction protection passed. |

Coverage includes every install entry point, unchanged repeated installs,
duplicate-name conflicts, preserving original files, replacement backups outside
discovery, invalid-manifest atomicity, missing Python, custom Codex HOME, linked
destination rejection, credential expiry/provider guards and usage counters.
The Ubuntu/Windows CI matrix is configured but has not run remotely. No push,
pull request, merge or publication was performed.

## Runtime configuration

Each selected baseline/candidate pair used the same provider, model and effort
within its runtime. Effort was `medium` throughout. Astra was not used.

| Runtime | Version | Provider/account | Model | Selected elapsed sum |
| --- | --- | --- | --- | --- |
| Codex | 0.157.1 | Existing ChatGPT subscription | `gpt-6-sol` | 1282.430 s |
| Claude Code | 2.1.290 | Existing claude.ai first-party subscription | `claude-sonnet-5-5` | 283.927 s |
| Pi | 1.0.4, pinned local installation | OpenAI ChatGPT subscription, native `openai-codex` | `gpt-6-luna` | 434.922 s |
| OpenCode | 1.18.31 | OpenAI ChatGPT subscription, native `openai` | `gpt-6-luna` | 790.085 s |

Claude's initial `sonnet` alias resolved to the same recorded Sonnet 5.5 model;
later trials pinned that identifier. Codex and OpenCode did not emit a resolved
backend model identifier in their JSON; their requested identifiers are recorded
without inventing an observed value. Elapsed sums are per-trial totals, not wall
time or a speed comparison. Token fields retain native units and unavailable
fields; they do not establish dollar cost or a ranking across different models.

Pi and OpenCode used the already valid Codex subscription access token in place,
through child environment variables and their native transports. Pi's temporary
model configuration contains an environment reference; OpenCode receives OAuth
JSON through `OPENCODE_AUTH_CONTENT`. The runner never writes a resolved access
token or refresh token, never changes user auth, and rejects near-expiry access.
Earlier OpenCode Go trials are excluded from these results.

## Behavioral results

`B → C` means baseline to candidate. Verifier creation and handoff are candidate
only because the generator was absent from the baseline.

| Runtime | Small | API/consumer | Contradictory bug | Council | Verifier | Fresh handoff | Candidate gate |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Codex | pass → pass | pass → pass | pass → pass | fail → pass | blocked | blocked | **BLOCKED** |
| Claude Code | pass → pass | pass → pass | pass → pass | fail → pass | pass | pass | pass for tested cases |
| Pi / OpenAI | pass → pass | pass → pass | pass → pass | fail → pass | pass | pass | pass for tested cases |
| OpenCode / OpenAI | pass → pass | pass → pass | pass → pass | fail → pass | pass | pass | pass for tested cases |

The 40 selected trials contain 34 passes, four baseline council failures and two
Codex blocks. Candidate trials contain 22 passes and two blocks. Baseline council
sessions handled findings and availability truthfully but omitted complete
ready-to-paste fallback packets. Candidates retained full reviewer input/errors,
executed the runnable numeric dispute check, preserved disagreement and produced
complete packets. Kiro has package/copy-installer coverage only in this round.

The small case stayed within the requested punctuation change and did not use an
unrelated arithmetic receipt as proof. The API case found the scheduled JSON
consumer, preserved integer cents and checked the actual wire behavior. The bug
case retained the cache-on/cache-off contradiction, tested a distinguishing input
and verified the supported quantity-handling fix.

Claude and Pi's API candidates used the existing harness directly; automatic
loading of the supplied `verify-project` guide was not demonstrated in those
cases. OpenCode loaded that guide/reference but removed `evidence/api.json` after
capture; the raw transcript and independent oracle receipt survive. These are
limits on guide-routing/evidence-retention claims, even though the scoped API
behavior criteria passed.

Council uses explicitly synthetic recorded reviews plus controlled unavailable
CLI wrappers. It tests finding validation, disagreement and truthful fallback,
not the quality of live outside reviewers. The selected candidate runs preserved
the original reviewed source and both review inputs. Codex's fixture packet names
the controlled wrappers; a real review must use the normal reviewer executables.
Production council reviewers remain Codex and Claude CLI on all host runtimes.

The passing generator/handoff sessions created valid guide references and ran a
real HTTP create-and-list feature using the existing project harness. Fresh
native session IDs differ from their generators. Eight retained receipts cover
Claude (three), Pi (two), OpenCode (two), and Codex's harness-only attempt (one).
Each records HTTP 201, the created item in the list, process shutdown, owned data
removal and evidence surviving cleanup. Codex's receipt does not qualify guide
creation. The fixture application/harness source remained unchanged. Only this
local API feature was exercised; web/CLI references are packaged but their
generator workflows were not separately behavior-tested.

## Remaining Codex gate

The ordinary native Windows workspace sandbox denied writes to
`.agents/skills/verify-project`. The agent could run the fixture API harness, but
could not create the requested skill. The handoff was blocked before execution
because the guide did not exist.

A bounded retry granting only the exact child directory through `--add-dir`
failed before shell startup with:

```text
UnsupportedOperation: windows elevated sandbox cannot reopen writable descendants under read-only carveouts directly
```

That failed setting is not a runner default. Qualification needs supported write
access to the requested project skill target, followed by fresh Codex generator
and handoff trials with the same model/effort. Publication stays blocked until
both succeed. No weaker API-only result substitutes for them.

## Retained corrections and limits

The excluded-attempt ledger preserves 38 setup, protocol or superseded attempts
and their reasons: the earlier wrong OpenCode provider; an unavailable Codex
model; native Windows profile/shell failures; Pi's initial OAuth setup and
attachment-style invocation; council check/packet refinements; and the failed
Codex writable-child retry. Selected Pi sessions use native `/skill:` expansion
through stdin, with a fresh full baseline/candidate set after that correction.
The selected council trials use the final complete-packet instructions.

An early Codex council run bypassed PATH wrappers and reached a global reviewer;
it is excluded. A fresh controlled pair names the wrappers explicitly. Codex
still emitted a host-skill metadata warning despite isolation flags, so complete
absence of host context is not claimed; the designated skill copies were read.
Failed and partial receipts were retained, not overwritten.

These observations support the tested cases and review of this branch. They do
not establish general reliability, browser/UI coverage, whole-application
acceptance, deployment or permission to publish.
