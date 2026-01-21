"""Tests for filesystem operations and security."""

from __future__ import annotations

import sys
from pathlib import Path
import pytest

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from app.filesystem import (
    validate_path,
    list_directory,
    read_file,
    PathValidationError,
)
from app.config import SANDBOX_ROOT


class TestPathValidation:
    """Test path validation and security."""

    def test_validate_simple_path(self):
        """Valid simple path should resolve correctly."""
        result = validate_path("welcome.txt")
        assert result.is_absolute()
        assert str(result).startswith(str(SANDBOX_ROOT.resolve()))

    def test_validate_subdirectory_path(self):
        """Valid subdirectory path should resolve correctly."""
        result = validate_path("docs/guide.md")
        assert result.is_absolute()
        assert str(result).startswith(str(SANDBOX_ROOT.resolve()))

    def test_validate_empty_path(self):
        """Empty path should resolve to sandbox root."""
        result = validate_path("")
        assert result.resolve() == SANDBOX_ROOT.resolve()

    def test_validate_leading_slash(self):
        """Path with leading slash should be handled correctly."""
        result = validate_path("/welcome.txt")
        assert result.is_absolute()
        assert str(result).startswith(str(SANDBOX_ROOT.resolve()))

    def test_prevent_directory_traversal_dotdot(self):
        """Directory traversal with .. should be blocked."""
        with pytest.raises(PathValidationError, match="escape sandbox"):
            validate_path("../etc/passwd")

    def test_prevent_directory_traversal_multiple_dotdot(self):
        """Multiple .. traversal attempts should be blocked."""
        with pytest.raises(PathValidationError, match="escape sandbox"):
            validate_path("docs/../../etc/passwd")

    def test_prevent_directory_traversal_encoded(self):
        """Encoded directory traversal characters are treated literally."""
        # URL encoded paths are treated as literal filenames by Path
        # This is acceptable since the resolve() check will catch actual traversal
        result = validate_path("..%2F..%2Fetc%2Fpasswd")
        assert str(result).startswith(str(SANDBOX_ROOT.resolve()))

    def test_prevent_absolute_path_escape(self):
        """Absolute paths are treated as relative to sandbox root."""
        # Leading slashes are stripped, so /etc/passwd becomes sandbox/etc/passwd
        result = validate_path("/etc/passwd")
        assert str(result).startswith(str(SANDBOX_ROOT.resolve()))
        # The path is treated as relative to sandbox
        assert result == SANDBOX_ROOT / "etc/passwd"

    def test_prevent_sibling_directory_attack(self):
        """Sibling directories with similar prefixes should be blocked."""
        # If sandbox is at /path/to/sandbox, paths like ../sandbox_backup
        # should be blocked even though "sandbox_backup" starts with "sandbox"
        with pytest.raises(PathValidationError, match="escape sandbox"):
            # Try to escape to a sibling directory
            validate_path("../sandbox_sibling/secret.txt")

    def test_reject_symlinks(self):
        """Symlinks should be rejected to prevent information leakage."""
        # Create a symlink in the sandbox
        link_path = SANDBOX_ROOT / "test_link"
        target_path = SANDBOX_ROOT / "welcome.txt"

        try:
            link_path.symlink_to(target_path)

            # Accessing the symlink should raise an error
            with pytest.raises(PathValidationError, match="Symlinks are not allowed"):
                validate_path("test_link")
        finally:
            # Clean up
            if link_path.exists():
                link_path.unlink()

    def test_reject_symlink_in_directory_path(self):
        """Symlinks in directory paths should be rejected."""
        # Create a symlinked directory
        link_dir = SANDBOX_ROOT / "link_dir"
        target_dir = SANDBOX_ROOT / "docs"

        try:
            link_dir.symlink_to(target_dir)

            # Accessing through the symlinked directory should fail
            with pytest.raises(PathValidationError, match="Symlinks are not allowed"):
                validate_path("link_dir/guide.md")
        finally:
            # Clean up
            if link_dir.exists():
                link_dir.unlink()


