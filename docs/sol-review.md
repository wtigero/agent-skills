# Independent Sol review and fixes

The independent Sol static audit of `e5d1d235128582e155394f143cb18003ef465ecb`
identified three actionable findings and one runtime-dependent concern. The
implementing agent reproduced all four and fixed them in
`b522a881831dec3fe5a04d23a918dd6f52fd974a`. The fixes passed the complete offline
suite on Linux and Windows/Git Bash. Sol has not reviewed the fix commit; this
report does not grant publication approval.

## Reviewer record

The authorized reviewer was Codex CLI 0.161.0, requested model `gpt-6.1-sol`,
effort `high`, using the configured ChatGPT subscription. No Astra was used.
Both attempts were fresh ephemeral sessions in `read-only` mode with approval
`never`, plugins/apps/memories/hooks/multi-agent disabled, and no reviewer
inspection of credential files.
The event stream did not provide an observed model field; it is retained as null.

| Attempt | Result | Seconds | Native usage: input / cached input / output / reasoning output |
| --- | --- | --- | --- |
| Native shell review | Unverified: shell startup failed before any read | 29.682 | 84394 / 62464 / 634 / 151 |
| Source packet review | Static audit completed; zero command executions | 586.199 | 124663 / 112128 / 6040 / 4365 |

Usage counters are native telemetry, not additive billing totals. The second
attempt retained a stream-disconnect/retry warning. The first attempt's exact
error was `helper_unknown_error: setup refresh had errors`. It was a native shell
availability failure, not an automatic approval rejection. The fallback kept the
read-only sandbox and supplied numbered source from the pinned commit through
stdin. The packet omitted baseline source, several changed files and parts of
the evidence exports. It therefore did not establish complete diff coverage or
independently validate every behavioral verdict and credential-persistence claim.

The [full reviewer response](../evaluation/results/sol-review/packet-review.md)
preserves the reviewer's original findings, reproductions, expected results and
limitations. The [failed first response](../evaluation/results/sol-review/shell-review.md),
[complete review brief](../evaluation/results/sol-review/review-brief.txt),
[attempt metadata and raw hashes](../evaluation/results/sol-review/attempts.json),
[first stderr](../evaluation/results/sol-review/shell-stderr.txt), and
[packet stderr](../evaluation/results/sol-review/packet-stderr.txt) are retained.
Full raw streams and the source packet remain under the recorded ignored
`.evaluation/` directories. Exported text replaces private path prefixes and
normalizes line endings to LF;
reviewer assessments have not been rewritten to incorporate later fixes.

## Aggregator assessment

These are the implementing agent's adjudications and executed checks, separate
from the independent review. Original line numbers refer to the reviewed commit.

| Finding | Original evidence | Executed result | Correction |
| --- | --- | --- | --- |
| R1: blocking, supported | `evaluation/run.py:244-245` | Linux child ignored SIGTERM; second timeout escaped after 16.014 s, leaving the owned child alive until the probe cleaned it up. | Allow five seconds for graceful shutdown, then SIGKILL only the owned process group. Collect partial streams and return the timeout status. After fix: 6.008 s, `ready` output retained, no escaped timeout. |
| R2: consider, supported | `scripts/skills.py:130-142` | Temporary HOME: shared then Claude both succeeded; shared repeat failed. | Claude installation now checks OpenCode's overlapping discovery roots. Both installation orders reject the second install, preserve original bytes/timestamps, and leave repeats unchanged; `--replace` cannot bypass the alternate-root conflict. |
| R3: consider, supported | `evaluation/run.py:271-280` | Fault-injected invalid baseline reserved a directory without `run.json`. No provider was called. | Config validation and revision resolution run inside the durable blocker path. A blocked record retains the requested baseline ref, null unresolved revision and error. A retry preserves that record and requires a fresh output root. |
| R4: consider, now supported | `scripts/skills.py:157-158` | Installer parsed `prove-it # local copy` literally and installed a duplicate. Pi 1.0.4's native loader accepted the aliased skill as `prove-it`. | Parse plain, single-quoted and double-quoted single-line names with YAML comments; match frontmatter delimiters on their own lines. Ambiguous name syntax stops preflight before writes, using only Python's standard library. |

The reviewer originally marked R4's runtime consequence **unverified**. The
subsequent native Pi loader check resolves that gap for Pi; it does not establish
native parser behavior on the other runtimes. Regression tests exercise all three
supported comment forms and a description containing `---`, original-file
preservation, and ambiguous-name rejection.

Executed evidence:

- [Before probes](../evaluation/results/sol-review/before-probes.json) and
  [after probes](../evaluation/results/sol-review/after-probes.json): temporary
  HOME installers and baseline-resolution fault injection.
- [POSIX before](../evaluation/results/sol-review/posix-timeout-before.json) and
  [after](../evaluation/results/sol-review/posix-timeout-after.json): actual owned
  process ignoring SIGTERM. Every probe cleaned up its own child; no process was
  terminated by name.
- [Native Pi parser proof](../evaluation/results/sol-review/pi-commented-name-proof.json):
  direct `loadSkillsFromDir` call, with no model/provider invocation.
- [Regression tests](../tests/test_evaluation.py) and
  [installer checks](../tests/test_bundle.py) provide repeatable offline checks.

## Fix validation and remaining limits

Both complete runs used `python -m unittest discover -s tests -v` on the fix
source, with temporary HOME and paths containing spaces. CI discovers these tests
automatically; the configured remote matrix has not been run.

| Environment | Result | Seconds | Limits |
| --- | --- | --- | --- |
| Ubuntu/WSL, Python 3.12.3 | 29 passed, 1 skipped, 0 failed | 8.297 | Windows junction case skipped; real symlinks and forced POSIX termination passed. |
| Windows, Python 3.13.13, Git Bash | 25 passed, 5 skipped, 0 failed | 50.224 | Four native symlink privilege cases skipped (WinError 1314), plus POSIX termination; copy and NTFS junction checks passed. |

Full logs: [Linux](../evaluation/results/sol-review/linux-tests.txt),
[Windows](../evaluation/results/sol-review/windows-tests.txt).
[Export hashes](../evaluation/results/sol-review/export-sha256.json) identify
the sanitized evidence files using canonical LF line endings, including on
Windows checkouts; the attempt metadata separately identifies raw
review streams and prompts.

Public skill instructions, references, metadata and the manifest are byte-for-byte
unchanged from the reviewed revision. Existing successful behavioral trials
remain applicable to those skill bytes; they were not rerun after these installer
and failure-path fixes. Offline regression checks qualify the corrected paths,
not new behavioral success on the four model runtimes. The existing Codex default
Windows sandbox block and other qualification limits remain as recorded in
[the qualification report](qualification.md). No push, PR, merge or publication
was performed. No unresolved disagreement requires Astra escalation at this point.
