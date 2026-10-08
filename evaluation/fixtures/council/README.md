# Review fixture

The explicit review target is `billing.py`; the checkout is intentionally clean.
`review-evidence/` contains synthetic recorded reports for testing aggregation
and disagreement preservation. They are not live CLI output. Reviewer CLIs are
deliberately unavailable in this test environment; invoking them returns a
fixture availability error. Do not install or authenticate reviewers here.
Review only; leave billing.py and the recorded reports unchanged.
