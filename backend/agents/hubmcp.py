import asyncio
from langchain_mcp_adapters.client import MultiServerMCPClient
from dotenv import load_dotenv
import os

load_dotenv()

token = os.getenv("GITHUB_ACCESS_TOKEN")


async def setup_mcp_client():
    """Initialize and return MCP client with GitHub tools."""
    client = MultiServerMCPClient(
        {
            "github": {
                "command": "npx",
                "args": ["-y", "@modelcontextprotocol/server-github"],
                "env": {"GITHUB_PERSONAL_ACCESS_TOKEN": token},
                "transport": "stdio",
            }
        }
    )
    print("✅ MCP Client created successfully")
    return client


async def get_mcp_tools():
    """Get all MCP tools from the client."""
    client = await setup_mcp_client()
    tools = await client.get_tools()
    print(f"✅ Loaded {len(tools)} GitHub MCP tools")
    return tools


# For synchronous imports
def get_tools_sync():
    """Synchronous wrapper to get MCP tools."""
    return asyncio.run(get_mcp_tools())
