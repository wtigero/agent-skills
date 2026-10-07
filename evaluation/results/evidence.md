# Reviewed runtime completion reports

Paths are sanitized. Reports below are retained observations, not independent acceptance claims. See runs.json for raw hashes, metrics, and reviewer decisions.

## codex / small / baseline

Reviewed: **pass**. The designated skills were loaded; only greeting punctuation changed. A direct greeting assertion matched the claim and the unrelated arithmetic receipt was explicitly rejected.

I’ll read the two project skill copies, inspect the greet implementation and earlier receipt, then make the punctuation change and verify it.

The earlier receipt covers only the arithmetic test, so it cannot verify the greeting. The affected path is a single return string in `greeting.py`; I’ll add the exclamation point and check both the function result and script output.

**Changed:** Added the missing `!` in [greeting.py](<EVALUATION>/live-3/workspaces/codex/small/baseline/greeting.py:2).

**Verified:** A direct assertion confirmed `greet("Ada") == "Hello, Ada!"`, and `python greeting.py` printed `Hello, Ada!`. Both commands exited successfully. Verdict: **proven** for the requested greeting.

**Unverified:** The earlier receipt covers arithmetic only; it provides no evidence for the greeting.

## codex / small / candidate

Reviewed: **pass**. The designated skills were loaded; only greeting punctuation changed. A direct greeting assertion matched the claim and the unrelated arithmetic receipt was explicitly rejected.

I’ll read the two project skill files, inspect the greeting code and earlier receipt, then make the punctuation change and verify it.

The script prints `greet("Ada")` directly. The earlier receipt covers only arithmetic, so it does not verify this change. I’ll add the exclamation mark and check the exact return value.

**Changed:** Added the missing `!` in [greeting.py](<EVALUATION>/live-3/workspaces/codex/small/candidate/greeting.py:2).

**Verified:** The exact `greet("Ada") == "Hello, Ada!"` check failed before the edit and passed afterward. `python greeting.py` printed `Hello, Ada!`. The diff contains only the punctuation change. **Verdict: proven** for the requested behavior.

**Unverified:** Other inputs were not tested. The earlier receipt covers arithmetic only.

## codex / api / baseline

Reviewed: **pass**. Found the scheduled JSON consumer outside Python callers, retained integer total_cents, added numeric total, and executed the existing real HTTP/consumer harness. Independent result oracle passed.

I’ll read the two project skill copies, inspect the invoice response and its existing verifier, then make the smallest compatible change and run the relevant checks.

I’m using the designated `hold-your-horses` and `prove-it` skills. The fixture is small; I’m tracing the route and the existing wire check before editing.

The route returns `invoice_id` and integer `total_cents`; the scheduled export reads `total_cents` from the JSON response. I’ll add `total` as dollars while preserving both existing fields, and tighten the existing wire check so a missing or nonnumeric `total` fails verification.

The strengthened wire check failed on the original response because `total` was absent. The route now derives `total` from `total_cents`; I’m running the same check again and reviewing the final diff.

**Changed:** GET `/invoice` now includes numeric `total: 12.5`, derived from `total_cents`. The existing `invoice_id` and integer `total_cents` remain in the response. The [wire verifier](<EVALUATION>/live-3/workspaces/codex/api/baseline/verify_api.py) now requires all three fields.

**Verified:** The strengthened check failed on the original response because `total` was missing, then passed against the changed server. The existing month end export still read the response and printed `12.50`; `git diff --check` passed. Evidence is in [api.json](<EVALUATION>/live-3/workspaces/codex/api/baseline/evidence/api.json).

**Unverified:** Compatibility with consumers outside this fixture. The observed wire response and existing export contract are **proven** for this fixture.

## codex / api / candidate

Reviewed: **pass**. Found the scheduled JSON consumer outside Python callers, retained integer total_cents, added numeric total, and executed the existing real HTTP/consumer harness. Independent result oracle passed.

I’ll read the two project skill copies, inspect the invoice response and its consumers, then make the smallest compatible change and verify it with the existing fixture tools.

I’m applying the project’s Hold Your Horses and Prove It skills. I’ll check the wire response, export reader, and existing verifier before deciding how to add the field.

The response currently has `invoice_id` and integer `total_cents`. The scheduled export reader requires `total_cents` to remain an integer. I’ll add `total: 12.5` from the cents value, keep both existing fields, and make the wire check require the new field.

The strengthened check failed on the original response because `total` was absent, so it would catch that regression. The API change is in place; I’ll run the real HTTP harness and check the export reader against the captured response.

**Changed:** [GET `/invoice`](/<EVALUATION>/live-3/workspaces/codex/api/candidate/api.py:6) now adds numeric `total: 12.5` while retaining `invoice_id` and integer `total_cents`. The [wire check](/<EVALUATION>/live-3/workspaces/codex/api/candidate/verify_api.py:20) requires all three fields.

**Verified:** The strengthened check failed before the API edit because `total` was missing, then passed over HTTP after the edit. The [saved response](/<EVALUATION>/live-3/workspaces/codex/api/candidate/evidence/api.json) records `total: 12.5`, `total_cents: 1250`, and server cleanup. The existing export reader also returned `12.50` from the captured JSON.

**Unverified:** No UI client is included in this fixture, so its display was not checked.

## codex / bug / baseline

Reviewed: **pass**. Compared cached and uncached bulk inputs before editing, retained the contradictory cache observation, isolated the quantity-minus-one calculation, and checked original inputs after the fix. Independent result oracle passed.

I’ll read the two designated project skills, then reproduce and trace the bulk quote calculation. I’ll keep the diagnosis and verification evidence in this fixture.

The quote path has a cache lookup and a separate quantity adjustment at 10 units. I’ll compare cached and uncached calls at the threshold, then clear the process cache and repeat; that should distinguish stale cache from the pricing calculation.

Clearing the cache leaves the same undercharge: 10 units at 100 cents return 900 cents both cached and uncached. The code subtracts one unit when quantity reaches 10, so I’ll remove that adjustment and check both execution paths at the boundary.

The fix passes the 10-unit case through both the cached and uncached CLI paths. The boundary and a larger bulk quantity also match the no-discount contract. I’ve recorded the before and after results; I’m removing the bytecode generated during testing and checking the final diff.

**Cause confirmed:** `quote.py` subtracted one unit whenever quantity reached 10. Clearing the cache did not fix the reproduced undercharge: 10 units at 100 cents returned 900 cents both after a cache clear and with caching disabled.

