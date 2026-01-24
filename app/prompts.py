"""Prompt templates for the MCP server."""


def summarize_text(text: str) -> str:
    """
    Generate a prompt for summarizing provided text.

    Use this prompt to get concise summaries of documents, articles, or any
    text content. The AI will extract key points and main ideas.

    Args:
        text: The text content to be summarized

    Returns:
        A formatted prompt requesting a summary of the text
    """
    return f"""Please provide a concise summary of the following text. Focus on the main ideas and key points:

{text}

Summary:"""


def extract_tasks(text: str) -> str:
    """
    Generate a prompt for extracting actionable tasks from text.

    Use this prompt to identify action items, TODOs, and tasks from meeting
    notes, documentation, or any text containing work items.

    Args:
        text: The text content containing potential tasks

    Returns:
        A formatted prompt requesting extraction of tasks from the text
    """
    return f"""Analyze the following text and extract all actionable tasks, action items, and TODOs.
Format each task as a clear, actionable item with any mentioned deadlines or assignees.

Text:
{text}

Tasks:"""


def analyze_code(code: str, language: str = "python") -> str:
    """
    Generate a prompt for analyzing code quality and structure.

    Use this prompt to get detailed analysis of code including potential bugs,
    code smells, performance issues, and improvement suggestions.

    Args:
        code: The source code to analyze
        language: Programming language of the code (default: "python")

    Returns:
        A formatted prompt requesting code analysis
    """
    return f"""Analyze the following {language} code. Provide insights on:
1. Code quality and readability
2. Potential bugs or issues
3. Performance considerations
4. Security vulnerabilities
5. Suggestions for improvement

Code:
```{language}
{code}
```

Analysis:"""


def write_design_doc(feature_description: str, context: str = "") -> str:
    """
    Generate a prompt for creating a technical design document.

    Use this prompt to create comprehensive design documents for new features
    or systems, including architecture, implementation details, and trade-offs.

    Args:
        feature_description: Description of the feature or system to design
        context: Additional context about the project or constraints (optional)

    Returns:
        A formatted prompt requesting a design document
    """
    context_section = f"\n\nProject Context:\n{context}" if context else ""

    return f"""Create a detailed technical design document for the following feature:{context_section}

Feature Description:
{feature_description}

Please structure the design document with the following sections:
1. Overview and Goals
2. Architecture and Components
3. Implementation Approach
4. API/Interface Design
5. Data Models (if applicable)
6. Security Considerations
7. Testing Strategy
8. Alternative Approaches Considered
9. Open Questions and Risks

Design Document:"""


def refactor_instructions(code: str, issues: str, language: str = "python") -> str:
    """
    Generate a prompt for creating refactoring instructions.

    Use this prompt to get step-by-step refactoring guidance for improving
    existing code, addressing technical debt, or resolving specific issues.

    Args:
        code: The source code that needs refactoring
        issues: Description of problems or areas to improve
        language: Programming language of the code (default: "python")

    Returns:
        A formatted prompt requesting refactoring instructions
    """
    return f"""Provide detailed refactoring instructions for the following {language} code.

Issues to address:
{issues}

Current Code:
```{language}
{code}
```

Please provide:
1. Step-by-step refactoring instructions
2. Explanation of why each change improves the code
3. The refactored code
4. Any potential risks or considerations

Refactoring Instructions:"""


def summarize_prompt(text: str) -> str:
    """
    Legacy alias for summarize_text().

    .. deprecated::
        Use summarize_text() instead. This function is maintained for
        backward compatibility with existing MCP clients.

    Args:
        text: The text content to be summarized

    Returns:
        A formatted prompt requesting a summary of the text
    """
    return summarize_text(text)
