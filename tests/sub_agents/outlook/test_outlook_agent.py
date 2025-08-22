import pytest
from google.adk.evaluation.agent_evaluator import AgentEvaluator


@pytest.mark.flaky(reruns=3)
@pytest.mark.asyncio
async def test_outlook_agent():
    """Test the outlook agent's basic ability via a session file."""
    await AgentEvaluator.evaluate(
        agent_module="misstea.sub_agents.outlook",
        eval_dataset_file_path_or_dir="tests/sub_agents/outlook/outlook_agent.test.json",
    )
