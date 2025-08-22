import os
from pathlib import Path

import pytest
from google.adk.evaluation.agent_evaluator import AgentEvaluator


@pytest.mark.flaky(reruns=int(os.getenv("SUB_AGENT_TEST_RERUNS")) or 3)  # type: ignore
@pytest.mark.asyncio
async def test_coding_agent():
    """Test the coding agent's basic ability via a session file."""

    def cleanup() -> None:
        """Delete files used for testing if they exist."""
        Path("./tests/sub_agents/coding/dummy_file_write.txt").unlink(missing_ok=True)
        Path("./tests/sub_agents/coding/dummy_file_replace.txt").unlink(missing_ok=True)

    try:
        cleanup()

        with Path("./tests/sub_agents/coding/dummy_file_replace.txt").open("w") as f:
            f.write("This is a string.")

        await AgentEvaluator.evaluate(
            agent_module="misstea.sub_agents.coding",
            eval_dataset_file_path_or_dir="tests/sub_agents/coding/coding_agent.test.json",
        )
    finally:
        cleanup()
