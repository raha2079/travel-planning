"""MCP server entry point for travel planning plugin."""

import sys
import asyncio
from pathlib import Path

# Add parent directory to path to import contract and plugin modules
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from plugin.server import main

if __name__ == "__main__":
    asyncio.run(main())
