# Lesson 5: Copilot CLI Fundamentals

> **XP:** 50 | **Difficulty:** Intermediate | **Time:** 20 minutes

## Learning Objectives

- Understand what GitHub Copilot CLI is and how it differs from VS Code Chat
- Launch Copilot CLI and enter interactive mode
- Use core slash commands to control sessions, navigation, and configuration
- Manage context effectively using tokens, `/context`, and `/compact`
- Navigate working directories with `/cd` and project-aware launching
- Complete a guided first CLI session from start to finish

---

## What Is Copilot CLI?

GitHub Copilot CLI is a **conversational AI assistant that lives in your terminal**. Think of it as having a senior developer sitting next to you — one who can read your code, run commands, edit files, and explain complex concepts, all without leaving the command line.

Unlike traditional CLI tools that take a command and return output, Copilot CLI operates in **agentic mode**: it can reason about multi-step problems, execute shell commands on your behalf, and iterate until a task is complete.

### Key Capabilities

| Capability | Description |
|------------|-------------|
| 🗣️ **Conversational** | Ask questions in natural language — no special syntax needed |
| 🔧 **Agentic Execution** | Copilot can run commands, read files, and make edits autonomously |
| 📁 **Context-Aware** | Understands your repo structure, git history, and project files |
| 🔄 **Iterative** | Keeps conversation history so you can refine and follow up |
| 🛡️ **Safe by Default** | Asks permission before running commands that modify your system |

### How to Launch

Getting started is as simple as one command:

```bash
copilot
```

That's it! This drops you into an **interactive session** where you can chat, ask questions, and give instructions. You'll see a prompt where you can start typing naturally.

```
$ copilot
Welcome to GitHub Copilot CLI!

> What files are in this project?
```

> 💡 **Pro Tip:** Launch Copilot CLI from your project's root directory. It automatically picks up context from the current working directory, making its responses far more relevant.

---

## Copilot CLI vs. VS Code Chat

If you've used GitHub Copilot Chat in VS Code, you might wonder how the CLI version compares. Here's a side-by-side breakdown:

| Feature | VS Code Chat | Copilot CLI |
|---------|-------------|-------------|
| **Interface** | Side panel in editor | Terminal / command line |
| **File Context** | Open editor tabs, `@workspace` | Working directory, `/context` |
| **Code Editing** | Inline diffs in editor | Direct file writes with confirmation |
| **Command Execution** | Terminal integration | Native shell execution (agentic) |
| **Best For** | Writing code in open files | Repo-wide tasks, automation, DevOps |
| **Multi-Step Tasks** | Manual iteration | Autonomous agentic workflows |
| **Git Operations** | Via terminal panel | Native — reads diffs, commits, branches |
| **Accessibility** | Requires VS Code | Works in any terminal, SSH, CI |

### When to Use Each

- **VS Code Chat** → You're actively editing a specific file and want inline suggestions
- **Copilot CLI** → You need to explore a codebase, run multi-step tasks, or work across many files

They complement each other. Many developers use VS Code Chat for focused editing and Copilot CLI for broader tasks like debugging builds, setting up infrastructure, or onboarding to a new project.

---

## Core Slash Commands

Slash commands give you direct control over your Copilot CLI session. They're organized into four categories:

### Session Commands

These control the conversation itself — starting fresh, getting help, or managing history.

| Command | Description | When to Use |
|---------|-------------|-------------|
| `/help` | Show all available commands and usage tips | First thing in any new session |
| `/clear` | Clear the terminal screen | When output gets cluttered |
| `/new` | Start a brand-new conversation (resets history) | Switching to a completely different task |
| `/compact` | Summarize conversation history to free up tokens | When the session gets long or slow |

```
> /help
Available commands:
  /help      Show this help message
  /clear     Clear the screen
  /new       Start a new conversation
  ...
```

> 💡 **Pro Tip:** Use `/new` when switching tasks. Leftover context from a previous conversation can confuse Copilot and lead to less accurate responses.

### Navigation Commands

These control what Copilot can see and where it operates.

| Command | Description | When to Use |
|---------|-------------|-------------|
| `/cwd` | Show the current working directory | Verify where Copilot is operating |
| `/cd <path>` | Change the working directory | Switch to a different project or subdirectory |
| `/context` | Show current context window usage | Check how much context is being used |

