from __future__ import annotations

from typing import TYPE_CHECKING, AsyncGenerator

from google.adk.agents import BaseAgent, LlmAgent, ParallelAgent, SequentialAgent
from google.adk.events import Event
from google.adk.tools import google_search
from google.genai import types as genai_types

from misstea.constants import AGENT_MODEL

if TYPE_CHECKING:
    from google.adk.agents.invocation_context import InvocationContext


class ParallelGoogleSearchAgent(BaseAgent):
    """A Google Search agent that can perform multiple searches in parallel."""

    async def _run_async_impl(
        self, ctx: InvocationContext
    ) -> AsyncGenerator[Event, None]:
        queries = ctx.session.state.get("queries")

        if not queries:
            yield Event(
                author=self.name,
                content=genai_types.Content(
                    parts=[
                        genai_types.Part(
                            text="No queries provided in the session state."
                        )
                    ]
                ),
            )
            return

        # Fan-out
        search_agents = []
        for i, query in enumerate(queries):
            agent = LlmAgent(
                name=f"Searcher_{i}",
                model=AGENT_MODEL,
                instruction=f"Perform a Google search for: {query}",
                tools=[google_search],
                output_key=f"result_{i}",
            )
            search_agents.append(agent)

        parallel_search = ParallelAgent(name="ParallelSearch", sub_agents=search_agents)

        # Gather
        gatherer = LlmAgent(
            name="Gatherer",
            model=AGENT_MODEL,
            instruction="Summarize the following search results:\n"
            + "\n".join([f"{{{f'result_{i}'}}}" for i in range(len(queries))]),
        )

        workflow = SequentialAgent(
            name="SearchWorkflow", sub_agents=[parallel_search, gatherer]
        )

        async for event in workflow.run_async(ctx):
            yield event


def get_google_search_agent() -> ParallelGoogleSearchAgent:
    """Return a Google Search agent.

    Returns:
        Agent: The Google Search agent.

    """
    return ParallelGoogleSearchAgent(
        name="google_search_agent",
        description=(
            "Performs multiple Google searches in parallel and summarizes the results."
        ),
    )


google_search_agent = get_google_search_agent()