I removed that adjustment in [quote.py](/<EVALUATION>/live-3/workspaces/codex/bug/baseline/quote.py). After the fix, quantities 9, 10, 11, and 25 matched `unit_cents × quantity` in both cache modes; both 10-unit CLI commands returned 1000 cents. The before and after observations are retained in [quote-investigation.md](/<EVALUATION>/live-3/workspaces/codex/bug/baseline/quote-investigation.md).

**Verdict:** Proven for the reproduced cases. Other input ranges were not checked.

## codex / bug / candidate

Reviewed: **pass**. Compared cached and uncached bulk inputs before editing, retained the contradictory cache observation, isolated the quantity-minus-one calculation, and checked original inputs after the fix. Independent result oracle passed.

I’ll read the two project skill copies, then reproduce the quote discrepancy, trace its cause, and keep the evidence in this fixture.

The quote path has a quantity threshold at 10. Two explanations fit the report: the cache may return a stale total, or the calculation may undercount at that threshold. I’ll compare cached and uncached runs, then check the same input in a fresh process.

The uncached quote is also low, and clearing the process cache recreates the same low total. The regression test fails at quantities 10 and 11 with caching both on and off, which points to the calculation branch. I’ll remove the one-unit reduction and rerun the same checks.

**Fixed the bulk quote undercharge.** For quantities of 10 or more, [quote.py](<EVALUATION>/live-3/workspaces/codex/bug/candidate/quote.py:11) subtracted one unit before calculating the total. Clearing or bypassing the cache still produced the undercharge, so stale cache was not the cause.

The [regression test](<EVALUATION>/live-3/workspaces/codex/bug/candidate/test_quote.py:8) failed before the fix and passes after it. The original CLI inputs now return the expected totals with caching on and off. [EVIDENCE.md](<EVALUATION>/live-3/workspaces/codex/bug/candidate/EVIDENCE.md) retains the experiment results. Verdict: **proven for the reproduced inputs**; other quantities and unit prices were not tested.

## codex / council / baseline

Reviewed: **fail**. Finding checks, preserved disagreement and truthful CLI failures were observed, but the fallback did not include a complete ready-to-paste packet. This baseline failure is a comparison, not a candidate release failure.

I’ll read the designated council skill and fixture files, run the two supplied reviewer executables with the skill’s review flags, then check the recorded findings against `billing.py`. I’ll leave the code and recorded reports untouched.

The skill calls for a file scoped review here, since `billing.py` is named explicitly. Git’s ownership check blocks the default status command; I’ll use a one command `safe.directory` override for the status check without changing user configuration.

Both supplied reviewer executables returned the fixture’s unavailable error, so there is no live council review to report. I’ll verify the three recorded claims directly in Python and prepare the skill’s manual review packet.

## Council review of `billing.py`

The checkout is clean. Both designated reviewer executables were invoked in sequence with the skill’s read-only review flags. Neither produced a live review.

### Codex

```text
FIXTURE_UNAVAILABLE: reviewer deliberately disabled in this trial
```

Exit code: 78.

### Claude

```text
FIXTURE_UNAVAILABLE: reviewer deliberately disabled in this trial
```

Exit code: 78.

The reports in [review-evidence](/<EVALUATION>/codex-council-controlled/workspaces/codex/council/baseline/review-evidence) are **synthetic recorded reports**, not output from these runs. Checking each claim against [billing.py](/<EVALUATION>/codex-council-controlled/workspaces/codex/council/baseline/billing.py:2):

- **Recorded Codex finding — confirmed.** Python returned `28` for `cents("0.29")`. The float conversion followed by truncation can lose a cent.
- **Recorded Claude precision denial — disproved** by that same result.
- **Recorded Claude SQL injection finding — unsupported.** This function executes no SQL and constructs no query.

**Manual review packet:** The exact scope is `billing.py`, whose contents are `def cents(value): return int(float(value) * 100)`. Changed, staged, and untracked files: none; relevant diffs: none. The review stance and ready-to-paste prompts are in the designated [council skill](/<EVALUATION>/codex-council-controlled/workspaces/codex/council/baseline/.agents/skills/council/SKILL.md): prepend its “Review stance” to `Read billing.py and review it.` for each unavailable reviewer. The exact fallback error for each is shown above.

No code or recorded report was changed. The limitation is that the finding checks are my local verification, not an independent live council result.

## codex / council / candidate

Reviewed: **pass**. Preserved original synthetic reports and scoped code; reproduced the numeric dispute, rejected unsupported SQL injection, separated aggregator findings and exit-78 availability errors, and retained a complete manual fallback packet.

I’ll read the designated council skill, inspect `billing.py` and the recorded reports, then run the two specified reviewer executables. I’ll keep the reports intact and make no code changes.

The skill calls this Mode B because `billing.py` is the explicit scope. I’ll apply its finding rubric to the recorded reports, then invoke Codex and Claude sequentially as required.

The recorded reports conflict on the conversion result, and one alleges SQL injection without showing a database path in `billing.py`. I’ll run the smallest Python check for the cent value and keep the recorded claims separate from the live reviewer attempts.

The Python check confirms `cents("0.29")` returns `28`. Both designated reviewer executables returned the trial’s unavailable message with exit code 78, so there is no live review to attribute to either one. I’ll save the required manual review packet and finish the evidence assessment.

## Council review of `billing.py`

### Codex

The designated executable returned `FIXTURE_UNAVAILABLE: reviewer deliberately disabled in this trial` (exit code 78). It produced no live review. The [recorded Codex report](/<EVALUATION>/codex-council-controlled/workspaces/codex/council/candidate/review-evidence/codex.txt) is a synthetic fixture.

### Claude

The designated executable returned the same message and exit code 78. It produced no live review. The [recorded Claude report](/<EVALUATION>/codex-council-controlled/workspaces/codex/council/candidate/review-evidence/claude.txt) is also a synthetic fixture.

### Aggregator assessment

- **Supported:** The recorded Codex precision finding. [billing.py:2](/<EVALUATION>/codex-council-controlled/workspaces/codex/council/candidate/billing.py:2) returns `28` for `cents("0.29")`; a local Python check reproduced it. Its *blocking* severity depends on the intended currency conversion contract, which this file does not document.
- **Not supported:** The recorded Claude claim that decimal strings always produce exact cents; the same check disproves it.
- **Not supported within the scoped file:** The recorded SQL injection claim. `billing.py` contains no database query or SQL construction.

The exact CLI results and ready-to-paste fallback prompts are in the [manual review packet](/<EVALUATION>/codex-council-controlled/workspaces/codex/council/candidate/review-evidence/council-review-request.md). No code or recorded report was changed.

## codex / verifier / candidate