```
> /cwd
Current working directory: /home/user/repos/my-project

> /cd ../other-project
Changed directory to: /home/user/repos/other-project

> /context
Context: 12,450 / 128,000 tokens used (9.7%)
```

### Review Commands

These help you inspect, share, and hand off work.

| Command | Description | When to Use |
|---------|-------------|-------------|
| `/diff` | Show a diff of changes made in this session | Review what Copilot modified before committing |
| `/share` | Generate a shareable link to the conversation | Share a session with a teammate |
| `/delegate` | Hand off the current task to an agent | Escalate complex tasks to a specialized agent |

```
> /diff
Modified files:
  M src/utils.js  (+12, -3)
  A tests/utils.test.js  (+45)
```

### Configuration Commands

These adjust how Copilot operates.

| Command | Description | When to Use |
|---------|-------------|-------------|
| `/model` | View or change the AI model being used | Switch to a more capable or faster model |
| `/agent` | View or switch the active agent type | Choose a specialized agent for your task |
| `/allow-all` | Skip confirmation prompts for commands | When you trust the operation and want speed |

```
> /model
Current model: claude-sonnet-4-20250514

> /model gpt-4.1
Switched to model: gpt-4.1
```

> ⚠️ **Caution:** Use `/allow-all` carefully. It lets Copilot execute commands without asking for confirmation. Only enable it when you're confident in what you're doing and working in a safe environment.

---

## Context Management

Context is the "memory" Copilot uses during your session. Every message you send, every file it reads, and every command output it sees consumes **tokens** from a finite context window.

### Understanding Tokens

| Concept | Details |
|---------|---------|
| **Token** | A unit of text (~4 characters or ~¾ of a word) |
| **Context Window** | The total tokens available in a session (model-dependent) |
| **Usage** | Grows with each message, file read, and command output |
| **Limit** | When full, Copilot loses track of earlier conversation |

### Checking Context Usage

Use `/context` to see how much of your context window is consumed:

```
> /context
Context usage: 24,800 / 128,000 tokens (19.4%)
  - Conversation history: 18,200 tokens
  - File contents: 5,400 tokens
  - System prompt: 1,200 tokens
```

### The `/compact` Strategy

When your context fills up, Copilot may start "forgetting" earlier parts of the conversation. The `/compact` command solves this by **summarizing** the conversation history into a shorter form, freeing up tokens while preserving the key points.

**When to use `/compact`:**
- Context usage exceeds ~60-70%
- Copilot starts repeating itself or losing track of earlier instructions
- You're about to start a complex multi-step task and need room

```
> /compact
Compacting conversation...
Summarized 45 messages into 2,400 tokens (was 18,200 tokens).
Context usage: 9,000 / 128,000 tokens (7.0%)
```

> 💡 **Pro Tip:** Think of `/compact` as "saving your game." It preserves the important state while freeing up space for new work. Use it proactively before long tasks, not just when you hit the limit.

---

## Working Directory Matters

Copilot CLI is deeply aware of where it's running. The working directory determines which files it can see, which git repo it references, and how relevant its suggestions are.

### Best Practices

1. **Always launch from your project root:**
   ```bash
   cd ~/repos/my-project
   copilot
   ```

2. **Use `/cwd` to verify your location:**
   ```
   > /cwd
   Current working directory: /home/user/repos/my-project
   ```

3. **Switch directories mid-session with `/cd`:**
   ```
   > /cd src/components
   Changed directory to: /home/user/repos/my-project/src/components
   ```

4. **Return to the project root when needed:**
   ```
   > /cd /home/user/repos/my-project
   ```

### Why It Matters

When Copilot operates in the correct directory, it can:
- Read your `package.json`, `requirements.txt`, or other config files
- Understand your project structure and suggest relevant file paths
- Run build commands, tests, and linters that actually work
- Access your `.git` history for informed suggestions

---

## Your First CLI Session — A Walkthrough

Let's walk through a real session to see how everything fits together. Follow along in your own terminal!

### Step 1: Launch and Orient

```bash
cd ~/repos/github-copilot-tutorials
copilot
```

```
> /help
```

Take a moment to read through the available commands. This is your command palette for the CLI.

### Step 2: Check Your Bearings

```
> /cwd
```

Confirm you're in the right project directory.

```
> /context
```

See your starting context usage — it should be minimal at the start of a fresh session.

### Step 3: Ask a Question

Try asking Copilot something about your project:

