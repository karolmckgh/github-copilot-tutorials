# Lesson 6: Agentic Workflows in CLI

**XP: 50** | **Difficulty: Intermediate** | **Time: 25 minutes**

---

## 🎯 Learning Objectives

By the end of this lesson, you will:
- Understand what "agentic" means and how Copilot CLI operates as an autonomous agent
- Know the agentic loop: plan → read → edit → run → verify → iterate
- Master the approval system and know when to use auto-approval
- Execute multi-step tasks entirely through conversational prompts
- Review agentic changes effectively using `/diff`
- Write prompts that guide the agent toward correct, complete solutions

---

## 🤖 What Makes Copilot CLI "Agentic"?

Traditional AI assistants wait for you to tell them what to do at every step. An **agentic** AI is different—it takes initiative. When you describe a goal, Copilot CLI autonomously:

1. 📋 **Plans** the steps needed to accomplish your goal
2. 📖 **Reads** files to understand your codebase
3. ✏️ **Edits** files to implement changes
4. ▶️ **Runs** commands to test, build, or verify
5. 🔍 **Verifies** the results of its actions
6. 🔄 **Iterates** to fix problems and refine the solution

This means you can describe a high-level goal—like "add input validation to the signup form"—and Copilot will figure out which files to read, what changes to make, how to test them, and how to fix any issues that come up.

**The key difference:** You describe *what* you want, not *how* to do it step by step.

---

## 🔄 The Agentic Loop

Every agentic task follows a cycle. Here's how Copilot CLI thinks:

```
┌──────────────────────────────────────────────────────┐
│                  THE AGENTIC LOOP                    │
│                                                      │
│   ┌──────────┐                                       │
│   │ DESCRIBE │  You tell Copilot what you want       │
│   └────┬─────┘                                       │
│        ↓                                             │
│   ┌──────────┐                                       │
│   │   PLAN   │  Copilot breaks it into steps         │
│   └────┬─────┘                                       │
│        ↓                                             │
│   ┌──────────┐                                       │
│   │   READ   │  Reads relevant files & context       │
│   └────┬─────┘                                       │
│        ↓                                             │
│   ┌──────────┐                                       │
│   │   EDIT   │  Makes code changes (asks approval)   │
│   └────┬─────┘                                       │
│        ↓                                             │
│   ┌──────────┐                                       │
│   │   RUN    │  Runs tests/commands (asks approval)  │
│   └────┬─────┘                                       │
│        ↓                                             │
│   ┌──────────┐     ┌──────────┐                      │
│   │  VERIFY  │────→│   DONE   │  All checks pass!    │
│   └────┬─────┘     └──────────┘                      │
│        │ Issues?                                     │
│        ↓                                             │
│   ┌──────────┐                                       │
│   │   FIX    │  Goes back to EDIT or RUN             │
│   └────┬─────┘                                       │
│        │                                             │
│        └──→ (loops back to EDIT)                     │
└──────────────────────────────────────────────────────┘
```

### What This Looks Like in Practice

When you say: *"Add a function that reverses a string, with tests"*

Copilot will:
1. **Plan:** "I'll create the function, then write tests, then run them"
2. **Read:** Check existing files to understand the project structure
3. **Edit:** Create the function file → ⚠️ *asks your approval*
4. **Edit:** Create the test file → ⚠️ *asks your approval*
5. **Run:** Execute the tests → ⚠️ *asks your approval*
6. **Verify:** Check if tests pass
7. **Fix:** If tests fail, edit the code and re-run

This entire flow happens in a single conversation—you just approve or adjust along the way.

---

## 🔐 The Approval System

Copilot CLI doesn't make changes silently. It uses an **approval system** to keep you in control. Before any action with side effects, you'll see a prompt asking for permission.

### Types of Approvals

| Action | What Copilot Asks | Risk Level |
|--------|-------------------|------------|
| **File Edit** | "Allow edit to `src/utils.js`?" | 🟡 Medium |
| **File Creation** | "Allow creation of `tests/utils.test.js`?" | 🟢 Low |
| **Shell Command** | "Allow `npm test`?" | 🟡 Medium |
| **Destructive Command** | "Allow `rm -rf build/`?" | 🔴 High |

### How to Respond to Approvals

When Copilot asks for approval, you can:

- ✅ **Approve** — Let it proceed with the action
- ❌ **Deny** — Skip this action (Copilot will adapt)
- 💬 **Modify** — Ask Copilot to change its approach before proceeding