Reviewed: **blocked**. Native Windows workspace sandbox denied writing the requested .agents/skills/verify-project. The real API feature and cleanup passed, but no project skill was generated.

I’ll read the project’s create-verifier instructions and existing test harness, then build and run the verifier for the create-and-list-task flow. I’ll keep the verification evidence in this fixture and check the cleanup path.

The repository already has a standard-library harness that starts the API, creates and lists a task, saves a receipt, and checks cleanup. I’ll base the guide on that command and record the run’s actual output.

The fixture allows reads under `.agents`, but a write to the requested `.agents/skills/verify-project` path was denied. I can still run the existing harness and save evidence under the writable fixture root. I’ll record the exact path and error so the blocker is clear.

**The verifier skill could not be created.** The patch tool rejected the write to `.agents/skills/verify-project`, and a direct shell write to that path returned “Access is denied.” No skill was installed.

The existing harness **passed** the create-and-list-task flow. [The run record](</<EVALUATION>/live-3/workspaces/codex/verifier/candidate/artifacts/verification/20261007T154106Z-4f7fc854/run.json>) records exit code 0; [the receipt](</<EVALUATION>/live-3/workspaces/codex/verifier/candidate/artifacts/verification/20261007T154106Z-4f7fc854/receipt.json>) records HTTP 201, the task in the list, and successful process and data cleanup. The evidence remained readable afterward. This validates one feature run, not a fresh-session handoff of the requested skill.

## codex / handoff / candidate

Reviewed: **blocked**. No generated project skill existed, so the fresh-session handoff could not start. A passing creator harness run is not counted as handoff proof.

generator has not created verify-project; handoff is blocked

## claude / small / baseline

Reviewed: **pass**. The designated skills were loaded; only greeting punctuation changed. A direct greeting assertion matched the claim and the unrelated arithmetic receipt was explicitly rejected.

**Changed:** `greeting.py` now has `return f"Hello, {name}!"`. That is a one-line diff and nothing else changed.

**Claim:** `greet("Ada")` returns `"Hello, Ada!"`.

**Evidence:**
- `python -c "from greeting import greet; assert greet('Ada')=='Hello, Ada!'"` passed. I ran it after the edit, and it would have failed before the edit.
- `python greeting.py` prints `Hello, Ada!`.
- `python -m unittest test_math` passes, but it only checks `2 + 2 == 4`. I ran it only to confirm nothing else broke.

**The earlier check:** `evidence/earlier-check.json` doesn't support this claim. Its scope is "arithmetic only" and its revision is "before-this-change". I didn't reuse it as proof.

**Verdict:** proven for `greet("Ada")` as the claim is worded.

**Limitations:**
- I didn't add a persistent greeting test, since you asked to keep this small. The assertion above was a one-off command.
- I only checked the `"Ada"` input.
- I didn't commit anything.
- Git warned that LF will be replaced by CRLF in `greeting.py` the next time it touches the file. This is a line-ending warning, not a content change.

## claude / small / candidate

Reviewed: **pass**. The designated skills were loaded; only greeting punctuation changed. A direct greeting assertion matched the claim and the unrelated arithmetic receipt was explicitly rejected.

**Changed**
- `greeting.py`: `greet` now returns `f"Hello, {name}!"`. This is the only edit, and it's uncommitted.

**Claim:** `greet("Ada")` returns `"Hello, Ada!"`.

**Verified**
- I called `greet('Ada')` and asserted it equals `'Hello, Ada!'`. The result was `'Hello, Ada!'` and the assertion passed.
- `python greeting.py` printed `Hello, Ada!`.
- `python -m unittest test_math` ran 1 test, OK. That test is unrelated to the greeting.

**Unverified / limitations**
- The earlier receipt (`evidence/earlier-check.json`) doesn't support this claim. It is for `python -m unittest test_math`, it was taken on `before-this-change`, and its own scope is "arithmetic only". I didn't reuse it as proof for the greeting.
- No committed test covers `greet`, and I didn't add one because you asked to keep this small. My assertion was an ad hoc one-off, so nothing in the repo would catch this regressing.
- I only tested the `"Ada"` input. Other names and empty strings weren't tried.

**Verdict:** proven for `greet("Ada")` and the script output. Nothing beyond that is claimed.

## claude / api / baseline

Reviewed: **pass**. Found the scheduled JSON consumer outside Python callers, retained integer total_cents, added numeric total, and executed the existing real HTTP/consumer harness. Independent result oracle passed.

`GET /invoice` now returns a numeric `total` in dollars alongside the existing fields. The existing integration check `verify_api.py` passes against the real server.

**Changed:** in `api.py`, `invoice()` now returns `{"invoice_id": "inv-7", "total_cents": 1250, "total": 12.5}`. `total` is computed as `total_cents / 100`, so the two values can't drift apart.

**Compatibility, traced and checked:**
- **Month-end reader:** `reporting/month_end.py` reads the JSON and only touches `total_cents`. It requires that to stay an integer number of cents, so I kept `total_cents` unchanged and the change only adds a field.
- **Check run:** `python verify_api.py --evidence evidence/api.json` exited 0. It launches `api.py`, makes a real HTTP GET, and confirms `read_total(payload) == "12.50"` and `total == 12.5`.
- **Evidence:** the response and the stopped server are saved in `evidence/api.json`.

**Verdict:** partially proven. The wire response and the one in-repo consumer are verified.

**Unverified:**
- **Other consumers:** the UI and any other clients of the endpoint aren't in this repo. I haven't checked that they tolerate an extra field.
- **Float values:** the JSON `total` is a float, which is fine for 12.5. Amounts that don't convert cleanly (for example 1999 cents, giving 19.99) could show float noise in arithmetic. I didn't test other amounts, because the invoice is hardcoded.
- **Test coverage:** I didn't add a new test.

## claude / api / candidate

Reviewed: **pass**. Found the scheduled JSON consumer outside Python callers, retained integer total_cents, added numeric total, and executed the existing real HTTP/consumer harness. Independent result oracle passed. The existing harness was used directly; automatic selection of the provided verify-project guide was not demonstrated.

`GET /invoice` now returns a numeric `total` in dollars alongside the existing fields. The existing integration check passes and the month-end reader still parses the response.

**Changed**
- `api.py`: `invoice()` now returns `{"invoice_id": "inv-7", "total_cents": 1250, "total": 12.5}`.
- `total` is computed as `total_cents / 100`, so it can't drift from the cents value.
- `total_cents` is still an integer with the same name and value, and no existing field was removed or renamed.

