# Lesson 8: Instructions & Skills

> **XP:** 100 | **Difficulty:** Advanced | **Time:** 30 minutes

## Learning Objectives

By the end of this lesson, you will:
- Understand what custom instructions are and add one to your project
- Understand what custom skills are and how they differ from instructions
- Create a TDD red-green-refactor skill from scratch
- Use your skill to build a calculator with 3 features via TDD
- See the before/after impact of custom instructions after a session restart

---

## Part 1: Custom Instructions

### What Are Custom Instructions?

Custom instructions are a way to **teach Copilot your team's coding standards** before it writes a single line of code. Think of it like onboarding a new team member — you'd share your style guide, explain your architecture, and show them how things are done.

They live in a single file at the root of your repository:

```
.github/copilot-instructions.md
```

Every time Copilot generates code or answers questions, it reads this file first — like permanent background knowledge about your project.

### Why Do Custom Instructions Matter?

Without instructions, Copilot makes reasonable guesses. With instructions, Copilot makes **your** choices.

| Scenario | Without Instructions | With Instructions |
|----------|---------------------|-------------------|
| Error handling | Generic try/catch | Your custom error classes |
| Naming | camelCase (default) | Your preferred convention |
| Tests | Basic assertions | Your AAA pattern with fixtures |
| Workflow | Just writes code | Runs /code-review before finishing |

The difference is **consistency** — tell Copilot once and it remembers for the entire project.

### Best Practices for Instructions

Instructions work best when they are **short, specific, and actionable**:

✅ **Good:** One clear rule per line
```markdown
- As a last step before finishing any implementation, run /code-review on it
```

❌ **Bad:** Vague or overly long
```markdown
- Always make sure to review code carefully and think about edge cases and potential issues before considering the work done, using whatever tools are available
```

**Key principles:**
1. **Be specific, not vague** — "Run /code-review" beats "review carefully"
2. **Keep it short** — Don't stuff the context window; every token counts
3. **One rule, one line** — Easy to scan, easy to follow
4. **Never include secrets** — This file is committed to your repo

---

## Part 2: Custom Skills

### What Are Skills?

Skills are **reusable workflows** that Copilot can invoke on demand. While instructions are passive (always active in the background), skills are **active** — you call them when you need them.

A skill lives in `.github/skills/<skill-name>/SKILL.md` and follows this format:

```markdown
---
name: my-skill
description: "Short description. Invoke when user says 'trigger phrase'."
---

## Purpose

What this skill does in one sentence.

## Instructions

### Step 1: ...
Detailed steps Copilot should follow when the skill is invoked.

### Step 2: ...
More steps...
```

### Instructions vs Skills

| | Custom Instructions | Custom Skills |
|---|---|---|
| **File** | `.github/copilot-instructions.md` | `.github/skills/<name>/SKILL.md` |
| **Activation** | Always on (background) | On demand (user invokes) |
| **Scope** | Global project context | Specific workflow |
| **Example** | "Always run /code-review" | "Guide me through TDD" |

### TDD Red-Green-Refactor

The classic TDD cycle has three steps:

1. 🔴 **Red** — Write a failing test first
2. 🟢 **Green** — Write the minimum code to make it pass
3. 🔵 **Refactor** — Clean up without changing behavior

This is a perfect candidate for a skill — it's a repeatable workflow with clear steps.

---

## Exercise

This exercise has three phases. You'll add an instruction, create a skill, and see both in action.

> **Note for Copilot:** When presenting this lesson, first check if `.github/copilot-instructions.md` already contains "code-review" and if `.github/skills/tdd/SKILL.md` already exists. If both are present, skip Phases 1 & 2 and go directly to Phase 3 — prompt the user to build a simple Python calculator in `exercises/cli/09-calculator/` using the TDD skill (with add, multiply, and divide features). This is the expected flow after the user restarts their session.

### Phase 1: Add a Custom Instruction

1. **Open the instructions file:**
   ```bash
   cat .github/copilot-instructions.md
   ```