### Example Approval Flow

```
Copilot: I'll create a new file `src/validators.js` with input validation helpers.

📝 Allow creation of src/validators.js?
> Yes

Copilot: Now I'll add the validation import to `src/app.js`.

📝 Allow edit to src/app.js?
> Yes

Copilot: Let me run the tests to make sure everything works.

💻 Allow command: npm test?
> Yes

Copilot: ✅ All 24 tests passed. The validation is working correctly.
```

---

## ⚡ Auto-Approval with `/allow-all`

Tired of approving every single action? The `/allow-all` command tells Copilot to proceed without asking for permission.

```
> /allow-all
```

### When It's Safe ✅

- You're working on a personal project or scratch branch
- The task is well-defined and low-risk (e.g., "add comments to this file")
- You plan to review all changes with `/diff` afterward
- You're in a sandboxed or disposable environment

### When to Be Careful ⚠️

- Working on shared/production code
- The task involves deleting files or running destructive commands
- You're not sure what changes Copilot might make
- The task is broad or ambiguous

**Pro Tip:** Even with `/allow-all` enabled, always review changes with `/diff` before committing. Trust but verify!

---

## 🛠️ Multi-Step Task Execution

The real power of agentic workflows is handling complex, multi-step tasks. Let's look at two common scenarios.

### Scenario 1: Adding a New Feature

**Your prompt:**
> "Create a utility function called `parseCSV` that takes a CSV string and returns an array of objects. Each row should become an object with column headers as keys. Include error handling for malformed input. Write tests and make sure they pass."

**What Copilot does:**

```
Step 1: Read project structure
        → Checks package.json, existing utils, test setup

Step 2: Create src/parseCSV.js
        → Writes the function with header parsing and error handling

Step 3: Create tests/parseCSV.test.js
        → Writes tests for: valid input, empty string, missing headers,
          malformed rows, special characters in values

Step 4: Run npm test
        → Discovers one test fails (edge case with quoted commas)

Step 5: Fix src/parseCSV.js
        → Updates regex to handle quoted fields

Step 6: Run npm test again
        → ✅ All tests pass
```

### Scenario 2: Finding and Fixing a Bug

**Your prompt:**
> "Users report that the search function returns duplicate results. Find the bug and fix it."

**What Copilot does:**

```
Step 1: Search for the search function
        → Finds searchItems() in src/search.js

Step 2: Read src/search.js
        → Identifies the search logic

Step 3: Analyze the code
        → Spots that results from multiple filters are concatenated
          without deduplication

Step 4: Edit src/search.js
        → Adds deduplication using a Set based on item ID

Step 5: Read existing tests
        → Checks tests/search.test.js for coverage

Step 6: Add a test for duplicates
        → Writes a test that verifies no duplicate IDs in results

Step 7: Run tests
        → ✅ All tests pass, including the new one
```

---

## 💡 Effective Prompting for Agentic Tasks

Agentic prompts are different from simple questions. You're describing a **mission**, not asking a one-off question. Here's how to write great ones:

### 1. Be Specific About the End State

❌ **Vague:** "Add some validation"

✅ **Specific:** "Add email validation to the signup form. The email field should reject inputs without an @ symbol and show the error message 'Please enter a valid email address' below the field."

### 2. Describe Constraints

❌ **Unconstrained:** "Refactor the database module"

✅ **Constrained:** "Refactor the database module to use async/await instead of callbacks. Don't change the function signatures—the public API should stay the same. Keep all existing tests passing."

### 3. Specify What "Done" Looks Like

❌ **Open-ended:** "Improve error handling"

✅ **Clear done state:** "Add try/catch blocks to all API route handlers. Each catch should log the error with the request ID and return a JSON response with `{ error: 'Internal Server Error', requestId: '...' }` and status 500. All existing tests should still pass."

### 4. Break Down Ambiguous Tasks

If your request is too broad, Copilot might go in an unexpected direction. Compare:

❌ **Too broad:** "Set up the project"

✅ **Focused:** "Initialize a new Node.js project with Express. Create a basic server in `src/index.js` that listens on port 3000 and has a health check endpoint at `GET /health` that returns `{ status: 'ok' }`. Add a start script to package.json."

### Prompt Template for Agentic Tasks

Here's a template you can adapt:

