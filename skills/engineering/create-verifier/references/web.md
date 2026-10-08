# Web driver

Inspect the project's browser tests and available browser harness first. Reuse
its startup, test accounts, fixtures and selectors. Do not install a browser
framework merely to write the guide if a suitable harness already exists.

Record the local URL, viewport if relevant, authentication setup by configured
source, and a short path through the UI using stable roles/labels/test IDs.
State assertions on visible user outcomes and relevant persisted/API state.
A page loading or a screenshot alone does not prove a form saved data.

Capture the assertion result and the screenshot/trace that supports the claim.
Document the exact existing test command when automated; when interaction is
manual, describe concrete actions independent of agent-specific tool names.
Bound waits by readiness conditions instead of arbitrary long sleeps. Reuse
existing app processes only if identified; cleanup must leave shared processes
running and close only this run's owned browser contexts/processes and data.
