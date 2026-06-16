# agent-skills

Practical skills for coding agents.

This repo is starting small on purpose. It currently publishes three skills:

- **[hold-your-horses](./skills/engineering/hold-your-horses/SKILL.md)** - slow down vague or risky development requests before touching code.
- **[prove-it](./skills/engineering/prove-it/SKILL.md)** - do not claim work is done, fixed, tested, or safe without proof.
- **[council](./skills/engineering/council/SKILL.md)** - get an independent, read-only review from Codex, Claude Code, or both.

## Hold Your Horses

Use this when an agent is about to jump into code before the request, current flow, data path, or impact is clear.

The ritual is:

1. **Read it** - inspect the request and the exact artifact the user pointed at.
2. **Clarify it** - ask only what remains unclear after reading.
3. **Trace it** - follow the current code, data, contracts, and tests.
4. **Frame it** - write the as-is flow, to-be flow, affected surface, and risk.
5. **Plan it** - list the concrete tasks needed to reach the to-be flow.
6. **Trim it** - reduce the plan to the necessary tasks only.
7. **Implement it** - make the smallest implementation that follows the trimmed plan.
8. **Review the diff** - remove scope creep before claiming completion.

The point is simple: no code from a guess.

## Prove It

Use this when an agent is about to say something is fixed, complete, tested, safe, or ready to ship.

The ritual is:

1. **Find the claim** - state exactly what is being asserted.
2. **Find the proof** - identify the strongest evidence that matches that claim.
3. **Break the proof** - ask whether the evidence would fail if the claim were false.
4. **Run the proof** - execute a fresh narrow check that supports the claim.
5. **Name what remains unproven** - keep the truth boundary explicit.

The point is simple: no claim without proof.

## Council

No rubber stamps. Bring outside eyes.

Use this when you want an independent second opinion on a change from a model
outside the one you are working in.

The ritual is:

1. **Choose the scope** - decide whether the council reviews git changes, files, or pasted content.
2. **Summon outside reviewers** - route the review to Codex, Claude Code, or both.
3. **Keep them blind** - do not feed one reviewer's answer into the other.
4. **Demand evidence** - require findings to cite real code, snippets, or sources.
5. **Return the disagreement** - show each reviewer's output without smoothing it into false consensus.

It routes a **read-only** review to an external agent CLI -- Codex, Claude Code,
or both -- over git changes, specific file paths, or pasted content:

- `council` (or `council both`) - run Codex and Claude, returned side by side.
- `council codex` / `council claude` - run just one.

Every member reviews as an unbiased outside auditor: findings grounded in the
real code, web research allowed, framed as severity-tagged recommendations
rather than commands. The reviewers never edit -- Codex `review` is for
read-only review, Codex `exec` runs `--sandbox read-only`, and Claude runs
`--permission-mode plan`.

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
