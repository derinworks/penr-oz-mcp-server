"""Filesystem operations with sandbox security."""

import os
from pathlib import Path
from typing import List, Dict

from app.config import SANDBOX_ROOT


class PathValidationError(Exception):
    """Raised when a path fails security validation."""
    pass


def validate_path(path: str) -> Path:
    """
    Validate and resolve a path within the sandbox.

    Args:
        path: Relative path within the sandbox

    Returns:
        Absolute resolved path within sandbox

    Raises:
        PathValidationError: If path escapes sandbox or is invalid
    """
    try:
        # Ensure sandbox exists
        SANDBOX_ROOT.mkdir(parents=True, exist_ok=True)

        # Resolve the full path
        if path.startswith('/'):
            # Remove leading slash for relative path
            path = path.lstrip('/')

        candidate_path = SANDBOX_ROOT / path

        # Check for symlinks before resolving to prevent information leakage
        # Check the target path and all parent directories for symlinks
        current = candidate_path
        sandbox_resolved = SANDBOX_ROOT.resolve()

        while current != sandbox_resolved:
            if current.exists() and current.is_symlink():
                raise PathValidationError(
                    f"Symlinks are not allowed: {path}"
                )
            if current == current.parent:
                break
            current = current.parent

        # Now resolve to handle .. and check bounds
        full_path = candidate_path.resolve()

        # Check if resolved path is within sandbox
        # Use is_relative_to() to prevent sibling directory attacks
        if not full_path.is_relative_to(sandbox_resolved):
            raise PathValidationError(
                f"Path '{path}' attempts to escape sandbox"
            )

        return full_path

    except (ValueError, OSError) as e:
        raise PathValidationError(f"Invalid path '{path}': {e}")


def list_directory(path: str = "") -> List[Dict[str, str]]:
    """
    List contents of a directory within the sandbox.

    Args:
        path: Relative path within sandbox (default: root)

    Returns:
        List of dictionaries with file/directory information

    Raises:
        PathValidationError: If path is invalid or escapes sandbox
        FileNotFoundError: If directory doesn't exist
        NotADirectoryError: If path is not a directory
    """
    full_path = validate_path(path)

    if not full_path.exists():
        raise FileNotFoundError(f"Directory not found: {path}")

    if not full_path.is_dir():
        raise NotADirectoryError(f"Not a directory: {path}")

    entries = []
    for item in sorted(full_path.iterdir()):
        # Skip symlinks to prevent information leakage outside sandbox
        if item.is_symlink():
            continue

        # Use lstat() to avoid following symlinks
        item_stat = item.lstat()
        is_dir = item_stat.st_mode & 0o040000  # S_IFDIR

        entry = {
            "name": item.name,
            "type": "directory" if is_dir else "file",
            "path": str(item.relative_to(SANDBOX_ROOT))
        }

        # Add size for files (using lstat data)
        if not is_dir:
            entry["size"] = item_stat.st_size

        entries.append(entry)

    return entries


def read_file(path: str) -> str:
    """
    Read text content from a file within the sandbox.

    Args:
        path: Relative path to file within sandbox

    Returns:
        File contents as string

    Raises:
        PathValidationError: If path is invalid or escapes sandbox
        FileNotFoundError: If file doesn't exist
        IsADirectoryError: If path is a directory
        UnicodeDecodeError: If file is not valid text
    """
    full_path = validate_path(path)

    if not full_path.exists():
        raise FileNotFoundError(f"File not found: {path}")

    if full_path.is_dir():
        raise IsADirectoryError(f"Path is a directory: {path}")

    try:
        return full_path.read_text(encoding='utf-8')
    except UnicodeDecodeError as e:
        raise UnicodeDecodeError(
            e.encoding, e.object, e.start, e.end,
            f"File is not valid UTF-8 text: {path}"
        )
