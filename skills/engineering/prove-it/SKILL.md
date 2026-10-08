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
4. **Validate the proof.**
5. **Name what remains unproven.**

The point is not every test; it is evidence that still matches the exact claim.

## 1. Find the claim

State one exact claim at a time. Examples:

- The bug is fixed.
- The new behavior works.
- The root cause is confirmed.
- The regression test detects the reproduced failure.
- The change is ready for the stated release scope.
- The migration or data change is validated.

If the claim is vague, narrow it before evaluating evidence.

For each important claim, name the fact that must be true and a check that can
make it false. "Compatible API" may require an existing consumer to parse the
response, while a passing server unit test establishes a different fact. Keep
this mapping brief; a small edit does not need a separate evidence framework.

Separate symptom resolution, root-cause confirmation, and release readiness.
Evidence for one does not establish the others.

## 2. Find the proof

Pick the strongest matching evidence:

| Claim | Strong proof |
| --- | --- |
| Bug fixed | The original failing repro passes after the fix under matching conditions. |
| Root cause confirmed | A controlled experiment distinguishes the cause from alternatives and explains the observed failure. |
| Regression test works | Test fails without the fix and passes with it. |
| New behavior works | Workflow, API call, CLI command, or job reaches the changed path. |
| Build passes | Build command completed with exit 0 for the claimed code and configuration. |
| Ready for stated release scope | Evidence covers the target revision and relevant release requirements; unresolved gaps limit the verdict. |

Prefer proof that reaches real behavior: repro, workflow, API call, job, targeted test, affected build/check, or manual check with exact input, environment, and observed output. If proof is missing, say so; do not use confidence language.

When an existing `verify-project` skill covers the claim, read its relevant route
and reference, then use that recipe or its applicable recorded evidence. Check
the actual assertions: the presence of a verifier, a successful launch, or a
passing unrelated route is not proof of the changed behavior. If no verifier
exists, use the project's current harness; creating one is not a prerequisite.

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

## 4. Validate the proof

Check the evidence's provenance and whether it still applies:

- Relevant code revision or working-tree state.
- Exact command or check, inputs or fixtures, and relevant environment and configuration.
- Completed result and an inspectable output or result artifact.

Reuse a completed check, including CI, when these still match the claim. CI for
HEAD does not validate uncommitted behavior changes. Rerun when relevant code,
inputs, configuration, or environment changed, provenance is missing, or live
state makes the result stale. Do not rerun solely because another skill or
completion message needs the same evidence.

Memory and another agent's summary are pointers to evidence. Inspect the
underlying result before relying on it.

When a new run is needed:

- Start with the original repro, changed test, or targeted command.
- Broaden only when shared code, public contracts, packaging, data, config, or deploy behavior changed.
- Capture the exact command, relevant state, and result.
- If the proof cannot run, state the blocker and what evidence is still missing.

Do not call a proof successful unless it completed and checked the expected behavior.

For intermittent failures, report attempts and failures before and after under
comparable conditions. A run with no failures does not prove the bug cannot recur.

## 5. Name what remains unproven

Close with one precise verdict:

- `proven` - the evidence directly supports the claim.
- `partially proven` - important evidence passed, but scope is limited.
- `not proven` - evidence is missing, weak, failed, or does not reach the claim.

List what remains unverified; that is the truth boundary.

## Output

Keep the output proportional to the claim. Include the claim, evidence, verdict,
and remaining gaps in the existing completion report when one is already being
produced. Use the template below when a separate proof report is useful:

```markdown
**Claim**
- ...

**Proof**
- Command or result artifact: `...`
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

- Do not reuse verification output without checking its provenance and continued applicability.
- Do not accept "tests pass" unless the relevant tests are named.
- Do not accept a regression test unless it would fail without the fix.
- Do not use a build, lint, or typecheck result as proof of runtime behavior unless that is the claim.
- Do not claim behavior from code inspection alone when a runnable proof exists.
- Do not defend the claim because you authored the fix or chose the test.
- Do not hide failed or skipped verification.
- Do not broaden the claim beyond what the proof actually covers.
