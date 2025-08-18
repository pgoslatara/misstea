from google.adk.agents import LlmAgent
from google.adk.tools import google_search

from misstea.constants import AGENT_MODEL


def get_google_search_agent() -> LlmAgent:
    """Return a Google Search agent.

    Returns:
        Agent: The Google Search agent.

    """
    return LlmAgent(
        model=AGENT_MODEL,
        name="google_search_agent",
        instruction="You are a helpful search assistant. You must use the google_search tool to answer questions.",
        tools=[google_search],
    )


root_agent = get_google_search_agent()
