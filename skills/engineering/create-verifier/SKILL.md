---
name: create-verifier
description: Create a project-specific verify-project skill from the repository's existing launch commands and test harness. Use when a project needs a repeatable web, API, or CLI verification guide that a fresh agent session can run, with durable evidence and cleanup.
---

# Create Verifier

Build a verification recipe that another session can actually run.

This produces a project skill, not a claim that every feature works. Keep the
first version small: at most three main feature paths and one executed path.
Use the user's chosen model and budget. Extra agents are optional, not a gate.

## 1. Inspect the project and choose the target

Read project instructions, package/build files, existing tests, launch scripts,
health checks, and any current verification guide before writing commands.
Prefer the existing harness and dependencies over adding a parallel framework.
Identify the OS/shell, prerequisites, configuration sources, local data setup,
and the web, API, or CLI entry points that matter to the request.

Write only the requested target(s), relative to the repository root:

| Agent consuming the guide | Project skill directory |
| --- | --- |
| Codex, Pi, OpenCode (shared) | `.agents/skills/verify-project` |
| Claude Code | `.claude/skills/verify-project` |
| Kiro | `.kiro/skills/verify-project` |

Use the current agent's target if clear from the request; otherwise ask only
which target is needed while continuing repository inspection. Do not create
all three by default. Before writing, look for a `verify-project` in the target
and the current runtime's other searched locations to avoid name collisions.
If one exists, read it and show proposed edits before overwriting it; preserve
its useful commands and evidence. Apply only changes the user has authorized.

## 2. Design the smallest useful guide

Read [the output template](references/guide-template.md). Read only the driver
reference needed for the selected app surface:

- [Web](references/web.md): browser interaction with an existing browser harness.
- [API](references/api.md): real requests and contract assertions.
- [CLI](references/cli.md): executable commands, exit status, stdout and stderr.

For a mixed app, read a second driver reference only when the chosen feature
crosses that surface. Keep commands grounded in inspected project files.
Write exact working directories, inputs, expected outputs, readiness checks,
evidence paths, and bounded timeouts. Do not invent a successful run or a tool
that the consuming runtime does not have.

The generated `SKILL.md` must include:

- Portable frontmatter: `name: verify-project`, a specific routing description.
- **Status and scope**: `draft` or `validated`, relevant revision/working-tree
  state, OS/shell, prerequisites, and what was actually exercised.
- **Feature map**: up to three user paths, with entry point, assertion, and
  relevant reference. Label mapped-but-unrun paths explicitly.
- **Launch**: existing command(s), local configuration, owned process/run ID,
  readiness condition and timeout. Refer to configured credentials by name or
  source; never embed secret values.
- **Doctor**: cheap checks distinguishing missing dependencies/auth, wrong
  environment, stale builds, port conflicts, and a reachable app. A successful
  health endpoint does not establish feature behavior.
- **Drive**: the exact steps for each mapped path and observable assertions.
- **Evidence**: durable files with commands, inputs, observed results, exit
  status, revision, environment and timestamps. Include screenshots/traces when
  they prove a UI claim; HTTP responses for API claims; output for CLI claims.
- **Cleanup**: stop only the processes started for this run, remove only owned
  temporary data, and leave evidence readable. Include a check that proves it.

Place project-specific long recipes under the generated skill's `references/`
and link them relative to `SKILL.md`. All required files must ship with the
guide or be stable project paths. Do not point into this creator's install
directory, a previous session's temporary files, or a missing runtime plugin.
Use generic actions such as "open the URL with the available browser harness"
plus concrete selectors and assertions. Avoid Claude-specific tool names or
assuming any one agent's browser, shell, or subagent API.

## 3. Execute one feature, then clean up

Run the guide as written, adjusting it when observed behavior disagrees:

1. Launch and pass Doctor using the recorded configuration.
2. Drive one mapped feature through the real app/API/CLI, including its assertion.
3. Save commands and actual results in the durable evidence directory.
4. Perform Cleanup, including error paths if the run failed.
5. Check the owned process/data is gone and saved evidence still exists and is
   readable. Record that result in the evidence.

Do not broaden "one feature passed" to application acceptance. Do not replace
a blocked UI/API run with a unit test while keeping the same claim. If a
dependency, auth, permission, or runtime blocks execution, deliver the usable
parts as **draft**, record the exact blocker and unrun steps, and continue
independent inspection. No placeholder success receipts.

## 4. Make the handoff testable

Check the generated skill name, frontmatter and every relative reference.
Give a fresh session the repository, target skill path, feature and evidence
location without requiring conversation history. When a cold-session run is
requested, have it load the generated `SKILL.md` and needed references, run the
feature, save new evidence and clean up; keep its result separate from the
creator's run. Do not assert a cold handoff passed unless it ran.

In the existing completion report, link the generated files and evidence,
state the selected target, status, executed feature and cleanup result, and
list mapped-but-unrun paths or blockers. Do not create a second mandatory
report when another engineering skill is already reporting the work.
