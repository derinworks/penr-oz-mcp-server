"""Tests for API integration tools."""

import asyncio
import pytest
import respx
import httpx
from app.api import (
    fetch_json,
    InvalidURLError,
    TimeoutError,
    HTTPError,
    JSONDecodeError,
)


@pytest.mark.asyncio
async def test_fetch_json_invalid_url_scheme():
    """Test that invalid URL schemes raise InvalidURLError."""
    with pytest.raises(InvalidURLError):
        await fetch_json("ftp://example.com/data.json")


@pytest.mark.asyncio
async def test_fetch_json_empty_url():
    """Test that empty URL raises InvalidURLError."""
    with pytest.raises(InvalidURLError):
        await fetch_json("")


@pytest.mark.asyncio
async def test_fetch_json_malformed_url():
    """Test that malformed URLs raise appropriate errors."""
    with pytest.raises((InvalidURLError, Exception)):
        await fetch_json("not-a-url")


@pytest.mark.asyncio
@respx.mock
async def test_fetch_json_success(respx_mock):
    """Test successful JSON fetch with mocked HTTP response."""
    # Mock a successful JSON response
    mock_data = {
        "name": "cpython",
        "full_name": "python/cpython",
        "description": "The Python programming language"
    }
    respx_mock.get("https://api.example.com/data").mock(
        return_value=httpx.Response(200, json=mock_data)
    )

    result = await fetch_json("https://api.example.com/data")

    # Verify we got the mocked data back
    assert isinstance(result, dict)
    assert result["name"] == "cpython"
    assert result["full_name"] == "python/cpython"


@pytest.mark.asyncio
@respx.mock
async def test_fetch_json_follows_redirects(respx_mock):
    """Test that HTTP redirects are automatically followed."""
    # Mock the final destination with JSON data
    final_data = {"status": "success", "redirected": True}
    respx_mock.get("https://api.example.com/final").mock(
        return_value=httpx.Response(200, json=final_data)
    )

    # Mock the initial URL with a redirect
    respx_mock.get("https://api.example.com/redirect").mock(
        return_value=httpx.Response(
            302,
            headers={"Location": "https://api.example.com/final"}
        )
    )

    # The redirect should be followed automatically
    result = await fetch_json("https://api.example.com/redirect")

    assert isinstance(result, dict)
    assert result["status"] == "success"
    assert result["redirected"] is True


@pytest.mark.asyncio
@respx.mock
async def test_fetch_json_with_timeout(respx_mock):
    """Test that timeout error is properly raised."""
    # Mock a timeout
    respx_mock.get("https://api.example.com/slow").mock(
        side_effect=httpx.TimeoutException("Connection timeout")
    )

    with pytest.raises(TimeoutError):
        await fetch_json("https://api.example.com/slow", timeout=1.0)


@pytest.mark.asyncio
@respx.mock
async def test_fetch_json_http_error(respx_mock):
    """Test that HTTP errors are properly handled."""
    # Mock a 404 response
    respx_mock.get("https://api.example.com/notfound").mock(
        return_value=httpx.Response(404, json={"error": "Not found"})
    )

    with pytest.raises(HTTPError):
        await fetch_json("https://api.example.com/notfound")


@pytest.mark.asyncio
@respx.mock
async def test_fetch_json_invalid_json(respx_mock):
    """Test that invalid JSON responses raise JSONDecodeError."""
    # Mock a response with invalid JSON
    respx_mock.get("https://api.example.com/invalid").mock(
        return_value=httpx.Response(200, text="not valid json")
    )

    with pytest.raises(JSONDecodeError):
        await fetch_json("https://api.example.com/invalid")


@pytest.mark.asyncio
@respx.mock
async def test_fetch_json_network_error(respx_mock):
    """Test that network errors are properly handled."""
    # Mock a network error
    respx_mock.get("https://api.example.com/error").mock(
        side_effect=httpx.ConnectError("Connection failed")
    )

    with pytest.raises(Exception):  # Will be wrapped in APIError
        await fetch_json("https://api.example.com/error")


@pytest.mark.asyncio
@respx.mock
async def test_fetch_json_cancelled_error_propagates(respx_mock):
    """Test that CancelledError is properly propagated without wrapping."""
    # Mock a slow response to allow cancellation
    async def slow_response(request):
        await asyncio.sleep(10)
        return httpx.Response(200, json={"data": "value"})

    respx_mock.get("https://api.example.com/slow").mock(side_effect=slow_response)

    # Create a task and cancel it
    task = asyncio.create_task(fetch_json("https://api.example.com/slow"))
    await asyncio.sleep(0.1)  # Let the request start
    task.cancel()

    # CancelledError should propagate, not be wrapped in APIError
    with pytest.raises(asyncio.CancelledError):
        await task
