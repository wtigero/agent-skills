---
name: smallest-safe-change
description: Keep coding-agent changes surgical and low-risk. Use when implementing a requested code change, fixing a narrow bug, responding to review feedback, or touching an unfamiliar codebase where unrelated refactors, broad rewrites, or hidden behavior changes would be risky. Forces the agent to inspect the concrete path first, define the smallest viable edit, preserve existing behavior, and report blast radius and verification.
---

# Smallest Safe Change

Make the requested change with the least behavioral surface area that still solves the real problem.

## Workflow

### 1. Anchor on the concrete target

Start from the exact artifact the user named: file, route, function, error string, DOM node, command, test, or PR comment.

- Read the named artifact before searching broadly.
- Identify the caller or runtime path that reaches it.
- State the current behavior and the requested behavior in one sentence each.
- If the request is underspecified, make the smallest reasonable assumption and say it.

### 2. Define the safe boundary

Before editing, name the boundary of the change:

- Files or modules expected to change.
- Public interfaces that should not change.
- Tests or commands that should still pass.
- Related areas intentionally left alone.

If the fix requires crossing the boundary, stop and explain why before expanding scope.

### 3. Prefer existing shape

Use local patterns over new abstractions.

- Reuse existing helpers, conventions, error handling, styling, and naming.
- Add a new abstraction only when it removes real duplication or matches a clear local pattern.
- Avoid opportunistic cleanup, renames, formatting churn, dependency swaps, and broad rewrites.
- Do not modify unrelated files just because you noticed improvements.

### 4. Make the edit

Implement the smallest edit that changes the observed behavior.

- Keep behavior-preserving refactors separate from behavior changes.
- Preserve compatibility for existing callers unless the user asked for a breaking change.
- Make failure modes explicit when the existing code already does so.
- Add or update focused tests when the risk justifies it.

### 5. Verify the claimed path

Run the narrowest useful verification first, then broaden only as needed.

- Run the directly affected test or command.
- If no test exists, use a reproducible command, fixture, or manual check that reaches the edited path.
- If verification cannot run, say exactly why and what remains unverified.

### 6. Report

Keep the final answer short:

- What changed.
- Why this was the smallest safe change.
- What was verified.
- Any remaining risk or follow-up that is deliberately out of scope.

## Guardrails

- Do not use this skill to justify doing nothing if the requested behavior is clearly broken.
- Do not hide a necessary larger fix; surface it and ask for scope expansion.
- Do not claim safety from code inspection alone when a runnable check is available.
