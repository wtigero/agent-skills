# Output template

Replace placeholders with inspected project commands and actual observations.
Do not keep imaginary routes or empty sections. This is a structure, not proof.

```markdown
---
name: verify-project
description: Verify <project>'s <specific user paths> using its existing <harness>. Use for local behavior checks and repros with saved evidence and cleanup.
---

# Verify <project>

Status: draft | validated
Scope: <revision/dirty state, OS/shell, relevant runtime versions>
Executed: <feature and evidence path, or exact blocker>

## Feature map

| Path | Entry point | Assertion | Recipe | State |
| --- | --- | --- | --- | --- |
| <one of at most three paths> | <URL/command> | <observable result> | [recipe](references/feature.md) | executed / unrun |

## Launch

<working directory, prerequisites/config source, command, owned run/process ID,
readiness check and bounded timeout; for a CLI, any build/setup needed>

## Doctor

<cheap dependency/config/health checks and how to interpret failures>

## Drive

Read only the selected feature reference. Run its steps and assertions against
the actual instance/command started above.

## Evidence

<durable run directory, exact capture commands, provenance and result fields;
record failed checks too; keep secrets out of committed artifacts>

## Cleanup

<stop only owned process, remove owned temporary data, confirm termination,
confirm evidence files remain readable>
```

In the feature reference, include exact inputs, assertions, capture commands,
failure interpretation and any surface-specific prerequisites. A cold session
must not need the creator skill or the conversation to resolve these files.