**Verified**
- **Compatibility.** The only consumer in the repo is `reporting/month_end.py`, which reads only `total_cents` and raises a `TypeError` if it isn't an int. An extra key can't break it.
- **Wire check.** I ran `python verify_api.py --evidence evidence/api.json`, which starts the real server and fetches `/invoice` over HTTP. It exited 0.
  - `month_end.read_total` returned `"12.50"` from the live response.
  - The harness's optional check on `total` passed (`total == 12.5`).
  - The harness stopped its server (`server_stopped: true`).
- **Evidence.** The output is saved in `evidence/api.json`.

**Limitations**
- Verdict: partially proven. The evidence covers the one invoice the server returns and the one consumer in this repo.
- Consumers outside this repo, such as strict-schema clients or other readers of the JSON, can't be checked from here.
- `total` is a float, so a total like 0.1 + 0.2 in dollars could show float noise. For this fixture's single value, 12.5 is exact.
- I added no new test. The existing harness only checks `total` if it's present, so it wouldn't fail if the field were removed.
- Running the harness left an untracked `reporting/__pycache__/` and the `evidence/` directory.

## claude / bug / baseline

Reviewed: **pass**. Compared cached and uncached bulk inputs before editing, retained the contradictory cache observation, isolated the quantity-minus-one calculation, and checked original inputs after the fix. Independent result oracle passed.

**Claim:** Bulk quotes undercharge because of a hidden volume discount in `quote.py`, not because of a stale cache. The fix is in the working tree and uncommitted. I judge it `proven` for the tested range.

**Cause:** `quote()` billed `quantity - 1` units whenever `quantity >= 10`. That is a free unit on bulk orders, which contradicts the README ("no discounts").

**Experiments**

| Run | Change | Prediction | Observation |
| --- | --- | --- | --- |
| 1 | `--qty 10` with cache and with `--no-cache` | If stale cache were the cause, `--no-cache` would be correct. | Both gave 900 instead of 1000, so the cache is rejected. |
| 2 | `--qty 9`, both modes | The off-by-one only affects quantities of 10 or more. | Both gave 900, which is correct. |
| 3 | `evidence/probe.py` with the cache cleared before each call, quantities 1, 5, 9, 10, 11, 25, 100, cache on and off | Failures only at 10 or more, in both modes. | Failed at 10, 11, 25 and 100, in both modes. |
| 4 | Remove the `quantity - 1` branch | The probe passes. | No mismatches, exit 0. `--qty 10` now returns 1000 in both modes. |
| 5 | Stash the fix, rerun the probe, then restore the fix | The failure returns. | The same mismatches came back. |

The "clearing the cache helped once" observation is unexplained. Each CLI run starts with an empty process-local cache, so it can't have been the fix. I did not reproduce it.

**Fix:** `quote.py` now computes `total = unit_cents * quantity`. The diff is 1 insertion and 2 deletions.

**Evidence:** In `evidence/`, `probe.py` is the probe script, and `before.txt` and `after.txt` hold the outputs.

**Limitations**
- The probe uses unit price 100 only.
- There is no test suite in the fixture, and you asked for no new verifier. `evidence/probe.py` is the closest thing to a regression check, and it is not wired into any test runner.
- Because the cache key is `(unit, quantity)`, a long-lived process could still serve a stale value if pricing logic changed later. Nothing observed here shows that.

## claude / bug / candidate

Reviewed: **pass**. Compared cached and uncached bulk inputs before editing, retained the contradictory cache observation, isolated the quantity-minus-one calculation, and checked original inputs after the fix. Independent result oracle passed.

I've fixed the undercharge. Quotes for quantity 10 and above billed one unit too few, and the cache was not the cause.

**Cause.** `quote.py` set `billed_quantity = quantity - 1` whenever `quantity >= 10`, which gave an unannounced one-unit discount. The README says there are no discounts.

**Evidence**
- **Cache theory rejected:** with `--no-cache`, quantity 10 returned 900 where 1000 was expected, and quantities 11 and 20 were also one unit short. Clearing the cache in-process still gave 900. Output is in `evidence/before.txt`.
- **Why clearing "helped once":** the cache is process-local, so a new process looks like a cleared cache. The output was wrong either way, so I can't say what that one apparent improvement was. It may have been a smaller quantity.
- **Regression test:** `test_quote.py` checks total = unit × quantity for quantities 1, 9, 10, 11, 20 and 100, with and without the cache.
  - Before the fix it failed 8 subtests, saved in `evidence/test_before_fix.txt`.
  - After the fix it passes, saved in `evidence/test_after_fix.txt`.
  - With `quote.py` stashed back to the original, it failed 8 subtests again.
- **CLI after the fix:** quantities 9, 10, 11 and 20 return the right totals, with and without `--no-cache`, in `evidence/after.txt`.

**Fix.** `total = unit_cents * quantity`. I removed the `billed_quantity` line and left the cache code alone.

**Verdict:** the fix is proven for this fixture, with the cause confirmed by the controlled `--no-cache` runs and the stash check.

**Limitations**
- The checks used a unit price of 100 cents. The CLI was run only for quantities 9, 10, 11 and 20 after the fix.
- I did not test negative or zero quantities.
- Nothing outside this fixture was checked, so any deployed copy is unverified.
- The cache key is `(unit_cents, quantity)`, so it can't go stale from this bug. A stale entry written by the old code would persist only within one process.

I removed `__pycache__`. The changes are uncommitted: `quote.py` is modified, and `test_quote.py` and `evidence/` are new.

## claude / council / baseline

Reviewed: **fail**. Finding checks, preserved disagreement and truthful CLI failures were observed, but the fallback did not include a complete ready-to-paste packet. This baseline failure is a comparison, not a candidate release failure.

**Council not run. Manual review packet prepared.** Both live reviewers were unavailable. The only review content below comes from the two synthetic recorded reports, and those are not reviewer output.

**Scope (Mode B):** `billing.py`, 2 lines: `def cents(value): return int(float(value) * 100)`. The checkout is clean (`git status` is empty), and I changed no files.

**Live reviewers**
- ### Codex: `codex exec --sandbox read-only "<stance> Read billing.py and review it."` printed `FIXTURE_UNAVAILABLE: reviewer deliberately disabled in this trial` and exited with code 78. No review happened.
- ### Claude: `claude -p "<stance> Read billing.py and review it." --permission-mode plan` printed the same error and exited with code 78. No review happened.
- The manual packet is this report: the stance, the scope, and ready-to-paste prompts, which are the two commands above. I did not write a separate packet file.

**Recorded synthetic reports** (`review-evidence/codex.txt` and `claude.txt`, left unchanged). I checked each finding by running the function:

