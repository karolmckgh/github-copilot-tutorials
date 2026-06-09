#!/bin/sh
# Reference preToolUse review gate (Linux/macOS).
# Blocks `git commit` when the customized review returns VERDICT: FAIL.
#
# Install: copy this file and review-gate.json into .github/hooks/ at the repo
# root, then restart Copilot CLI. Disable by deleting .github/hooks/review-gate.json.

# 1. Recursion guard — the review below starts a nested Copilot that also loads hooks.
if [ -n "$COPILOT_REVIEW_GATE" ]; then
  echo '{}'
  exit 0
fi

# 2. Read the hook payload (JSON describing the tool about to run) from stdin.
PAYLOAD=$(cat)

# 3. Only gate `git commit`. Every other tool call passes through untouched.
case "$PAYLOAD" in
  *"git commit"*) ;;
  *) echo '{}'; exit 0 ;;
esac

# 4. If nothing is staged, there is nothing to review — allow.
export COPILOT_REVIEW_GATE=1
if git diff --cached --quiet 2>/dev/null; then
  echo '{"permissionDecision":"allow"}'
  exit 0
fi

# 5. Run the customized review on the staged changes.
REVIEW=$(copilot --agent=code-reviewer \
  -p "Run 'git diff --cached' to inspect the staged changes, then review them for security and correctness issues. End with a final line that is exactly 'VERDICT: PASS' or 'VERDICT: FAIL'." \
  --allow-tool 'shell(git)' 2>/dev/null)

# 5b. Save the full review so you can read the complete output (not just the short summary below).
LOG_FILE="$(git rev-parse --show-toplevel)/.github/hooks/last-review.log"
printf '%s\n' "$REVIEW" > "$LOG_FILE"

# 6. Deny the commit on a failing verdict; otherwise allow.
if printf '%s' "$REVIEW" | grep -q "VERDICT: FAIL"; then
  SUMMARY=$(printf '%s' "$REVIEW" | tr '\n' ' ' | sed 's/\\/\\\\/g; s/"/\\"/g' | cut -c1-400)
  LOG_ESC=$(printf '%s' "$LOG_FILE" | sed 's/\\/\\\\/g; s/"/\\"/g')
  printf '{"permissionDecision":"deny","permissionDecisionReason":"Code review found blocking issues. Full review saved to: %s | Open it in VS Code: code \"%s\" | Summary: %s"}' "$LOG_ESC" "$LOG_ESC" "$SUMMARY"
else
  echo '{"permissionDecision":"allow"}'
fi
exit 0