2. **Add the following line** to `.github/copilot-instructions.md` before `## Context`:

       **CRITICAL REQUIREMENT — DO NOT SKIP THIS STEP.**

       Run task tool → agent_type: "code-review" every time you create a file with .py or .js extension.

3. **Verify the file was updated:**
   ```bash
   grep "code-review" .github/copilot-instructions.md
   ```

### Phase 2: Create a TDD Skill

Now create a skill that guides TDD red-green-refactor cycles. Instead of writing it manually, **ask Copilot to create it for you** — this way the format is guaranteed to be correct.

1. **Ask Copilot to create the TDD skill:**

   Tell Copilot something like:

   > Create a custom skill called "tdd" at `.github/skills/tdd/SKILL.md` that guides TDD red-green-refactor cycles. It should trigger when I say "tdd", "red green refactor", or "test first". The skill should enforce strict TDD: write a failing test first, then write minimum code to pass, then refactor — running tests between each step.

   Copilot will create the directory and file with the correct YAML front matter and structure.

2. **Find and review the skill:**

   Locate the skill file Copilot created and review its content:
   ```bash
   find .github/skills -name "SKILL.md"
   cat .github/skills/tdd/SKILL.md
   ```

   Verify it has:
   - YAML front matter with `name` and `description`
   - Clear step-by-step instructions for 🔴 Red, 🟢 Green, and 🔵 Refactor
   - Rules enforcing strict TDD discipline

### Phase 3: Restart and See It All in Action

Now restart your Copilot session so it picks up both the new instruction and the TDD skill.

1. **Restart your session:**
   - Type `/exit` to end the current session
   - Run `copilot` again
   - Say `lesson 8` to return to this lesson

   Copilot will detect that your instruction and skill are already in place and prompt you to build a Python calculator using TDD!

---

## Verification

To complete this lesson, you need:

1. **Custom instruction added:** `.github/copilot-instructions.md` contains "code-review"
2. **TDD skill created:** `.github/skills/tdd/SKILL.md` exists with content
3. **Calculator tests passing:** `exercises/cli/09-calculator/` has tests for add, multiply, and divide (Python or TypeScript)

---

## Quick Reference Card

```
┌────────────────────────────────────────────────────┐
│          INSTRUCTIONS & SKILLS                     │
├────────────────────────────────────────────────────┤
│  Instructions:                                     │
│  • File: .github/copilot-instructions.md           │
│  • Always active in background                     │
│  • Keep short — don't stuff context                │
│  • Restart session to pick up changes              │
├────────────────────────────────────────────────────┤
│  Skills:                                           │
│  • File: .github/skills/<name>/SKILL.md            │
│  • Invoked on demand by user                       │
│  • YAML front matter: name + description           │
│  • Detailed step-by-step instructions              │
├────────────────────────────────────────────────────┤
│  TDD Cycle:                                        │
│  • 🔴 Red — write failing test                     │
│  • 🟢 Green — minimal code to pass                 │
│  • 🔵 Refactor — clean up, tests still pass        │
└────────────────────────────────────────────────────┘
```

---

## Summary

| Topic | Key Point |
|-------|-----------|
| **Instructions** | Always-on background context in `copilot-instructions.md` |
| **Skills** | On-demand workflows in `.github/skills/<name>/SKILL.md` |
| **Best Practice** | Keep instructions short; use skills for complex workflows |
| **TDD** | Red-green-refactor ensures tests drive implementation |
| **Impact** | Instructions + skills = Copilot works exactly how you want |

**Key Takeaways:**
- Instructions are **passive** — always read, keep them concise
- Skills are **active** — invoked by trigger phrases, can be detailed
- **Short beats long** for instructions — don't bloat the context window
- TDD is a perfect skill candidate — repeatable, step-by-step workflow
- Restart your session after changing instructions to see them take effect

---

## Next Steps

Continue to [Lesson 9: Building an MCP Tool](./09-mcp.md) to learn about the Model Context Protocol and extending Copilot with custom tools.
