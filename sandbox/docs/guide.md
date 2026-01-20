# User Guide

## Available Tools

### list_files
Lists files and directories within the sandbox.

**Usage:**
```python
list_files("")  # List root directory
list_files("docs")  # List docs subdirectory
```

### read_text_file
Reads the content of a text file.

**Usage:**
```python
read_text_file("welcome.txt")
read_text_file("docs/guide.md")
```

## Security

All file operations are sandboxed. Attempts to access files outside the sandbox will fail with a PathValidationError.
