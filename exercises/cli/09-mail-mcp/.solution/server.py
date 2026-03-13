"""
Mail.tm MCP Server — Reference Solution
=========================================
Complete working implementation of the 5 MCP tools.
"""

from mcp.server.fastmcp import FastMCP
import httpx

mcp = FastMCP("mail-tm")
BASE_URL = "https://api.mail.tm"


@mcp.tool()
async def get_domains() -> list[dict]:
    """Get available Mail.tm email domains."""
    async with httpx.AsyncClient() as client:
        resp = await client.get(f"{BASE_URL}/domains")
        resp.raise_for_status()
        data = resp.json()
        return data.get("hydra:member", [])


@mcp.tool()
async def create_account(address: str, password: str) -> dict:
    """Create a temporary email account on Mail.tm.

    Args:
        address: Full email address (e.g., user@example.com)
        password: Password for the account (min 8 characters)
    """
    async with httpx.AsyncClient() as client:
        resp = await client.post(
            f"{BASE_URL}/accounts",
            json={"address": address, "password": password}
        )
        resp.raise_for_status()
        return resp.json()


@mcp.tool()
async def login(address: str, password: str) -> str:
    """Login to Mail.tm and return the authentication token.

    Args:
        address: Email address to login with
        password: Account password
    """
    async with httpx.AsyncClient() as client:
        resp = await client.post(
            f"{BASE_URL}/token",
            json={"address": address, "password": password}
        )
        resp.raise_for_status()
        return resp.json()["token"]


@mcp.tool()
async def list_messages(token: str) -> list[dict]:
    """List all messages in the inbox.

    Args:
        token: Authentication token from login
    """
    async with httpx.AsyncClient() as client:
        resp = await client.get(
            f"{BASE_URL}/messages",
            headers={"Authorization": f"Bearer {token}"}
        )
        resp.raise_for_status()
        data = resp.json()
        return data.get("hydra:member", [])


@mcp.tool()
async def read_message(token: str, message_id: str) -> dict:
    """Read a specific email message by ID.

    Args:
        token: Authentication token from login
        message_id: The ID of the message to read
    """
    async with httpx.AsyncClient() as client:
        resp = await client.get(
            f"{BASE_URL}/messages/{message_id}",
            headers={"Authorization": f"Bearer {token}"}
        )
        resp.raise_for_status()
        return resp.json()


if __name__ == "__main__":
    mcp.run(transport="stdio")
