"""Tool definitions for the MCP server."""

from fastmcp import tool


@tool
def ping() -> str:
    """Health check tool."""
    return "pong"
