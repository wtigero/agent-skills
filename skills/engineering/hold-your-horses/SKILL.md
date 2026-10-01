---
name: hold-your-horses
description: Use before implementation when the desired behavior, affected flow, data, contracts, or success criteria are unclear, or when a broad change or proposed refactor has uncertain scope or impact.
---

# Hold Your Horses

No code before the flow is clear.

## Ritual

Run before implementing:

1. **Read it.**
2. **Clarify intent.**
3. **Trace it.**
4. **Frame it.**
5. **Plan it.**
6. **Trim it.**
7. **Implement it.**
8. **Review the diff.**

Scale the depth to uncertainty and impact, not the number of files. For a clear,
bounded change, use **Read it -> Trace the affected path -> Implement it ->
Review the diff**, run the relevant verification, and report `Changed`,
`Verified`, and `Unverified`. Tiny mechanical edits need only nearby context.
Do not shorten the investigation while affected data, contracts, shared callers,
or production impact remain unclear.

Reuse flow, constraints, plans, and evidence already established in this task
while they still match the affected code and environment. Reopen only the parts
invalidated by new observations or changes.

## 1. Read it

- Inspect the exact artifact the user named: file, route, screen, command, error, issue, log line, data example, or PR comment.
- Read the request constraints and nearby docs, tests, types, migrations, or config attached to that artifact.
- Separate what is known from what is assumed.

Do not ask until you have read the concrete target, unless access is impossible.

## 2. Clarify intent

- Restate the desired outcome in one sentence.
- Name the user-facing or operational result and success criteria.
- Ask only blocking questions whose answers cannot be discovered from the repo, runtime, docs, or database.
- If no question is needed, state the assumption and why it is safe to continue.

Do not ask broad preference questions when the codebase can answer them.

## 3. Trace it

Start at the named artifact and follow the real path:

- Entry point, callers, branches, validation, permissions, and errors.
- Data models, migrations, queries, indexes, seeds, fixtures, or external tables when data is involved.
- API, event, queue, CLI, config, exported type, or SDK contracts when other consumers may depend on the shape.
- Existing shared helpers, utilities, components, libraries, middleware, validators, formatters, and domain services that already solve part of the problem.
- Local project patterns near the target: naming, module boundaries, data access, errors, validation, UI components, and test style.
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

After tracing, reopen clarification before coding if an assumption was wrong, the target flow is unclear, or the change is larger than expected.

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
- Follow the local project pattern unless it conflicts with `To Be`; name any deliberate deviation before coding.
- Every `Do Now` item must directly support `To Be` or `Verification`; otherwise move it to `Defer`.
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
- Code that breaks local project patterns without a necessary reason.

If a much simpler equivalent exists, prefer it before completion. Fix only what is necessary; do not start a broad cleanup pass.

## Output

- Use short headings, bullets, and blank lines.
- Prefer numbered tasks for `Do Now`.
- Omit empty `Open Question`, `Defer`, or `Ask First` sections.
- Keep flow, scope, and verification distinguishable when the work needs a detailed plan.
- Use the template below when it helps explain unresolved scope or risk. Do not emit every thinking template unless work is risky or the user asks.

Before implementation, show the flow and trimmed plan when uncertainty or impact
requires the full workflow. Add `Defer` or `Open Question` only when there is
something to report:

```markdown
**As Is**
- ...

**To Be**
- ...

**Do Now**
1. ...
2. ...

**Verification**
- ...
```

After implementation, report:

- **Changed** - what changed.
- **Verified** - what was verified.
- **Unverified** - what remains unverified or intentionally out of scope.

Include `Kept Small` or `Simpler Alternative` when a scope decision or trade-off
matters. When another skill also checks completion, include its evidence and
limits here rather than producing a second completion report.

## Guardrails

- Do not use this skill to delay obvious one-line fixes with unnecessary process.
- Do not code through an unresolved blocking question.
- Do not treat code inspection as database verification when live data matters.
- Do not claim the flow is clear if affected consumers or data paths were not inspected.