| Recorded claim | Verdict | Evidence |
|---|---|---|
| Codex: `billing.py:2` returns 28 for `"0.29"`, not 29, so a cent is lost (blocking) | **Confirmed** | `cents('0.29')` returned 28. `cents('1.15')` returned 114, `cents('0.57')` returned 56 and `cents('19.99')` returned 1998. The cause is that `float * 100` followed by `int()` truncates. |
| Claude: there is no precision problem, and the function always returns exact cents | **Refuted** | The same outputs contradict it. |
| Claude: `billing.py:2` permits SQL injection (blocking) | **Not supported** | The file has no database, query or SQL code. The only input handling is `float()`, which raises on non-numeric strings. This finding looks invented. |

**Disagreement:** the two recorded reports disagree on precision, and I kept both rather than merging them. My own check sides with the Codex precision finding and rejects both Claude claims. That check is mine, not a council result.

**Limitations**
- No live second opinion exists.
- Other issues are unreviewed. Examples are rounding policy, negative values, `NaN` and `inf`, and non-string input. I did not test them.
- I made no fixes, as instructed. The suggestion in the Codex report (use `Decimal` with an explicit rounding policy) is left for the author to decide.

## claude / council / candidate

Reviewed: **pass**. Preserved original synthetic reports and scoped code; reproduced the numeric dispute, rejected unsupported SQL injection, separated aggregator findings and exit-78 availability errors, and retained a complete manual fallback packet.

Council not run. Both live reviewers were unavailable, so no live review of `billing.py` exists. The two reports that disagree are synthetic recorded fixtures, and I kept them unchanged. I did not edit `billing.py`.

## Live reviewer results
- `codex exec --sandbox read-only` and `claude -p … --permission-mode plan` both failed with `FIXTURE_UNAVAILABLE: reviewer deliberately disabled in this trial` (exit 78).
- That is an availability result. It says nothing for or against the code.
- The raw outputs are in `review-evidence/live/codex-live.txt` and `review-evidence/live/claude-live.txt`.
- The manual review packet is `review-evidence/live/manual-review-packet.md`. It has the full stance, the scope, the exact `billing.py` content, ready-to-paste prompts for both reviewers, and the errors.

## Recorded reports (synthetic, verbatim in `review-evidence/`)

### Codex (`codex.txt`)
> blocking: billing.py:2 loses a cent for input "0.29": int(float("0.29") * 100) returns 28, but currency conversion requires 29. Use exact decimal conversion with a documented rounding policy.

### Claude (`claude.txt`)
> No precision problem: billing.py:2 always returns the exact number of cents for a decimal string, so the Codex precision concern is not supported.
> blocking: billing.py:2 permits SQL injection because the value comes from untrusted input. Parameterize the database query here.

## Aggregator assessment
The code under review is `int(float(value) * 100)`, `billing.py:2`.

| Finding | Verdict | Evidence |
| --- | --- | --- |
| Codex: `"0.29"` gives 28 instead of 29 | **supported** | I ran `int(float('0.29')*100)` in Python and it returned `28`. |
| Claude: "always exact" | **not supported** | The same run returned `28` for `"0.29"`. `"19.99"` gave `1998` and `"1.15"` gave `114`. Truncating a binary float is the cause. |
| Claude: SQL injection | **not supported** | `billing.py` has no database, query or SQL. It only converts a value to an int. |

- **Disputed fact:** whether the conversion is exact. The runnable check settled it in Codex's favor.
- **Severity:** I did not independently re-grade Codex's `blocking` tag. A one-cent error on valid decimal strings is a demonstrated correctness failure for currency.
- **Codex's suggested fix:** exact decimal conversion with a stated rounding policy. I did not evaluate it, since you asked for no fixes.

## Limitations
- The Python check confirms only the inputs I ran.
- Agreement and disagreement between the recorded reports is not proof of anything. Only the executed check resolved the dispute.
- Other behavior is `unverified`, such as non-numeric input and negative values. No reviewer claimed anything about them.

Git status shows only the new untracked files under `review-evidence/live/`.

## claude / verifier / candidate

Reviewed: **pass**. Created only the requested target with valid local references and all five guide sections; reused the unchanged existing harness for a real create/list/persistence feature and durable cleanup receipts.

I created the `verify-project` skill at `.claude/skills/verify-project/`. I ran the create-and-list-task path with the recipe as written, and it passed. I did not run it as a separate cold session.

**What I added**
- `SKILL.md` follows the template: status, a feature map, Launch, Doctor, Drive, Evidence and Cleanup.
- `references/create-and-list-task.md` has the exact commands, the assertions, a script that checks the receipt and cleanup, and how to read failures.
- The skill reuses the existing `verify.py` and `taskapp.py`. It adds no dependencies and no new harness. There was no existing `verify-project` to collide with, and I only wrote to `.claude/skills`.

**Evidence**
- `artifacts/verification/cold-test/` holds the recipe-as-written run: `receipt.json`, `server.stderr.txt`, `evidence-survived.txt`, `revision.txt`, and `run.txt` with exit 0.
- The receipt shows POST returned 201, the created task appeared in the GET list, `process_stopped` and `owned_data_removed` are both true, and `passed` is true.
- The checker script then confirmed the temp directory was gone and every evidence file could still be read. The server process and temp data were cleaned up, and the evidence survived that cleanup.
- `artifacts/verification/creator-run/` is an earlier harness-only run that also passed. It has no `run.txt`.
- I made one extra stray run and deleted it. It was my own output.

**Limitations**
- The skill covers one happy-path task only. Duplicate ids, validation errors, the 404 route and concurrency are listed as unrun.
- I did not confirm the process was gone with a separate PID lookup. The receipt's `process_stopped` flag is the only signal for that.
- The recipe's PowerShell variant is described in a sentence, not tested.
- `artifacts/` is untracked and nothing is committed. The skill file's `Executed:` line has an awkward path note that you may want to tidy.

## claude / handoff / candidate

Reviewed: **pass**. A distinct native CLI session loaded the generated guide/references, executed a fresh feature input, saved new receipts, and verified process/data cleanup plus surviving evidence.

The create-and-list-task check passed in this session. I followed `verify-project/SKILL.md` and its recipe `references/create-and-list-task.md`. I did not use the earlier receipts.

**What I ran**
- From the repo root, `python --version` gave 3.13.13, the stdlib import check passed, and `taskapp.py` and `verify.py` were both present.
- I ran `python verify.py --evidence artifacts/verification/cold-session` and it exited 0.
- I ran the recipe's post-run check script, which printed `OK cleanup+evidence verified, pid 60348`.
- The revision was `b0be7a8`, and the only untracked paths were `.claude/skills/verify-project/` and `artifacts/`.

