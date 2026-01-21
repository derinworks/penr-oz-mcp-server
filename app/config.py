"""Central configuration for the MCP server."""

import os
from pathlib import Path

SERVER_NAME = "penr-oz-mcp-server"
VERSION = "0.1.0"
ENVIRONMENT = "development"

# Filesystem sandbox configuration
PROJECT_ROOT = Path(__file__).parent.parent
SANDBOX_ROOT = PROJECT_ROOT / "sandbox"
