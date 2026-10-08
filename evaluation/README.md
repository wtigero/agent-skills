# Behavioral qualification

This is an **opt-in live evaluation**, separate from the manual offline tests. It uses
configured provider accounts and consumes their normal quota. Do not add it to
CI, supply credentials in the config, or introduce a new paid provider. Use the
user's model/effort choices; default to available Luna/Sol models where supported.
An Astra escalation needs the existing necessity gate, not just a difficult task.

Candidate runs require a clean checkout. Skills and fixtures are read from the
recorded commit archives, and baseline caches use resolved commit IDs even when
the requested ref moves. Handoff reuses the retained generator workspace.
The primary evaluator executable is resolved before reviewer-unavailability
wrappers modify PATH. Literal subscription access tokens are redacted from owned
workspace, home and result files on both session success and failure; links to
other locations block the artifact audit and are never followed. This literal
redaction is not a guarantee against arbitrary encoded or deliberately concealed
credentials. Use fixture-only data and inspect evidence before exporting it.

## Cases and acceptance

| Case | Observable acceptance in both baseline and candidate sessions |
| --- | --- |
| `small` | Change only the requested greeting behavior; perform matching proof or explicitly leave it unproven. Never treat the supplied arithmetic receipt as proof of the greeting. No unnecessary workflow/agents. |
| `api` | Find the scheduled JSON consumer outside Python callers, preserve integer cents, add dollar total, and run a real wire/consumer assertion. A matching project verifier is provided. |
| `bug` | Record the failing quantity and evidence with cache both enabled and disabled; preserve the contradiction to the first theory. Choose a discriminating check, fix the supported cause, rerun the original scenario, and distinguish cause from symptom relief. |
| `council` | Review the explicit file even with a clean git diff. Preserve the complete synthetic recorded reports, verify each finding and retain their disagreement. Attempt the selected reviewer CLIs, report intentional availability errors and prepare truthful manual packets. Do not label archived fixtures as live reviews or edit code. |
| `verifier` + `handoff` | Candidate only: create `verify-project` for the requested target, valid relative references, at most three paths, Launch/Doctor/Drive/Evidence/Cleanup. Execute create-and-list-task with surviving receipts and cleanup. A fresh session must load the generated skill and needed references, run the real feature again, save new evidence and clean up. |

The Council fixture's reviewer texts are explicitly **synthetic recorded input**.
Its CLIs return an actual controlled availability error; there are no simulated
live LLM reviews. This covers aggregation/disagreement plus fallback, not the
quality of real outside reviewers. Council's production reviewer interface stays
Codex/Claude, including when the caller is Pi/OpenCode.
Native Codex sandbox shells can reconstruct PATH. Its controlled trial names
the wrapper executables explicitly; a run that reaches a global reviewer is a
protocol deviation and cannot qualify this availability case.

The verifier fixture exercises a real local HTTP API via the project's existing
Python harness; it does not establish browser/UI coverage. All fixtures use the
standard library and owned processes/data. Mechanical oracles check resulting
behavior separately, but **transcript review** decides skill acceptance; record
who performed that review and do not present an agent's assessment as human QA.
An oracle passing later does not prove the agent ran a matching check itself.

## Run

Pin the candidate commit first and use baseline `e003656`. Copy
`runtime.example.json` into the ignored `.evaluation/` directory, replace command
arrays with local executable paths, and select accessible models/efforts. On
Windows prefer the native executable (or `node` plus CLI `.js`) over `.cmd` shims,
so prompt text does not pass through a command shell. Pin Pi locally to the
qualified version, without changing a global installation. This round uses Pi
`@earendil-works/pi-coding-agent@1.0.4`; its Node requirement must already be met.

```bash
python evaluation/run.py --config .evaluation/runtime.json \
  --runtime codex --scenario small --variant baseline
python evaluation/run.py --config .evaluation/runtime.json \
  --runtime codex --scenario small --variant candidate
```

