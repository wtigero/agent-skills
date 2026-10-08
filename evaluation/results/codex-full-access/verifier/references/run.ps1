Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$repo = (Resolve-Path (Join-Path $PSScriptRoot '../../../..')).Path
$python = (Get-Command python -ErrorAction Stop).Source
$version = & $python --version 2>&1
if ($LASTEXITCODE -ne 0) { throw "Python check failed: $version" }
$revision = (& git -C $repo rev-parse --short HEAD 2>&1) -join "`n"
$workingTree = (& git -C $repo status --porcelain=v1 2>&1) -join "`n"
$runId = (Get-Date).ToUniversalTime().ToString('yyyyMMddTHHmmssZ') + '-' + [guid]::NewGuid().ToString('N').Substring(0, 8)
$relativeEvidence = "artifacts/verification/$runId"
$evidence = Join-Path $repo $relativeEvidence
New-Item -ItemType Directory -Path $evidence -Force | Out-Null
$stdout = Join-Path $evidence 'harness.stdout.txt'
$stderr = Join-Path $evidence 'harness.stderr.txt'
$startedAt = (Get-Date).ToUniversalTime().ToString('o')
$startInfo = New-Object System.Diagnostics.ProcessStartInfo
$startInfo.FileName = $python
$startInfo.Arguments = "verify.py --evidence $relativeEvidence"
$startInfo.WorkingDirectory = $repo
$startInfo.UseShellExecute = $false
$startInfo.CreateNoWindow = $true
$startInfo.RedirectStandardOutput = $true
$startInfo.RedirectStandardError = $true
$process = [System.Diagnostics.Process]::Start($startInfo)
$stdoutTask = $process.StandardOutput.ReadToEndAsync()
$stderrTask = $process.StandardError.ReadToEndAsync()
$timedOut = -not $process.WaitForExit(30000)
if ($timedOut) {
    & taskkill.exe /PID $process.Id /T /F | Out-Null
    $process.WaitForExit(5000) | Out-Null
}
if ($process.HasExited) { $process.WaitForExit() }
$exitCode = if ($process.HasExited) { $process.ExitCode } else { $null }
[System.IO.File]::WriteAllText($stdout, $(if ($process.HasExited) { $stdoutTask.Result } else { '' }))
[System.IO.File]::WriteAllText($stderr, $(if ($process.HasExited) { $stderrTask.Result } else { 'Harness did not exit after timeout cleanup.' }))
$receiptPath = Join-Path $evidence 'receipt.json'
$receipt = if (Test-Path -LiteralPath $receiptPath) { Get-Content -LiteralPath $receiptPath -Raw | ConvertFrom-Json } else { $null }
$serverStopped = $false
$dataRemoved = $false
$evidenceReadable = $false
if ($null -ne $receipt) {
    $serverStopped = if ($receipt.pid) { $null -eq (Get-Process -Id $receipt.pid -ErrorAction SilentlyContinue) } else { $false }
    $dataRemoved = if ($receipt.owned_data_dir) { -not (Test-Path -LiteralPath $receipt.owned_data_dir) } else { $false }
    $evidenceReadable = $true
}
$runner = [ordered]@{
    started_at = $startedAt
    finished_at = (Get-Date).ToUniversalTime().ToString('o')
    command = "$python verify.py --evidence $relativeEvidence"
    working_directory = $repo
    revision = $revision
    initial_working_tree = $workingTree
    os = [System.Environment]::OSVersion.VersionString
    shell = $PSVersionTable.PSVersion.ToString()
    python = $version -join "`n"
    harness_pid = $process.Id
    timeout_seconds = 30
    timed_out = $timedOut
    exit_code = $exitCode
    receipt_readable = $evidenceReadable
    server_stopped_after_cleanup = $serverStopped
    owned_data_removed_after_cleanup = $dataRemoved
    evidence_readable = $evidenceReadable -and (Test-Path -LiteralPath (Join-Path $evidence 'server.stderr.txt')) -and (Test-Path -LiteralPath $stdout) -and (Test-Path -LiteralPath $stderr)
}
$runnerPath = Join-Path $evidence 'runner.json'
$runner | ConvertTo-Json -Depth 5 | Set-Content -LiteralPath $runnerPath -Encoding utf8
$saved = Get-Content -LiteralPath $runnerPath -Raw | ConvertFrom-Json
Write-Output "Evidence: $evidence"
if ($timedOut -or $exitCode -ne 0 -or $null -eq $receipt -or -not $receipt.passed -or -not $receipt.process_stopped -or -not $receipt.owned_data_removed -or -not $serverStopped -or -not $dataRemoved -or -not $saved.evidence_readable) {
    throw "Verification or cleanup failed; inspect $evidence"
}
Write-Output 'PASS: create-and-list-task; owned process/data removed; evidence readable.'
