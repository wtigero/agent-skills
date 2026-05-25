Skills are organized into bucket folders under `skills/`:

- `engineering/` - daily code work
- `productivity/` - daily non-code workflow tools
- `misc/` - kept around but rarely used
- `personal/` - tied to a local setup, not promoted
- `in-progress/` - drafts not yet ready to ship
- `deprecated/` - no longer used

Every skill in `engineering/`, `productivity/`, or `misc/` must have a reference in the top-level `README.md` and an entry in `.claude-plugin/plugin.json`. Skills in `personal/`, `in-progress/`, and `deprecated/` must not appear in either.

Codex-ready skills should include `agents/openai.yaml` next to `SKILL.md` with `display_name`, `short_description`, and `default_prompt` UI metadata.

Each skill entry in the top-level `README.md` must link the skill name to its `SKILL.md`.

Each bucket folder should have a `README.md` that lists every skill in the bucket with a one-line description, with the skill name linked to its `SKILL.md`.
