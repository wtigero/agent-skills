Published skills live under `skills/` and must be sharp enough to appear in the public README.

Keep the public bundle small. Do not add a skill just to make the repo look fuller.

Every published skill must have a reference in the top-level `README.md` and an entry in `.claude-plugin/plugin.json`.

Drafts can live locally in `skills/in-progress/`, but that directory is ignored and must not be part of the public bundle.

Codex-ready skills should include `agents/openai.yaml` next to `SKILL.md` with `display_name`, `short_description`, and `default_prompt` UI metadata.

Each skill entry in the top-level `README.md` must link the skill name to its `SKILL.md`.

Each category folder should have a `README.md` that lists every published skill in the category with a one-line description, with the skill name linked to its `SKILL.md`.