```
> What is the structure of this repository? Give me a high-level overview.
```

Copilot will read your directory structure and provide a summary. Notice how it automatically explores files to answer your question — that's agentic behavior in action.

### Step 4: Go Deeper

Follow up with a more specific question:

```
> What lessons are available in the .worktrees/foundation/lessons directory?
```

Copilot remembers your previous conversation and builds on it.

### Step 5: Manage Your Context

```
> /context
```

Check how much context has been used. If you've been chatting for a while:

```
> /compact
```

Watch as the conversation is summarized and tokens are freed up.

### Step 6: Wrap Up

When you're done, you can simply close the terminal or start a new conversation:

```
> /new
```

---

## Exercise: Explore Copilot CLI

### Your Task

Launch Copilot CLI, explore its commands, and interact with it about this repository. When you're done, say **"verify"** and Copilot will automatically save your session log!

### Steps

1. **Open your terminal** and navigate to the tutorial repository:
   ```bash
   cd ~/repos/github-copilot-tutorials
   ```

2. **Launch Copilot CLI:**
   ```bash
   copilot
   ```

3. **Try the help command:**
   ```
   > /help
   ```
   Note which commands are available.

4. **Check your working directory:**
   ```
   > /cwd
   ```

5. **Check your context usage:**
   ```
   > /context
   ```
   See how many tokens are being used — it should be low at the start of a session.

6. **Try compacting the conversation:**
   ```
   > /compact
   ```
   Notice how it summarizes the conversation history and frees up tokens.

7. **Ask Copilot a question about this repo:**
   ```
   > Describe the purpose of this repository in one paragraph.
   ```

8. **Say "verify"** — Copilot will automatically generate your session log at `exercises/cli/05-session.md` based on your conversation, including:
   - Which commands you tried and what they did
   - The answer Copilot gave about the repository
   - Any observations or insights from the session

### Bonus Challenges

- Try switching models with `/model` and compare response styles
- Use `/cd` to navigate into a subdirectory, then ask Copilot about the files there
- Ask Copilot to explain a specific file in the repository and note the token cost
- Start a `/new` session and see how context resets

---

## Verification

To complete this lesson, say **"verify"**. Copilot will:

1. Review your conversation history for CLI commands tried and questions asked
2. Auto-generate `exercises/cli/05-session.md` with your session log
3. Verify the file exists and has sufficient content
4. Award your XP! 🎉

> 💡 **Note:** You must have tried at least one slash command and asked Copilot a question about the repo before verifying.

---

## Quick Reference Card

```
┌─────────────────────────────────────────────────────────┐
│           COPILOT CLI — SLASH COMMANDS                  │
├──────────────┬──────────────────────────────────────────┤
│  SESSION     │  /help  /clear  /new  /compact           │
│  NAVIGATION  │  /cwd   /cd     /context                 │
│  REVIEW      │  /diff  /share  /delegate                │
│  CONFIG      │  /model /agent  /allow-all               │
├──────────────┴──────────────────────────────────────────┤
│  Launch:    copilot                                     │
│  Best tip:  Always launch from your project root!       │
│  Context:   Use /compact before it fills up             │
│  Safety:    /allow-all skips confirmations — be careful  │
└─────────────────────────────────────────────────────────┘
```

---

## Summary

| Concept | Key Takeaway |
|---------|-------------|
| Copilot CLI | Conversational AI in your terminal with agentic capabilities |
| Launching | Run `copilot` from your project root directory |
| Slash Commands | Direct controls for session, navigation, review, and config |
| Context Window | Finite token budget — monitor with `/context` |
| `/compact` | Summarizes history to free tokens — use proactively |
| Working Directory | Determines what Copilot can see — always verify with `/cwd` |
| vs. VS Code Chat | CLI excels at repo-wide tasks; VS Code Chat at focused editing |

**Key Takeaways:**

- Copilot CLI is more than a chatbot — it's an agentic assistant that can execute commands and edit files
- Slash commands give you precise control over your session without breaking the conversational flow
- Context management is a skill — learn to use `/compact` proactively, not reactively
- The working directory is the foundation of relevant responses — always launch from your project root
- CLI and VS Code Chat are complementary tools — use each where it shines

---

## Next Steps

Continue to [Lesson 6: Agentic Workflows](./06-agentic-workflows.md) to learn how Copilot CLI can execute multi-step tasks autonomously — from debugging builds to scaffolding entire features.
