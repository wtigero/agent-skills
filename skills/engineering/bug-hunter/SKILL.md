---
name: bug-hunter
description: Investigate bugs, intermittent failures, and performance regressions by tracing failure paths and testing competing causes. Use when a reported failure needs diagnosis before choosing a fix.
---

# Bug Hunter

Find the cause. Bring the evidence.

Scale the investigation to uncertainty. A clear, localized failure may need
only a direct repro and one discriminating check. Do not invent competing
hypotheses to fill a quota or require a recital before working.

Reuse relevant repros, traces, and results already established in the task while
their conditions still apply. This skill works without other skills installed.
When a fix is part of the request, continue through verification and cleanup.

## 1. Establish the failure and feedback loop

- Capture the user's exact symptom, expected behavior, trigger, input, and relevant code and environment state.
- Build the smallest runnable check that reaches that symptom: a failing test, API or CLI invocation, trace replay, or focused harness.
- Observe the failure before using the check to claim a fix. Preserve the original scenario when minimizing it; a nearby failure is a different investigation.
- Preliminary hypotheses can guide repro construction, but remain provisional until tested.

If the project has a `verify-project` skill, inspect only the relevant route and
references. Reuse its launch, health check, driver, and cleanup to build a repro
another session can repeat. Otherwise start with the existing project harness.
Record the command, inputs, expected failure, observed result, and evidence path;
launching successfully does not mean the reported feature was reproduced.

If the failure cannot be reproduced, inspect available logs, captured artifacts,
and source paths. State the missing observation and ask only for access or inputs
that cannot be discovered. Continue useful investigation without calling the
failure reproduced or the root cause confirmed.

For intermittent failures, record attempts and failures. Increase the reproduction
rate with controlled repetition or stress when useful, and label altered timing,
concurrency, or instrumentation. Compare results under equivalent conditions;
one clean run does not establish that the bug is fixed.

## 2. Trace the fail path

Follow the trigger through the relevant callers, branches, validation, state,
and external boundaries to the first observed divergence from expected behavior.
Distinguish source-derived expectations from state actually observed at runtime.

- Use a debugger when it can reach the failure efficiently; otherwise use source tracing, captured state, or targeted instrumentation.
- Compare passing and failing cases to identify relevant differences in input, configuration, timing, concurrency, or build state.
- Tag temporary probes with a unique prefix so their observations and cleanup can be tracked. Avoid broad logging that does not distinguish causes.

For performance regressions, establish a comparable baseline before optimizing.
Match workload, data, concurrency, runtime, configuration, and warmup. Use a
profiler, query plan, differential run, or bisect when it answers the current
question. Record repeated measurements and variation before claiming an improvement.

## 3. Test competing causes

Rank the plausible hypotheses supported by the fail path. For each, state:

- How it produces the symptom through the traced path.
- The observation it predicts.
- A result that would reject or materially weaken it.

Show the leading hypotheses and next experiment briefly before running it;
continue without waiting unless information or authorization is actually needed.

Choose the experiment whose outcomes best distinguish the hypotheses. Try a
disproof first when practical, but do not treat surviving it as confirmation.
Change one relevant variable at a time and keep the comparison conditions stable.
A bypass that removes the symptom may identify a path without proving its cause.

## 4. Keep an experiment ledger

Record the baseline and each experiment, including failed or inconclusive runs:

| Run | State and change | Prediction | Observation | Implication |
| --- | --- | --- | --- | --- |
| ... | ... | ... | ... | ... |

Include or link the command, relevant code and environment state, inputs, and
actual result. A setup failure is not evidence about the bug. Keep entries short;
save a scratch artifact for long investigations so the observations survive
context changes.

Check each new hypothesis against earlier observations. If results conflict,
investigate changed conditions or probe effects and refine the explanation.
Do not silently discard a run that contradicts the preferred cause.

Keep the contradictory output itself, not just the latest explanation. Before
fixing, choose a controlled check that would produce different results under
the remaining causes. If only symptom relief is observed, report a mitigation
and leave root-cause confirmation open.

## 5. Establish the cause and fix within scope

Call a cause confirmed only when observations support the proposed mechanism
and a discriminating experiment supports it over the relevant alternatives.
Where practical, prevent the proposed cause and show the original repro passes;
restore it in an isolated check and show the failure returns.

If evidence establishes only a likely cause or a mitigation, say so. Symptom
resolution, root-cause confirmation, and release readiness are separate claims.

When a fix is part of the task:

1. Turn the repro into a regression test when a suitable seam reaches the actual failure pattern. Observe it fail before the fix.
2. Make the smallest change that addresses the supported cause and preserves the required contracts. Observe the regression test pass when one is available.
3. Rerun the original scenario under matching conditions. For intermittent or performance bugs, compare equivalent repeated runs.

If no suitable test seam exists, state that gap and use the strongest available
repro. Do not expand into architecture changes just to satisfy a test requirement.

## 6. Close with evidence

Remove temporary probes and throwaway artifacts introduced for this investigation,
unless they are being retained as a regression test or useful repro. Preserve
pre-existing work and the evidence needed to explain the result.

Report the cause and confidence, decisive experiment, any fix or mitigation,
verification result, and remaining gaps. Include commands or result artifacts.
Reuse applicable evidence and merge this into the existing completion report;
do not create another mandatory report or claim an untested deployment.
