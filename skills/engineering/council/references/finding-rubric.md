# Finding rubric

Apply these dimensions independently. Confidence does not determine severity.

| Dimension | Required evidence |
| --- | --- |
| Evidence | An accessible `file:line`, exact snippet, reproducible result, or version-matched primary source. State the trigger, affected path, and observed or source-derived consequence. Mark unchecked external facts `unverified`. |
| Severity | `blocking`: a demonstrated correctness/security/contract failure that prevents the stated outcome. `consider`: a relevant risk or improvement with an explicit condition and tradeoff. `nit`: a style or clarity preference with no claimed behavior failure. Explain the impact rather than escalating by tone. |
| Relevance | Connect the finding to the requested files, change, or acceptance criteria. Distinguish a regression, a pre-existing issue that affects this task, and unrelated work. Do not broaden the scope to justify a finding. |

The aggregator checks every finding against the actual scoped revision, retaining
the original output even when it is wrong. Use `supported`, `unverified`, or `not
supported`, with evidence and any remaining uncertainty. If reviewers reach
different conclusions, show the disputed fact and the check needed to resolve
it. A vote is not proof. A failed reviewer run is an availability result, not an
approval or rejection of the code.

When the disputed behavior is runnable in this checkout, execute the smallest
check that distinguishes the claims and retain its actual output. Repeating a
reviewer's explanation does not resolve the dispute. If the check cannot run,
keep that fact `unverified` and state the missing check.
