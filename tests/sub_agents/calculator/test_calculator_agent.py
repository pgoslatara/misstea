import os

import pytest
from google.adk.evaluation.agent_evaluator import AgentEvaluator


@pytest.mark.flaky(reruns=int(os.getenv("SUB_AGENT_TEST_RERUNS", 3)))
@pytest.mark.asyncio
async def test_calculator_agent():
    """Test the calculator agent's basic ability via a session file."""
    await AgentEvaluator.evaluate(
        agent_module="misstea.sub_agents.calculator",
        eval_dataset_file_path_or_dir="tests/sub_agents/calculator/calculator_agent.test.json",
    )
