"""Sub-agents for MissTea."""

from misstea.sub_agents.calculator.agent import root_agent as calculator_agent
from misstea.sub_agents.coding.agent import root_agent as coding_agent
from misstea.sub_agents.filesystem.agent import root_agent as filesystem_agent
from misstea.sub_agents.github.agent import root_agent as github_agent
from misstea.sub_agents.google_search.agent import root_agent as google_search_agent
from misstea.sub_agents.image_generator.agent import root_agent as image_generator_agent
from misstea.sub_agents.interactive_blogger.agent import (
    root_agent as interactive_blogger_agent,
)
from misstea.sub_agents.outlook.agent import root_agent as outlook_agent
from misstea.sub_agents.terraform.agent import root_agent as terraform_agent

__all__ = [
    "calculator_agent",
    "coding_agent",
    "filesystem_agent",
    "github_agent",
    "google_search_agent",
    "image_generator_agent",
    "interactive_blogger_agent",
    "outlook_agent",
    "terraform_agent",
]
