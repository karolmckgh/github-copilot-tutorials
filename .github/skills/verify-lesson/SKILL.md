---
name: verify-lesson
description: "Verify lesson completion by checking exercise files and criteria. Invoke when user says 'verify', 'check my work', 'done', or 'did I complete'."
---

## Purpose

This skill validates that a learner has completed the exercise requirements for their current lesson. It checks files in the `exercises/` directory, provides helpful feedback, and awards XP upon successful completion.

## Instructions

### Step 1: Determine Current Lesson

1. Read `progress.json` from the repository root
2. Get the `currentLesson` value
3. If `currentLesson` is null:
   - Tell the user: "You haven't started yet! Say 'start tutorial' to begin."
   - Exit early

### Step 2: Check Verification Criteria

Based on the current lesson number, check the appropriate criteria:

| Lesson | Location | Criteria | Description |
|--------|----------|----------|-------------|
| 1 | `exercises/chat/01-result.md` | Auto-saved from conversation, then verified (>50 chars) | First Chat exercise result |
| 2 | `exercises/chat/02-refactored.*` | Auto-saved from conversation, then verified | Refactoring exercise |
| 3 | `exercises/chat/03-tests.*` | Auto-saved from conversation, then verified | Tests generated with /tests |
| 4 | `exercises/chat/04-workspace-edit.*` | Auto-saved from conversation, then verified (>50 chars) | Workspace editing exercise |
| 5 | `exercises/cli/05-session.md` | Auto-saved from conversation, then verified (>50 chars) | CLI session notes |
| 6 | `exercises/cli/06-*.*` (not `.gitkeep`) | Any file matching pattern exists | Feature implementation |
| 7 | `exercises/cli/07-*.*` (not `.gitkeep`) | Project directory or file exists | Fleet mode exercise |
| 8 | `.github/copilot-instructions.md` + `.github/skills/tdd/SKILL.md` + `exercises/cli/09-calculator/` | Instruction updated, TDD skill exists, calculator tests pass (Python or TypeScript) | Instructions & Skills |
| 9 | `exercises/cli/09-mail-mcp/server.py` + `exercises/cli/09-mail-mcp/test_server.py` + `.copilot/mcp-config.json` | MCP server has tool definitions, tests exist/pass, config file present | MCP Servers |

### Step 3: Perform Verification

For each lesson, follow this verification logic:

#### Lesson 1 - Chat Introduction
```
Step A: Auto-save conversation result
  - Look back through the conversation history for the learner's Copilot Chat exchange
    (code snippet, question asked, and Copilot's explanation)
  - Generate exercises/chat/01-result.md with:
      # My First Copilot Chat
      ## Code I Asked About
      <the code snippet from the conversation>
      ## My Question
      <the question the learner asked>
      ## Copilot's Response
      <Copilot's explanation from the conversation>
      (Include any follow-up Q&A if present)
  - If no relevant exchange is found in the conversation, do NOT create the file
    and fail with a message asking the learner to first have a conversation with
    Copilot about the code (Steps 1-3) before verifying.

Step B: Verify the file
  Check: exercises/chat/01-result.md exists
  Check: File content length > 50 characters
  Pass if: Both conditions met
```

#### Lesson 2 - Refactoring
```
Step A: Auto-save refactored code
  - Look back through the conversation history for refactored code that the
    learner produced using Copilot (the original code is a hard-to-read
    JavaScript function: function calc(a,b,c,d) {...})
  - Detect the language from the refactored code (default to .js if unclear)
  - Save to exercises/chat/02-refactored.js (or appropriate extension based
    on detected language: .py, .ts, .java, .go, .rb, .cs, etc.)
  - Include a header comment noting this was refactored with Copilot
  - If no refactored code is found in the conversation, do NOT create the
    file and fail with a message asking the learner to first refactor the
    code with Copilot (Steps 1-3) before verifying.

Step B: Verify the file
  Check: Any file matching exercises/chat/02-refactored.* exists
    Accept: .md, .py, .js, .ts, .java, .go, .rb, .cs, etc.
  Pass if: At least one matching file exists with content
```

