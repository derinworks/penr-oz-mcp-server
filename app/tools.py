"""Tool definitions for the MCP server."""

from typing import List, Dict
from app.filesystem import list_directory, read_file, PathValidationError


def ping() -> str:
    """Health check tool."""
    return "pong"


def list_files(path: str = "") -> List[Dict[str, str]]:
    """
    List files and directories within the sandbox.

    Args:
        path: Relative path within sandbox (default: root directory)

    Returns:
        List of file/directory entries with metadata

    Raises:
        PathValidationError: If path attempts to escape sandbox
        FileNotFoundError: If directory doesn't exist
        NotADirectoryError: If path is not a directory
    """
    return list_directory(path)


def read_text_file(path: str) -> str:
    """
    Read text content from a file within the sandbox.

    Args:
        path: Relative path to file within sandbox

    Returns:
        File contents as text

    Raises:
        PathValidationError: If path attempts to escape sandbox
        FileNotFoundError: If file doesn't exist
        IsADirectoryError: If path is a directory
        UnicodeDecodeError: If file is not valid UTF-8 text
    """
    return read_file(path)
