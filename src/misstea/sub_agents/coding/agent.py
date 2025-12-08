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

        Information:
            * When looking for a file path that was manually inputted, if the path does not exist, then assume that a typo was made. Use your tools to identify where the typo was most likely made and fix it, then alert the user that you have corrected the path. For example, if directed to a directory named `/home/pslattery/workpsace/client_a` and you find that this doesn't exist, first check that `/home/pslattery/workpsace` exists, if it does not, then assess if a similarly named directory like `/home/pslattery/workspace` exists and use that instead.
            * How I structure my repositories:
                * All my client work lives in the `/home/pslattery/workspace` directory. Each sub-directory within this directory contains the files for a single client, for example `/home/pslattery/workspace/client_a` contains all files for client_a.
                * For each client I have a `repos` directory. Each sub-directory within this directory represents a repository. For example, `/home/pslattery/workspace/client_a/repos/data-dbt` contains all files the for the `data-dbt` repository for client_a.
                * Non-client repositories are stored in `/home/pslattery/repos`.
                * If asked to find a repository, assess if it relates to a client or not, then use the above information to search for the relevant directory.
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
