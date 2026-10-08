# agent-skills

Practical skills for coding and writing.

Thai: [README.th.md](./README.th.md)

This repo stays small on purpose. It currently publishes six skills:

- **[hold-your-horses](./skills/engineering/hold-your-horses/SKILL.md)** - slow down vague or risky development requests before touching code.
- **[prove-it](./skills/engineering/prove-it/SKILL.md)** - do not claim work is done, fixed, tested, or safe without proof.
- **[council](./skills/engineering/council/SKILL.md)** - get an independent, read-only review from Codex, Claude Code, or both.
- **[bug-hunter](./skills/engineering/bug-hunter/SKILL.md)** - trace failures and test competing causes before choosing a fix.
- **[create-verifier](./skills/engineering/create-verifier/SKILL.md)** - build and exercise a project-specific verification guide that a fresh session can follow.
- **[write-like-me](./skills/writing/write-like-me/SKILL.md)** - turn your ideas into articles and posts in your own voice, using plain words.

This README is the public summary. The exact operating rules live in each
`SKILL.md`.

Each skill works on its own. When combining them, reuse established flow and
applicable evidence, and include the outcome in one completion report.

## Hold Your Horses

No code before the flow is clear.

Use this before implementation when the problem, flow, affected data, contracts,
or success criteria are unclear, or a broad change or proposed refactor has
uncertain scope or impact.

It forces the agent to:

- Read the concrete target instead of guessing.
- Clarify only what is truly blocking.
- Trace the real path through code, data, contracts, helpers, and tests.
- Check hidden consumers, wire/data formats and installed dependency behavior; name the facts that need proof before editing.
- Frame risk, trim the plan, implement narrowly, and review the diff.

Scale the depth to uncertainty and impact. Clear, bounded changes use a short
path: read, trace the affected path, implement, review the diff, and verify.
Report `Changed`, `Verified`, and `Unverified`; add scope decisions or alternatives
when they matter. Do not shorten unresolved data, contract, or production risk.

The point is simple: clear the flow, then touch the code.

## Prove It

No claim without proof.

Use this when an agent is about to say something is fixed, complete, tested, safe, or ready to ship.

It forces the agent to:

- State one exact claim.
- Pick the strongest proof that matches that claim.
- Ask whether the proof would fail if the claim were false.
- Check that proof matches the relevant code, inputs, and environment; rerun when it no longer does.
- Name what remains unproven.

Good proof reaches real behavior: a repro, workflow, API call, job, targeted
test, affected build/check, or manual check with the relevant input and observed
output. A matching, inspectable CI or earlier check can be reused. Symptom
resolution, root-cause confirmation, and release readiness are separate claims.
Use an existing project verifier when it checks the relevant fact. Its presence
or an unrelated passing route does not prove the claim.

The point is simple: no claim without proof.

## Council

No rubber stamps. Bring outside eyes.

Use this when you want an independent second opinion on a change from a model
outside the one you are working in.

It routes a **read-only** outside review to Codex, Claude Code, or both:

- `council` (or `council both`) - run Codex and Claude, returned side by side.
- `council codex` / `council claude` - run just one.

The review rules stay simple:

- Reviewers stay independent.
- Findings must cite real evidence.
- Disagreement is returned as-is instead of smoothed into fake consensus.
- Raw reviewer outputs remain complete; a separate aggregator assessment checks evidence, severity and relevance for each finding.

If the reviewer CLI cannot run, Council prepares a manual review packet instead
of pretending the review happened. You get reviewer output or a ready-to-paste
brief, never fake certainty.

The point is simple: return the outside view, even when it disagrees.

## Bug Hunter

Find the cause. Bring the evidence.

Use this when a bug, intermittent failure, or performance regression needs
diagnosis before choosing a fix.

It guides the agent to:

- Build a feedback loop that reproduces the reported symptom.
- Trace the fail path and test predictions that distinguish plausible causes.
- Keep an experiment ledger and check explanations against earlier observations.
- Fix within scope, verify the original scenario, and remove temporary probes.

Preliminary hypotheses can help build a repro, but remain provisional until
tested. A hypothesis surviving disproof is still a candidate. Intermittent and
performance failures need comparable repeated runs, not a single clean result.

The point is simple: follow the failure and bring evidence for the cause.

## Create Verifier

This is optional setup for projects that need a reusable verification recipe
across sessions. `bug-hunter` investigates causes; `prove-it` judges whether
evidence supports a claim. They can reuse `verify-project` or the existing harness
without first creating a guide. The creator's trial checks that its recipe runs;
later changes still need evidence matching their own claims.

Use this to create a `verify-project` skill from a repository's existing harness.
It covers Launch, Doctor, Drive, Evidence and Cleanup, maps up to three main
feature paths, and exercises one through the real app/API/CLI. Evidence must
survive cleanup. An execution blocker leaves the guide `draft`, with the unrun
steps and cause recorded. A validated path does not establish whole-app coverage.

Select only the target you need: `.agents/skills/verify-project` for
Codex/Pi/OpenCode, `.claude/skills/verify-project` for Claude Code, or
`.kiro/skills/verify-project` for Kiro. Existing verifiers are inspected and
proposed changes shown before overwrite. Generated references are relative to
the project skill, so a fresh session does not need this conversation.

## Write Like Me

Your ideas, in words you would use yourself.

