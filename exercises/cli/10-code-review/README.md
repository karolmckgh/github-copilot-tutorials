# Exercise 10: Code Review — Review, Customize, Automate

Practice running an AI code review, customizing it to your standards, and turning
it into an automated commit gate using a Copilot CLI hook.

## File Overview

| File | Description |
|---|---|
| `sample/user_service.py` | **Deliberately flawed** Python to review |
| `.solution/code-reviewer.agent.md` | Reference custom review agent |
| `.solution/code-review.instructions.md` | Reference instructions that tune `/review` |
| `.solution/hooks/` | Reference `preToolUse` review-gate (json + sh + ps1) |

## Steps

1. **Baseline review** — in Copilot CLI, run:
   ```
   /review exercises/cli/10-code-review/sample/user_service.py
   ```
   Later, say **"verify"** and Copilot saves the review to `review-report.md`.

2. **Customize** — create one (or both):
   - A custom agent at `.github/agents/code-reviewer.agent.md`
   - Instructions at `.github/instructions/code-review.instructions.md` (`applyTo: "**/*.py"`)

3. **Automate** — create `.github/hooks/review-gate.json` + `review-gate.sh` +
   `review-gate.ps1` that intercept `git commit`, run your review on the staged
   diff, and **deny** the commit on `VERDICT: FAIL`.

4. **Test** — restart the CLI (`/exit`, then `copilot`), stage the buggy file,
   and ask Copilot to commit it. The gate should block the commit. The full review
   is saved to `.github/hooks/last-review.log` (open it with
   `code .github/hooks/last-review.log`); the deny message shows a short summary.

## What a good review should catch in `user_service.py`

- SQL injection (f-string interpolation in queries)
- Hardcoded secret (`API_KEY`)
- Plain-text password storage + missing input validation
- Resource leak (DB connection never closed)
- `== None` instead of `is None`
- Division-by-zero risk
- Bare `except:` that swallows errors

## Stuck?

Reference implementations are in `.solution/`. Disable the gate afterward by
deleting `.github/hooks/review-gate.json` (changes load when the CLI restarts).
