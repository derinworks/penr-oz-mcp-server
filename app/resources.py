"""Resource definitions for the MCP server."""

from app.filesystem import read_file, PathValidationError


def info() -> str:
    """Basic server info."""
    return "penr-oz MCP server"


def ozfs_resource(path: str) -> str:
    """
    Read-only file access via ozfs:// protocol.

    Args:
        path: File path within sandbox (extracted from ozfs://{path})

    Returns:
        File contents as text

    Raises:
        PathValidationError: If path attempts to escape sandbox
        FileNotFoundError: If file doesn't exist
        IsADirectoryError: If path is a directory
    """
    # Remove leading slash if present
    if path.startswith('/'):
        path = path[1:]

    return read_file(path)