Use this for articles, posts, Thai notes you want to write in English, or drafts
that feel generic or unlike you.

It draws out your point and real examples, uses your writing samples when
available, and drafts with common words and correct grammar. It edits out filler
without inventing personal stories or polishing away your voice. Short pieces
do not need a long interview or outline.

For example:

```text
Use $write-like-me to turn these notes into a short English post.
Keep my direct tone and use words I can say myself.
Ask if my point or example is missing.
```

## Install

Requirements: Bash and Python **3.9+** (`python3`, then `python` on PATH).
Only the Python standard library is used; Ruby is no longer needed. Run these
commands in Bash on Linux or **Git Bash on Windows**, including checkouts and
HOME paths containing spaces.

For a shared installation used by Codex, Pi and OpenCode:

```bash
./scripts/link-agent-skills.sh
```

This installs into `~/.agents/skills`. Both [Pi](https://pi.dev/docs/latest/skills)
and [OpenCode](https://opencode.ai/docs/skills/) support this discovery location.
Keep one copy of each skill per runtime's search paths to avoid precedence
surprises. The installer checks standard user and current-project/ancestor
locations (up to the git root); it reports a conflict and preserves all existing
skills before making any installations. Custom plugin/package/configured extra
skill paths must be checked separately.

For Claude Code:

```bash
./scripts/link-claude-skills.sh
```

For the existing Codex-specific location (`${CODEX_HOME:-~/.codex}/skills`):

```bash
./scripts/link-codex-skills.sh
```

For Kiro:

```bash
./scripts/link-kiro-skills.sh
```

List published skills:

```bash
./scripts/list-skills.sh
```

Codex/Claude/shared installers create **real directory symlinks** and check the
result; Kiro always copies. If symlinks are unavailable, use `--copy`:

```bash
./scripts/link-agent-skills.sh --copy
./scripts/link-claude-skills.sh --copy
```

Identical installs are left untouched, including timestamps. A different or
broken link, local edit or extra file is a conflict. To replace one destination
skill explicitly:

```bash
./scripts/link-agent-skills.sh --copy --replace prove-it
```

Repeat `--replace <name>` for multiple skills. The entire original directory or
link is moved to `<destination-parent>/agent-skills-backups/<runtime>/<run-id>/<name>`
before replacement, outside all checked discovery roots. Duplicate names in
other searched locations are still conflicts: inspect and consolidate them
yourself; `--replace` never removes other locations. Linked discovery/backup
directories are refused to prevent writes reaching the source checkout.
`CODEX_HOME`, `XDG_CONFIG_HOME` and `PI_CODING_AGENT_DIR` overrides are respected.

Shared and Claude installations check their overlapping OpenCode discovery
roots in either installation order. Existing skill names may use plain or
quoted single-line YAML strings with comments. Ambiguous name declarations
stop preflight for inspection before any installation writes.

## Use

Start a fresh session after installing. Existing sessions may need a skill reload.

| Runtime | Example |
| --- | --- |
| Codex | `Use $hold-your-horses before changing this API, then $prove-it to check compatibility.` |
| Claude Code | `/hold-your-horses Check this API change.` then `/prove-it Verify the claim.` |
| Pi | `/skill:hold-your-horses Check this API change.` then `/skill:prove-it Verify the claim.` |
| OpenCode | `Load the hold-your-horses skill and check this API change; use prove-it before claiming it works.` |
| Kiro | `Use create-verifier for this repo, targeting Kiro only.` |

For a project guide: `Use create-verifier for this repo, targeting shared
Codex/Pi/OpenCode skills only. Exercise the export feature and keep the evidence.`
In the next session, load `verify-project` and run that feature using its reference.

Council reviewers remain **Codex and Claude CLIs** on every runtime. The default
is both, sequentially; `council codex` or `council claude` selects one. Pi and
OpenCode do not need a reviewer extension. Respect the user's configured model,
effort and budget; these skills do not authorize paid model escalation.

## Validation and release status

```bash
python -m unittest discover -s tests -v
```

The deterministic suite is run manually on Linux and Windows/Git Bash with
temporary HOME directories. This repository has no automatic CI workflow.
It covers bundle metadata/references, path safety,
fresh/repeated installs, copies, real links, conflicts, backups and preservation.
It makes no provider calls.

Behavioral qualification compares baseline `e003656` with the candidate in fresh
Codex, Claude, Pi and OpenCode sessions; Kiro is packaging-only. The scenarios,
runner and acceptance rubric are in [evaluation](evaluation/README.md), with
results in [the qualification report](docs/qualification.md). Missing auth,
failed runs and untested scope remain explicit gates. Publishing requires the
deterministic checks and all four behavioral runtime gates to pass. Results
support the cases exercised, not a ranking of tools using different models.

## Inspiration

[pstack-claude](https://github.com/michael-denyer/pstack-claude) informed the focus
on impact beyond direct callers and reusable project verification recipes,
especially its `blast-radius` and `create-verification-skill` ideas. The public
instructions here are written for this bundle, with a smaller workflow and
runtime-neutral project guides.

## Layout

Published skills live under `skills/`. Each skill has a `SKILL.md` and optional `agents/openai.yaml` metadata for Codex.

`.claude-plugin/plugin.json` is the source of truth for the public bundle. Installers and `list-skills.sh` use that manifest.
