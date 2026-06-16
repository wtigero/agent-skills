---
name: council
description: Use when the user asks to convene a council, get a second opinion, or an independent / outside code review, or says "council". Routes a read-only review to an external agent CLI -- Codex, Claude Code, or both -- over git changes, file paths, or pasted content.
---

# Council

No rubber stamps. Bring outside eyes.

Use Council when one model's confidence is not enough. It convenes an
independent, **read-only** review from Codex, Claude Code, or both -- models
outside the one you are working in -- then returns their findings without
merging away disagreement.

## Ritual

Run when the user asks for an outside review, second opinion, or council:

1. **Choose the scope.**
2. **Summon outside reviewers.**
3. **Keep them blind.**
4. **Demand evidence.**
5. **Return the disagreement.**

If the council cannot speak, prepare the brief. The work should not stall.

This skill is **review-only**. Do not fix, patch, refactor, stage, commit, or
edit project files during this skill. A manual review packet is allowed only as
the documented fallback below.

## Review stance (every member must follow)

Prepend this stance to the prompt of every member you invoke:

> Act as an unbiased outside auditor. Do not assume the author's intent was
> correct and do not rubber-stamp. Ground every finding in the actual code --
> cite `file:line` or the exact snippet. No invented, generic, or speculative
> findings; mark anything you cannot verify as `unverified`. You may search the
> web to confirm API/library behavior, current best practices, deprecations, or
> security advisories, and cite the source. Frame findings as recommendations
> with rationale and trade-offs (for example, "X is usually better than Y
> because ..."), tagged by severity: `blocking`, `consider`, or `nit`. Separate
> correctness and security issues from style preferences. The author decides --
> do not demand changes. Review only; do not edit anything.

## Routing -- who reviews

| User says | Run |
| --- | --- |
| `council` / `council both` / engine unspecified | **Both** Codex and Claude, one after the other |
| `council codex ...` | Codex only |
| `council claude ...` | Claude Code only |

Default when no engine is named: **both**. In "both" mode, label the two
outputs `### Codex` and `### Claude`, and keep them independent -- do not feed one
member's review into the other; each reviews the code fresh.

## Prerequisites

- `codex` and `claude` on PATH (`command -v codex`, `command -v claude`).
- Selected members signed in (`codex login status`; Claude Code authed). If one
  member is unavailable, run the rest and prepare a manual review packet for the
  skipped member.

## What to review (scope)

- **Mode A -- git changes:** work already in git (staged, unstaged, committed, or
  a branch). Run from inside the repo.
- **Mode B -- specific files or content:** explicit paths, or pasted/piped
  content. **No `git add`/commit needed.**

Before a Mode A run, confirm there is something to review:
`git status --short --untracked-files=all` plus `git diff --shortstat` and
`git diff --shortstat --cached`. Treat untracked files as reviewable. Only say
"nothing to review" when the relevant status is genuinely empty.

For untracked files, collect their paths from `git status --short
--untracked-files=all` and include them explicitly in the reviewer prompt. Do
not rely on `git diff` alone; it does not contain untracked file contents.

## Commands per member

Pass the **Review stance** as the prompt/instructions in every command below
(shown as `<stance>`).

**Codex** (`codex review` is for read-only review; `codex exec` runs
`--sandbox read-only`. If `codex review` requests write or edit permissions,
stop and use the manual review packet fallback. Web search is on by default --
add the top-level `--search` flag for live results, e.g. `codex --search exec ...`):

```bash
# Mode A -- git changes
codex review --uncommitted "<stance> Review the uncommitted git changes.
  Include untracked paths listed by git status."
# or --base <branch> / --commit <sha>

# Mode B -- paths or piped content
codex exec --sandbox read-only "<stance> Read <paths> and review them."
cat <file> | codex exec --sandbox read-only "<stance> Review the code in <stdin>."
```

**Claude Code** (always headless `-p` + `--permission-mode plan` so it can read
and web-search but cannot edit):

```bash
# Mode A -- git changes
claude -p "<stance> Review the uncommitted git changes (git diff plus untracked
  paths listed by git status)." --permission-mode plan

# Mode B -- paths or piped content
claude -p "<stance> Read <paths> and review them." --permission-mode plan
cat <file> | claude -p "<stance> Review the code from stdin." --permission-mode plan
```

If Claude cannot reach the web in your setup, append
`--allowedTools "WebSearch WebFetch Read Grep Glob Bash(git status:*) Bash(git diff:*)"`.

## Fallback -- manual review packet

If a selected reviewer CLI is missing, not logged in, blocked by sandbox,
unable to run headlessly, or otherwise unavailable, do not pretend the council
ran.

Create a Markdown review packet instead. Prefer returning it in the response. If
the user asks for a file, write it to the requested path; otherwise use
`/tmp/council-review-request.md` rather than adding noise to the repo.

The packet must contain:

1. The review stance.
2. The exact scope to review.
3. Changed files, staged files, and untracked files.
4. Relevant diffs and file contents for untracked files. Use paths only when the
   reviewer can access the same repo checkout.
5. Ready-to-paste prompts for each unavailable reviewer.
6. The exact CLI error that triggered the fallback.

Label it clearly:

```text
Council not run. Manual review packet prepared.
```

Do not present the packet as reviewer output.

## Run it

1. Pick members from the routing table.
2. Pick scope (a git diff/branch -> A; explicit paths or pasted content -> B).
3. For Mode A, confirm there is something to review (see above).
4. Run each selected member's command with the stance prepended. Include
   untracked paths explicitly when they exist. In "both" mode,
   run sequentially.
5. If a member cannot run, produce the manual review packet fallback for that
   member and label it as not reviewed.
6. Return each member's output **verbatim**, under its `### Codex` / `### Claude`
   heading. If the two disagree, show both -- do not merge the disagreement away.

## Boundaries

- Review-only. Codex `review` must not be allowed to edit; Codex `exec` always
  runs `--sandbox read-only`; Claude always `--permission-mode plan`. Never fix,
  refactor, or commit during this skill. If
  the user wants fixes after seeing the council, that is a separate, explicit step.
- Do not invent findings. On a CLI error (not logged in, missing path, empty
  diff), report the exact error and which member produced it.
