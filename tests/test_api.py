"""Tests for API integration tools."""

import pytest
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
async def test_fetch_json_success():
    """Test successful JSON fetch from a public API."""
    # Using a reliable public API endpoint
    result = await fetch_json("https://api.github.com/repos/python/cpython")

    # Verify we got a dictionary back
    assert isinstance(result, dict)
    # Verify some expected fields exist
    assert "name" in result
    assert "full_name" in result


@pytest.mark.asyncio
async def test_fetch_json_with_timeout():
    """Test that timeout parameter works."""
    # This should work with a reasonable timeout
    result = await fetch_json(
        "https://api.github.com/repos/python/cpython",
        timeout=30.0
    )
    assert isinstance(result, dict)


@pytest.mark.asyncio
async def test_fetch_json_http_error():
    """Test that HTTP errors are properly handled."""
    # GitHub returns 404 for non-existent repos
    with pytest.raises(HTTPError):
        await fetch_json("https://api.github.com/repos/this-does-not-exist-12345/nope-12345")
