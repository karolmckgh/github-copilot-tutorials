# Lesson 10: Code Review — Review, Customize, and Automate

> **XP:** 100 | **Difficulty:** Advanced | **Time:** ~40 minutes
> **Prerequisites:** Lesson 8 (Instructions & Skills), Lesson 9 (MCP Servers)

## 🎯 Learning Objectives

By the end of this lesson, you will:
- Run an AI code review with the built-in **`/review`** command
- **Customize** your reviews two ways — a **custom review agent** and **custom instructions** — and know when to use each
- Understand exactly **when** each customization loads into context
- Build a **Copilot CLI `preToolUse` hook** that gates `git commit` behind your customized review, **blocking commits** that contain high-severity issues

---

## Part 1: Reviewing Code with `/review`

Copilot CLI ships with a built-in **Code review** agent. You invoke it with the `/review` slash command, and it analyzes your changes — surfacing real issues while minimizing noise.

```
> /review
```

You can also scope it with a prompt, path, or file pattern:

```
> /review exercises/cli/10-code-review/sample/user_service.py
```

The review agent looks at your **changes** (your working tree / staged diff) and reports problems like security bugs, logic errors, and risky patterns. It does **not** modify your code — it gives you feedback to act on.

> 💡 **Tip:** `/review` is great *before* you commit. Think of it as a second pair of eyes that never gets tired.

We've included a deliberately flawed Python file to review: `exercises/cli/10-code-review/sample/user_service.py`. It hides several classic problems — SQL injection, a hardcoded secret, a bare `except`, missing input validation, a resource leak, and a `== None` comparison. A good review should catch them.

---

## Part 2: Customizing Your Reviews

The built-in review is solid, but every team has its own standards. There are **two** ways to customize code review in Copilot CLI, and they behave very differently. Knowing which to reach for is the key skill in this lesson.

### Option A — A Custom Review Agent (loads on demand)

A **custom agent** is a specialized version of Copilot defined in a Markdown file at `.github/agents/<name>.agent.md`. It has YAML front matter (`name`, `description`, optional `tools`) followed by a prompt that defines its expertise.

```markdown
---
name: code-reviewer
description: Strict reviewer focused on security and correctness. Invoke for code reviews.
---

You are a senior code reviewer. Review the provided changes and report issues
grouped by severity (BLOCKER, HIGH, MEDIUM, LOW). For each issue give the file,
line, the problem, and a concrete fix. Prioritize:
- Security (injection, hardcoded secrets, unsafe deserialization)
- Correctness (logic errors, unhandled errors, resource leaks)
- Missing input validation

End your response with a single line: `VERDICT: PASS` or `VERDICT: FAIL`.
Use FAIL if there is any BLOCKER or HIGH severity issue.
```

You invoke a custom agent by selecting it with `/agent`, naming it in a prompt ("use the code-reviewer agent to review my changes"), or from the command line:

```bash
copilot --agent=code-reviewer -p "Review the staged changes"
```

**When does it load?** Only **when you invoke the agent.** Its instructions never enter your context during normal work — true on-demand scoping, zero pollution. This also makes it perfect for automation (Part 3), because naming the agent guarantees your standards apply.

> ⚠️ **Important:** A custom agent is **not** run by the `/review` command. `/review` always runs the *built-in* code-review agent. To change what `/review` itself does, use Option B.

### Option B — Custom Instructions (tunes the built-in `/review`)

Custom instructions are natural-language rules Copilot loads automatically. The built-in code-review agent **honors them**, so they're the way to customize the `/review` command itself.

A **path-specific** instructions file lives at `.github/instructions/<name>.instructions.md` and uses an `applyTo` glob:

```markdown
---
applyTo: "**/*.py"
---

When reviewing Python code, always flag:
- String-interpolated SQL (use parameterized queries)
- Hardcoded secrets or credentials
- Bare `except:` clauses
- Missing input validation on public functions
- Comparisons to None using `==` (use `is`)
Rank findings by severity and suggest a concrete fix for each.
```

**When does it load?** This is the crucial difference:

