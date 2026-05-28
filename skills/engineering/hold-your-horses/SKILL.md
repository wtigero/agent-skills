---
name: hold-your-horses
description: Use when a development request is vague, risky, cross-cutting, data-related, broad, multi-file, unclear, or tempting to refactor; when the problem, flow, affected data, contracts, or success criteria are not yet clear before implementation.
---

# Hold Your Horses

No code before the flow is clear.

## Ritual

Slow down and run this sequence before implementing:

1. **Read it.**
2. **Clarify it.**
3. **Trace it.**
4. **Frame it.**
5. **Plan it.**
6. **Trim it.**
7. **Implement it.**
8. **Review the diff.**

For tiny mechanical edits, use the compressed path: **Read it -> Implement it -> Review the diff.** Emit only `Changed`, `Verified`, and `Unverified`.

Do not use the compressed path when behavior, data, contracts, shared helpers, or production risk are involved. The point is not ceremony; the point is to avoid coding from a guess.

## 1. Read it

Use the context already available before asking the user anything.

- Read the user's request carefully, including exact wording and constraints.
- Inspect the exact artifact the user named: file, route, screen, command, error, issue, log line, data example, or PR comment.
- Check nearby docs, tests, types, migrations, or config when they are directly attached to the named artifact.
- Separate what is known from what is assumed.

Do not ask a question until you have read the concrete target, unless access to that target is impossible.

## 2. Clarify it

Clarify what remains unclear after reading the request and concrete target.

- Restate the desired outcome in one sentence.
- Identify the user-facing behavior or operational result.
- Name the success criteria that would prove the work is done.
- Ask only blocking questions whose answers cannot be discovered from the repo, runtime, docs, or database.
- If the ambiguity is low-risk, state a reasonable assumption and continue.

Do not ask broad preference questions when the codebase can answer them.

## 3. Trace it

Inspect the current system before proposing the change.

Start from the exact artifact the user named: file, route, screen, command, error, issue, or data example. Then follow the real path:

- Entry point and caller path.
- Existing branches, validation, permissions, and error handling.
- Data models, migrations, queries, indexes, seeds, fixtures, or external tables when data is involved.
- API, event, queue, CLI, config, exported type, or SDK contracts when other consumers may depend on the shape.
- Existing shared helpers, utilities, components, libraries, middleware, validators, formatters, and domain services that already solve part of the problem.
- Tests or checks that currently cover the path.

If database access is relevant but unavailable, inspect schema/migration/model/query code and state what remains unverified.

## 4. Frame it

Before editing, think through the working model. These are thinking fields, not a required standalone user-facing report.

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

Use `Open question: none` only when the flow is actually clear.

If tracing reveals that the original request is risky, wrong-layer, or larger than expected, stop and ask a follow-up before coding.

## 5. Plan it

Turn the to-be flow into concrete tasks before editing.

Write the task list with enough detail to expose risk:

- Code paths, files, modules, or handlers likely to change.
- Data, schema, query, fixture, seed, or migration work if relevant.
- Tests, reproductions, smoke checks, or manual verification needed.
- Contract, config, permission, deploy-order, or compatibility checks if affected.
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

Analyze the task list again before implementation. Keep only what is necessary to make the to-be flow true without adding avoidable bugs or side effects.

Split the plan into these thinking fields:

```markdown
**Do Now**
1. ...
2. ...

**Defer**
- ...

**Ask First**
- None.
```

Keep `Do now` narrow:

- Prefer existing patterns, helpers, names, tests, and error handling.
- Reuse an existing shared helper, component, or library before adding a new local implementation.
- Keep public interfaces compatible unless the user explicitly approved a breaking change.
- Separate behavior changes from cleanup.
- Avoid opportunistic refactors, formatting churn, dependency swaps, and unrelated file edits.
- Add or update focused tests when they prove the changed behavior or prevent regression.

If the smallest correct change is larger than the agreed boundary, report why before expanding scope.

## 7. Implement it

Implement only the `Do now` tasks.

The output of this step is the working diff, not another report.

- Work in the order that gives the fastest useful feedback.
- Stop if the code contradicts the framed flow or exposes a new blocking question.
- Keep any additional discovery separate from unrelated cleanup.
- Do not silently pull deferred tasks back into scope.

## 8. Review the diff

Self-review before claiming completion.

Review as an outsider. Do not defend the diff because you wrote it.

Check the actual diff for:

- Scope creep or unrelated edits.
- Changed contracts, data shape, config behavior, or deploy ordering.
- Weak tests that pass without exercising the traced path.
- Debug prints, temporary files, local paths, secrets, or generated noise.
- Missing verification for the success criteria.
- Strange code shape, surprising control flow, duplicated logic, or abstractions that do not earn their complexity.
- Code that could be replaced by a smaller existing helper, a simpler branch, a deletion, or a few lines.
- New local code that duplicates a shared helper, component, library, validator, formatter, or domain service.

If the review finds a much simpler equivalent change, prefer the simpler change before completion. Fix only what is necessary. Do not start a broad cleanup pass during review.

## Output

Keep output scannable.

- Use short headings and bullets.
- Put a blank line between sections.
- Prefer numbered tasks for `Do Now`.
- Use `None.` for empty `Open Question`, `Defer`, or `Ask First` sections.
- Do not collapse the flow, plan, and verification into one paragraph.
- Emit the template below to the user. Do not emit every intermediate thinking template unless the work is risky or the user asks for the full reasoning.

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