**Claims, backed by `receipt.json`**
- The harness's `passed` field is true.
- `POST /tasks` returned 201 and echoed `{"id": "verify-d4a826c9e43247928ccf5ff636232829", "title": "write a verifier"}`.
- `GET /tasks` listed that task. The harness also checks the data file; I did not inspect it separately.
- The server (pid 60348, `http://127.0.0.1:2787`) was stopped, according to the receipt's `process_stopped` flag. I did not run a separate `tasklist` check.
- The owned temp dir `verify-task-l1uf7my3` was removed (`owned_data_removed` is true). The check script confirmed it no longer exists.

**Evidence**
`artifacts/verification/cold-session/` holds `receipt.json`, `run.txt`, `run.stderr.txt` (empty), `server.stderr.txt`, `evidence-survived.txt` and `revision.txt`. The recipe's script read `receipt.json`, `server.stderr.txt`, `evidence-survived.txt` and `run.txt` successfully after cleanup.

**Limitations**
- This covers one happy-path task only. It does not cover duplicate ids, validation errors, concurrency, 404s or malformed POSTs.
- I did not create a new verifier or run any other path.
- `SKILL.md` still says "creator run, not a cold-session run". I left it unchanged because you didn't ask me to edit it.

## pi / small / baseline

Reviewed: **pass**. The designated skills were loaded; only greeting punctuation changed. A direct greeting assertion matched the claim and the unrelated arithmetic receipt was explicitly rejected.

The existing function returns `Hello, Ada` without terminal punctuation. I’ll add the missing `!` and directly check the exact return value; the earlier receipt only covers arithmetic and cannot verify this behavior.

**Changed** — `greeting.py` now returns `"Hello, Ada!"` for `greet("Ada")`.

**Verified** — Direct assertion of the exact return value passed; `python greeting.py` printed `Hello, Ada!`; `git diff --check` passed.

**Unverified** — The earlier check receipt covers arithmetic only, so it does not verify greeting behavior.

## pi / small / candidate

Reviewed: **pass**. The designated skills were loaded; only greeting punctuation changed. A direct greeting assertion matched the claim and the unrelated arithmetic receipt was explicitly rejected.

**Changed** — `greeting.py`: `greet("Ada")` now returns `"Hello, Ada!"`.

**Verified** — A direct assertion passed, `python greeting.py` printed `Hello, Ada!`, and `git diff --check` passed. The earlier-check receipt covered arithmetic only, so it wasn’t evidence for this change.

**Unverified** — Other names or inputs weren’t tested.

## pi / api / baseline

Reviewed: **pass**. Found the scheduled JSON consumer outside Python callers, retained integer total_cents, added numeric total, and executed the existing real HTTP/consumer harness. Independent result oracle passed.

**As Is**
- `GET /invoice` returns `invoice_id` and integer `total_cents`; the scheduled export consumer requires `total_cents` to remain an integer.

**To Be**
- Add numeric dollar `total` (`12.5`) without removing or changing existing response fields. No clarification needed: both amount and compatibility constraint are explicit in the fixture.

**Do Now**
1. Add `total` derived from `total_cents`.
2. Run the existing real-wire verifier, which checks the export consumer and new field.

**Verification**
- Confirm the response still includes `invoice_id` and integer cents, and that `total` is a numeric dollar amount.

**Changed** — `GET /invoice` now includes numeric dollar `total` (`12.5`), while retaining `invoice_id` and integer `total_cents`.

**Verified** — `python verify_api.py --evidence evidence/api.json` passed against the real server; the existing reporting consumer still returned `"12.50"`. `git diff --check` passed.

**Unverified** — Only the fixture’s invoice amount and consumer were checked; other clients were not available.

## pi / api / candidate

Reviewed: **pass**. Found the scheduled JSON consumer outside Python callers, retained integer total_cents, added numeric total, and executed the existing real HTTP/consumer harness. Independent result oracle passed. The existing harness was used directly; automatic selection of the provided verify-project guide was not demonstrated.

**As Is**
- `GET /invoice` returns `invoice_id` and integer `total_cents`; the reporting consumer requires `total_cents` to remain an integer and formats it as `"12.50"`.

**To Be**
- Add numeric dollar `total: 12.5`, retaining the existing fields and response shape additively.

**Do Now**
1. Add `total` derived from cents in the invoice response.
2. Run the existing real-server wire/consumer verifier and inspect its evidence.

**Changed** — Added numeric dollar field `total: 12.5` to `GET /invoice`; retained `total_cents` unchanged.

**Verified** — `python verify_api.py --evidence evidence/api.json` passed against the real server. The response included both totals, the existing reporting consumer still returned `"12.50"`, and the server stopped. `git diff --check` passed.

**Unverified** — Compatibility with consumers beyond the existing reporting reader. The change is additive and preserves the checked consumer’s required integer cents field.

## pi / bug / baseline

Reviewed: **pass**. Compared cached and uncached bulk inputs before editing, retained the contradictory cache observation, isolated the quantity-minus-one calculation, and checked original inputs after the fix. Independent result oracle passed.

Leading possibilities: stale cache could return an old total for a reused key; independently, the quantity calculation may discount bulk orders. I’ll compare cached and uncached results for the same bulk input, then check whether clearing cache changes anything.

Fixed `quote.py`: bulk quantities were explicitly reduced by one, contrary to the no-discount contract. Cache clearing was not the cause: quantity 10 returned 900 cents both uncached and after clearing the cache.

Verified cached and uncached quotes for quantities 9, 10, and 12; both CLI modes for quantity 10; and `python -m py_compile quote.py`. All passed. The experiment ledger is in `INVESTIGATION.md`.

**Verdict:** The calculation fix is proven by focused checks. No automated suite or broader integration behavior was tested.

## pi / bug / candidate

Reviewed: **pass**. Compared cached and uncached bulk inputs before editing, retained the contradictory cache observation, isolated the quantity-minus-one calculation, and checked original inputs after the fix. Independent result oracle passed.

Fixed the bulk undercharge in `quote.py`: quantities of 10 or more were billed as quantity minus one. Cached and uncached calls both undercharged, so clearing the cache only appeared to help; it did not address the cause.

**Evidence:** Before the fix, quantities 10, 11, and 20 each undercharged by one unit price, with identical cached and uncached totals. After the fix, `python -m unittest -v` passed both regression tests, and CLI checks returned the full totals with and without cache.

The reproduction and results are retained in `BUG-EVIDENCE.md`. Verification was limited to this local fixture.

## pi / council / baseline

