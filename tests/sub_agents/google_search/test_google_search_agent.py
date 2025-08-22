import os

import pytest
from google.adk.evaluation.agent_evaluator import AgentEvaluator


@pytest.mark.flaky(reruns=int(os.getenv("SUB_AGENT_TEST_RERUNS")) or 3)  # type: ignore
@pytest.mark.asyncio
async def test_google_search_agent():
    """Test the google_search agent's basic ability via a session file."""
    await AgentEvaluator.evaluate(
        agent_module="misstea.sub_agents.google_search",
        eval_dataset_file_path_or_dir="tests/sub_agents/google_search/google_search_agent.test.json",
    )
