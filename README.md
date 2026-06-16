# agent-skills

Practical skills for coding agents.

Thai: [README.th.md](./README.th.md)

This repo stays small on purpose. It currently publishes three skills:

- **[hold-your-horses](./skills/engineering/hold-your-horses/SKILL.md)** - slow down vague or risky development requests before touching code.
- **[prove-it](./skills/engineering/prove-it/SKILL.md)** - do not claim work is done, fixed, tested, or safe without proof.
- **[council](./skills/engineering/council/SKILL.md)** - get an independent, read-only review from Codex, Claude Code, or both.

This README is the public summary. The exact operating rules live in each
`SKILL.md`.

## Hold Your Horses

No code before the flow is clear.

Use this when a development request is vague, risky, cross-cutting,
data-related, broad, multi-file, unclear, or tempting to refactor before the
problem, flow, affected data, contracts, or success criteria are clear.

It forces the agent to:

- Read the concrete target instead of guessing.
- Clarify only what is truly blocking.
- Trace the real path through code, data, contracts, helpers, and tests.
- Frame risk, trim the plan, implement narrowly, and review the diff.

Tiny mechanical edit: use **Read it -> Implement it -> Review the diff** and
emit only `Changed`, `Verified`, and `Unverified`. Do not compress behavior,
data, contracts, shared helpers, or production risk.

The point is simple: clear the flow, then touch the code.

## Prove It

No claim without proof.

Use this when an agent is about to say something is fixed, complete, tested, safe, or ready to ship.

It forces the agent to:

- State one exact claim.
- Pick the strongest proof that matches that claim.
- Ask whether the proof would fail if the claim were false.
- Run fresh proof now.
- Name what remains unproven.

Good proof reaches real behavior: a repro, workflow, API call, job, targeted
test, affected build/check, or manual check with the relevant input and observed
output.

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

Installers link the published skills from this repo into each agent's skill directory.

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
