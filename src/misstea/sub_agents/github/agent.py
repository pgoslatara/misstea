import os

from google.adk.agents import Agent
from google.adk.tools.mcp_tool import McpToolset  # ty: ignore[possibly-missing-import]
from google.adk.tools.mcp_tool.mcp_session_manager import StreamableHTTPServerParams

from misstea.constants import AGENT_MODEL

root_agent = Agent(
    model=AGENT_MODEL,
    name="github_agent",
    instruction="Help users get information from GitHub",
    tools=[
        McpToolset(
            connection_params=StreamableHTTPServerParams(
                url="https://api.githubcopilot.com/mcp/",
                headers={
                    "Authorization": f"Bearer {os.environ['PERSONAL_ACCESS_TOKEN_GITHUB']}",
                    "X-MCP-Toolsets": "all",
                    "X-MCP-Readonly": "true",
                },
            ),
        )
    ],
)