Repeat for `api`, `bug`, `council` in each of `codex`, `claude`, `pi`, `opencode`.
Use one initial pair per case/runtime. Then run `verifier --variant candidate`
and `handoff --variant candidate` in that order. The latter starts a fresh CLI
session in the generator's project and uses its generated guide, not history.
There is no baseline generator: that skill did not exist at `e003656`.

The runner creates separate workspaces and temporary HOME/config/cache roots.
Codex and Claude use their existing auth locations **in place**; user config/MCP
loading is disabled where CLI flags allow. Designated project skill paths are
explicit in every prompt, preventing ambiguity with legacy same-name skills.
Record any remaining user-context contamination during transcript review.
Pi receives `/skill:<first-skill> <task>` through stdin so its native skill
expansion runs; the prompt also names any other required skills and references.
Pi's `@file` is an attachment block and must not be mistaken for a native skill
invocation. An invocation change requires a fresh baseline/candidate pair.
If native Codex protected-path rules deny the requested project skill directory,
retain the blocked gate. A passing API harness cannot substitute for generating
and loading the skill. This Windows qualification also tried a narrowly scoped
`--add-dir`; the native elevated sandbox rejected writable descendants under
read-only carveouts before shell startup, so that failed option is not a default.

For an explicitly authorized full-access session and a trusted isolated fixture,
`--codex-sandbox danger-full-access` selects the native CLI policy for that one
trial. The runner default stays `workspace-write`; the chosen policy is recorded
in `run.json` and the actual command. This does not qualify protected-path writes
under the default sandbox. Use a fresh output root, then run generator and handoff
with the same explicit policy; retain earlier blocked results.

This round uses the existing Claude subscription and OpenAI for Pi/OpenCode.
`--openai-subscription-auth` reads an already valid Codex ChatGPT access token
in place and passes it only through the child environment. Pi 1.0.4 uses its
native `openai-codex` subscription transport with an `apiKey` environment reference
in temporary `models.json` (the value is a subscription bearer, not a Platform
API key); OpenCode 1.18.31 uses its built-in `openai` OAuth
transport and `OPENCODE_AUTH_CONTENT`. No resolved credential or refresh token
is copied, linked, printed or written. Captured streams redact the access token.
The runner blocks tokens that expire before the trial's timeout plus a minute;
refresh through Codex before retrying. User auth/configuration is not modified.
These are subscription routes, separate from paid OpenAI Platform API keys.

Alternatively use an already configured `OPENAI_API_KEY` with the native
`openai` provider and without that flag. Provider changes require fresh paired
trials; earlier OpenCode Go runs are retained but excluded from the OpenAI gate.

Each result retains prompt, actual command, raw stdout/stderr, final report,
revision, skill fingerprints, CLI version, provider, requested/observed model,
effort, timestamps, elapsed time and available token usage. Null metrics mean
unavailable. A timeout stops only the owned CLI process tree and keeps partial
output. Windows uses PID-scoped tree termination; POSIX gives the owned process
group five seconds after SIGTERM, then forces SIGKILL if needed. Leader exit or
pipe EOF does not shorten the group's grace period; descendants with redirected
pipes are also stopped. Invalid config
or revision setup leaves a blocked `run.json` with the requested baseline ref.
Existing result/workspace paths cannot be overwritten; use a fresh
`--output .evaluation/rerun-<reason>` only after a fix or an ambiguous result.

## Review and gate

Inspect the full transcript and artifacts, recording `pass`, `fail`, or `blocked`
per candidate case. Check that the chosen model/effort and relevant settings
match within each before/after pair. Preserve earlier failed receipts and explain
any rerun. A blocked login/model/provider is a runtime gate, not a failed skill
and not a successful evaluation. Do not spend repeated calls on a known auth
blocker; mark its unattempted cases blocked with the same cause.

Publish only when deterministic Linux + Windows/Git Bash checks pass and all
five candidate behavioral cases pass on **all four** runtimes. Kiro has only
package/installer coverage in this round. The qualification report must separate
mechanical checks, agent observations, untested coverage and blocked gates. One
pair per case demonstrates only those observations, not general reliability or
a tool ranking when models differ.
