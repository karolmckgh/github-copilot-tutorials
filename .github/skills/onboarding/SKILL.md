---
name: onboarding
description: "Assess learner's prior Copilot knowledge and customize their tutorial journey by skipping content they already know. Invoke when user starts the tutorial or says 'start', 'begin', or 'assess my level'."
---

## Purpose

This skill helps learners skip content they're already familiar with, creating a personalized learning path through the GitHub Copilot tutorials.

## Instructions

### Step 0: Check for Existing Progress

Before presenting the self-assessment, read `progress.json` from the repository root. If the file exists, is valid JSON, and shows meaningful progress, offer to resume instead of starting fresh.

**Meaningful progress** means ANY of these are true:
- `currentLesson` is set and > 1
- `xp` is > 0
- At least one lesson in `lessons` has `"status": "completed"` or `"status": "in_progress"`

If meaningful progress is found:

1. **Summarize the existing progress** briefly, e.g.:
   > "Welcome back! 👋 I see you have existing progress:"
   > - **Level:** intermediate
   > - **Current Lesson:** 6 (Plan & Implement)
   > - **XP:** 125 ✨
   > - **Completed:** Lessons 1, 2, 3, 5

2. **Ask the user what they'd like to do** using the ask_user tool:
   - "Continue where I left off (Lesson 6)" ← dynamically show their current lesson
   - "Start fresh (reset all progress)"
   - "Re-assess my level (keep completed lessons)"

3. **Handle the user's choice:**
   - **Continue:** Skip to Step 4, using their existing `skillLevel` and `currentLesson`. No changes to `progress.json`.
   - **Start fresh:** Reset `progress.json` to the default template (clear all lessons, XP, achievements) and proceed to Step 1 for a fresh self-assessment.
   - **Re-assess:** Proceed to Step 1 for self-assessment, but when updating `progress.json` in Step 3, preserve existing `lessons` completion data (as described in the Re-Assessment section below).

If no meaningful progress is found (new user or empty progress), proceed directly to Step 1.

### Step 1: Present Self-Assessment Options

When invoked, present these 4 options to the user in a clear, formatted list and wait for their response:

**Question:** "What's your current experience with GitHub Copilot?"

**Choices:**
1. "I'm completely new to Copilot"
2. "I know Chat basics but not CLI"
3. "I know both Chat and CLI basics"
4. "I'm advanced - show me custom instructions/skills only"

### Step 2: Map Selection to Skill Level

Based on the user's selection, determine their skill level and lessons to skip:

| Selection | Skill Level | Skip Lessons | Start At |
|-----------|-------------|--------------|----------|
| "I'm completely new to Copilot" | beginner | [] (none) | Lesson 1 |
| "I know Chat basics but not CLI" | intermediate | [1, 2, 3, 4] | Lesson 5 (Copilot CLI Fundamentals) |
| "I know both Chat and CLI basics" | advanced | [1, 2, 3, 4, 5, 6, 7] | Lesson 8 (Instructions & Skills) |

### Step 3: Update progress.json

Read the current `progress.json` file from the repository root and update it with:

```json
{
  "version": "1.0",
  "started_at": "<current ISO timestamp>",
  "skillLevel": "<beginner|intermediate|advanced|expert>",
  "skippedLessons": [<array of lesson numbers to skip>],
  "lessons": {}
}
```

**Important:** Use the edit tool to update the file. Set `started_at` to the current timestamp if it's null.

### Step 4: Guide User to Starting Lesson

After updating progress.json, provide guidance based on skill level **and current platform**.

#### Detecting Platform

- If the user is in **Copilot CLI** (terminal session), they need handoff instructions for Chat lessons (1-4)
- If the user is in **VS Code Copilot Chat**, they can start Chat lessons directly

#### For Beginners (Starting at Lesson 1)

**If in Copilot CLI:**
> "Great! You're starting from the beginning with Copilot Chat lessons."
>
> 📋 **Lessons 1-4 are best done in VS Code Copilot Chat!**
>
> Here's how to get set up:
> 1. **Ensure GitHub Copilot Chat is installed** in VS Code
>    - Open VS Code → Extensions → search "GitHub Copilot Chat" → Install
> 2. **Open Copilot Chat** — click the 💬 chat icon to the **right of the search bar** in VS Code
> 3. **Add context** — click "Add Context" in the Chat panel, then add the `github-copilot-tutorials` folder
> 4. **Start the tutorial** — type "start tutorial" in the Chat
> 5. **Close this CLI session** — type `/exit` to close Copilot CLI for now
>
> You'll come back to the CLI for Lessons 5-9! 🚀

**If in VS Code Chat:**
> "Great! You're starting from the beginning. Let's begin with Lesson 1: Introduction to Copilot Chat. Type 'start lesson 1' when ready."

#### For Intermediate (Starting at Lesson 5)

> "Since you know Chat basics, you'll start with the CLI section. Lessons 1-4 are marked as skipped but available if you want to review them. Type 'start lesson 5' when ready."

**Note:** If user is in VS Code Chat, remind them to switch to Copilot CLI for lessons 5+.

#### For Advanced (Starting at Lesson 8)

> "You're jumping to the customization content. Lessons 1-7 are available for reference if needed. Type 'start lesson 8' when ready."

## Lesson Structure Reference

For mapping purposes, here's the expected lesson structure:

**Chat Section (Lessons 1-4):**
- Lesson 1: Introduction to Copilot Chat
- Lesson 2: Effective Prompting
- Lesson 3: Slash Commands
- Lesson 4: Chat Participants (@workspace, @terminal)

**CLI Section (Lessons 5-7):**
- Lesson 5: Copilot CLI Fundamentals
- Lesson 6: Plan & Implement
- Lesson 7: Fleet Agents

**Customization Section (Lessons 8-9):**
- Lesson 8: Instructions & Skills
- Lesson 9: MCP Servers

## Skipped Lesson Display

When showing the tutorial outline or lesson list:
- **Completed lessons**: Show with ✅ checkmark
- **Skipped lessons**: Show collapsed/minimized with ⏭️ icon and "(skipped - click to expand)" label
- **Current/Available lessons**: Show normally

Example display for intermediate user:
```
⏭️ Lesson 1: Introduction to Copilot Chat (skipped - click to expand)
⏭️ Lesson 2: Effective Prompting (skipped - click to expand)
⏭️ Lesson 3: Slash Commands (skipped - click to expand)
⏭️ Lesson 4: Chat Participants (@workspace, @terminal) (skipped - click to expand)
→ Lesson 5: Copilot CLI Fundamentals (START HERE)
  Lesson 6: Plan & Implement
  Lesson 7: Fleet Agents
  Lesson 8: Instructions & Skills
```

## Re-Assessment

If a user wants to change their skill level:
1. They can invoke the onboarding skill again
2. Present the same options
3. Update progress.json accordingly
4. Note: This does NOT reset completed lessons, only updates skippedLessons

## Error Handling

- If progress.json doesn't exist, create it with the template structure
- If progress.json has invalid JSON, notify the user and offer to reset it
- Always preserve existing `lessons` completion data when updating skill level
