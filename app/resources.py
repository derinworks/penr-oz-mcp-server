"""Resource definitions for the MCP server."""

from fastmcp import resource


@resource("oz://info")
def info() -> str:
    """Basic server info."""
    return "penr-oz MCP server"
