"""
Mail.tm MCP Server Tests — Reference Solution
================================================
Complete working tests for all 5 MCP tools.
"""

import pytest
from unittest.mock import AsyncMock, patch, MagicMock
import httpx

from server import get_domains, create_account, login, list_messages, read_message

BASE_URL = "https://api.mail.tm"


@pytest.fixture
def mock_response():
    """Create a mock httpx Response."""
    def _make(json_data, status_code=200):
        response = MagicMock(spec=httpx.Response)
        response.status_code = status_code
        response.json.return_value = json_data
        response.raise_for_status = MagicMock()
        return response
    return _make


@pytest.mark.asyncio
async def test_get_domains(mock_response):
    """Test that get_domains returns available email domains."""
    expected = {"hydra:member": [{"id": "1", "domain": "example.com", "isActive": True}]}

    mock_client = AsyncMock()
    mock_client.__aenter__ = AsyncMock(return_value=mock_client)
    mock_client.__aexit__ = AsyncMock(return_value=False)
    mock_client.get = AsyncMock(return_value=mock_response(expected))

    with patch("server.httpx.AsyncClient", return_value=mock_client):
        domains = await get_domains()

    assert len(domains) == 1
    assert domains[0]["domain"] == "example.com"
    mock_client.get.assert_called_once_with(f"{BASE_URL}/domains")


@pytest.mark.asyncio
async def test_create_account(mock_response):
    """Test that create_account creates a new email account."""
    expected = {"id": "abc123", "address": "test@example.com"}

    mock_client = AsyncMock()
    mock_client.__aenter__ = AsyncMock(return_value=mock_client)
    mock_client.__aexit__ = AsyncMock(return_value=False)
    mock_client.post = AsyncMock(return_value=mock_response(expected))

    with patch("server.httpx.AsyncClient", return_value=mock_client):
        result = await create_account("test@example.com", "password123")

    assert result["address"] == "test@example.com"
    mock_client.post.assert_called_once_with(
        f"{BASE_URL}/accounts",
        json={"address": "test@example.com", "password": "password123"}
    )


@pytest.mark.asyncio
async def test_login(mock_response):
    """Test that login returns an authentication token."""
    expected = {"token": "jwt-token-here"}

    mock_client = AsyncMock()
    mock_client.__aenter__ = AsyncMock(return_value=mock_client)
    mock_client.__aexit__ = AsyncMock(return_value=False)
    mock_client.post = AsyncMock(return_value=mock_response(expected))

    with patch("server.httpx.AsyncClient", return_value=mock_client):
        token = await login("test@example.com", "password123")

    assert token == "jwt-token-here"


@pytest.mark.asyncio
async def test_list_messages(mock_response):
    """Test that list_messages returns inbox messages."""
    expected = {"hydra:member": [
        {"id": "msg1", "from": {"address": "sender@test.com"}, "subject": "Hello"}
    ]}

    mock_client = AsyncMock()
    mock_client.__aenter__ = AsyncMock(return_value=mock_client)
    mock_client.__aexit__ = AsyncMock(return_value=False)
    mock_client.get = AsyncMock(return_value=mock_response(expected))

    with patch("server.httpx.AsyncClient", return_value=mock_client):
        messages = await list_messages("my-token")

    assert len(messages) == 1
    assert messages[0]["subject"] == "Hello"
    mock_client.get.assert_called_once_with(
        f"{BASE_URL}/messages",
        headers={"Authorization": "Bearer my-token"}
    )


@pytest.mark.asyncio
async def test_read_message(mock_response):
    """Test that read_message returns a specific message."""
    expected = {
        "id": "msg1",
        "from": {"address": "sender@test.com"},
        "subject": "Hello",
        "text": "Hello World!"
    }

    mock_client = AsyncMock()
    mock_client.__aenter__ = AsyncMock(return_value=mock_client)
    mock_client.__aexit__ = AsyncMock(return_value=False)
    mock_client.get = AsyncMock(return_value=mock_response(expected))

    with patch("server.httpx.AsyncClient", return_value=mock_client):
        message = await read_message("my-token", "msg1")

    assert message["subject"] == "Hello"
    assert message["text"] == "Hello World!"
    mock_client.get.assert_called_once_with(
        f"{BASE_URL}/messages/msg1",
        headers={"Authorization": "Bearer my-token"}
    )
