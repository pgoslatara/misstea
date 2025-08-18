import pytest
from google.adk.evaluation.agent_evaluator import AgentEvaluator


@pytest.mark.flaky(reruns=3)
@pytest.mark.asyncio
async def test_coding_agent_with_single_test_file():
    """Test the coding agent's basic ability via a session file."""
    await AgentEvaluator.evaluate(
        agent_module="misstea.sub_agents.coding",
        eval_dataset_file_path_or_dir="tests/sub_agents/coding/coding_agent.test.json",
    )
