from google.adk.agents import Agent

from misstea.constants import AGENT_MODEL
from misstea.sub_agents.web_scraper.tools import (
    fetch_web_page_contents,
)


def get_web_scraper_agent() -> Agent:
    """Return a web scraper agent.

    Returns:
        Agent: The web scraper agent.

    """
    return Agent(
        model=AGENT_MODEL,
        name="web_scraper_agent",
        instruction="""You are a helpful web scraper assistant. You can:

        * Fetch detailed content from a web page using fetch_web_page_contents.
        """,
        tools=[fetch_web_page_contents],
    )


root_agent = get_web_scraper_agent()