#### Lesson 3 - Tests
```
Step A: Auto-save generated tests
  - Look back through the conversation history for test code the learner
    generated using the /tests slash command
  - Detect the language (Python or JavaScript) from the test content
    (e.g., presence of pytest/unittest → .py, jest/mocha → .js)
  - Save to exercises/chat/03-tests.py (or .js based on detected language)
  - If no test code is found in the conversation, do NOT create the file
    and fail with a message asking the learner to first use /tests to
    generate tests (Steps 1-3) before verifying.

Step B: Verify the file
  Check: exercises/chat/03-tests.* exists
    Accept any extension
  Pass if: At least one matching file exists with content
```

#### Lesson 4 - Workspace Editing
```
Step A: Auto-save conversation result
  - Look back through the conversation history for the learner's @workspace
    queries and the responses they received
  - Generate exercises/chat/04-workspace-edit.md with:
      # @workspace Exercise Results
      ## Query Used
      <the @workspace query the learner asked>
      ## What @workspace Found
      <summary of what Copilot found in response>
      ## Something I Learned
      <an interesting insight from the exchange>
      (Include any follow-up queries if present)
  - If no @workspace exchange is found in the conversation, do NOT create
    the file and fail with a message asking the learner to first try some
    @workspace queries (Steps 1-3) before verifying.

Step B: Verify the file
  Check: exercises/chat/04-workspace-edit.md exists
  Check: File content length > 50 characters
  Pass if: Both conditions met
```

#### Lesson 5 - CLI Introduction
```
Step A: Auto-save session log
  - Look back through the conversation history for the learner's Copilot CLI
    exploration: slash commands tried (e.g., /help, /cwd, /context, /compact),
    questions asked about the repo, and Copilot's responses
  - Generate exercises/cli/05-session.md with:
      # Lesson 5: CLI Session Log

      ## Commands Explored

      | Command | What It Did |
      |---------|-------------|
      | <command> | <what it did / what the learner observed> |
      (Include all slash commands the learner tried during the session)

      ## Repo Question

      **Q:** <the question the learner asked about the repo>

      **A:** <Copilot's answer from the conversation>

      ## Observations

      - <key insights or surprises the learner experienced>
      - <anything notable about how Copilot behaved>
      (Synthesize observations from the conversation flow)

  - If no relevant CLI interaction is found in the conversation (no slash
    commands tried AND no questions asked about the repo), do NOT create the
    file and fail with a message asking the learner to first explore some
    slash commands and ask a question about the repo before verifying.

Step B: Verify the file
  Check: exercises/cli/05-session.md exists
  Check: File content length > 50 characters
  Pass if: Both conditions met
```

#### Lesson 6 - CLI Feature Implementation
```
Check: Any file matching exercises/cli/06-*.* exists (excluding .gitkeep)
Pass if: At least one matching file exists with content (e.g., 06-feature.js, 06-word-counter.py, 06-project-tracker.js)
```

#### Lesson 7 - Fleet Agents
```
Check: Any file or directory matching exercises/cli/07-*.* exists (excluding .gitkeep)
Pass if: At least one matching file exists with content, or a project directory exists
```

#### Lesson 8 - Custom Instructions & Skills
```
Check: .github/copilot-instructions.md contains "code-review"
Check: .github/skills/tdd/SKILL.md exists with content (>100 chars)
Check: exercises/cli/09-calculator/ has test + implementation files (Python OR TypeScript)
  Python: exercises/cli/09-calculator/src/calculator.py + test_calculator.py (or tests/ directory)
  TypeScript: exercises/cli/09-calculator/src/calculator.ts + calculator.test.ts
Bonus: Run tests — "python -m pytest" for Python or "npm test" for TypeScript — all tests pass
Pass if: Instruction file updated AND tdd skill exists AND calculator has tests + implementation
```

#### Lesson 9 - MCP Servers
```
Check: exercises/cli/09-mail-mcp/server.py contains "@mcp.tool()" (at least one tool defined)
Check: exercises/cli/09-mail-mcp/test_server.py exists with content (>100 chars)
Check: .copilot/mcp-config.json contains "mail-tm" server configuration
Bonus: Run tests — "python -m pytest exercises/cli/09-mail-mcp/test_server.py" — all tests pass
Pass if: Server has tool definitions AND tests exist AND mcp-config.json has mail-tm entry
```

### Step 4: Handle Result

#### On Success ✅

