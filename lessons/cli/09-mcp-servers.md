# Lesson 9: MCP Servers — Extending Copilot with Custom Tools

> **XP:** 100 | **Difficulty:** Advanced | **Time:** ~45 minutes
> **Prerequisites:** Lesson 8 (Instructions & Skills), Python 3.10+

## 🎯 Learning Objectives

By the end of this lesson, you will:
- Explain what MCP (Model Context Protocol) is and how it extends Copilot
- Build a Python MCP server that wraps an external API
- Configure MCP servers for GitHub Copilot CLI
- Use custom MCP tools in Copilot conversations

---

## Part 1: What is MCP?

MCP — the **Model Context Protocol** — is an open standard for connecting AI assistants to external tools. Think of it as a universal adapter: you write a server once, and any MCP-compatible client (like Copilot CLI) can use it.

An MCP server exposes **tools** — functions that Copilot can call during conversations to access external data and services.

```
Copilot CLI (client) ↔ MCP Server (your code) ↔ External API / Database / Service
```

Two transport types exist:
- **stdio** — Local process communication via stdin/stdout. This is what we'll use.
- **SSE** — Server-Sent Events over HTTP for remote servers.

| Use Case | Example |
|----------|---------|
| Database access | Query Postgres or SQLite databases |
| API wrappers | Interact with REST or GraphQL APIs |
| File processors | Parse PDFs, CSVs, or custom formats |
| Business logic | Enforce company-specific workflows |

If you can write a Python function for it, Copilot can use it.

---

## Part 2: The Mail.tm API

We'll wrap the **Mail.tm** API — a free temporary email service. No API key needed, perfect for learning. Base URL: `https://api.mail.tm`

| Endpoint | Method | Auth | Description |
|----------|--------|------|-------------|
| `/domains` | GET | No | List available email domains |
| `/accounts` | POST | No | Create a new email account |
| `/token` | POST | No | Login and get a bearer token |
| `/messages` | GET | Yes | List inbox messages |
| `/messages/{id}` | GET | Yes | Read a specific message |

**Workflow:** get domains → create account (`{"address": "user@domain.com", "password": "..."}`) → login for bearer token → check messages

> 💡 **Tip:** Mail.tm has a rate limit of **8 requests/second** per IP — plenty for learning.

---

## Part 3: Building the MCP Server

Install the Python MCP SDK and an async HTTP client:

```bash
pip install "mcp[cli]" httpx
```

Every MCP server starts the same way — create a `FastMCP` instance, then define tools with the `@mcp.tool()` decorator on async functions. The **docstring** becomes the tool description Copilot sees, and **type hints** define the parameter schema.

```python
import httpx
from mcp.server.fastmcp import FastMCP

BASE_URL = "https://api.mail.tm"
mcp = FastMCP("mail-tm")
```

### Tool 1: Get Domains (simplest — no auth)

```python
@mcp.tool()
async def get_domains() -> list[dict]:
    """Get available Mail.tm email domains."""
    async with httpx.AsyncClient() as client:
        resp = await client.get(f"{BASE_URL}/domains")
        resp.raise_for_status()
        return resp.json().get("hydra:member", [])
```

### Tool 2: Create Account

```python
@mcp.tool()
async def create_account(address: str, password: str) -> dict:
    """Create a new Mail.tm email account.

    Args:
        address: Full email address (e.g., user@domain.com). Use get_domains to find valid domains.
        password: Password for the account (minimum 8 characters).
    """
    async with httpx.AsyncClient() as client:
        resp = await client.post(f"{BASE_URL}/accounts", json={"address": address, "password": password})
        resp.raise_for_status()
        return resp.json()
```

### Tool 3: Login

```python
@mcp.tool()
async def login(address: str, password: str) -> str:
    """Login to Mail.tm and return a bearer token."""
    async with httpx.AsyncClient() as client:
        resp = await client.post(f"{BASE_URL}/token", json={"address": address, "password": password})
        resp.raise_for_status()
        return resp.json()["token"]
```

### Tool 4: List Messages

```python
@mcp.tool()
async def list_messages(token: str) -> list[dict]:
    """List inbox messages for a Mail.tm account.

    Args:
        token: Bearer token from the login tool.
    """
    async with httpx.AsyncClient() as client:
        resp = await client.get(f"{BASE_URL}/messages", headers={"Authorization": f"Bearer {token}"})
        resp.raise_for_status()
        return resp.json().get("hydra:member", [])
```

### Tool 5: Read Message

```python
@mcp.tool()
async def read_message(token: str, message_id: str) -> dict:
    """Read a specific Mail.tm message by ID.

    Args:
        token: Bearer token from the login tool.
        message_id: The ID of the message to read (from list_messages).
    """
    async with httpx.AsyncClient() as client:
        resp = await client.get(f"{BASE_URL}/messages/{message_id}", headers={"Authorization": f"Bearer {token}"})
        resp.raise_for_status()
        return resp.json()
```

### Running the Server

```python
if __name__ == "__main__":
    mcp.run(transport="stdio")
```

> 💡 **Tip:** Docstrings are critical — they tell Copilot **when** and **how** to use each tool. Write clear descriptions with parameter explanations.

---

## Part 4: Configuring for Copilot CLI

MCP servers are configured in `.copilot/mcp-config.json` at the root of your repository:

```json
{
  "mcpServers": {
    "mail-tm": {
      "type": "stdio",
      "command": "python",
      "args": ["exercises/cli/09-mail-mcp/server.py"]
    }
  }
}
```

Copilot CLI discovers this file automatically when you start a session.

| Field | Purpose |
|-------|---------|
| `"mail-tm"` | A name you choose for this server |
| `"type": "stdio"` | Transport — local process via stdin/stdout |
| `"command"` | The executable to run (e.g., `python`, `node`) |
| `"args"` | Arguments passed to the command |