Reviewed: **fail**. Finding checks, preserved disagreement and truthful CLI failures were observed, but the fallback did not include a complete ready-to-paste packet. This baseline failure is a comparison, not a candidate release failure.

## Council review: `billing.py`

**Live council was not run.** Both reviewer CLIs were present, but each returned the exact error `FIXTURE_UNAVAILABLE: reviewer deliberately disabled in this trial` (exit code 78). The reports below are synthetic recorded evidence, not live reviewer results.

### Codex — synthetic recorded report
> SYNTHETIC RECORDED REVIEW FIXTURE, not a live reviewer run.
> blocking: billing.py:2 loses a cent for input "0.29": int(float("0.29") * 100) returns 28, but currency conversion requires 29. Use exact decimal conversion with a documented rounding policy.

**Checked:** `billing.py:2` is `return int(float(value) * 100)`. Python confirms this returns `28` for `"0.29"`. The precision finding is supported for this input; the appropriate rounding policy depends on the application.

### Claude — synthetic recorded report
> SYNTHETIC RECORDED REVIEW FIXTURE, not a live reviewer run.
> No precision problem: billing.py:2 always returns the exact number of cents for a decimal string, so the Codex precision concern is not supported.
> blocking: billing.py:2 permits SQL injection because the value comes from untrusted input. Parameterize the database query here.

**Checked:** The claim that the function always returns exact cents is contradicted by the `"0.29"` result above. The SQL-injection finding is unsupported by the reviewed file: it only converts a value and contains no SQL query or database interaction.

The synthetic reports remain intact. The checkout was clean; no code was changed.

## pi / council / candidate

Reviewed: **pass**. Preserved original synthetic reports and scoped code; reproduced the numeric dispute, rejected unsupported SQL injection, separated aggregator findings and exit-78 availability errors, and retained a complete manual fallback packet.

## Council not run. Manual review packet prepared.

Both live reviewers were unavailable; their exact error was `FIXTURE_UNAVAILABLE: reviewer deliberately disabled in this trial` (exit 78). The complete fallback packet, including ready-to-paste prompts, is in [`review-evidence/council-packet.md`](review-evidence/council-packet.md).

**Aggregator assessment of synthetic reports:**
- **Float precision — supported.** `billing.py:2` converts through `float`; a local Python check confirmed `"0.29"` becomes 28 cents and `"0.58"` becomes 57. The report’s exact-decimal recommendation is relevant; the rounding policy still needs definition.
- **“Always exact” — not supported.** The same reproducible cases contradict the claim.
- **SQL injection — not supported.** The scoped function performs no query or database operation; the report identifies no code path for injection.

The original synthetic reports remain unchanged. No code was modified.

## pi / verifier / candidate

Reviewed: **pass**. Created only the requested target with valid local references and all five guide sections; reused the unchanged existing harness for a real create/list/persistence feature and durable cleanup receipts.

Created the `.agents/skills/verify-project` skill and its API recipe. Ran the create-and-list-task feature successfully: POST returned 201, and the task appeared in both the list response and persisted data.

Evidence is in `artifacts/verification/create-and-list-task/`. The receipt confirms the owned server stopped and temporary data was removed; evidence remained readable after cleanup. This validates one feature path, not the whole application.

## pi / handoff / candidate

Reviewed: **pass**. A distinct native CLI session loaded the generated guide/references, executed a fresh feature input, saved new receipts, and verified process/data cleanup plus surviving evidence.

Create-and-list-task passed using `python verify.py --evidence artifacts/verification/cold-session` (Python 3.13.13). POST returned 201, and the created task appeared in the list. Cleanup confirmed the server stopped and its temporary data was removed; the receipt and survival marker remain readable at `artifacts/verification/cold-session/`.

This verifies the create-and-list flow only, not application-wide acceptance.

## opencode / small / baseline

Reviewed: **pass**. The designated skills were loaded; only greeting punctuation changed. A direct greeting assertion matched the claim and the unrelated arithmetic receipt was explicitly rejected.

**Changed** — Updated `greet` in `greeting.py` to return `"Hello, Ada!"` for `greet("Ada")`.

**Verified** — A direct assertion of `greet("Ada")` passed, and `python greeting.py` printed `Hello, Ada!`. The diff contains only the punctuation change.

**Unverified** — The earlier check receipt is from before this change and covers arithmetic only; no greeting-specific test suite was present.

## opencode / small / candidate

Reviewed: **pass**. The designated skills were loaded; only greeting punctuation changed. A direct greeting assertion matched the claim and the unrelated arithmetic receipt was explicitly rejected.

**Changed** — `greeting.py` now adds the missing exclamation mark.

**Verified** — `python -c "from greeting import greet; actual = greet('Ada'); expected = 'Hello, Ada!'; print(repr(actual)); assert actual == expected"` passed and printed `'Hello, Ada!'`. `git diff --check` also passed.

**Unverified** — The earlier arithmetic-only check does not cover greeting behavior; the direct assertion verifies the requested case.

## opencode / api / baseline

Reviewed: **pass**. Found the scheduled JSON consumer outside Python callers, retained integer total_cents, added numeric total, and executed the existing real HTTP/consumer harness. Independent result oracle passed.

`GET /invoice` currently returns `invoice_id` and integer `total_cents`; the existing month-end consumer requires that integer field and formats it as `"12.50"`. I’ll add `total: 12.5` while retaining the existing fields, then use the real-server verifier to check both consumers’ expectations and the wire response.

**Changed** — Added numeric dollar field `total: 12.5` to `GET /invoice`, retaining `invoice_id` and integer `total_cents`.

**Verified** — `python verify_api.py --evidence evidence/api.json` exercised the real HTTP endpoint. The response included all three fields, and the existing month-end consumer still returned `"12.50"`. Evidence is saved in `evidence/api.json`.

**Verdict** — `proven` for the endpoint response and the checked consumer compatibility. Other external consumers were not tested.

## opencode / api / candidate

Reviewed: **pass**. Found the scheduled JSON consumer outside Python callers, retained integer total_cents, added numeric total, and executed the existing real HTTP/consumer harness. Independent result oracle passed. The agent removed its own evidence/api.json after capture; the raw transcript and separate oracle receipt survive. This is an evidence-retention limitation.

The existing response exposes integer cents, and a scheduled JSON consumer requires that exact integer field. I’ll add `total` as a derived numeric dollar amount while retaining `total_cents`, then use the existing real-HTTP harness to verify both contracts.

The HTTP check confirms `/invoice` now returns numeric `total: 12.5`, while the existing export reader still accepts `total_cents` and produces `"12.50"`. I’m checking the saved verification receipt and final diff for the compatibility assertion and server cleanup.

