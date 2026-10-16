"""MCP server implementation for travel planning plugin."""

import json
import sys
from pathlib import Path
from mcp.server import Server
from mcp.server.stdio import stdio_server
import mcp.types as types

# Add parent to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

import contract
from plugin import tools

# Global server instance
server = Server("travel-planning")


@server.list_tools()
async def list_tools() -> list[types.Tool]:
    """List available tools."""
    return [
        types.Tool(
            name="load_request",
            description="Load the travel request with origin, destination, budget, currency, and preferences",
            inputSchema={
                "type": "object",
                "properties": {},
                "additionalProperties": False,
            },
        ),
        types.Tool(
            name="search_flights",
            description="Search available flights, select the preferred one, and return the flight IDs list",
            inputSchema={
                "type": "object",
                "properties": {},
                "additionalProperties": False,
            },
        ),
        types.Tool(
            name="search_hotels",
            description="Search available hotels, select one that fits budget, and return the hotel IDs list",
            inputSchema={
                "type": "object",
                "properties": {},
                "additionalProperties": False,
            },
        ),
        types.Tool(
            name="check_budget",
            description="Calculate total cost (flight + hotel × nights) with full breakdown and check if within budget",
            inputSchema={
                "type": "object",
                "properties": {},
                "additionalProperties": False,
            },
        ),
        types.Tool(
            name="validate_selection",
            description="Validate the final selection and return all booking details",
            inputSchema={
                "type": "object",
                "properties": {},
                "additionalProperties": False,
            },
        ),
    ]


@server.call_tool()
async def call_tool(name: str, arguments: dict) -> list[types.TextContent]:
    """Handle tool calls."""
    try:
        if name == "load_request":
            result = tools.load_request()
        elif name == "search_flights":
            result = tools.search_flights()
        elif name == "search_hotels":
            result = tools.search_hotels()
        elif name == "check_budget":
            result = tools.check_budget()
        elif name == "validate_selection":
            result = tools.validate_selection()
        else:
            return [types.TextContent(type="text", text=f"Unknown tool: {name}")]

        # Return result as JSON
        return [types.TextContent(type="text", text=json.dumps(result, indent=2))]
    except Exception as e:
        return [types.TextContent(type="text", text=f"Error: {str(e)}")]


async def main():
    """Run the MCP server."""
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            server.create_initialization_options()
        )
