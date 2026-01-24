"""Tests for prompt templates."""

from __future__ import annotations

import asyncio
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from app.prompts import summarize_text, summarize_prompt
from server import create_mcp


def test_summarize_text_prompt() -> None:
    """Test that summarize_text generates a valid prompt."""
    result = summarize_text("This is a test document.")
    assert "test document" in result
    assert "summary" in result.lower()


def test_summarize_prompt_backward_compatibility() -> None:
    """Test that legacy summarize_prompt still works."""
    text = "This is a test document."
    legacy_result = summarize_prompt(text)
    new_result = summarize_text(text)

    # Legacy function should produce the same output as the new one
    assert legacy_result == new_result


def test_all_prompts_registered() -> None:
    """Test that all prompts including legacy are registered."""
    mcp = create_mcp()
    prompts = asyncio.run(mcp.get_prompts())

    prompt_names = list(prompts.keys()) if isinstance(prompts, dict) else [p.name for p in prompts]

    # Check new prompts are registered
    assert "summarize_text" in prompt_names
    assert "extract_tasks" in prompt_names
    assert "analyze_code" in prompt_names
    assert "write_design_doc" in prompt_names
    assert "refactor_instructions" in prompt_names

    # Check legacy prompt is also registered for backward compatibility
    assert "summarize_prompt" in prompt_names
