"""Sub-agents for MissTea."""

from misstea.sub_agents.coding.agent import coding_agent
from misstea.sub_agents.github.agent import root_agent as github_agent
from misstea.sub_agents.google_search.agent import google_search_agent
from misstea.sub_agents.outlook.agent import outlook_agent
from misstea.sub_agents.terraform.agent import terraform_agent

__all__ = [
    "coding_agent",
    "github_agent",
    "google_search_agent",
    "outlook_agent",
    "terraform_agent",
]
