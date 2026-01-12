# penr-oz MCP Server

A minimal FastMCP-based server scaffold for the penr-oz project. This repository provides a clean starting point for adding tools, resources, and prompts.

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

## Project layout

```text
penr-oz-mcp-server/
|-- pyproject.toml
|-- README.md
|-- server.py
|-- app/
|   |-- __init__.py
|   |-- tools.py
|   |-- resources.py
|   |-- prompts.py
|   `-- config.py
`-- tests/
    `-- test_server_smoke.py
```

## Modules

- `app/config.py` holds server metadata and environment flags.
- `app/tools.py` defines MCP tools.
- `app/resources.py` defines MCP resources.
- `app/prompts.py` defines MCP prompt templates.
- `server.py` wires everything together and starts the server.

## Adding tools, resources, and prompts

Define a new tool/resource/prompt in the relevant module, then register it in `server.py`.

Example registration:

```python
from app.tools import ping
mcp.add_tool(ping)
```

## Testing

```bash
pytest
```
