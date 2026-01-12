"""Prompt templates for the MCP server."""


def summarize_prompt(text: str) -> str:
    """Return a prompt asking for a summary of the provided text."""
    return f"Summarize the following text:\n\n{text}"
