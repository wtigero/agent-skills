---
name: prove-it
description: Use when work is being claimed complete, fixed, tested, validated, ready to ship, or safe; when a test, reproduction, smoke check, CI result, or verification claim may be weak, missing, misleading, or unrun.
---

# Prove It

No claim without proof.

## Ritual

Run this sequence before saying work is done, fixed, tested, or safe:

1. **Find the claim.**
2. **Find the proof.**
3. **Break the proof.**
4. **Run the proof.**
5. **Name what remains unproven.**

The point is not to run every test. The point is to make sure fresh evidence proves the exact claim being made.

## 1. Find the claim

State the claim in one sentence.

Examples:

- The bug is fixed.
- The new behavior works.
- The regression test proves the old bug cannot return.
- The change is safe to ship.
- The migration or data change is validated.

If the claim is vague, narrow it before evaluating evidence.

## 2. Find the proof

Identify the strongest available evidence for the claim.

The proof must match the claim:

| Claim | Strong proof |
| --- | --- |
| Bug fixed | Original failing reproduction now passes. |
| Regression test works | Test fails without the fix and passes with it. |
| New behavior works | User-visible workflow, API call, CLI command, or job reaches the changed path. |
| Build passes | Build command exits 0 in this run. |
| Safe to ship | Targeted checks pass and risk-specific gaps are named. |

Prefer proof that reaches the real behavior:

- Original failing reproduction now passes.
- Regression test fails before the fix and passes after it.
- User-visible workflow, API call, CLI command, or job reaches the changed path.
- Targeted unit or integration test exercises the real branch and assertion.
- Build, typecheck, lint, or CI result covers the affected surface.
- Manual check is recorded with exact input, environment, and observed output.

If the proof is missing, say so. Do not replace missing proof with confidence language.

## 3. Break the proof

Challenge whether the evidence would catch the problem returning.

Ask:

- Would this proof fail if the bug or broken behavior came back?
- Does it reach the same path the claim depends on?
- Is it asserting the behavior, or only implementation details?
- Are mocks, fixtures, snapshots, or stubs hiding the real failure?
- Does it cover the relevant edge case, data shape, permission, config, or deploy order?
- Did the test become weaker, broader, or more forgiving while making it pass?

If the proof can pass while the claim is false, it is not sufficient proof.

## 4. Run the proof

Run fresh proof in the current session. Old logs, prior CI, cached output, memory, or another agent's success report can guide what to run, but they are not proof by themselves.

Run the narrowest proof that actually supports the claim.

- Start with the original repro, changed test, or targeted command.
- Broaden only when shared code, public contracts, packaging, data, config, or deploy behavior changed.
- Capture the exact command and result.
- If the proof cannot run, state the blocker and what evidence is still missing.

Do not call a proof successful unless it completed and checked the expected behavior.

## 5. Name what remains unproven

Close with a precise verdict:

- `proven` - the evidence directly supports the claim.
- `partially proven` - important evidence passed, but scope is limited.
- `not proven` - evidence is missing, weak, failed, or does not reach the claim.

Then list what remains unverified in plain terms. This is not a failure; it is the truth boundary.

## Output

Keep output scannable. Use headings, bullets, and blank lines; do not collapse the proof into one paragraph.

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
- Do not hide failed or skipped verification.
- Do not broaden the claim beyond what the proof actually covers.
