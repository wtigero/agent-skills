---
name: migration-safety
description: Plan, review, or execute risky schema, data, storage, queue, cache, search-index, or production migrations. Use when the user mentions migrations, backfills, database changes, data cleanup, deploy ordering, rollback, irreversible operations, production data, or compatibility between old and new application versions. Forces backup, dry-run, batching, compatibility, validation, and rollback discipline.
---

# Migration Safety

Treat migrations as production operations, not ordinary code edits.

## Workflow

### 1. Classify the migration

Name the type and risk:

- Schema change.
- Data backfill or cleanup.
- Storage or file migration.
- Search index rebuild.
- Queue or stream cleanup.
- Cache key or format change.
- Production config or infrastructure migration.

Identify whether it is reversible, online, idempotent, and compatible with old application versions.

### 2. Map affected readers and writers

Trace every code path that reads or writes the changed data.

Check:

- Old app writing new data.
- New app reading old data.
- Retries and duplicate execution.
- Background jobs, cron tasks, workers, webhooks, consumers.
- Reports, exports, analytics, or admin tools.

If old and new versions can run at the same time, require expand-and-contract unless proven unnecessary.

### 3. Require a restoration point

Before any destructive or hard-to-reverse operation:

- Confirm a backup, snapshot, export, or rollback artifact exists.
- Record when it was taken and what it covers.
- Know the restore command or owner.
- Avoid proceeding on assumptions like "the provider probably has backups."

For read-only planning, state what backup would be required before execution.

### 4. Design the execution plan

Prefer operations that are:

- Bounded and batchable.
- Idempotent.
- Resume-safe.
- Observable.
- Tested on representative data.
- Safe to stop midway.

For large data changes, include batch size, ordering, rate limits, lock risk, timeout handling, and resume cursor.

### 5. Validate before and after

Prepare checks before execution:

- Preflight query or command proving the current state.
- Dry run or sample run when feasible.
- Post-run validation proving the intended state.
- Negative check for rows or records that should no longer exist.
- Application-level smoke test when behavior changes.

Do not call the migration complete until validation passes.

### 6. Report status

Use explicit status:

- `plan only` - no data changed.
- `ready to run` - prerequisites and checks are defined.
- `running` - include batch progress and next checkpoint.
- `validated` - post-checks passed.
- `blocked` - name the missing prerequisite or unsafe assumption.

## Guardrails

- Never run destructive production changes without an explicit restoration point.
- Never assume deploy order is safe; reason through old and new versions.
- Never hide partial execution. If a run stopped midway, report exactly where.
- Never rely only on row counts when data correctness matters.
