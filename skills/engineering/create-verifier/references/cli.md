# CLI driver

Inspect the actual command entry point, build/package scripts, help and existing
CLI tests. Use the installed/project executable and working directory explicitly.
Record shell, environment, inputs/stdin, arguments, expected exit code and the
specific stdout/stderr/file assertion. Quote paths for the recorded shell,
including paths with spaces. Help or a build alone is not a feature check.

Run in an owned temporary working/data directory, keeping durable evidence
outside it. Capture stdout, stderr, exit code, input fixture and output assertions.
When the path has a persistent side effect, read it back with the CLI/project
tools. Cleanup removes only the owned temp directory and processes; then reopen
the captured evidence to show that cleanup did not remove the proof.
