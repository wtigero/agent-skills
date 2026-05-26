# agent-skills

Practical skills for coding agents.

This repo is starting small on purpose. It currently publishes one skill:

- **[hold-your-horses](./skills/engineering/hold-your-horses/SKILL.md)** - slow down vague or risky development requests before touching code.

## Hold Your Horses

Use this when an agent is about to jump into code before the request, current flow, data path, or impact is clear.

The ritual is:

1. **Read it** - inspect the request and the exact artifact the user pointed at.
2. **Question it** - ask only what remains unclear after reading.
3. **Trace it** - follow the current code, data, contracts, and tests.
4. **Shape it** - write the current flow, target flow, boundary, and verification plan.
5. **Cut it small** - make the narrowest change that solves the real problem.
6. **Review the diff** - remove scope creep before claiming completion.

The point is simple: no code from a guess.

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
