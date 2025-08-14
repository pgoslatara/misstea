from google.adk.agents import Agent

from misstea.constants import AGENT_MODEL
from misstea.sub_agents.coding.tools import read_file, replace_in_file, write_to_file


def get_coding_agent() -> Agent:
    """Return a coding agent.

    Returns:
        Agent: The coding agent.

    """
    return Agent(
        model=AGENT_MODEL,
        name="coding_agent",
        instruction="You are a helpful coding assistant. You can read, write, and modify files.",
        tools=[read_file, write_to_file, replace_in_file],
    )


coding_agent = get_coding_agent()