```
[What to do]
Create/Fix/Refactor [specific thing] in [specific location].

[How it should work]
It should [behavior description]. When [input/condition], it returns [output].

[Constraints]
- Don't modify [protected files/APIs]
- Use [specific patterns/libraries]
- Keep existing tests passing

[Verification]
Write tests and run them to confirm everything works.
```

---

## 🔍 Reviewing Changes with `/diff`

After Copilot completes an agentic task, **always review what changed**. The `/diff` command shows you every file modification in a familiar diff format.

```
> /diff
```

### What to Look For

| Check | Why It Matters |
|-------|---------------|
| **Correctness** | Does the code actually do what you asked? |
| **Side effects** | Did it change files you didn't expect? |
| **Style consistency** | Does the new code match your project's style? |
| **Completeness** | Is anything missing from the requirements? |
| **Edge cases** | Does the code handle errors and boundary conditions? |
| **Security** | Any hardcoded secrets, unsafe patterns, or vulnerabilities? |

### Example `/diff` Output

```diff
--- a/src/utils.js
+++ b/src/utils.js
@@ -12,6 +12,18 @@ function formatDate(date) {
   return `${year}-${month}-${day}`;
 }

+function validateEmail(email) {
+  if (typeof email !== 'string') {
+    return { valid: false, error: 'Email must be a string' };
+  }
+  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
+  if (!emailRegex.test(email)) {
+    return { valid: false, error: 'Please enter a valid email address' };
+  }
+  return { valid: true, error: null };
+}
+
 module.exports = {
   formatDate,
+  validateEmail,
 };
```

**Pro Tip:** If you spot something you don't like in the diff, tell Copilot! Say "Change the email regex to also reject addresses without a TLD" and it will update the code.

---

## ✏️ Exercise: Build a Feature End-to-End

Now it's your turn! Use Copilot CLI's agentic workflow to implement a small feature from scratch—describing, approving, verifying, and reviewing.

### Your Task

Use Copilot CLI to build **one** of the following features (or come up with your own!):

**Option A: Word Counter (Python)**
> "Create a word counter utility in Python somewhere in the exercises folder. It should count how often each word appears in a text."

**Option B: Todo Parser (JavaScript)**
> "Build a function that extracts todo items from markdown text. Save it in the exercises directory."

**Option C: Your Own Idea**
> Pick any small, self-contained feature. Save it to `exercises/cli/06-feature.*` (any extension). Make sure it includes both implementation and tests.

### Steps