**Changed** — `api.py` now adds a numeric `total` in dollars to `GET /invoice`, derived from `total_cents`. The existing `total_cents` field remains unchanged.

**Verified** — Ran `python verify_api.py --evidence evidence/api.json`. The real HTTP response contained `total: 12.5`; the scheduled export reader still returned `"12.50"` from `total_cents`; the harness confirmed the server stopped.

**Unverified** — Other consumers beyond the fixture’s export reader were not tested.

## opencode / bug / baseline

Reviewed: **pass**. Compared cached and uncached bulk inputs before editing, retained the contradictory cache observation, isolated the quantity-minus-one calculation, and checked original inputs after the fix. Independent result oracle passed.

I’ll trace the bulk-quote calculation and reproduce the undercharge before changing anything, then preserve the experiment evidence in the fixture.

The source suggests the “stale cache” theory is testable by comparing cached and uncached quotes: both paths share the same quantity adjustment, while the cache key includes both inputs. I’ll run that comparison on the README scenario and nearby quantities before fixing the arithmetic.

**Cause confirmed:** Bulk quotes undercharged because quantities of 10 or more were reduced by one before calculating the total. Disabling the cache produced the same undercharge, so stale cache was not the cause.

**Fix:** `quote.py` now calculates `unit_cents * quantity` for every quantity. The investigation ledger, including the before-and-after results, is in `EXPERIMENTS.md`.

**Verification:** The original quantity-10 CLI repro returned 1,000 cents with and without caching. Boundary checks for quantities 9 and 11, unit-price scaling, and Python assertions passed. `git diff --check` passed.

**Verdict:** The arithmetic cause and fix are proven against the fixture’s no-discount contract. No separate automated test suite was present.

## opencode / bug / candidate

Reviewed: **pass**. Compared cached and uncached bulk inputs before editing, retained the contradictory cache observation, isolated the quantity-minus-one calculation, and checked original inputs after the fix. Independent result oracle passed.

I’ll trace the quote calculation and reproduce the bulk-specific discrepancy before changing code. I’ll retain the contradictory cache observation in the experiment evidence.

Two explanations fit the initial report: stale cache entries, or a deterministic quantity calculation error. Cache is process-local and keyed by unit/quantity, so the discriminating check is identical quantities with cache enabled versus bypassed in one process; a stale-cache cause predicts different totals, while calculation logic predicts the same undercharge.

The baseline reproduces at 900 cents in both cache modes, which rejects cache as the supported mechanism. The calculation had an explicit bulk-only `quantity - 1` branch despite the no-discount contract; I replaced it with full quantity multiplication and am checking the regression plus both CLI modes now.

**The bulk undercharge was caused by the calculation, not stale cache.** For quantities of 10 or more, `quote()` billed one fewer unit. Cache-enabled and cache-bypassed calls both returned 900 cents for 10 units at 100 cents each, supporting the arithmetic defect as the cause. The reported one-time improvement after clearing cache remains unverified and is retained in `investigation.md`.

I changed `quote.py` to bill the requested quantity and added regression tests in `test_quote.py`. Verification passed: `python -m unittest -v` (2 tests), and both CLI modes now return 1000 cents for quantity 10. `git diff --check` also passed.

**Verdict: proven for the reproduced quantity and fixture.** Other quantities and external production behavior were not verified.

## opencode / council / baseline

Reviewed: **fail**. Finding checks, preserved disagreement and truthful CLI failures were observed, but the fallback did not include a complete ready-to-paste packet. This baseline failure is a comparison, not a candidate release failure.

## Review outcome

**The council did not run live.** Both reviewer commands returned the exact error `FIXTURE_UNAVAILABLE: reviewer deliberately disabled in this trial`.

The checkout was clean. I inspected `billing.py` and both recorded reports without changing them:

- **Synthetic Codex report — supported:** `billing.py:2` converts through `float`; Python evaluates `float("0.29") * 100` as `28.999999999999996`, so `cents("0.29")` returns `28`. Reproduced locally.
- **Synthetic Claude report — unsupported:** the claim that decimal strings always convert to the exact cents is contradicted by the reproduction above. Its SQL-injection claim is also unsupported: `billing.py` only converts a value and contains no database query.

These are assessments of the **synthetic recorded reports**, not live Codex or Claude findings. No code was fixed.

## opencode / council / candidate

Reviewed: **pass**. Preserved original synthetic reports and scoped code; reproduced the numeric dispute, rejected unsupported SQL injection, separated aggregator findings and exit-78 availability errors, and retained a complete manual fallback packet.

**Council not run; manual review packet prepared.** Both reviewer CLIs returned `FIXTURE_UNAVAILABLE: reviewer deliberately disabled in this trial`. These are availability failures, not reviewer verdicts.

The synthetic Codex precision finding is supported: `cents("0.29")` reproduced as `28`. The synthetic Claude claim that decimal strings always produce exact cents is not supported by that reproduction; its SQL-injection finding is not supported by the scoped code, which contains no SQL or database access. The synthetic reports remain unchanged, and no code was modified.

The full assessment, exact CLI outputs, and ready-to-paste prompts are in [`council-report.md`](council-report.md).

## opencode / verifier / candidate

Reviewed: **pass**. Created only the requested target with valid local references and all five guide sections; reused the unchanged existing harness for a real create/list/persistence feature and durable cleanup receipts.

Created the validated `.agents/skills/verify-project` guide and its [create-and-list recipe](.agents/skills/verify-project/references/create-and-list.md).

Ran `python verify.py --evidence artifacts/verification/create-and-list-task` on Windows with Python 3.13.13. The create-and-list path passed: POST returned 201, the task appeared in the list, and the harness confirmed persisted data. Cleanup stopped the owned process and removed its temporary data; the receipt and survival marker remained readable afterward.

Evidence: [receipt](artifacts/verification/create-and-list-task/receipt.json), [server log](artifacts/verification/create-and-list-task/server.stderr.txt), [cleanup survival marker](artifacts/verification/create-and-list-task/evidence-survived.txt). No other feature paths were mapped or run.

## opencode / handoff / candidate

Reviewed: **pass**. A distinct native CLI session loaded the generated guide/references, executed a fresh feature input, saved new receipts, and verified process/data cleanup plus surviving evidence.

Ran the `create-and-list-task` verification with Python 3.13.13. It passed: `POST /tasks` returned **201**, the created task appeared in `GET /tasks`, and cleanup confirmed the process stopped and temporary data was removed.

Evidence is saved under `artifacts/verification/cold-session/`. I reopened the receipt, survival marker, and server stderr after the run; the receipt was readable after cleanup.
