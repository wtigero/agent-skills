# API driver

Start with existing API integration tests, request collections or project
scripts. Choose a local/test instance and fixture supported by the repository.
Record base URL, method, path, headers by configured source, body, expected
status and exact contract assertions. Reach the real handler and consumer shape
when that is the claim; a mock returning the expected object does not prove it.

Save a redacted request/response, status, command exit code and assertion result.
For state changes, check the read-back and isolate data with an owned identifier.
Keep cleanup scoped to that identifier; record whether it succeeded. If auth or
external services block the real call, label the path unrun and the guide draft
instead of substituting a health endpoint or fabricated response.
