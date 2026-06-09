#!/usr/bin/env pwsh
# Reference preToolUse review gate (Windows, PowerShell 7+).
# Blocks `git commit` when the customized review returns VERDICT: FAIL.
#
# Install: copy this file and review-gate.json into .github/hooks/ at the repo
# root, then restart Copilot CLI. Disable by deleting .github/hooks/review-gate.json.

# 1. Recursion guard — the review below starts a nested Copilot that also loads hooks.
if ($env:COPILOT_REVIEW_GATE) { '{}'; exit 0 }

# 2. Read the hook payload (JSON describing the tool about to run) from stdin.
$payload = [Console]::In.ReadToEnd()

# 3. Only gate `git commit`. Every other tool call passes through untouched.
if ($payload -notmatch 'git commit') { '{}'; exit 0 }

# 4. If nothing is staged, there is nothing to review — allow.
$env:COPILOT_REVIEW_GATE = '1'
git diff --cached --quiet 2>$null
if ($LASTEXITCODE -eq 0) { '{"permissionDecision":"allow"}'; exit 0 }

# 5. Run the customized review on the staged changes.
$review = copilot --agent=code-reviewer `
  -p "Run 'git diff --cached' to inspect the staged changes, then review them for security and correctness issues. End with a final line that is exactly 'VERDICT: PASS' or 'VERDICT: FAIL'." `
  --allow-tool 'shell(git)' 2>$null | Out-String

# 5b. Save the full review so you can read the complete output (not just the short summary below).
$logFile = Join-Path (git rev-parse --show-toplevel) '.github/hooks/last-review.log'
$review | Out-File -FilePath $logFile -Encoding utf8

# 6. Deny the commit on a failing verdict; otherwise allow.
if ($review -match 'VERDICT: FAIL') {
  $summary = ($review -replace '\s+', ' ').Trim()
  if ($summary.Length -gt 400) { $summary = $summary.Substring(0, 400) }
  $reason = "Code review found blocking issues. Full review saved to: $logFile | Open it in VS Code: code `"$logFile`" | Summary: $summary"
  @{ permissionDecision = 'deny'; permissionDecisionReason = $reason } | ConvertTo-Json -Compress
} else {
  '{"permissionDecision":"allow"}'
}
exit 0
