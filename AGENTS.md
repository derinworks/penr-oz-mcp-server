# AGENTS

## Project purpose
This repository is a minimal FastMCP-based MCP server scaffold for the penr-oz project.

## Repository structure
- `server.py`: FastMCP entrypoint and component registration.
- `app/config.py`: server name, version, and environment flags.
- `app/tools.py`: MCP tools.
- `app/resources.py`: MCP resources.
- `app/prompts.py`: MCP prompt templates.
- `tests/test_server_smoke.py`: smoke tests for registration.

## Coding conventions
- Clarity over cleverness.
- Keep functions small and explicit.
- Add docstrings to all functions and modules.
- Avoid overengineering; prefer straightforward patterns.

## How to add tools, resources, and prompts
1) Define the new function in `app/tools.py`, `app/resources.py`, or `app/prompts.py`.
2) Import it in `server.py`.
3) Register it on the `FastMCP` instance:

```python
from app.tools import ping
mcp.add_tool(ping)
```

## Run and smoke test
- Install: `pip install -e .`
- Run server: `python server.py`
- Run tests: `pytest`

## Non-goals
- No production hardening or deployment configuration.
- No secrets or credentials in repo.
- No databases, auth, or heavy infrastructure.
