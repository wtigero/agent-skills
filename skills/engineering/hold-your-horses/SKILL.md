---
name: hold-your-horses
description: Use when a development request is vague, risky, cross-cutting, data-related, or likely to be overbuilt; when the problem, current flow, affected data, contracts, or success criteria are not yet clear before implementation.
---

# Hold Your Horses

No code before the flow is clear.

## Ritual

Slow down and run this sequence before implementing:

1. **Read it.**
2. **Question it.**
3. **Trace it.**
4. **Shape it.**
5. **Cut it small.**
6. **Review the diff.**

Compress the ritual for tiny mechanical edits, but do not skip it when behavior, data, contracts, or production risk are involved. The point is not ceremony; the point is to avoid coding from a guess.

## 1. Read it

Use the context already available before asking the user anything.

- Read the user's request carefully, including exact wording and constraints.
- Inspect the exact artifact the user named: file, route, screen, command, error, issue, log line, data example, or PR comment.
- Check nearby docs, tests, types, migrations, or config when they are directly attached to the named artifact.
- Separate what is known from what is assumed.

Do not ask a question until you have read the concrete target, unless access to that target is impossible.

## 2. Question it

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
- Tests or checks that currently cover the path.

If database access is relevant but unavailable, inspect schema/migration/model/query code and state what remains unverified.

## 4. Shape it

Before editing, write the working model in a compact block:

```text
Current flow:
Target flow:
Change boundary:
Affected data/contracts:
Verification:
Open question:
```

Use `Open question: none` only when the flow is actually clear.

If tracing reveals that the original request is risky, wrong-layer, or larger than expected, stop and ask a follow-up before coding.

## 5. Cut it small

Implement the narrowest change that makes the target flow true.

- Prefer existing patterns, helpers, names, tests, and error handling.
- Keep public interfaces compatible unless the user explicitly approved a breaking change.
- Separate behavior changes from cleanup.
- Avoid opportunistic refactors, formatting churn, dependency swaps, and unrelated file edits.
- Add or update focused tests when they prove the changed behavior or prevent regression.

If the smallest correct change is larger than the agreed boundary, report why before expanding scope.

## 6. Review the diff

Self-review before claiming completion.

Check the actual diff for:

- Scope creep or unrelated edits.
- Changed contracts, data shape, config behavior, or deploy ordering.
- Weak tests that pass without exercising the traced path.
- Debug prints, temporary files, local paths, secrets, or generated noise.
- Missing verification for the success criteria.

Fix only what is necessary. Do not start a broad cleanup pass during review.

## Output

Before implementation, show the compact flow block when the work is non-trivial.

After implementation, report:

- What changed.
- Why the change is small enough.
- What was verified.
- What remains unverified or intentionally out of scope.

## Guardrails

- Do not use this skill to delay obvious one-line fixes with unnecessary process.
- Do not code through an unresolved blocking question.
- Do not treat code inspection as database verification when live data matters.
- Do not claim the flow is clear if affected consumers or data paths were not inspected.
