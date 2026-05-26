# agent-skills

Practical skills for coding agents.

This repo is starting small on purpose. It currently publishes two skills:

- **[hold-your-horses](./skills/engineering/hold-your-horses/SKILL.md)** - slow down vague or risky development requests before touching code.
- **[prove-it](./skills/engineering/prove-it/SKILL.md)** - do not claim work is done, fixed, tested, or safe without proof.

## Hold Your Horses

Use this when an agent is about to jump into code before the request, current flow, data path, or impact is clear.

The ritual is:

1. **Read it** - inspect the request and the exact artifact the user pointed at.
2. **Question it** - ask only what remains unclear after reading.
3. **Trace it** - follow the current code, data, contracts, and tests.
4. **Shape it** - write the current flow, target flow, boundary, and verification plan.
5. **Plan it** - list the concrete tasks needed to reach the target flow.
6. **Cut it small** - trim the plan to the necessary tasks only.
7. **Change it** - make the smallest implementation that follows the trimmed plan.
8. **Review the diff** - remove scope creep before claiming completion.

The point is simple: no code from a guess.

## Prove It

Use this when an agent is about to say something is fixed, complete, tested, safe, or ready to ship.

The ritual is:

1. **Find the claim** - state exactly what is being asserted.
2. **Find the proof** - identify the strongest evidence for that claim.
3. **Break the proof** - ask whether the evidence would fail if the claim were false.
4. **Run the proof** - execute the narrowest check that supports the claim.
5. **Name what remains unproven** - keep the truth boundary explicit.

The point is simple: no claim without proof.

## Install

For Claude Code:

```bash
./scripts/link-claude-skills.sh
```

For Codex:

```bash
./scripts/link-codex-skills.sh
```

List published skills:

```bash
./scripts/list-skills.sh
```

## Layout

Published skills live under `skills/`. Each skill has a `SKILL.md` and optional `agents/openai.yaml` metadata for Codex.

Only skills listed in `.claude-plugin/plugin.json` are part of the public bundle.
