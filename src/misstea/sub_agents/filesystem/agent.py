from pathlib import Path

from google.adk.agents import LlmAgent
from google.adk.tools.mcp_tool.mcp_toolset import (
    MCPToolset,
    StdioConnectionParams,
    StdioServerParameters,
)

from misstea.constants import AGENT_MODEL


def get_filesystem_agent() -> LlmAgent:
    """Return an Image Generator agent.

    Returns:
        Agent: The Image Generator agent.

    """
    return LlmAgent(
        model=AGENT_MODEL,
        name="filesystem_agent",
        instruction=f"""
        You are a helpful filesystem assistant that can help users manage their files.

        You have access to filesystem tools through the Model Context Protocol (MCP).
        You can:
        - List files and directories
        - Read file contents
        - Write to files
        - Create directories

        The current working directory is: {Path().absolute().__str__()}

        Always be helpful and explain what you're doing when performing file operations.
        If a user asks about files, use the available tools to check the filesystem.
        """,
        tools=[
            MCPToolset(
                connection_params=StdioConnectionParams(
                    server_params=StdioServerParameters(
                        command="npx",
                        args=[
                            "-y",  # Auto-confirm npm package installation
                            "@modelcontextprotocol/server-filesystem",
                            Path().absolute().__str__(),
                        ],
                    )
                ),
            )
        ],
    )


root_agent = get_filesystem_agent()
