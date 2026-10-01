# agent-skills

Practical skills for coding agents.

Thai: [README.th.md](./README.th.md)

This repo stays small on purpose. It currently publishes three skills:

- **[hold-your-horses](./skills/engineering/hold-your-horses/SKILL.md)** - slow down vague or risky development requests before touching code.
- **[prove-it](./skills/engineering/prove-it/SKILL.md)** - do not claim work is done, fixed, tested, or safe without proof.
- **[council](./skills/engineering/council/SKILL.md)** - get an independent, read-only review from Codex, Claude Code, or both.

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

If the reviewer CLI cannot run, Council prepares a manual review packet instead
of pretending the review happened. You get reviewer output or a ready-to-paste
brief, never fake certainty.

The point is simple: return the outside view, even when it disagrees.

## Install

Installers link published skills into Codex and Claude Code's skill directories,
and copy them into Kiro's.

For Claude Code:

```bash
./scripts/link-claude-skills.sh
```

For Codex:

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

## Layout

Published skills live under `skills/`. Each skill has a `SKILL.md` and optional `agents/openai.yaml` metadata for Codex.

`.claude-plugin/plugin.json` is the source of truth for the public bundle. Installers and `list-skills.sh` use that manifest.