| Mechanism | Loads… | Customizes `/review`? |
|-----------|--------|------------------------|
| Repo-wide `.github/copilot-instructions.md` | On **every** request (always-on) | ✅ Yes |
| Path-specific `.github/instructions/*.instructions.md` | When Copilot works on files matching `applyTo` | ✅ Yes |
| Custom agent `.github/agents/*.agent.md` | **Only when the agent is invoked** | ❌ No (separate agent) |

There is **no** mechanism that loads "only when `/review` runs" — instructions are scoped by **path/context**, not by the command. Use a narrow `applyTo` (e.g. `**/*.py`) instead of repo-wide instructions to avoid adding review rules to every unrelated prompt. You can also add `excludeAgent: "code-review"` to a file's front matter to opt it *out* of code review.

### Which should I use?

- **Keep typing `/review`** and want it smarter → **custom instructions** (Option B).
- **Want zero context pollution** and an agent you can automate → **custom agent** (Option A). *Recommended for the hook in Part 3.*

---

## Part 3: A Copilot Pre-Commit Review Hook

Now the capstone: make the review run **automatically** before a commit. Copilot CLI supports **hooks** — shell commands that run at key points in an agent's lifecycle, defined in JSON files at `.github/hooks/*.json`.

The most powerful hook is **`preToolUse`**: it runs *before* the agent executes any tool, and it can **allow or deny** that tool. We'll use it to intercept `git commit`, run our customized review on the staged changes, and **deny the commit** if the review fails.

### The hook configuration

`.github/hooks/review-gate.json`:

```json
{
  "version": 1,
  "hooks": {
    "preToolUse": [
      {
        "type": "command",
        "bash": ".github/hooks/review-gate.sh",
        "powershell": ".github/hooks/review-gate.ps1",
        "timeoutSec": 120
      }
    ]
  }
}
```

Include **both** `bash` (Linux/macOS) and `powershell` (Windows) keys so the hook works everywhere. On Windows you need PowerShell 7+ (`pwsh --version`).

### What the script does

The `preToolUse` hook receives JSON on **stdin** describing the tool about to run: `{ "toolName": "...", "toolArgs": { ... } }`. The shell tool is `bash` or `powershell`, and the actual command lives in `toolArgs`. The script:

1. **Recursion guard** — if `COPILOT_REVIEW_GATE` is already set, allow and exit (the review itself starts a nested Copilot).
2. Read the JSON; pull out the command string.
3. If it is **not** a `git commit` → output `{}` and exit (allow — the default).
4. If it **is** `git commit` → run the customized review on the staged diff:
   ```bash
   git diff --cached | copilot --agent=code-reviewer \
     -p "Review this staged diff. End with VERDICT: PASS or VERDICT: FAIL." \
     --allow-tool 'shell(git)'
   ```
5. Decide:
   - Review contains `VERDICT: FAIL` → print
     `{"permissionDecision":"deny","permissionDecisionReason":"<summary>"}`
   - Otherwise → print `{"permissionDecision":"allow"}`

### How the decision works

The hook controls the tool by writing JSON to **stdout**:

| Field | Values | Notes |
|-------|--------|-------|
| `permissionDecision` | `"allow"` / `"deny"` / `"ask"` | Whether the commit runs |
| `permissionDecisionReason` | string | **Required** when denying — shown to the agent |

> ⚠️ **`preToolUse` is fail-closed:** if your script crashes, exits non-zero, or times out, the tool is **denied**. That's a safe default for a security gate — but it's why we raise `timeoutSec` and add the recursion guard. Use `--allow-tool` (or `--allow-all-tools`) so the nested review can run without interactive prompts.

> 📝 **Scope:** This hook gates commits made by **the Copilot agent** in this repo, not commits you type yourself in a separate terminal. To turn it off, delete `.github/hooks/review-gate.json` (changes load when the CLI restarts).

---

## 🏋️ Exercise

### Build an automated, customized review gate

1. **Run a baseline review.** In Copilot CLI, review the flawed sample:
   ```
   /review exercises/cli/10-code-review/sample/user_service.py
   ```
   Read what it finds. Then say **"verify"** later and Copilot will save this review to `exercises/cli/10-code-review/review-report.md` for you.

