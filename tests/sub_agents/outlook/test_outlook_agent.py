import pytest
from click.testing import CliRunner

from misstea.main import cli


@pytest.mark.flaky(reruns=5)
def test_outlook_agent_e2e(caplog):
    """Test that the outlook agent can be called and returns the expected output."""
    runner = CliRunner()
    result = runner.invoke(
        cli,
        ["run"],
        input="List all meetings in my calendar on 1st August 2025.",
    )

    assert caplog.text.find("name: call_outlook_agent, args: {'question': ") >= 0
    assert "Meeting for misstea unit tests" in result.stdout
