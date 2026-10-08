# Codex full-access follow-up

Original blocked trials remain in the parent results snapshot. Paths are sanitized; raw hashes are in runs.json.

## Codex / verifier

Implementing-agent transcript review: the designated creator and needed references were read. Only the shared project guide was created. The final PowerShell recipe ran the existing unchanged harness, recorded HTTP 201/create/list/persistence, exit 0, owned process/data cleanup and durable evidence. Earlier quoting/exit-code wrapper failures remain recorded. Fresh-session use is assessed separately.

I’ll read the designated project skill and inspect the repository’s existing harness, then build and run the verifier against the create and list task flow.

The repository already has a Python harness that starts the API, creates and lists a task, saves a receipt, and cleans up. I’ll make the skill call that harness and add a bounded runner that records the command outcome and checks the evidence after cleanup.

The first run exposed a Windows PowerShell argument quoting issue: the runner passed the evidence path with extra quote characters, so the harness failed before it could write a receipt. I’ve kept that failed run’s logs and will switch to a repository relative path, then rerun.

The revised runner passed the create and list flow. The harness recorded HTTP 201, the matching task in the list and data file, and cleanup of its server and temporary data. I’ll finish by checking the saved evidence and removing only the probe files I created while fixing the runner.

Created a **validated** [verify-project skill](<EVALUATION>/codex-full-access/workspaces/codex/verifier/candidate/.agents/skills/verify-project/SKILL.md) under `.agents/skills` only. It uses the repository’s existing Python harness.

The [final run evidence](<EVALUATION>/codex-full-access/workspaces/codex/verifier/candidate/artifacts/verification/20261008T045918Z-d764980b/runner.json) records exit code 0: task creation returned 201, the created task appeared in the list, the owned server and temporary data were removed, and the evidence remained readable after cleanup.

Scope is one executed feature path. A separate fresh-session handoff run was not performed.

## Codex / handoff

Implementing-agent transcript review: a distinct native session loaded the generated guide and references, ran a new real create/list feature, saved a new receipt under the requested cold-session evidence location and checked cleanup/evidence survival. It did not edit the generated guide or fixture application/harness.

I’ll read the fixture’s verify-project skill and its required references, run the create-and-list-task check, then inspect the saved evidence and cleanup result.

The skill’s runner creates a timestamped evidence directory. I’ll run it as written, then move this run’s records under `artifacts/verification/cold-session` and check them there.

The new run passed the HTTP and persistence assertions. Its receipt and runner also report that the owned server and temporary data were removed. I’ll move only this new run into `cold-session` and confirm the records remain readable.

**PASS — create-and-list-task.** In this session, I ran the fixture’s verify-project runner. It recorded HTTP 201 for task creation, found the same task in the list, and confirmed it persisted.

The new [receipt](</<EVALUATION>/codex-full-access/workspaces/codex/verifier/candidate/artifacts/verification/cold-session/20261008T050051Z-c4054983/receipt.json>) and [runner record](</<EVALUATION>/codex-full-access/workspaces/codex/verifier/candidate/artifacts/verification/cold-session/20261008T050051Z-c4054983/runner.json>) remained readable after cleanup. The owned server was stopped and its temporary data removed.

**Limit:** This verifies the local HTTP path only. The runner record retains the evidence directory’s original path because I moved the completed run under `cold-session`.