2. **Create your custom review agent.** Now that you've seen the baseline, capture your standards in a reusable agent. Create the file **`.github/agents/code-reviewer.agent.md`** (in the repo root, *not* under `exercises/`) with **exactly** this content:

   ```markdown
   ---
   name: code-reviewer
   description: "Strict code reviewer focused on security and correctness. Invoke for code reviews or from automation."
   ---

   You are a senior code reviewer. Review the provided changes (or staged diff) and
   report issues grouped by severity: **BLOCKER**, **HIGH**, **MEDIUM**, **LOW**.

   For each issue, include:
   - The file and approximate line
   - A one-sentence description of the problem
   - A concrete suggested fix

   Prioritize, in order:
   1. **Security** — injection (SQL/command), hardcoded secrets or credentials,
      unsafe deserialization, plain-text passwords
   2. **Correctness** — logic errors, unhandled exceptions, resource leaks,
      division-by-zero and other unguarded edge cases
   3. **Input validation** — untrusted input reaching sensitive sinks
   4. **Style/robustness** — bare `except`, `== None` instead of `is None`

   Be concise and high-signal. Do not invent issues; only report real problems.
   Do not modify any files — provide feedback only.

   End your response with a single final line that is exactly one of:
   `VERDICT: PASS` or `VERDICT: FAIL`

   Use `VERDICT: FAIL` if there is **any** BLOCKER or HIGH severity issue.
   Otherwise use `VERDICT: PASS`.
   ```

   You can create it yourself, or ask Copilot to do it for you:

   > Create a custom agent at `.github/agents/code-reviewer.agent.md` with YAML front matter (`name: code-reviewer`, a `description`) and a prompt that reviews changes, groups findings by severity (BLOCKER/HIGH/MEDIUM/LOW) with a concrete fix each, and ends with a single line `VERDICT: PASS` or `VERDICT: FAIL` (FAIL if any BLOCKER/HIGH).

   Then **invoke your agent** on the same file and compare it to the baseline:
   ```
   copilot --agent=code-reviewer -p "Review exercises/cli/10-code-review/sample/user_service.py"
   ```
   The exact content above is also saved at `exercises/cli/10-code-review/.solution/code-reviewer.agent.md`.

   > 🔁 **Optional — also tune the built-in `/review`.** Remember a custom agent is *not* used by `/review`. If you also want the `/review` command itself to follow these rules, create `.github/instructions/code-review.instructions.md` (with `applyTo: "**/*.py"`) capturing the same Python checks, then re-run `/review`.

3. **Scaffold the commit-gate hook (using your step-2 agent).** Now **tell Copilot to create the hook for you** — copy-paste this prompt:

   > **Create a Copilot CLI commit-gate hook for me.** Add three files under `.github/hooks/` at the repo root:
   > 1. `review-gate.json` — a `preToolUse` hook (`version: 1`) that runs `review-gate.sh` on bash and `review-gate.ps1` on powershell, with `timeoutSec: 120`.
   > 2. `review-gate.sh` and `review-gate.ps1` — gate scripts that: read the hook payload from stdin; pass through (`{}`) any tool call that isn't `git commit`; otherwise run my **`code-reviewer`** agent on the staged diff via `copilot --agent=code-reviewer -p "...VERDICT: PASS/FAIL..." --allow-tool 'shell(git)'`; output `{"permissionDecision":"deny","permissionDecisionReason":"..."}` when the review ends in `VERDICT: FAIL`, otherwise `{"permissionDecision":"allow"}`.
   >
   > Make it **fail-closed** with a recursion guard (`COPILOT_REVIEW_GATE`), and allow the commit when nothing is staged.

   The hook intercepts the agent's `git commit`, runs your **`code-reviewer`** agent from step 2 on the staged diff, and **denies** the commit on `VERDICT: FAIL`. Copilot should produce the three files below — use them to check its work (the same files are saved in `exercises/cli/10-code-review/.solution/hooks/`):

   **a. `.github/hooks/review-gate.json`** — registers the `preToolUse` hook:
   ```json
   {
     "version": 1,
     "hooks": {
       "preToolUse": [
         {
           "type": "command",
           "bash": ".github/hooks/review-gate.sh",
           "powershell": ".github/hooks/review-gate.ps1",
           "timeoutSec": 120
         }
       ]
     }
   }
   ```

   **b. `.github/hooks/review-gate.sh`** — Linux/macOS gate script:
   ```sh
   #!/bin/sh
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

   # 5. Run YOUR code-reviewer agent (from step 2) on the staged changes.
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
   ```

   **c. `.github/hooks/review-gate.ps1`** — Windows (PowerShell 7+) gate script:
   ```powershell
   #!/usr/bin/env pwsh
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

   # 5. Run YOUR code-reviewer agent (from step 2) on the staged changes.
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
   ```

