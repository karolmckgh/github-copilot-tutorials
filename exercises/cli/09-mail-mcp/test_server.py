"""
Mail.tm MCP Server Tests — Exercise 9
=======================================
Write unit tests for each tool in server.py.

TDD workflow:
  1. Write a test for one tool
  2. Run: pytest test_server.py -v  →  watch it FAIL 🔴
  3. Implement the tool in server.py
  4. Run: pytest test_server.py -v  →  watch it PASS 🟢
  5. Repeat for the next tool

Mocking pattern (hint):
    1. Create a mock httpx.AsyncClient using AsyncMock
    2. Set up __aenter__ / __aexit__ so it works as an async context manager
    3. Patch "server.httpx.AsyncClient" to return your mock
    4. Call the tool function and assert on the result
"""

import pytest

# TODO: Import your tools from server.py
# TODO: Import mocking utilities (unittest.mock)


# ── Tool 1: get_domains ──────────────────────────────────────

# TODO: Write a test for get_domains


# ── Tool 2: create_account ───────────────────────────────────

# TODO: Write a test for create_account


# ── Tool 3: login ────────────────────────────────────────────

# TODO: Write a test for login


# ── Tool 4: list_messages ────────────────────────────────────

# TODO: Write a test for list_messages


# ── Tool 5: read_message ─────────────────────────────────────

# TODO: Write a test for read_message