1. Display success message:
```
╔═══════════════════════════════════════════════════════════╗
║                    ✅ LESSON VERIFIED!                    ║
╠═══════════════════════════════════════════════════════════╣
║  Lesson <N>: <Lesson Title>                               ║
║                                                           ║
║  🎉 Great work! You've completed this lesson!             ║
║                                                           ║
║  +<XP> XP earned!                                         ║
║  Total XP: <new_total> ✨                                 ║
╚═══════════════════════════════════════════════════════════╝
```

2. Update progress using Progress Skill operations:
   - Call "Mark Lesson Complete" with:
     - `lessonNumber`: current lesson
     - `exercisesCompleted`: 1
     - `exercisesTotal`: 1
   - This automatically handles XP, achievements, and currentLesson advancement

3. Check for and announce any new achievements:
```
🏆 Achievement Unlocked: <Achievement Name>!
   <Achievement Description>
```

4. Prompt next action:
```
Ready for the next lesson? Say "start lesson <N+1>" to continue!
```

#### On Failure ❌

Display helpful feedback with what's missing:

```
╔═══════════════════════════════════════════════════════════╗
║                   ❌ NOT QUITE THERE YET                   ║
╠═══════════════════════════════════════════════════════════╣
║  Lesson <N>: <Lesson Title>                               ║
║                                                           ║
║  Missing:                                                 ║
║  • <specific thing that's missing>                        ║
║                                                           ║
║  Expected:                                                ║
║  • <what should exist>                                    ║
║                                                           ║
║  💡 Tip: <helpful suggestion>                             ║
╚═══════════════════════════════════════════════════════════╝
```

## Failure Feedback Templates

### Lesson 1
**Missing:** No Copilot Chat conversation found in this session
**Expected:** A conversation where you asked Copilot to explain the sample code from Step 1
**Tip:** Go back and complete Steps 1-3 first — apply the code, select it, and ask Copilot a question about it. Then say "verify" again!

### Lesson 2
**Missing:** No refactored code found in this conversation
**Expected:** A conversation where you asked Copilot to refactor the `calc(a,b,c,d)` function from the exercise
**Tip:** Go back and complete Steps 1-3 first — craft a good prompt to refactor the code, iterate if needed. Then say "verify" again and I'll save the result for you!

### Lesson 3
**Missing:** No test code found in this conversation
**Expected:** Tests generated using the `/tests` slash command on the sample code
**Tip:** Go back and complete Steps 1-3 first — copy the sample code to a file, select it, and use `/tests` in Copilot Chat. Then say "verify" again and I'll save the tests for you!

### Lesson 4
**Missing:** No `exercises/chat/04-workspace-edit.*` file found
**Expected:** Evidence of using Copilot's workspace editing features
**Tip:** Use Chat's "Apply to workspace" feature and save the result.

### Lesson 5
**Missing:** No CLI interaction found in this conversation
**Expected:** A session where you tried slash commands (e.g., /help, /cwd) and asked Copilot a question about the repo
**Tip:** Go back and try some slash commands and ask a question like "Describe the purpose of this repository." Then say "verify" again and I'll save the session log for you!

### Lesson 6
**Missing:** No `exercises/cli/06-*.*` file found
**Expected:** Code for a feature implemented using the CLI (e.g., `06-feature.js`, `06-word-counter.py`, `06-project-tracker.js`)
**Tip:** Use `copilot` CLI to help build a small feature, then save the code to `exercises/cli/` with a `06-` prefix.

### Lesson 7
**Missing:** No `exercises/cli/07-*.*` file or project found
**Expected:** A project built using fleet mode (/fleet)
**Tip:** Use `/fleet` to build a multi-file project like a React wealth management dashboard.

### Lesson 8
**Missing:** One or more of: custom instruction, TDD skill, calculator exercise
**Expected:** `.github/copilot-instructions.md` with "code-review" line, `.github/skills/tdd/SKILL.md` with TDD workflow, and `exercises/cli/09-calculator/` with passing tests (Python or TypeScript)
**Tip:** Follow the three phases: add the instruction, create the TDD skill, then restart and use the skill to build the calculator with add, multiply, and divide.

