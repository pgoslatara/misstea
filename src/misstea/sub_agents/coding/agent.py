from google.adk.agents import Agent

from misstea.constants import AGENT_MODEL
from misstea.sub_agents.coding.tools import (
    list_directory_contents,
    read_directory,
    read_file,
    replace_in_file,
    write_to_file,
)


def get_coding_agent() -> Agent:
    """Return a coding agent.

    Returns:
        Agent: The coding agent.

    """
    return Agent(
        model=AGENT_MODEL,
        name="coding_agent",
        instruction="""You are a helpful coding assistant. You can:

        * Read, write, and modify files.

        Constraints:
        *
        """,
        tools=[
            list_directory_contents,
            read_directory,
            read_file,
            write_to_file,
            replace_in_file,
        ],
    )


root_agent = get_coding_agent()
