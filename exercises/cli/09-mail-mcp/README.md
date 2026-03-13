# Exercise 9: Build a Mail.tm MCP Server

Build a Python MCP (Model Context Protocol) server that wraps the [Mail.tm](https://mail.tm) temporary email API, giving Copilot CLI the ability to create disposable email accounts, check inboxes, and read messages.

## Setup

```bash
pip install -r requirements.txt
```

## File Overview

| File | Description |
|---|---|
| `server.py` | **Your code** — implement the 5 MCP tools here |
| `test_server.py` | **Your tests** — write unit tests for each tool |
| `.solution/` | Reference solution if you get stuck |

## Tools to Implement

1. **get_domains** — Fetch available Mail.tm email domains
2. **create_account** — Register a new temporary email account
3. **login** — Authenticate and retrieve a JWT token
4. **list_messages** — List inbox messages for an account
5. **read_message** — Read a specific email by ID

## Running Tests

```bash
pytest test_server.py -v
```

## Running the Server

Standalone (stdio transport):

```bash
python server.py
```

Or register it in your MCP config (e.g. `.copilot/mcp.json`) and use it from Copilot CLI directly.

## Stuck?

Check the reference solution in `.solution/` for a complete working implementation.
