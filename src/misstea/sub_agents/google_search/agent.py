from google.adk.agents import Agent
from google.adk.tools import google_search

from misstea.constants import AGENT_MODEL

google_search_agent = Agent(
    name="google_search_agent",
    model=AGENT_MODEL,
    instruction="Answer questions using Google Search when needed. Always cite sources.",
    description="Professional search assistant with Google Search capabilities",
    tools=[google_search],
)
