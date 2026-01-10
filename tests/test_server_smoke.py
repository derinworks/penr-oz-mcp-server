"""Smoke tests for server scaffolding."""

from server import create_mcp


def test_server_registers_components() -> None:
    """Server initializes with at least one tool, resource, and prompt."""
    mcp = create_mcp()

    tools = getattr(mcp, "tools", None)
    resources = getattr(mcp, "resources", None)
    prompts = getattr(mcp, "prompts", None)

    assert tools, "Expected at least one registered tool."
    assert resources, "Expected at least one registered resource."
    assert prompts, "Expected at least one registered prompt."
