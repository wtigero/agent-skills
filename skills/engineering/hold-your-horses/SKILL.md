---
name: hold-your-horses
description: Use when a development request is vague, risky, cross-cutting, data-related, broad, multi-file, unclear, or tempting to refactor; when the problem, flow, affected data, contracts, or success criteria are not yet clear before implementation.
---

# Hold Your Horses

No code before the flow is clear.

## Ritual

Run before implementing:

1. **Read it.**
2. **Clarify it.**
3. **Trace it.**
4. **Frame it.**
5. **Plan it.**
6. **Trim it.**
7. **Implement it.**
8. **Review the diff.**

Tiny mechanical edit: use **Read it -> Implement it -> Review the diff** and emit only `Changed`, `Verified`, and `Unverified`. Do not compress behavior, data, contracts, shared helpers, or production risk.

## 1. Read it

- Inspect the exact artifact the user named: file, route, screen, command, error, issue, log line, data example, or PR comment.
- Read the request constraints and nearby docs, tests, types, migrations, or config attached to that artifact.
- Separate what is known from what is assumed.

Do not ask until you have read the concrete target, unless access is impossible.

## 2. Clarify it

- Restate the desired outcome in one sentence.
- Name the user-facing or operational result and success criteria.
- Ask only blocking questions whose answers cannot be discovered from the repo, runtime, docs, or database.
- State low-risk assumptions and continue.

Do not ask broad preference questions when the codebase can answer them.

## 3. Trace it

Start at the named artifact and follow the real path:

- Entry point, callers, branches, validation, permissions, and errors.
- Data models, migrations, queries, indexes, seeds, fixtures, or external tables when data is involved.
- API, event, queue, CLI, config, exported type, or SDK contracts when other consumers may depend on the shape.
- Existing shared helpers, utilities, components, libraries, middleware, validators, formatters, and domain services that already solve part of the problem.
- Tests or checks that currently cover the path.

If database access matters but is unavailable, inspect schema/migration/model/query code and state what remains unverified.

## 4. Frame it

Before editing, frame the working model. These are thinking fields, not a required standalone report.

```markdown
**As Is**
- ...

**To Be**
- ...

**Affected Data / Contracts**
- ...

**Risk**
- ...

**Open Question**
- None.
```

Use `Open Question: None.` only when the flow is actually clear. If tracing shows the request is risky, wrong-layer, or larger than expected, stop and ask before coding.

## 5. Plan it

Turn the to-be flow into risk-revealing tasks:

- Code paths, files, modules, or handlers likely to change.
- Data, schema, query, fixture, seed, or migration work if relevant.
- Tests, reproductions, smoke checks, or manual verification needed.
- Contract, config, permission, deploy-order, or compatibility checks.
- Cleanup or refactor ideas that are tempting but not required.

Use these thinking fields:

```markdown
**To Do**
1. ...
2. ...

**Verification**
- ...

**Tempting But Deferred**
- ...
```

The task list is a thinking tool, not permission to do everything on it.

## 6. Trim it

Keep only what makes the to-be flow true without avoidable bugs or side effects.

```markdown
**Do Now**
1. ...
2. ...

**Defer**
- ...

**Ask First**
- None.
```

Keep `Do Now` narrow:

- Prefer existing patterns, helpers, names, tests, and error handling before adding local code.
- Keep public interfaces compatible unless the user explicitly approved a breaking change.
- Avoid opportunistic refactors, formatting churn, dependency swaps, and unrelated file edits.
- Add or update focused tests when they prove the changed behavior or prevent regression.

If the smallest correct change is larger than the agreed boundary, report why before expanding scope.

## 7. Implement it

Implement only the `Do Now` tasks.

- Work in the order with the fastest useful feedback.
- Stop if the code contradicts the framed flow or exposes a new blocking question.
- Keep discovery separate from unrelated cleanup.
- Do not silently pull deferred tasks back into scope.

## 8. Review the diff

Review as an outsider. Do not defend the diff because you wrote it.

Check the actual diff for:

- Scope creep or unrelated edits.
- Changed contracts, data shape, config behavior, or deploy ordering.
- Weak tests that pass without exercising the traced path.
- Debug prints, temporary files, local paths, secrets, or generated noise.
- Missing verification for the success criteria.
- Strange code shape, surprising control flow, duplicated logic, or abstractions that do not earn their complexity.
- Code that could be replaced by a smaller existing helper, a simpler branch, a deletion, or a few lines.
- New local code that duplicates a shared helper, component, library, validator, formatter, or service.

If a much simpler equivalent exists, prefer it before completion. Fix only what is necessary; do not start a broad cleanup pass.

## Output

- Use short headings, bullets, and blank lines.
- Prefer numbered tasks for `Do Now`.
- Use `None.` for empty `Open Question`, `Defer`, or `Ask First` sections.
- Do not collapse flow, plan, and verification into one paragraph.
- Emit the template below. Do not emit every thinking template unless work is risky or the user asks.

Before implementation, show the flow and trimmed plan when the work is non-trivial:

```markdown
**As Is**
- ...

**To Be**
- ...

**Do Now**
1. ...
2. ...

**Defer**
- None.

**Verification**
- ...

**Open Question**
- None.
```

After implementation, report:

- **Changed** - what changed.
- **Kept Small** - why the change is small enough.
- **Simpler Alternative** - any smaller equivalent approach found during review, or `None.`
- **Verified** - what was verified.
- **Unverified** - what remains unverified or intentionally out of scope.

## Guardrails

- Do not use this skill to delay obvious one-line fixes with unnecessary process.
- Do not code through an unresolved blocking question.
- Do not treat code inspection as database verification when live data matters.
- Do not claim the flow is clear if affected consumers or data paths were not inspected.
