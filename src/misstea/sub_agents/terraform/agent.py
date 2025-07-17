from google.adk.agents import Agent
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset
from mcp import StdioServerParameters

from misstea.constants import AGENT_MODEL


def terraform_mcp():
    """Return a Terraform MCP Toolset.

    Returns:
        MCPToolset: An instance of MCPToolset configured for Terraform.

    """
    # https://github.com/hashicorp/terraform-mcp-server?tab=readme-ov-file#usage-with-vs-code
    return MCPToolset(
        connection_params=StdioServerParameters(
            command="docker",
            args=["run", "-i", "--rm", "hashicorp/terraform-mcp-server"],
        ),
    )


terraform_agent = Agent(
    model=AGENT_MODEL,
    name="terraform_agent",
    instruction="You are a data engineer doing research on how to use Terraform modules. You always use Terraform's documentation to answer questions but you never return code examples.",
    tools=[terraform_mcp()],
)
