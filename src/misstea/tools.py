from google.adk.tools import ToolContext
from google.adk.tools.agent_tool import AgentTool

from misstea.sub_agents import github_agent, outlook_agent, terraform_agent


async def call_github_agent(
    question: str,
    tool_context: ToolContext,
):
    """Tool to call GitHub agent.

    Returns:
        Any: The output from the GitHub agent.

    """
    agent_tool = AgentTool(agent=github_agent)

    github_agent_output = await agent_tool.run_async(
        args={"request": question}, tool_context=tool_context
    )
    tool_context.state["github_agent_output"] = github_agent_output
    return github_agent_output


async def call_outlook_agent(
    question: str,
    tool_context: ToolContext,
):
    """Tool to call Outlook agent.

    Returns:
        Any: The output from the Outlook agent.

    """
    agent_tool = AgentTool(agent=outlook_agent)

    outlook_agent_output = await agent_tool.run_async(
        args={"request": question}, tool_context=tool_context
    )
    tool_context.state["outlook_agent_output"] = outlook_agent_output
    return outlook_agent_output


async def call_terraform_agent(
    question: str,
    tool_context: ToolContext,
):
    """Tool to call Terraform agent.

    Returns:
        Any: The output from the Terraform agent.

    """
    agent_tool = AgentTool(agent=terraform_agent)

    terraform_agent_output = await agent_tool.run_async(
        args={"request": question}, tool_context=tool_context
    )
    tool_context.state["terraform_agent_output"] = terraform_agent_output
    return terraform_agent_output
