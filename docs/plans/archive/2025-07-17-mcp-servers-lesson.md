# Plan: Lesson 9 — MCP Servers (Mail.tm)

## Problem

The tutorial ends at lesson 8. We need a lesson 9 that teaches learners how to build a Python MCP (Model Context Protocol) server from scratch that wraps the Mail.tm temporary email API, configure it in `.copilot/mcp-config.json`, and use it through the Copilot CLI.

## Approach

Create a hands-on lesson where the learner:
1. Learns what MCP is and how it extends Copilot's capabilities
2. Builds a Python MCP server with tools for Mail.tm (get domains, create account, login, list messages, read message)
3. Writes tests first (TDD approach) for each tool
4. Configures the server in `.copilot/mcp-config.json`
5. Uses the MCP tools through Copilot CLI conversations

**Language:** Python (consistent with lesson 8's calculator exercise)
**XP:** 100 (advanced topic, same tier as lesson 8)
**Mail.tm scope:** Core tools — get_domains, create_account, login, list_messages, read_message

## Workplan

- [x] **1.** Create lesson content `lessons/cli/09-mcp-servers.md`
  - Header: 100 XP, Advanced, ~45 min
  - Learning objectives: understand MCP, build server, configure for CLI, use tools
  - Theory section: What is MCP, how servers extend Copilot
  - Mail.tm API overview section
  - Step-by-step guide: building the MCP server with TDD
  - Configuration section: `.copilot/mcp-config.json`
  - Exercise: build the full server from scratch
  - Verification criteria, Quick Reference Card, Summary, Next Steps

- [x] **2.** Create exercise scaffold `exercises/cli/09-mail-mcp/`
  - `requirements.txt` — dependencies (`mcp`, `httpx`, `pytest`)
  - `server.py` — empty starter file with comments/structure
  - `test_server.py` — test stubs for TDD exercise
  - `README.md` — exercise instructions

- [x] **3.** Create reference solution `exercises/cli/09-mail-mcp/.solution/`
  - `server.py` — complete working MCP server
  - `test_server.py` — complete passing tests
  - Write failing tests first (TDD for each tool)
  - Implement minimal code to pass each test
  - Verify all tests pass

- [x] **4.** Create `.copilot/mcp-config.json`
  - Configure the mail-tm MCP server (stdio type, python command)
  - Point to `exercises/cli/09-mail-mcp/server.py`

- [x] **5.** Update lesson 8 "Next Steps" section
  - Change "Congratulations! You've completed the tutorial" to link to lesson 9
  - Keep congratulatory tone but indicate there's more

- [x] **6.** Update `README.md`
  - Add lesson 9 row to Part 2 CLI table

- [x] **7.** Update `.github/skills/verify-lesson/SKILL.md`
  - Add lesson 9 verification criteria to table (line ~33)
  - Add lesson 9 to XP reference table
  - Add lesson 9 to lesson titles table
  - Update valid range from "1-8" to "1-9"

- [x] **8.** Update `.github/skills/tutorial/SKILL.md`
  - Add lesson 9 to CLI track table
  - Update "Lessons 5-8" references to "Lessons 5-9"
  - Update loop range from `1 to 8` to `1 to 9`
  - Update validation from "1-8" to "1-9"
  - Add lesson 9 hint focus entry

- [x] **9.** Update `.github/skills/progress/SKILL.md`
  - Add lesson 9 to XP values table
  - Update XP calculation function (lesson 9 → 100 XP)

- [x] **10.** Update `.github/skills/dashboard/SKILL.md`
  - Add lesson 9 to lesson names table
  - Update max XP total (475 → 575)

- [x] **11.** Update `.github/skills/onboarding/SKILL.md`
  - Update "Lessons 5-8" references to "Lessons 5-9"
  - Keep advanced track starting at lesson 8 (not lesson 9 — MCP is a capstone)

## Notes

- Mail.tm API: `https://api.mail.tm`, free, no API key, rate limit 8 req/sec
- Workflow: GET /domains → POST /accounts → POST /token → GET /messages → GET /messages/{id}
- Python MCP SDK: `mcp` package with `@mcp.tool()` decorator
- MCP config format: `{ "mcpServers": { "name": { "type": "stdio", "command": "python", "args": [...] } } }`
- TDD is embedded in the lesson flow — learner writes tests before implementing each tool

## Risks

- Mail.tm API could be down or rate-limited during learner exercises
- Python `mcp` package API may have changed — need to verify current import paths
- Learner's Python environment may not have `pip` configured correctly