### Lesson 9
**Missing:** One or more of: MCP server, tests, MCP configuration
**Expected:** `exercises/cli/09-mail-mcp/server.py` with `@mcp.tool()` definitions, `exercises/cli/09-mail-mcp/test_server.py` with tests, and `.copilot/mcp-config.json` with mail-tm server config
**Tip:** Start by implementing `get_domains` (simplest tool), write a test first, then work through create_account, login, list_messages, and read_message.

## XP Reference (from Progress Skill)

| Lesson Range | XP Award |
|--------------|----------|
| Lessons 1-4  | 25 XP    |
| Lessons 5-7  | 50 XP    |
| Lessons 8-9  | 100 XP   |

## Lesson Titles Reference

| Lesson | Title |
|--------|-------|
| 1 | Introduction to GitHub Copilot Chat |
| 2 | Effective Prompting |
| 3 | Slash Commands |
| 4 | Chat Participants |
| 5 | Copilot CLI Fundamentals |
| 6 | Plan & Implement |
| 7 | Fleet Agents |
| 8 | Instructions & Skills |
| 9 | MCP Servers |

## Integration with Progress Skill

After successful verification, use the Progress Skill to:

1. **Mark Lesson Complete**
   - Updates `lessons[N]` with completion timestamp
   - Awards XP
   - Advances `currentLesson`
   - Checks for achievements

2. **Check Achievements** (automatic)
   - `first_lesson`: After completing any lesson
   - `chat_master`: After completing lessons 1-4
   - `cli_pro`: After completing lessons 5-7
   - `customizer`: After completing lesson 8
   - `mcp_builder`: After completing lesson 9
   - `completionist`: After completing all lessons
   - `century`: After reaching 100+ XP
   - `power_learner`: After reaching 500+ XP

## Already Completed Handling

If a lesson has already been verified:

```
╔═══════════════════════════════════════════════════════════╗
║                  ✅ ALREADY COMPLETED!                    ║
╠═══════════════════════════════════════════════════════════╣
║  Lesson <N>: <Lesson Title>                               ║
║                                                           ║
║  You completed this lesson on <date>                      ║
║  XP earned: <xp> (already awarded)                        ║
║                                                           ║
║  Your current lesson is <currentLesson>.                  ║
║  Say "verify" again after completing that lesson!         ║
╚═══════════════════════════════════════════════════════════╝
```

## Error Handling

- **progress.json missing**: Create default and prompt user to start tutorial
- **Invalid lesson number**: Notify user of valid range (1-9)
- **File system errors**: Provide clear error message with suggested fix
- **Partial completion**: List what's complete vs what's missing

## Example Interactions

### Example 1: Successful Verification

**User:** "verify"

**Agent checks:** `exercises/chat/01-result.md` exists with 150 characters of content

**Response:**
```
╔═══════════════════════════════════════════════════════════╗
║                    ✅ LESSON VERIFIED!                    ║
╠═══════════════════════════════════════════════════════════╣
║  Lesson 1: Introduction to GitHub Copilot Chat            ║
║                                                           ║
║  🎉 Great work! You've completed this lesson!             ║
║                                                           ║
║  +25 XP earned!                                           ║
║  Total XP: 25 ✨                                          ║
╚═══════════════════════════════════════════════════════════╝

🏆 Achievement Unlocked: First Steps!
   Complete your first lesson

Ready for the next lesson? Say "start lesson 2" to continue!
```

### Example 2: Failed Verification

**User:** "check my work"

**Agent checks:** `exercises/chat/01-result.md` does not exist

**Response:**
```
╔═══════════════════════════════════════════════════════════╗
║                   ❌ NOT QUITE THERE YET                   ║
╠═══════════════════════════════════════════════════════════╣
║  Lesson 1: Introduction to GitHub Copilot Chat            ║
║                                                           ║
║  Missing:                                                 ║
║  • exercises/chat/01-result.md not found                  ║
║                                                           ║
║  Expected:                                                ║
║  • A file documenting your first Copilot Chat interaction ║
║                                                           ║
║  💡 Tip: Create the file and paste your Chat conversation ║
║     result. Include the prompt you used and Copilot's     ║
║     response.                                             ║
╚═══════════════════════════════════════════════════════════╝
```

### Example 3: Verify Specific Lesson

**User:** "verify lesson 3"

**Agent:** Checks lesson 3 criteria regardless of current lesson
(Note: XP only awarded if lesson wasn't already completed)
