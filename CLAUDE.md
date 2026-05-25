Published skills live under `skills/` and must be sharp enough to appear in the public README.

Keep the public bundle small. Do not add a skill just to make the repo look fuller.

A skill is public only when both are true:

- It has a reference in the top-level `README.md`.
- It has an entry in `.claude-plugin/plugin.json`.

Local experiments must stay in ignored paths:

- `skills/local/`
- `skills/in-progress/`
- `skills/personal/`
- `skills/drafts/`
- `skills/deprecated/`

Do not add empty public categories or README sections. Add a category only when it contains a published skill.

Codex-ready skills should include `agents/openai.yaml` next to `SKILL.md` with `display_name`, `short_description`, and `default_prompt` UI metadata.

Each published skill entry in the top-level `README.md` must link the skill name to its `SKILL.md`.
