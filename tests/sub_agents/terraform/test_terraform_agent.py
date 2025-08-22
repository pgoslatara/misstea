import pytest
from google.adk.evaluation.agent_evaluator import AgentEvaluator


@pytest.mark.flaky(reruns=3)
@pytest.mark.asyncio
async def test_terraform_agent():
    """Test the terraform agent's basic ability via a session file."""
    await AgentEvaluator.evaluate(
        agent_module="misstea.sub_agents.terraform",
        eval_dataset_file_path_or_dir="tests/sub_agents/terraform/terraform_agent.test.json",
    )
