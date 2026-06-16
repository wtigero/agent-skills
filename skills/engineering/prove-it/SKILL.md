---
name: prove-it
description: Use when work is being claimed complete, fixed, tested, validated, ready to ship, or safe; when a test, reproduction, smoke check, CI result, or verification claim may be weak, missing, misleading, or unrun.
---

# Prove It

No claim without proof.

Act as an external auditor of the claim. Do not defend the work because you wrote it, ran it, or want it to be done.

## Ritual

Run before saying work is done, fixed, tested, or safe:

1. **Find the claim.**
2. **Find the proof.**
3. **Break the proof.**
4. **Run the proof.**
5. **Name what remains unproven.**

The point is not every test; it is fresh evidence for the exact claim.

## 1. Find the claim

State one exact claim. Examples:

- The bug is fixed.
- The new behavior works.
- The regression test proves the old bug cannot return.
- The change is safe to ship.
- The migration or data change is validated.

If the claim is vague, narrow it before evaluating evidence.

## 2. Find the proof

Pick the strongest matching evidence:

| Claim | Strong proof |
| --- | --- |
| Bug fixed | Original repro now passes. |
| Regression test works | Test fails without the fix and passes with it. |
| New behavior works | Workflow, API call, CLI command, or job reaches the changed path. |
| Build passes | Build command exits 0 in this run. |
| Safe to ship | Targeted checks pass and risk-specific gaps are named. |

Prefer proof that reaches real behavior: repro, workflow, API call, job, targeted test, affected build/check, or manual check with exact input, environment, and observed output. If proof is missing, say so; do not use confidence language.

## 3. Break the proof

Challenge whether the evidence would catch the problem returning. Try to make the claim false; if the check still passes, proof is weak.

Ask:

- Would this proof fail if the bug came back?
- Does it reach the same path the claim depends on?
- Is it asserting the behavior, or only implementation details?
- Are mocks, fixtures, snapshots, or stubs hiding the real failure?
- Does it cover the relevant edge case, data shape, permission, config, or deploy order?
- Did the test become weaker, broader, or more forgiving while making it pass?

If the proof can pass while the claim is false, it is not sufficient proof.

## 4. Run the proof

Run fresh proof now. Old logs, prior CI, cached output, memory, or another agent's report can guide, but are not proof.

- Start with the original repro, changed test, or targeted command.
- Broaden only when shared code, public contracts, packaging, data, config, or deploy behavior changed.
- Capture the exact command and result.
- If the proof cannot run, state the blocker and what evidence is still missing.

Do not call a proof successful unless it completed and checked the expected behavior.

## 5. Name what remains unproven

Close with one precise verdict:

- `proven` - the evidence directly supports the claim.
- `partially proven` - important evidence passed, but scope is limited.
- `not proven` - evidence is missing, weak, failed, or does not reach the claim.

List what remains unverified; that is the truth boundary.

## Output

Use headings, bullets, and blank lines.

```markdown
**Claim**
- ...

**Proof**
- Command: `...`
- Why this proves it: ...

**Result**
- ...

**Verdict**
- `proven` / `partially proven` / `not proven`

**Unproven**
- ...
```

For code changes, include the exact test, command, reproduction, CI result, or manual check that supports the verdict.

## Guardrails

- Do not use old verification output as proof unless it was rerun for this claim in the current session.
- Do not accept "tests pass" unless the relevant tests are named.
- Do not accept a regression test unless it would fail without the fix.
- Do not use a build, lint, or typecheck result as proof of runtime behavior unless that is the claim.
- Do not claim behavior from code inspection alone when a runnable proof exists.
- Do not defend the claim because you authored the fix or chose the test.
- Do not hide failed or skipped verification.
- Do not broaden the claim beyond what the proof actually covers.
