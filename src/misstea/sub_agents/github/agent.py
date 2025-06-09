import os

from google.adk.agents import Agent
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset, StdioServerParameters

from misstea.constants import AGENT_MODEL


def github_mcp():
    """Return a GitHub MCP Toolset.

    Returns:
        MCPToolset: An instance of MCPToolset configured for GitHub.

    """
    # https://github.com/github/github-mcp-server?tab=readme-ov-file#usage-with-vs-code
    return MCPToolset(
        connection_params=StdioServerParameters(
            command="docker",
            args=[
                "run",
                "-i",
                "--rm",
                "-e",
                "GITHUB_PERSONAL_ACCESS_TOKEN",
                "ghcr.io/github/github-mcp-server",
            ],
            env={
                "GITHUB_PERSONAL_ACCESS_TOKEN": os.environ[
                    "GITHUB_PERSONAL_ACCESS_TOKEN"
                ]
            },
        ),
    )


github_agent = Agent(
    model=AGENT_MODEL,
    name="github_agent",
    instruction="You are a data engineer doing research on code from GitHub. When asked for examples, you always use the top examples returned from GitHubs `search_code` tool.",
    tools=[github_mcp()],
)
