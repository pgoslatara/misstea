from typing import Any

from google.adk.tools import ToolContext
from google.adk.tools.agent_tool import AgentTool

from misstea.sub_agents import (
    calculator_agent,
    coding_agent,
    github_agent,
    google_search_agent,
    image_generator_agent,
    outlook_agent,
    terraform_agent,
)


async def _call_agent_helper(
    agent_obj: Any,
    agent_name: str,
    question: str,
    tool_context: ToolContext,
) -> Any:
    """Call an agent, store its output in tool_context.state, and return the output.

    Args:
        agent_obj: The agent object to call.
        agent_name: The name of the agent.
        question: The question to pass to the agent.
        tool_context: The tool context object.

    Returns:
        The output from the agent.

    """
    agent_tool = AgentTool(agent=agent_obj)
    agent_output = await agent_tool.run_async(
        args={"request": question}, tool_context=tool_context
    )
    tool_context.state[f"{agent_name}_agent_output"] = agent_output
    return agent_output


async def call_calculator_agent(
    question: str,
    tool_context: ToolContext,
) -> Any:
    """Tool to call Calculator agent.

    Returns:
        Any: The output from the Calculator agent.

    """
    return await _call_agent_helper(
        calculator_agent, "calculator", question, tool_context
    )


async def call_coding_agent(
    question: str,
    tool_context: ToolContext,
) -> Any:
    """Tool to call Coding agent.

    Returns:
        Any: The output from the Coding agent.

    """
    return await _call_agent_helper(coding_agent, "coding", question, tool_context)


async def call_github_agent(
    question: str,
    tool_context: ToolContext,
) -> Any:
    """Tool to call GitHub agent.

    Returns:
        Any: The output from the GitHub agent.

    """
    return await _call_agent_helper(github_agent, "github", question, tool_context)


async def call_google_search_agent(
    question: str,
    tool_context: ToolContext,
) -> Any:
    """Tool to call Google Search agent.

    Returns:
        Any: The output from the Google Search agent.

    """
    return await _call_agent_helper(
        google_search_agent, "google_search", question, tool_context
    )


async def call_image_generator_agent(
    question: str,
    tool_context: ToolContext,
) -> Any:
    """Tool to call Image Generator agent.

    Returns:
        Any: The output from the Image Generator agent.

    """
    return await _call_agent_helper(
        image_generator_agent, "image_generato", question, tool_context
    )


async def call_outlook_agent(
    question: str,
    tool_context: ToolContext,
) -> Any:
    """Tool to call Outlook agent.

    Returns:
        Any: The output from the Outlook agent.

    """
    return await _call_agent_helper(outlook_agent, "outlook", question, tool_context)


async def call_terraform_agent(
    question: str,
    tool_context: ToolContext,
) -> Any:
    """Tool to call Terraform agent.

    Returns:
        Any: The output from the Terraform agent.

    """
    return await _call_agent_helper(
        terraform_agent, "terraform", question, tool_context
    )