1. **Start Copilot CLI** in the repository root
2. **Enter plan mode** — press **Shift+Tab** to switch to plan mode (you'll see `[[PLAN]]` appear before your input). This tells Copilot to create a plan first before executing anything — the key to triggering the full agentic loop.
3. **Paste one of the prompts above** (or write your own) and press Enter
4. **Review the plan** — Copilot will generate a step-by-step plan. Read through it, then say **"go"**, **"start"**, or **"implement it"** to kick off execution.
5. **Watch the agentic loop** — observe how Copilot plans, reads, creates, and runs
6. **Approve or adjust** each action as it comes up
7. **Review with `/diff`** — check the generated code for correctness and style
8. **Fix any issues** — if tests fail, let Copilot iterate to fix them
9. **Verify** — make sure your file exists and tests pass

> 💡 **Why plan mode?** Entering plan mode (Shift+Tab) ensures Copilot creates a structured plan before acting. This is what triggers the full agentic experience — plan → execute → verify → iterate. Without it, Copilot may just answer conversationally instead of building your feature.

### Example Documentation

Save notes about your experience (optional but recommended):

```markdown
# Agentic Workflow Exercise

## Prompt I Used
"Create a Python script at exercises/cli/06-feature.py that..."

## What Copilot Did
1. Read the project structure
2. Created the file with the word_count function
3. Added test cases with assert statements
4. Ran the file — 2 tests failed
5. Fixed the punctuation stripping logic
6. Re-ran — all tests passed

## Approvals I Gave
- File creation: exercises/cli/06-feature.py ✅
- Shell command: python exercises/cli/06-feature.py ✅
- File edit: exercises/cli/06-feature.py ✅ (bug fix)
- Shell command: python exercises/cli/06-feature.py ✅ (re-run)

## What I Learned
- Being specific about edge cases (empty input, punctuation) helped
- Copilot caught and fixed its own bug on the second iteration
- The /diff output made it easy to verify the fix was correct
```

### Bonus Challenges

- 🌟 Try using `/allow-all` and then reviewing everything with `/diff` afterward
- 🌟 Intentionally give a vague prompt first, then refine it—see how the results differ
- 🌟 Ask Copilot to add a feature to your file after the initial implementation

---

## ✅ Verification

You've completed this lesson when:

- [ ] A file matching `exercises/cli/06-feature.*` exists (any extension)
- [ ] The file contains both implementation code and test cases
- [ ] The tests pass when you run the file

**The following file must exist:**
- `exercises/cli/06-feature.*` (any extension)

Run the verification:

```bash
ls exercises/cli/06-feature.* 2>/dev/null && echo "✅ Exercise complete!"
```

---

## 📋 Quick Reference Card

```
┌─────────────────────────────────────────────────────┐
│           AGENTIC WORKFLOWS CHEAT SHEET             │
├─────────────────────────────────────────────────────┤
│                                                     │
│  THE LOOP:  Describe → Plan → Read → Edit →         │
│             Run → Verify → Fix/Done                 │
│                                                     │
│  APPROVALS:                                         │
│    File Edit ........ "Allow edit to file?"    🟡    │
│    File Create ...... "Allow creation of file?" 🟢   │
│    Shell Command .... "Allow command: ...?"    🟡    │
│    Destructive ...... "Allow rm/delete ...?"   🔴    │
│                                                     │
│  AUTO-APPROVE:                                      │
│    /allow-all         Skip all approval prompts     │
│                                                     │
│  REVIEW CHANGES:                                    │
│    /diff              Show all file changes         │
│                                                     │
│  PROMPTING TIPS:                                    │
│    ✅ Describe the end state clearly                │
│    ✅ Set constraints (don't change X, use Y)       │
│    ✅ Say "write tests and run them"                │
│    ❌ Don't be vague ("make it better")             │
│    ❌ Don't skip review (/diff after every task)    │
│                                                     │
│  COMMON AGENTIC PROMPTS:                            │
│    "Create [feature] with tests, run them"          │
│    "Find and fix the bug causing [symptom]"         │
│    "Refactor [file] to [pattern], keep tests green" │
│    "Add [feature] to [file], don't change [other]"  │
│                                                     │
└─────────────────────────────────────────────────────┘
```

---

## 🎉 Summary

You've learned how to leverage Copilot CLI as an autonomous agent!

| Concept | What You Learned |
|---------|-----------------|
| **Agentic Loop** | Copilot plans, reads, edits, runs, and verifies autonomously |
| **Approval System** | You control every side effect—file edits, commands, creation |
| **Auto-Approval** | `/allow-all` skips prompts; use on safe tasks, review with `/diff` |
| **Multi-Step Tasks** | Copilot handles complex workflows: create → test → fix → verify |
| **Effective Prompts** | Describe end state, set constraints, specify "done" criteria |
| **Reviewing Changes** | `/diff` shows all modifications—check correctness, style, side effects |

### Key Takeaways

- 🤖 **Agentic = autonomous.** You describe the goal, Copilot figures out the steps
- 🔐 **Approvals keep you safe.** Every file edit and command requires your permission
- ⚡ **`/allow-all` speeds things up** but always review with `/diff` afterward
- 🎯 **Better prompts = better results.** Be specific about what "done" looks like
- 🔄 **Iteration is built in.** Copilot will fix its own mistakes when tests fail
- 👀 **Always review.** Trust the agent, but verify the output

---

## 📚 Additional Resources

- [GitHub Copilot CLI Documentation](https://docs.github.com/en/copilot/github-copilot-in-the-cli)
- [Copilot CLI Agentic Mode Guide](https://docs.github.com/en/copilot/using-github-copilot/using-copilot-coding-agent)
- [Prompt Engineering for Copilot](https://docs.github.com/en/copilot/using-github-copilot/prompt-engineering-for-github-copilot)

---

## 🚀 What's Next?

Continue to [Lesson 7: Advanced Agentic Workflows — Fleet Mode & TDD](./07-agentic-workflows-advanced.md) to learn how to use `/fleet` for parallel subagents and build full apps with TDD.

---

*You've unlocked one of the most powerful features of Copilot CLI. Agentic workflows turn you from a line-by-line coder into a director—describe the vision, let the agent execute, and review the results. Go build something amazing! 🚀*
