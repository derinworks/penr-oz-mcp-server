"""MCP server entrypoint for penr-oz."""

from fastmcp import FastMCP

from app.config import SERVER_NAME
from app.prompts import summarize_prompt
from app.resources import info
from app.tools import ping


def create_mcp() -> FastMCP:
    """Create and configure the FastMCP server instance."""
    mcp = FastMCP(name=SERVER_NAME)
    mcp.tool(ping)
    mcp.resource("oz://info")(info)
    mcp.prompt(summarize_prompt)
    return mcp


def main() -> None:
    """Run the MCP server."""
    mcp = create_mcp()
    mcp.run()


if __name__ == "__main__":
    main()