After configuring, start a new session and ask **"What tools do you have?"** — Copilot should list your Mail.tm tools. If they don't appear, verify the path and that the server runs without errors.

> 💡 **Tip:** You can configure **multiple** MCP servers in the same config file. Each gets its own key under `mcpServers`.

---

## Part 5: Using Your MCP Server

The magic of MCP is that you interact through **natural conversation** — no need to remember function names or parameters:

```
You: Create a temporary email address for me
Copilot: [calls get_domains → create_account → login]
         Done! Your temporary email is random123@dpptd.com
```

```
You: Check if I have any new emails
Copilot: [calls list_messages with the saved token]
         You have 2 new messages:
         1. "Welcome to Mail.tm" from noreply@mail.tm
         2. "Verify your account" from service@example.com
```

```
You: Read the second email
Copilot: [calls read_message with the message ID]
         Here's the content of "Verify your account"...
```

Copilot chains multiple tools together automatically — it figures out the right sequence based on your request.

---

## 🏋️ Exercise

### Build a Mail.tm MCP Server

Time to build it yourself! Follow the TDD approach — write a test, watch it fail, implement, watch it pass.

1. **Ask Copilot to** navigate to the exercise folder and install dependencies:
   ```
   Navigate to exercises/cli/09-mail-mcp/ and install the requirements
   ```

2. **Tell Copilot to** open `server.py`, review the `TODO` comments, and implement each tool using TDD:

   For each tool (`get_domains`, `create_account`, `login`, `list_messages`, `read_message`):
   - Write a test in `test_server.py` for the tool
   - Run `pytest test_server.py` and watch it fail 🔴
   - Implement the tool in `server.py`
   - Run `pytest test_server.py` and watch it pass 🟢

3. **Ask Copilot to** configure the MCP server by adding it to `.copilot/mcp-config.json` so Copilot CLI can discover it. You don't need to do this manually — Copilot can create the config file for you.

4. **Exit and resume** the session to load the MCP server:

   Copilot CLI discovers MCP servers at session startup, so you need to restart the session for your new server to be loaded.

   - Type `/exit` to exit Copilot CLI
   - You'll see a message like: `Resume this session with copilot --resume=<session-id>`
   - Run that command to resume your session with the MCP server now loaded

   > 💡 **Why resume?** Resuming keeps your conversation history and context intact while reloading the MCP configuration. A fresh `copilot` command would also load the MCP server, but you'd lose your session context.

5. **Test with Copilot CLI:**

   Now that the MCP server is loaded, try:
   - "Create a temporary email address for me"
   - "Check if I have any new emails"
   - "Read my latest message"

6. **Stuck?** A reference solution is available in `.solution/` if you need it.

> 💡 **Tip:** Start with `get_domains` — it's the simplest tool with no authentication. Build confidence before tackling the auth-dependent tools.

---

## ✅ Verification

Type **`verify`** or **`check my work`** to verify lesson completion.

**Completion criteria:**
1. `exercises/cli/09-mail-mcp/server.py` exists and contains MCP tool definitions (`@mcp.tool()`)
2. `exercises/cli/09-mail-mcp/test_server.py` exists with tests
3. `.copilot/mcp-config.json` exists and configures the `mail-tm` server
4. Server starts without import errors

---

## 📋 Quick Reference Card

```
┌─────────────────────────────────────────────────────┐
│              MCP SERVERS                            │
├─────────────────────────────────────────────────────┤
│  Setup:                                             │
│  • Install:  pip install "mcp[cli]" httpx           │
│  • Import:   from mcp.server.fastmcp import FastMCP │
│  • Create:   mcp = FastMCP("server-name")           │
├─────────────────────────────────────────────────────┤
│  Tools:                                             │
│  • Decorator: @mcp.tool()                           │
│  • Functions must be async                          │
│  • Docstring → tool description for Copilot         │
│  • Type hints → parameter schema                    │
├─────────────────────────────────────────────────────┤
│  Config (.copilot/mcp-config.json):                 │
│  • "type": "stdio" for local servers                │
│  • "command": executable (python, node)             │
│  • "args": path to server file                      │
├─────────────────────────────────────────────────────┤
│  Running:                                           │
│  • mcp.run(transport="stdio")                       │
│  • Copilot auto-discovers from config               │
│  • Test: "What tools do you have?"                  │
└─────────────────────────────────────────────────────┘
```

---

## 📝 Summary

| Topic | Key Point |
|-------|-----------|
| **MCP** | Open standard for connecting AI assistants to external tools |
| **Python SDK** | `FastMCP` class + `@mcp.tool()` decorator makes it simple |
| **Mail.tm** | Real-world API wrapper example — no API key needed |
| **Config** | One JSON file in `.copilot/` configures everything |
| **Usage** | Copilot automatically discovers and calls MCP tools |

**Key Takeaways:**
- MCP extends Copilot with **custom tools** via a standard protocol
- The Python SDK makes building servers easy — just decorate async functions
- **Docstrings are critical** — they tell Copilot when and how to use each tool
- Mail.tm provides a great real-world example of wrapping an external service
- Configuration is a single JSON file — Copilot handles discovery automatically

---

## 🚀 Next Steps

Congratulations! You've completed all lessons in the GitHub Copilot Tutorial! 🎉

You've learned everything from basic Chat features to building custom MCP servers. Here are some ideas for what to do next:

- **Build MCP servers** for your own APIs and services
- **Create custom instructions** for your team's workflows
- **Explore the MCP ecosystem** for pre-built servers at [modelcontextprotocol.io](https://modelcontextprotocol.io)
- **Share what you've learned** with your team

Revisit any lesson anytime to refresh your skills. Happy coding! 🚀
