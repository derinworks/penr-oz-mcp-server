"""MCP server entrypoint for penr-oz."""

from fastmcp import FastMCP

from app.config import SERVER_NAME
from app.prompts import summarize_prompt
from app.resources import info, ozfs_resource
from app.tools import ping, list_files, read_text_file


def create_mcp() -> FastMCP:
    """Create and configure the FastMCP server instance."""
    mcp = FastMCP(name=SERVER_NAME)

    # Register tools
    mcp.tool(ping)
    mcp.tool(list_files)
    mcp.tool(read_text_file)

    # Register resources
    mcp.resource("oz://info")(info)
    mcp.resource("ozfs://{path}")(ozfs_resource)

    # Register prompts
    mcp.prompt(summarize_prompt)

    return mcp


def main() -> None:
    """Run the MCP server."""
    mcp = create_mcp()
    mcp.run()


if __name__ == "__main__":
    main()
