"""
Mail.tm MCP Server — Exercise 9
================================
Implement 5 MCP tools that wrap the Mail.tm temporary email API.
Use httpx.AsyncClient to make HTTP requests to the API.

Base URL: https://api.mail.tm
API docs: https://docs.mail.tm/

TODO: Implement each tool below. Replace the NotImplementedError
with real code that calls the Mail.tm API using httpx.
"""

from mcp.server.fastmcp import FastMCP
import httpx

mcp = FastMCP("mail-tm")
BASE_URL = "https://api.mail.tm"


@mcp.tool()
async def get_domains() -> list[dict]:
    """Get available Mail.tm email domains."""
    # TODO: Use httpx.AsyncClient to GET /domains
    # Return the list from resp.json()["hydra:member"]
    raise NotImplementedError


@mcp.tool()
async def create_account(address: str, password: str) -> dict:
    """Create a temporary email account on Mail.tm.

    Args:
        address: Full email address (e.g., user@example.com)
        password: Password for the account (min 8 characters)
    """
    # TODO: POST /accounts with {"address": ..., "password": ...}
    raise NotImplementedError


@mcp.tool()
async def login(address: str, password: str) -> str:
    """Login to Mail.tm and return the authentication token.

    Args:
        address: Email address to login with
        password: Account password
    """
    # TODO: POST /token with {"address": ..., "password": ...}
    # Return resp.json()["token"]
    raise NotImplementedError


@mcp.tool()
async def list_messages(token: str) -> list[dict]:
    """List all messages in the inbox.

    Args:
        token: Authentication token from login
    """
    # TODO: GET /messages with Authorization: Bearer {token} header
    # Return the list from resp.json()["hydra:member"]
    raise NotImplementedError


@mcp.tool()
async def read_message(token: str, message_id: str) -> dict:
    """Read a specific email message by ID.

    Args:
        token: Authentication token from login
        message_id: The ID of the message to read
    """
    # TODO: GET /messages/{message_id} with Authorization header
    raise NotImplementedError


if __name__ == "__main__":
    mcp.run(transport="stdio")
