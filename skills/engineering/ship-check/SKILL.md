---
name: ship-check
description: Final readiness check before claiming work is complete, merging a PR, tagging a release, deploying, or telling the user something is safe to ship. Use when the user asks if work is done, asks to release or merge, requests a final check, or when an agent is about to close out implementation. Verifies diff scope, tests, docs, config, migrations, generated files, CI, rollback, and unverified claims.
---

# Ship Check

Do not declare work ready until the evidence supports that claim.

## Workflow

### 1. Identify the ship unit

Name what is being shipped:

- Local change, PR, package release, deployment, migration, documentation update, or generated artifact.
- Target branch, environment, version, or service when relevant.
- User-visible behavior or operational effect.

If the ship unit is unclear, clarify it before proceeding.

### 2. Inspect the actual diff

Review the full local or PR diff, not just the last file touched.

Check for:

- Unrelated edits or formatting churn.
- Secrets, local paths, debug output, temporary files, generated noise.
- Public API, config, schema, dependency, or build changes.
- Missing docs or examples when behavior changed.
- Tests changed in ways that weaken coverage.

### 3. Verify behavior

Match verification to risk.

- Run targeted tests for the edited path.
- Run broader tests or build checks when shared code, packaging, routing, config, or public API changed.
- Confirm generated artifacts are up to date when the repo expects them.
- For UI work, inspect the rendered result when feasible.
- For release work, check version, changelog, tag target, and CI status.

Do not replace failed verification with confidence language.

### 4. Check operational safety

For production, data, deployment, or migration work, require:

- Rollback or restoration path.
- Backward compatibility across deploy order.
- Observability signal after ship.
- Validation command or query.
- Clear owner for follow-up.

If any of these is missing, mark the work as not ready.

### 5. Produce the verdict

Use one of these verdicts:

- `ship` - evidence is sufficient.
- `ship with notes` - safe enough, with explicit minor caveats.
- `fix before ship` - known issue blocks readiness.
- `do not ship` - high risk or missing critical evidence.

Include the shortest evidence list that makes the verdict defensible.

## Output format

Lead with the verdict.

Then list:

- Scope checked.
- Verification run and result.
- Blocking issues, if any.
- Residual risk.
- Next action.

## Guardrails

- Do not say "looks good" without naming what was inspected.
- Do not treat a passing narrow test as proof for unrelated surfaces.
- Do not approve release or migration work without rollback thinking.
- Do not invent CI status; inspect it or say it was not checked.
