# Lesson 4: Chat Participants (@workspace, @terminal)

> **XP:** 25 | **Difficulty:** Beginner | **Time:** 15 minutes

## Learning Objectives

By the end of this lesson, you will:
- Understand what chat participants are and why they matter
- Know when to use `@workspace` vs `@terminal` vs other participants
- Practice using participants for context-aware queries

---

# Part 1: Key Concepts

## What Are Participants?

Chat participants are **context providers** prefixed with `@` that give Copilot Chat access to specific areas of your development environment. Instead of you manually copy-pasting context, participants tell Copilot exactly where to look.

Think of them as **specialists** you can call upon:

| Participant | What It Knows | Best For |
|-------------|---------------|----------|
| `@workspace` | Your entire codebase | Finding code, understanding architecture |
| `@terminal` | Terminal output & shell context | CLI help, error diagnosis |
| `@vscode` | VS Code settings & state | Editor configuration, extensions |
| `@github` | GitHub repo, issues, PRs | Repository info, collaboration |

### Why Use Participants?

Without participants, Copilot only sees what's in your current chat. With them:

1. **Precision** — answers grounded in specific context, not guesswork
2. **Efficiency** — no need to copy-paste files, errors, or configs
3. **Depth** — access information you couldn't reasonably include in a prompt

### Syntax

```
@participant your question here
```

Combine with slash commands for extra power:

```
@workspace /explain how does authentication work?
```

---

## @workspace — Your Codebase Expert

The most commonly used participant. It gives Copilot access to **all files** in your workspace: source code, project structure, dependencies, configs, and documentation.

### When to Reach for @workspace

| Scenario | Example Query |
|----------|---------------|
| Finding code | `@workspace where is the user authentication logic?` |
| Understanding architecture | `@workspace explain the project structure` |
| Locating patterns | `@workspace show all API endpoints` |
| Cross-file questions | `@workspace how does the frontend call the backend?` |
| Dependency questions | `@workspace what testing framework do we use?` |

### Pro Tips

- **Be specific** — "Where is user validation?" beats "Show me validation"
- **Use domain terms** — reference actual function/class names if you know them
- **Ask big-picture questions** — `@workspace` excels at architectural understanding
- **Combine with /explain** — `@workspace /explain how does caching work?`

---

## @terminal — Your CLI Sidekick

Provides context about your terminal session: recent output, errors, and shell environment. Invaluable when things go wrong at the command line.

### When to Reach for @terminal

| Scenario | Example Query |
|----------|---------------|
| Command errors | `@terminal why did that command fail?` |
| Learning CLI tools | `@terminal how do I use git rebase?` |
| Script debugging | `@terminal explain this shell error` |
| Command suggestions | `@terminal how do I find large files?` |

### Pro Tips

- **Run the command first** — `@terminal` works best with recent output in the terminal
- **Ask for alternatives** — `@terminal is there a better way to do this?`

---

## @vscode and @github

### @vscode — Editor Configuration

```
@vscode how do I change the theme?
@vscode what extension helps with Python formatting?
@vscode how do I set up keyboard shortcuts?
```

### @github — Repository Context

```
@github show me recent issues about authentication
@github what PRs are waiting for review?
@github explain the CI workflow in this repo
```

---

## Combining Participants

The real power comes from **chaining participants** in a workflow:

**Scenario:** You need to add a feature similar to an existing one.

1. `@workspace show me how the "create user" feature is implemented`
2. `@workspace /explain the data flow from API to database`
3. `@terminal how do I run just the user-related tests?`
4. `@vscode what's the shortcut to run tests in the current file?`

You can also combine participants with slash commands:

```
@workspace /explain the main application entry point
@terminal /fix this docker error
```

---

## Quick Reference Card

```
┌─────────────────────────────────────────────────────────┐
│              COPILOT CHAT PARTICIPANTS                   │
├─────────────────────────────────────────────────────────┤
│  @workspace  →  Entire codebase context                 │
│  @terminal   →  Terminal/shell context                  │
│  @vscode     →  VS Code settings & state                │
│  @github     →  GitHub repo, issues, PRs                │
├─────────────────────────────────────────────────────────┤
│  Syntax:                                                │
│  @participant your question here                        │
│  @participant /command additional context                │
├─────────────────────────────────────────────────────────┤
│  Pro Tips:                                              │
│  • @workspace for "where is…?" questions                │
│  • @terminal after running a command                    │
│  • Combine with /explain, /fix, /tests                  │
│  • Be specific about what you're looking for            │
└─────────────────────────────────────────────────────────┘
```

---

# Part 2: Exercise

## Explore a Codebase with @workspace

### Your Task

Use participants to explore **this tutorial repository**, discover its structure, and answer questions about it.

### Steps

1. **Open Copilot Chat** in VS Code (`Ctrl+Shift+I` or `Cmd+Shift+I`)

2. **Discover the project structure:**
   ```
   @workspace where are the lesson files located and what topics do they cover?
   ```

3. **Dig deeper into a pattern:**
   ```
   @workspace show me the structure of a typical lesson file
   ```

4. **Try a cross-file question:**
   ```
   @workspace find all markdown files that contain exercises
   ```

### Bonus Challenges

- Use `@workspace` to find all verification criteria across lessons
- Ask `@workspace` how many XP total are available in the tutorial
- Use `@terminal` to run a grep command that `@workspace` suggests

---

## Verification

Once you've tried the queries above, say **"verify"** and your exercise results will be saved automatically based on your conversation!

---

## Summary

**Key Takeaways:**
- Participants provide **targeted context** to Copilot — no more copy-pasting
- `@workspace` is your go-to for codebase questions (finding code, architecture, patterns)
- `@terminal` is invaluable for CLI troubleshooting (run first, then ask)
- `@vscode` and `@github` round out the toolkit for editor and repo context
- Combine participants with slash commands for maximum power

---

## Next Steps

Continue to [Lesson 5: Copilot CLI Fundamentals](../cli/05-fundamentals.md) to learn how to launch and navigate the Copilot CLI interactive mode.
