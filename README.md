# agent-skills

Practical skills for coding agents, review agents, and engineering workflows.

## Layout

Skills live under `skills/`, grouped by use case:

- `engineering/` - daily coding, review, debugging, and release work
- `productivity/` - communication and workflow helpers
- `misc/` - useful but rarely used skills
- `personal/` - local-only skills, not included in the public index
- `in-progress/` - drafts not ready to publish
- `deprecated/` - retired skills kept for reference

Each skill is its own directory containing a `SKILL.md` with YAML frontmatter and optional bundled resources.

## Install

For Claude Code, symlink every shippable skill into `~/.claude/skills/`:

```bash
./scripts/link-claude-skills.sh
```

For Codex, symlink every shippable skill into `${CODEX_HOME:-~/.codex}/skills/`:

```bash
./scripts/link-codex-skills.sh
```

List every `SKILL.md` in the repo:

```bash
./scripts/list-skills.sh
```

## Skills

### Engineering

- **[migration-safety](./skills/engineering/migration-safety/SKILL.md)** - Review and execute schema, data, and production migrations with rollback, compatibility, and validation discipline.
- **[ship-check](./skills/engineering/ship-check/SKILL.md)** - Final readiness check before claiming work is done, released, merged, or safe to ship.
- **[smallest-safe-change](./skills/engineering/smallest-safe-change/SKILL.md)** - Keep implementation work surgical: inspect the real path, minimize blast radius, and avoid unrelated churn.

### Productivity

_(none yet)_

### Misc

_(none yet)_