4. **Restart and test.** Type `/exit`, run `copilot`, then stage the buggy file and ask Copilot to commit it. The gate should **block** the commit and explain why. The full review (not just the short summary in the deny message) is saved to `.github/hooks/last-review.log` — open it with `code .github/hooks/last-review.log`. Fix the issues and watch the commit succeed.

5. **Stuck?** Reference solutions live in `exercises/cli/10-code-review/.solution/`.

> 💡 **Tip:** Start the gate script by handling the "not a git commit" case first — most tool calls should pass straight through untouched.

---

## ✅ Verification

Type **`verify`** or **`check my work`** to verify lesson completion.

**Completion criteria:**
1. A customized review exists — **either** `.github/agents/code-reviewer.agent.md` **or** `.github/instructions/code-review.instructions.md` (with content)
2. `.github/hooks/*.json` exists and defines a `preToolUse` hook that references your review-gate script
3. `exercises/cli/10-code-review/review-report.md` exists (auto-saved from your `/review` run)

---

## 📋 Quick Reference Card

```
┌─────────────────────────────────────────────────────┐
│                  CODE REVIEW                         │
├─────────────────────────────────────────────────────┤
│  Run a review:                                      │
│  • /review                  review all changes      │
│  • /review path/to/file     scope to a path         │
├─────────────────────────────────────────────────────┤
│  Customize:                                         │
│  • Agent:  .github/agents/<name>.agent.md           │
│      → loads ONLY when invoked (--agent=<name>)     │
│      → NOT used by /review                           │
│  • Instructions: .github/instructions/*.md          │
│      → applyTo glob; tunes the built-in /review     │
├─────────────────────────────────────────────────────┤
│  Automate (Copilot hook):                           │
│  • .github/hooks/*.json  →  preToolUse              │
│  • stdin:  { toolName, toolArgs }                   │
│  • stdout: {"permissionDecision":"deny",            │
│             "permissionDecisionReason":"..."}       │
│  • Fail-closed: errors/timeouts DENY the tool       │
└─────────────────────────────────────────────────────┘
```

---

## 📝 Summary

| Topic | Key Point |
|-------|-----------|
| **`/review`** | Built-in code-review agent; analyzes your changes, no edits |
| **Custom agent** | On-demand expertise; not run by `/review`; great for automation |
| **Custom instructions** | Tune the built-in `/review`; loaded by path/context, not by command |
| **`preToolUse` hook** | Intercepts a tool and can allow/deny it — gate commits on review |
| **Fail-closed** | A broken review-gate hook denies the commit — safe by default |

**Key Takeaways:**
- `/review` gives you a fast, low-noise review of your changes
- Use **instructions** to customize `/review`; use a **custom agent** for on-demand, automatable reviews
- Customization loads by **path/context** (instructions) or **on invocation** (agents) — never "only on `/review`"
- A `preToolUse` hook turns review into an enforced **quality gate** for commits

---

## 🚀 Next Steps

🎉 **Congratulations — you've completed the GitHub Copilot Tutorial!**

From your first Copilot Chat conversation to building MCP servers and an automated code-review gate, you've covered the full toolkit. Here's where to go next:

- **Apply it for real** — add a `code-reviewer` agent and a review-gate hook to one of your own repositories
- **Share your standards** — commit your custom instructions and agents so your whole team gets consistent reviews
- **Explore further** — combine hooks with the other lessons (skills, MCP servers, fleet agents) to automate your workflow end to end

Revisit any lesson anytime to refresh your skills. Happy reviewing! 🚀