class TestListDirectory:
    """Test directory listing functionality."""

    def test_list_root_directory(self):
        """Listing root directory should return entries."""
        entries = list_directory("")
        assert isinstance(entries, list)
        assert len(entries) > 0

        # Check structure of entries
        for entry in entries:
            assert "name" in entry
            assert "type" in entry
            assert "path" in entry
            assert entry["type"] in ["file", "directory"]

    def test_list_subdirectory(self):
        """Listing subdirectory should return correct entries."""
        entries = list_directory("docs")
        assert isinstance(entries, list)

        # Should have guide.md
        names = [e["name"] for e in entries]
        assert "guide.md" in names

    def test_list_nonexistent_directory(self):
        """Listing nonexistent directory should raise FileNotFoundError."""
        with pytest.raises(FileNotFoundError):
            list_directory("nonexistent")

    def test_list_file_not_directory(self):
        """Listing a file should raise NotADirectoryError."""
        with pytest.raises(NotADirectoryError):
            list_directory("welcome.txt")

    def test_list_directory_traversal_blocked(self):
        """Directory traversal in list should be blocked."""
        with pytest.raises(PathValidationError, match="escape sandbox"):
            list_directory("../")

    def test_list_returns_sorted_entries(self):
        """Directory listing should return sorted entries."""
        entries = list_directory("data")
        names = [e["name"] for e in entries]

        # Check if sorted
        assert names == sorted(names)

    def test_list_includes_file_sizes(self):
        """File entries should include size information."""
        entries = list_directory("data")

        for entry in entries:
            if entry["type"] == "file":
                assert "size" in entry
                assert isinstance(entry["size"], int)
                assert entry["size"] >= 0

    def test_list_skips_symlinks(self):
        """Directory listing should skip symlinks."""
        # Create a symlink in a directory
        link_path = SANDBOX_ROOT / "data" / "test_link"
        target_path = SANDBOX_ROOT / "welcome.txt"

        try:
            link_path.symlink_to(target_path)

            # List the directory
            entries = list_directory("data")
            names = [e["name"] for e in entries]

            # Symlink should not appear in listing
            assert "test_link" not in names
        finally:
            # Clean up
            if link_path.exists():
                link_path.unlink()


class TestReadFile:
    """Test file reading functionality."""

    def test_read_simple_file(self):
        """Reading a simple file should return content."""
        content = read_file("welcome.txt")
        assert isinstance(content, str)
        assert len(content) > 0
        assert "Welcome" in content

    def test_read_subdirectory_file(self):
        """Reading file in subdirectory should work."""
        content = read_file("docs/guide.md")
        assert isinstance(content, str)
        assert "User Guide" in content

    def test_read_json_file(self):
        """Reading JSON file should return text content."""
        content = read_file("data/sample.json")
        assert isinstance(content, str)
        assert "penr-oz-mcp-server" in content

    def test_read_nonexistent_file(self):
        """Reading nonexistent file should raise FileNotFoundError."""
        with pytest.raises(FileNotFoundError):
            read_file("nonexistent.txt")

    def test_read_directory_not_file(self):
        """Reading a directory should raise IsADirectoryError."""
        with pytest.raises(IsADirectoryError):
            read_file("docs")

    def test_read_directory_traversal_blocked(self):
        """Directory traversal in read should be blocked."""
        with pytest.raises(PathValidationError, match="escape sandbox"):
            read_file("../../../etc/passwd")

    def test_read_with_leading_slash(self):
        """Reading with leading slash should work."""
        content = read_file("/welcome.txt")
        assert isinstance(content, str)
        assert "Welcome" in content

    def test_read_rejects_symlinks(self):
        """Reading symlinks should be rejected."""
        # Create a symlink
        link_path = SANDBOX_ROOT / "read_link"
        target_path = SANDBOX_ROOT / "welcome.txt"

        try:
            link_path.symlink_to(target_path)

            # Reading the symlink should fail
            with pytest.raises(PathValidationError, match="Symlinks are not allowed"):
                read_file("read_link")
        finally:
            # Clean up
            if link_path.exists():
                link_path.unlink()


class TestSandboxIntegration:
    """Integration tests for sandbox security."""

    def test_sandbox_root_exists(self):
        """Sandbox root directory should exist or be created."""
        assert SANDBOX_ROOT.exists()
        assert SANDBOX_ROOT.is_dir()

    def test_cannot_escape_sandbox_with_symlink_path(self):
        """Paths that would escape via symlinks should be blocked."""
        # This tests the resolve() behavior
        result = validate_path("docs/../welcome.txt")

        # Should resolve to sandbox/welcome.txt
        assert result.resolve() == (SANDBOX_ROOT / "welcome.txt").resolve()

    def test_multiple_operations_maintain_security(self):
        """Multiple operations should all respect sandbox."""
        # List root
        entries = list_directory("")
        assert len(entries) > 0

        # Read a file
        content = read_file("welcome.txt")
        assert len(content) > 0

        # List subdirectory
        docs_entries = list_directory("docs")
        assert len(docs_entries) > 0

        # All operations should succeed within sandbox
        assert True
