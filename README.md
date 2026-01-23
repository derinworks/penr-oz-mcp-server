# penr-oz MCP Server

[![Tests](https://github.com/derinworks/penr-oz-mcp-server/actions/workflows/tests.yml/badge.svg)](https://github.com/derinworks/penr-oz-mcp-server/actions/workflows/tests.yml)

A FastMCP-based server for the penr-oz project with secure sandboxed filesystem operations. This repository provides tools for reading files and listing directories within a protected sandbox environment.

## Install

Create and activate a virtual environment first:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

```bash
pip install -e .
```

For development and testing:

```bash
pip install -e ".[dev]"
```

## Run

```bash
python server.py             # stdio server
fastmcp run server.py        # if using the FastMCP CLI
```

## Features

### API Integration Tools

The server provides tools for integrating with external HTTP APIs, demonstrating asynchronous operations with comprehensive error handling.

#### Tools

**`fetch_json(url: str, timeout: float = 10.0)`**
- Fetches JSON data from public HTTP APIs
- Supports asynchronous operations with configurable timeout
- Validates URLs and handles errors gracefully
- Example: `fetch_json("https://api.github.com/repos/python/cpython")`

**Error Handling:**
- `InvalidURLError`: Malformed URLs or unsupported schemes
- `TimeoutError`: Request exceeds timeout duration (default: 10s)
- `HTTPError`: Server returns error status (4xx, 5xx)
- `JSONDecodeError`: Response is not valid JSON
- `APIError`: Other network or request errors

**Usage Examples:**
```python
# Fetch repository information
await fetch_json("https://api.github.com/repos/python/cpython")

# With custom timeout
await fetch_json("https://api.example.com/data", timeout=5.0)
```

**Out of Scope:**
- Authentication and secrets management
- Webhooks or streaming
- Non-JSON responses

### Sandboxed Filesystem Access

The server provides secure, read-only access to files within a configured sandbox directory (`./sandbox/`). All file paths are validated to prevent directory traversal attacks.

#### Tools

**`list_files(path: str = "")`**
- Lists files and directories within the sandbox
- Returns metadata including name, type, path, and size
- Example: `list_files("docs")` to list the docs subdirectory

**`read_text_file(path: str)`**
- Reads UTF-8 text content from files within the sandbox
- Raises errors for non-existent files, directories, or invalid paths
- Example: `read_text_file("welcome.txt")`

#### Resources

**`ozfs://{path}`**
- Read-only file access via the ozfs:// protocol
- Example: `ozfs://docs/guide.md` returns the file contents

#### Security

- All paths are restricted to the `./sandbox/` directory
- Directory traversal attempts (e.g., `../`) are blocked
- Paths are validated and resolved before access
- Only UTF-8 text files can be read

## Project layout

```text
penr-oz-mcp-server/
|-- pyproject.toml
|-- README.md
|-- server.py
|-- app/
|   |-- __init__.py
|   |-- api.py             # API integration tools (fetch_json)
|   |-- config.py          # Server configuration and sandbox settings
|   |-- filesystem.py      # Filesystem operations with security validation
|   |-- tools.py           # MCP tools (ping, list_files, read_text_file)
|   |-- resources.py       # MCP resources (info, ozfs://)
|   `-- prompts.py         # MCP prompt templates
|-- sandbox/               # Sandboxed filesystem directory
|   |-- README.md
|   |-- welcome.txt
|   |-- docs/
|   `-- data/
`-- tests/
    |-- test_server_smoke.py
    `-- test_filesystem.py # Filesystem security and functionality tests
```

## Modules

- `app/api.py` - API integration tools for external HTTP services (fetch_json)
- `app/config.py` - Server metadata, environment flags, and sandbox configuration
- `app/filesystem.py` - Secure filesystem operations with path validation
- `app/tools.py` - MCP tools (ping, list_files, read_text_file)
- `app/resources.py` - MCP resources (info, ozfs://)
- `app/prompts.py` - MCP prompt templates
- `server.py` - Server initialization and component registration

## Adding tools, resources, and prompts

Define a new tool/resource/prompt in the relevant module, then register it in `server.py`.

Example registration:

```python
from app.tools import ping
mcp.add_tool(ping)
```

## Testing

Run the test suite locally:

```bash
pytest
```

### Continuous Integration

This project uses GitHub Actions to automatically run tests on every push and pull request. The CI workflow tests the codebase against Python 3.10, 3.11, and 3.12 to ensure compatibility across versions.

Tests must pass before pull requests can be merged. You can view the test results in the [Actions tab](https://github.com/derinworks/penr-oz-mcp-server/actions) or by clicking the badge at the top of this README.
